/** Read typed execution evidence without changing Jupyter traffic or cell code. */
import {setTimeout as delay} from 'node:timers/promises';

const JSON_LIMIT = 1024 * 1024;
export const DEFAULT_CELL_TIMEOUT_MS = 30000;

function readJSON(buffer) {
    if (buffer.length > JSON_LIMIT) throw new Error('Kernel JSON exceeds the receiving budget');
    return JSON.parse(buffer.toString('utf8'));
}

function checkedOffsets(buffer, width, minimum) {
    const number = offset => width === 8 ? Number(buffer.readBigUInt64LE(offset)) : buffer.readUInt32BE(offset);
    const count = number(0);
    if (!Number.isSafeInteger(count) || count < minimum || count > 1024 || width * (count + 1) > buffer.length) {
        throw new Error('Invalid kernel buffer table');
    }
    const offsets = Array.from({length: count}, (_, index) => number(width * (index + 1)));
    if (offsets[0] !== width * (count + 1) || offsets.some((value, index) =>
        !Number.isSafeInteger(value) || value > buffer.length || (index && value < offsets[index - 1]))) {
        throw new Error('Invalid kernel buffer offsets');
    }
    return offsets;
}

/** Decode JSON, legacy binary, or v1 headers; never decode widget buffers. */
export function decodeKernelMessage(payload) {
    if (typeof payload === 'string') {
        if (Buffer.byteLength(payload) > JSON_LIMIT) throw new Error('Kernel JSON exceeds the receiving budget');
        return JSON.parse(payload);
    }
    if (!Buffer.isBuffer(payload) || payload.length < 8) throw new Error('Unknown kernel transport');
    // v1 uses a little-endian uint64 table, including the final boundary;
    // the legacy transport uses a big-endian uint32 table of buffer starts.
    // These layouts follow jupyter_server.services.kernels.connection.base.
    if (payload.readUInt32LE(4) === 0) {
        const offsets = checkedOffsets(payload, 8, 6);
        if (offsets.at(-1) !== payload.length) throw new Error('Missing v1 final boundary');
        const part = index => payload.subarray(offsets[index], offsets[index + 1]);
        const header = readJSON(part(1));
        const parent_header = readJSON(part(2));
        const metadata = readJSON(part(3));
        const relevant = ['execute_reply', 'error', 'status'].includes(header?.msg_type);
        return {channel: part(0).toString('utf8'), header, parent_header, metadata,
            content: relevant ? readJSON(part(4)) : {}};
    }
    const offsets = checkedOffsets(payload, 4, 1);
    return readJSON(payload.subarray(offsets[0], offsets[1] ?? payload.length));
}

