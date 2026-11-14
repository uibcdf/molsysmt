/** Fast protocol association controls, separate from actual Jupyter receiving. */
import assert from 'node:assert/strict';
import {EventEmitter} from 'node:events';
import test from 'node:test';
import {DEFAULT_CELL_TIMEOUT_MS, decodeKernelMessage, observeCellExecutions, receiveCellMarker, receivingText} from './jupyter_cell_receiving.mjs';

function harness() {
    const page = new EventEmitter();
    const socket = new EventEmitter();
    socket.url = () => 'ws://localhost/api/kernels/example/channels?token=not-retained';
    page.locator = () => ({nth: () => ({locator: () => ({evaluateAll: async () => true})})});
    const observer = observeCellExecutions(page, {secrets: ['PRIVATE_TOKEN']});
    page.emit('websocket', socket);
    const emit = (direction, type, parent, content = {}, metadata = {}, id = 'request') => socket.emit(direction, {payload: JSON.stringify({
        header: {msg_type: type, msg_id: id}, parent_header: {msg_id: parent}, metadata, content,
    })});
    const request = (cell = 'owned', id = 'request') => emit('framesent', 'execute_request', '', {}, {cellId: cell}, id);
    const success = (id = 'request') => { emit('framereceived', 'execute_reply', id, {status: 'ok'}); emit('framereceived', 'status', id, {execution_state: 'idle'}); };
    return {page, socket, observer, emit, request, success};
}

test('the original finite cell deadline remains thirty seconds', () => assert.equal(DEFAULT_CELL_TIMEOUT_MS, 30000));
test('decoder rejects malformed and oversized transport without returning input', () => {
    for (const payload of ['not JSON', 'x'.repeat(1024 * 1024 + 1), Buffer.alloc(7), Buffer.alloc(16)]) {
        assert.throws(() => decodeKernelMessage(payload));
    }
});
test('redaction precedes truncation and retains both ends of a long diagnostic', () => {
    const result = receivingText('START PRIVATE_TOKEN ' + 'x'.repeat(20000) + ' ?token=OTHER_SECRET END', ['PRIVATE_TOKEN']);
    assert.equal(result.truncated, true);
    assert.ok(result.text.length < 8250);
    assert.match(result.text, /^START \[redacted\]/);
    assert.match(result.text, /END$/);
    assert.doesNotMatch(result.text, /PRIVATE_TOKEN|OTHER_SECRET/);
});
test('another cell and another parent cannot supply the armed execution error', () => {
    const h = harness();
    h.observer.arm('owned');
    h.request('other');
    h.emit('framereceived', 'error', 'request', {ename: 'WrongError'});
    assert.equal(h.observer.snapshot().request_observed, false);
    h.request();
    h.emit('framereceived', 'error', 'unrelated', {ename: 'WrongError'});
    assert.equal(h.observer.snapshot().python_error, null);
    h.emit('framereceived', 'error', 'request', {ename: 'AssertionError', evalue: 'original PRIVATE_TOKEN', traceback: ['original line']});
    h.emit('framereceived', 'execute_reply', 'request', {status: 'error', ename: 'LaterError'});
    const snapshot = h.observer.snapshot();
    assert.equal(snapshot.python_error.name, 'AssertionError');
    assert.equal(snapshot.python_error.value.text, 'original [redacted]');
    h.observer.dispose();
});
test('a matching parent on another socket cannot be attributed to this cell', () => {
    const h = harness();h.observer.arm('owned');h.request();
    const other = new EventEmitter();other.url = h.socket.url;
    h.page.emit('websocket', other);
    other.emit('framereceived', {payload: JSON.stringify({header: {msg_type: 'error'}, parent_header: {msg_id: 'request'}, content: {ename: 'WrongSocket'}})});
    assert.equal(h.observer.snapshot().python_error, null);
    h.observer.dispose();
});
test('late errors from a previous execution do not poison the same cell rerun', () => {
    const h = harness();h.observer.arm('owned');h.request('owned', 'old');h.success('old');
    h.observer.arm('owned');h.request('owned', 'new');
    h.emit('framereceived', 'error', 'old', {ename: 'OldError'});h.success('new');
    assert.equal(h.observer.snapshot().python_error, null);
    assert.equal(h.observer.snapshot().reply_status, 'ok');h.observer.dispose();
});
test('an output marker alone cannot confirm an unobserved request', async () => {
    const h = harness();h.observer.arm('owned');
    await assert.rejects(receiveCellMarker(h.page, h.observer, {cell_index: 0, marker: 'MARKER'}, {timeoutMs: 1}), {name: 'JupyterExecutionEvidenceError'});
    h.observer.dispose();
});
test('an aborted request is distinct from a Python exception', async () => {
    const h = harness();h.observer.arm('owned');h.request();h.emit('framereceived', 'execute_reply', 'request', {status: 'aborted'});
    await assert.rejects(receiveCellMarker(h.page, h.observer, {cell_index: 0, marker: 'MARKER'}), {name: 'JupyterExecutionAbortedError'});
    h.observer.dispose();
});
test('duplicate matching requests are rejected rather than guessed', async () => {
    const h = harness();h.observer.arm('owned');h.request();h.request('owned', 'second');
    await assert.rejects(receiveCellMarker(h.page, h.observer, {cell_index: 0, marker: 'MARKER'}), {name: 'JupyterExecutionEvidenceError'});
    h.observer.dispose();
});
test('ordinary stderr is not a Python execution error', async () => {
    const h = harness();h.observer.arm('owned');h.request();
    h.emit('framereceived', 'stream', 'request', {name: 'stderr', text: 'Traceback: AssertionError text'});h.success();
    const received = await receiveCellMarker(h.page, h.observer, {cell_index: 0, marker: 'MARKER'});
    assert.equal(received.marker_received, true);assert.equal(received.execution.python_error, null);h.observer.dispose();
});
test('malformed packets are explicit missing evidence, never a manufactured Python error', () => {
    const h = harness();h.observer.arm('owned');
    h.socket.emit('framereceived', {payload: 'null'});
    h.socket.emit('framereceived', {payload: Buffer.alloc(3)});
    assert.equal(h.observer.snapshot().unreadable_messages, 2);
    assert.equal(h.observer.snapshot().python_error, null);h.observer.dispose();
});
test('observation cleanup releases socket and page handlers', () => {
    const h = harness();h.observer.arm('owned');h.request();h.observer.dispose();
    assert.equal(h.page.listenerCount('websocket'), 0);assert.equal(h.socket.listenerCount('framesent'), 0);
    assert.equal(h.socket.listenerCount('framereceived'), 0);assert.equal(h.observer.snapshot().request_observed, false);
});
test('zero, infinite and extended deadlines are not accepted', async () => {
    const h = harness();h.observer.arm('owned');
    for (const timeoutMs of [0, -1, Infinity, NaN, 30001]) {
        await assert.rejects(receiveCellMarker(h.page, h.observer, {cell_index: 0, marker: 'MARKER'}, {timeoutMs}), RangeError);
    }
    h.observer.dispose();
});
