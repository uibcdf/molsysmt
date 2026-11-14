/** Real Jupyter execution controls; controller-ownership controls are synthetic. */
import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import {dirname} from 'node:path';
import {activeControllerSnapshot, observeCellExecutions, receiveCellMarker, receivingText} from './jupyter_cell_receiving.mjs';

const config = JSON.parse(await readFile(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS, 'utf8'));
const output = dirname(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS);
const notebook = JSON.parse(await readFile(output + '/notebooks/system.ipynb', 'utf8'));
const {chromium} = createRequire(config.viewer_root + '/molsysviewer/js/package.json')('playwright');
const secrets = [config.token];
const safe = value => JSON.parse(JSON.stringify(value, (_, item) => typeof item === 'string' ? receivingText(item, secrets).text : item));
const result = {schema: 'molsysmt.jupyter_cell_receiving@1', outcome: 'in_progress',
    scope: 'Real plain Jupyter execution/error/marker controls and synthetic controller identity controls; no molecular imports, Mol* canvas or recovered scientific session.', controls: {}};
let browser, observer;
try {
    browser = await chromium.launch({headless: true, executablePath: config.chromium, args: ['--no-sandbox']});
    const page = await browser.newPage({viewport: {width: 1200, height: 900}});
    page.setDefaultTimeout(30000);
    observer = observeCellExecutions(page, {secrets});
    await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/cell-errors-${Date.now()}/tree/system.ipynb?token=${config.token}`, {waitUntil: 'domcontentloaded'});
    const cell = index => page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index);
    await cell(0).filter({hasText: '_diagnostic_forbidden='}).waitFor();
    const no = page.getByRole('button', {name: 'No', exact: true});
    if (await no.isVisible()) await no.click();
    async function execute(index, marker, timeoutMs = 30000) {
        await page.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
        const context = {operation: 'synthetic cell receiving control', cell_index: index, cell_id: notebook.cells[index].id,
            marker, surface_kind: 'notebook', expected_surface_cell_index: index, expected_viewer_id: null, binding_stage: 'not_started'};
        observer.arm(context.cell_id);
        await cell(index).locator('.cm-content').click();
        await page.getByRole('button', {name: /Run this cell and advance/}).click();
        return receiveCellMarker(page, observer, context, {timeoutMs});
    }
    result.controls.setup = await execute(0, 'CELL_ERROR_READY');
    const started = performance.now();
    try { await execute(1, 'UNREACHED_RECOVERED_MARKER'); }
    catch (error) {
        result.controls.python_error = {name: error.name, receiving: error.receiving, elapsed_ms: performance.now() - started};
    }
    const python = result.controls.python_error;
    assert.equal(python?.name, 'JupyterCellError');
    assert.equal(python.receiving.phase, 'python_cell_error');
    assert.equal(python.receiving.binding_stage, 'not_started');
    assert.equal(python.receiving.marker_received, false);
    assert.equal(python.receiving.execution.python_error.name, 'AssertionError');
    assert.match(python.receiving.execution.python_error.value.text, /SYNTHETIC_PRE_SAVE_STRUCTURE_EXPECTED_1_GOT_0/);
    assert.equal(JSON.stringify(python).includes(config.token), false);
    assert.match(python.receiving.execution.python_error.value.text, /\[redacted\]/);
    // Receive the actual rendered MIME separately; no replacement error CSS is guessed.
    await cell(1).locator('.jp-OutputArea-output').filter({hasText: 'SYNTHETIC_PRE_SAVE'}).waitFor();
    result.error_dom = await cell(1).locator('.jp-OutputArea-output').evaluateAll(nodes => nodes.map(node => ({
        classes: node.className, mime_type: node.getAttribute('data-mime-type')})));
    result.controls.success_after_error = await execute(2, 'CELL_ERROR_SUCCESS');
    result.controls.same_cell_second_execution = await execute(2, 'CELL_ERROR_SUCCESS');
    try { await execute(3, 'CELL_ERROR_READY', 2000); }
    catch (error) { result.controls.absent_marker = {name: error.name, receiving: error.receiving}; }
    assert.equal(result.controls.absent_marker?.name, 'JupyterMarkerTimeoutError');
    assert.equal(result.controls.absent_marker.receiving.phase, 'cell_marker_missing');
    assert.equal(result.controls.absent_marker.receiving.execution.reply_status, 'ok');
    assert.equal(result.controls.absent_marker.receiving.execution.python_error, null);
    result.controls.warning_stderr = await execute(4, 'CELL_WARNING_SUCCESS');
    try { await execute(5, 'LONG_ERROR_UNREACHED'); }
    catch (error) { result.controls.bounded_error = {name: error.name, receiving: error.receiving}; }
    assert.equal(result.controls.bounded_error?.name, 'JupyterCellError');
    const large = result.controls.bounded_error.receiving.execution.python_error;
    assert.equal(large.name, 'RuntimeError');
    assert.equal(large.value.truncated, true);
    assert.equal(large.traceback.truncated, true);
    assert.ok(JSON.stringify(large).length < 13000);
    assert.equal(JSON.stringify(large).includes(config.token), false);
    const context = {...python.receiving};
    delete context.execution;
    context.expected_viewer_id = 'expected-recovered-controller';
    result.synthetic_controllers = [];
    async function controller({cellIndex, id, bindingStage}) {
        await page.evaluate(({cellIndex, id}) => {
            document.querySelector('#synthetic-diagnostic-controller')?.remove();
            const root = document.querySelectorAll('.jp-NotebookPanel .jp-Cell')[cellIndex];
            const canvasHost = document.createElement('div');
            canvasHost.id = 'synthetic-diagnostic-controller';
            root.appendChild(canvasHost);
            window.__longActive = {canvasHost, disposed: false, initOptions: {model: {get: () => id}},
                trajectory: {getTrajectoryState: () => ({currentFrame: 0, isPlaying: false})}};
        }, {cellIndex, id});
        return activeControllerSnapshot(page, {...context, binding_stage: bindingStage}, {secrets});
    }
    for (const [input, expected] of [
        [{cellIndex: 0, id: 'previous-controller', bindingStage: 'not_started'}, 'previous_or_other'],
        [{cellIndex: 0, id: context.expected_viewer_id, bindingStage: 'bound'}, 'previous_or_other'],
        [{cellIndex: 1, id: 'previous-controller', bindingStage: 'bound'}, 'previous_or_other'],
        [{cellIndex: 1, id: context.expected_viewer_id, bindingStage: 'not_started'}, 'unbound'],
        [{cellIndex: 1, id: context.expected_viewer_id, bindingStage: 'bound'}, 'bound_expected'],
        [{cellIndex: 1, id: null, bindingStage: 'bound'}, 'unbound'],
    ]) {
        const snapshot = await controller(input);
        assert.equal(snapshot.ownership, expected);
        assert.equal(snapshot.receiving.expected_viewer_id, context.expected_viewer_id);
        result.synthetic_controllers.push({input, expected_ownership: expected, snapshot});
    }
    await page.evaluate(() => { delete window.__longActive; document.querySelector('#synthetic-diagnostic-controller')?.remove(); });
    result.controls.complete = await execute(6, 'CELL_ERROR_COMPLETE');
    result.kernel = JSON.parse(await readFile(output + '/plain-kernel.json', 'utf8'));
    assert.deepEqual(result.kernel.forbidden_imports, []);
    result.outcome = 'passed';
} catch (error) {
    result.outcome = 'failed';
    result.failure = {name: error.name, message: error.message, receiving: error.receiving ?? null};
    process.exitCode = 1;
} finally {
    observer?.dispose();
    await browser?.close();
    await writeFile(output + '/cell-error-result.json', JSON.stringify(safe(result), null, 2));
}