/** Bound diagnostic strings, redacting credentials before shortening them. */
export function receivingText(value, secrets = [], limit = 8192) {
    let text = String(value ?? '').replace(/\x1b\[[0-9;]*m/g, '');
    for (const secret of secrets) if (typeof secret === 'string' && secret) text = text.replaceAll(secret, '[redacted]');
    text = text.replace(/([?&](?:token|access_token|key)=)[^&\s"'<>]+/gi, '$1[redacted]')
        .replace(/(authorization:\s*(?:bearer|token)\s+)\S+/gi, '$1[redacted]');
    const characters = text.length;
    if (characters > limit) text = text.slice(0, Math.floor(limit / 2)) + '\n[truncated]\n' + text.slice(-Math.floor(limit / 2));
    return {text, truncated: characters > limit, characters};
}

function pythonError(content, secrets) {
    return {
        name: receivingText(content?.ename ?? 'unknown', secrets, 160).text,
        value: receivingText(content?.evalue, secrets, 2048),
        traceback: receivingText(Array.isArray(content?.traceback) ? content.traceback.join('\n') : '', secrets),
    };
}

/** Observe only the explicitly armed cell/request; keep no code or widget buffers. */
export function observeCellExecutions(page, {secrets = []} = {}) {
    let active = null;
    let unreadableMessages = 0;
    const attached = [];
    function receive(socket, event, payload) {
        let message;
        try { message = decodeKernelMessage(payload); }
        catch { unreadableMessages++; return; }
        if (!message || typeof message !== 'object') { unreadableMessages++; return; }
        if (!active) return;
        const type = message.header?.msg_type;
        if (event === 'framesent' && type === 'execute_request' && message.metadata?.cellId === active.cell_id) {
            if (active.request_id !== null) { active.ambiguous = true; return; }
            const id = message.header?.msg_id;
            if (typeof id !== 'string' || !id || id.length > 256) { active.ambiguous = true; return; }
            active.request_id = id;
            active.socket = socket;
        }
        if (event !== 'framereceived' || socket !== active.socket || !active.request_id || message.parent_header?.msg_id !== active.request_id) return;
        if (type === 'error' || (type === 'execute_reply' && message.content?.status === 'error')) {
            active.python_error ??= pythonError(message.content, secrets);
        }
        if (type === 'execute_reply') active.reply_status = ['ok', 'error', 'aborted'].includes(message.content?.status) ? message.content.status : 'unknown';
        if (type === 'status' && message.content?.execution_state === 'idle') active.idle_received = true;
    }
    const connect = socket => {
        if (!/\/api\/kernels\/[^/]+\/channels$/.test(new URL(socket.url()).pathname)) return;
        for (const event of ['framesent', 'framereceived']) {
            const listener = ({payload}) => receive(socket, event, payload);
            socket.on(event, listener);
            attached.push({socket, event, listener});
        }
    };
    page.on('websocket', connect);
    return {
        arm(cellId) {
            if (typeof cellId !== 'string' || !cellId || cellId.length > 256) throw new TypeError('A manifest cell ID is required');
            active = {cell_id: cellId, request_id: null, socket: null, ambiguous: false,
                reply_status: null, idle_received: false, python_error: null};
            return active;
        },
        snapshot() {
            return {cell_id: active?.cell_id ?? null, request_observed: active?.request_id !== null && active !== null,
                ambiguous: active?.ambiguous ?? false, reply_status: active?.reply_status ?? null,
                idle_received: active?.idle_received ?? false, python_error: active?.python_error ?? null,
                unreadable_messages: unreadableMessages};
        },
        dispose() {
            page.off('websocket', connect);
            for (const {socket, event, listener} of attached) socket.off(event, listener);
            attached.length = 0;
            active = null;
        },
    };
}

/** Require the current cell's successful execution and exact output marker line. */
export async function receiveCellMarker(page, observer, context, {timeoutMs = DEFAULT_CELL_TIMEOUT_MS} = {}) {
    if (!Number.isFinite(timeoutMs) || timeoutMs <= 0 || timeoutMs > DEFAULT_CELL_TIMEOUT_MS) throw new RangeError('Cell timeout must be finite and in (0, 30000] milliseconds');
    const started = performance.now();
    context.phase = 'waiting_for_cell_marker';
    context.marker_received = false;
    context.timeout_ms = timeoutMs;
    const fail = (name, phase, message, evidence) => {
        context.phase = phase;
        const error = new Error(message);
        error.name = name;
        error.receiving = {...context, execution: evidence};
        throw error;
    };
    while (performance.now() - started < timeoutMs) {
        const evidence = observer.snapshot();
        if (evidence.ambiguous) fail('JupyterExecutionEvidenceError', 'ambiguous_cell_execution', 'More than one execution request matched the armed cell', evidence);
        if (evidence.python_error) fail('JupyterCellError', 'python_cell_error',
            `${evidence.python_error.name}: ${evidence.python_error.value.text}`, evidence);
        if (evidence.reply_status === 'aborted') fail('JupyterExecutionAbortedError', 'cell_execution_aborted', 'The armed cell execution was aborted', evidence);
        if (evidence.request_observed && evidence.reply_status === 'ok' && evidence.idle_received) {
            const seen = await page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(context.cell_index)
                .locator('.jp-OutputArea-output').evaluateAll((nodes, marker) => {
                    // Inspect bounded tails: the receiver's terminal marker is a line,
                    // not a substring in source code or another cell's stale output.
                    return nodes.slice(-64).some(node => (node.textContent ?? '').slice(-16384).split('\n').some(line => line.trim() === marker));
                }, context.marker);
            if (seen) {
                context.phase = 'cell_marker_received';
                context.marker_received = true;
                return {...context, execution: evidence};
            }
        }
        await delay(25);
    }
    const evidence = observer.snapshot();
    const complete = evidence.request_observed && evidence.reply_status === 'ok' && evidence.idle_received;
    fail(complete ? 'JupyterMarkerTimeoutError' : 'JupyterExecutionEvidenceError',
        complete ? 'cell_marker_missing' : 'cell_execution_unconfirmed',
        complete ? `Completed cell ${context.cell_index} did not produce its expected marker` : `Cell ${context.cell_index} execution could not be confirmed`, evidence);
}

/** Name expected/observed ownership before interpreting any controller geometry. */
export async function activeControllerSnapshot(page, context, {secrets = []} = {}) {
    if (!page || page.isClosed()) return {available: false, reason: 'page_unavailable', receiving: context};
    const observed = await page.evaluate(({expected, secrets}) => {
        const c = window.__longActive;
        const id = c?.initOptions?.model?.get('runtime_viewer_id') ?? null;
        const panel = [...document.querySelectorAll('.jp-NotebookPanel')].find(node => node.getClientRects().length);
        const root = expected.surface_kind === 'notebook'
            ? (() => {
                const cells = [...(panel?.querySelectorAll('.jp-Cell') ?? [])];
                return cells.some(node => node.hasAttribute('data-windowed-list-index'))
                    ? cells.find(node => node.getAttribute('data-windowed-list-index') === String(expected.expected_surface_cell_index))
                    : cells[expected.expected_surface_cell_index];
            })() : document.body;
        const inside = c?.canvasHost && root ? root.contains(c.canvasHost) : null;
        const identityMatches = typeof expected.expected_viewer_id === 'string' && typeof id === 'string' ? id === expected.expected_viewer_id : null;
        const bound = expected.binding_stage === 'bound' && inside === true && identityMatches === true;
        const ownership = !c ? 'no_controller' : c.disposed ? 'retired_controller'
            : bound ? 'bound_expected' : inside === false || identityMatches === false ? 'previous_or_other' : 'unbound';
        const r = c?.canvasHost?.getBoundingClientRect();
        const state = c?.trajectory?.getTrajectoryState();
        const safeId = typeof id === 'string' ? secrets.reduce((text, secret) => secret ? text.replaceAll(secret, '[redacted]') : text, id) : null;
        return {available: true, observed_viewer_id: safeId === null ? null : safeId.slice(0, 256),
            ownership, inside_expected_surface: inside, identity_matches: identityMatches,
            connected: c?.canvasHost?.isConnected ?? null, disposed: c?.disposed ?? null,
            trajectory: state ? {currentFrame: state.currentFrame, isPlaying: state.isPlaying} : null,
            rect: r ? {x: r.x, y: r.y, width: r.width, height: r.height} : null,
            viewport: {width: innerWidth, height: innerHeight}};
    }, {expected: context, secrets});
    return {...observed, observed_viewer_id: observed.observed_viewer_id === null ? null : receivingText(observed.observed_viewer_id, secrets, 256).text,
        receiving: context};
}
