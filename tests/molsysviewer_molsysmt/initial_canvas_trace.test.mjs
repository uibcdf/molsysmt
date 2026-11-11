/** Observe stages and diagnostic failures without substituting molecular science. */
import assert from 'node:assert/strict';
import {mkdtemp, readFile, rm, writeFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import {
    installInitialCanvasTrace, initialCanvasSessionTrace, saveInitialCanvasTrace,
} from './jupyter_initial_canvas_trace.mjs';

async function fixture(observedAtoms = 3983) {
    const state = {clock: 0, unsubscribed: 0};
    const cell = {querySelectorAll: () => []};
    const canvas = {
        isConnected: true,
        getBoundingClientRect: () => ({x: 0, y: 0, width: 640, height: 480}),
    };
    const wrapper = {
        parentElement: null, hasAttribute: () => true, getRootNode: () => ({}),
    };
    const target = {
        parentElement: wrapper, querySelector: () => canvas, getRootNode: () => ({}),
    };
    const draw = {
        reprCount: {value: 1}, boundingSphereVisible: {radius: 1},
        didDraw: {subscribe(callback) {
            state.draw = callback;
            callback(); // Cached replay must not be a newly observed draw.
            return {unsubscribe() {state.unsubscribed++;}};
        }},
    };
    const controller = {
        canvasHost: {...target, isConnected: true},
        getStructureData: () => ({elementCount: observedAtoms}),
        plugin: {
            canvas3d: draw,
            state: {data: {events: {changed: {subscribe(callback) {
                state.scene = callback;
                return {unsubscribe() {state.unsubscribed++;}};
            }}}}},
        },
    };
    const context = vm.createContext({
        window: {}, document: {hidden: false}, innerWidth: 800, innerHeight: 600,
        performance: {now: () => state.clock, timeOrigin: 1000},
    });
    const page = {
        async addInitScript(operation, argument) {
            vm.runInContext(`(${operation})(${JSON.stringify(argument)})`, context);
        },
    };
    await installInitialCanvasTrace(page, 3983, 'synthetic-attempt');
    return {state, trace: context.window.__initialCanvasTrace, cell, wrapper, target, controller};
}

test('mount before attachment is retained; cached draws do not count', async () => {
    const f = await fixture();
    f.trace.arm(f.cell, 'synthetic-attempt');
    f.state.clock = 2;
    f.trace.runClicked();
    f.state.clock = 3;
    f.trace.controllerStarted(f.target);
    f.wrapper.parentElement = f.cell;
    f.state.clock = 4;
    f.trace.controllerReady(f.controller, f.target);
    assert.equal(f.state.unsubscribed, 0);
    f.state.clock = 5;
    f.state.draw();
    const result = f.trace.finish();
    assert.equal(result.attempt, 'synthetic-attempt');
    assert.equal(result.belongs_to_initial_cell, true);
    assert.equal(result.observed_atoms, 3983);
    assert.equal(result.marks.run_clicked, 2);
    assert.equal(result.anchor, 'observer_arm_before_run_click');
    assert.equal(result.run_epoch_ms, 1000);
    assert.equal(result.run_clicked_epoch_ms, 1002);
    assert.equal(result.marks.widget_mount_started, 3);
    assert.equal(result.marks.first_native_draw, 5);
    assert.equal(f.state.unsubscribed, 2);
});

test('a wrong scene cannot supply the expected-scene draw milestone', async () => {
    const f = await fixture(24);
    f.trace.arm(f.cell, 'synthetic-attempt');
    f.trace.controllerStarted(f.target);
    f.trace.controllerReady(f.controller, f.target);
    f.state.draw();
    const result = f.trace.finish();
    assert.equal(result.observed_atoms, 24);
    assert.equal(result.marks.scene_registered, undefined);
    assert.equal(result.marks.first_native_draw, undefined);
    assert.equal(result.belongs_to_initial_cell, false);
    assert.equal(f.state.unsubscribed, 2);
});

test('unarmed, unavailable and failed writes remain diagnostic outcomes', async () => {
    const directory = await mkdtemp(join(tmpdir(), 'molsysmt-canvas-unit-'));
    try {
        for (const [name, page, expected] of [
            ['unarmed', {evaluate: async () => ({marks: {}})}, 'unarmed'],
            ['unavailable', {evaluate: async () => {throw Error('PRIVATE_DETAIL');}}, 'unavailable'],
        ]) {
            const path = join(directory, name + '.json');
            await saveInitialCanvasTrace(page, path, 'canvas_wait_failed');
            const raw = await readFile(path, 'utf8');
            const result = JSON.parse(raw);
            assert.equal(result.capture, expected);
            assert.equal(result.outcome, 'canvas_wait_failed');
            assert.ok(!raw.includes('PRIVATE'));
        }
        // A directory is not a writable diagnostic file; the original verdict survives.
        await saveInitialCanvasTrace({evaluate: async () => null}, directory, 'canvas_visible');
    } finally {
        await rm(directory, {recursive: true, force: true});
    }
});

test('an early canvas cancels sampling and preserves an unreached checkpoint', async () => {
    const directory = await mkdtemp(join(tmpdir(), 'molsysmt-canvas-early-'));
    try {
        const observer = initialCanvasSessionTrace({
            python: 'PRIVATE_UNAVAILABLE_EXECUTABLE',
            initial_canvas_attempt: 'synthetic-early-attempt',
        }, directory);
        observer.arm();
        await observer.finish('canvas_visible');
        const raw = await readFile(join(directory, 'initial-canvas-sessions.json'), 'utf8');
        const result = JSON.parse(raw);
        assert.equal(result.outcome, 'canvas_visible');
        assert.deepEqual(result.samples, [{
            stage: 'while_waiting', available: false, reason: 'checkpoint_not_reached',
        }]);
        assert.ok(!raw.includes('PRIVATE'));
    } finally {
        await rm(directory, {recursive: true, force: true});
    }
});

test('a sampler startup failure cannot supply a known kernel state', async () => {
    const directory = await mkdtemp(join(tmpdir(), 'molsysmt-canvas-unavailable-'));
    try {
        const observer = initialCanvasSessionTrace({
            python: 'PRIVATE_UNAVAILABLE_EXECUTABLE',
            initial_canvas_attempt: 'synthetic-failed-attempt',
        }, directory);
        observer.arm();
        await observer.finish('canvas_wait_failed');
        const raw = await readFile(join(directory, 'initial-canvas-sessions.json'), 'utf8');
        const result = JSON.parse(raw);
        assert.equal(result.outcome, 'canvas_wait_failed');
        assert.equal(result.samples[1].available, false);
        assert.equal(result.samples[1].reason, 'sampler_unavailable');
        assert.ok(!raw.includes('PRIVATE'));
    } finally {
        await rm(directory, {recursive: true, force: true});
    }
});

test('live checkpoints read bounded kernel state before timeout cleanup', {timeout: 30000}, async () => {
    assert.ok(process.env.INITIAL_CANVAS_TEST_PYTHON, 'Declare the qualified Python for the sampler.');
    const directory = await mkdtemp(join(tmpdir(), 'molsysmt-canvas-live-'));
    const original = process.env.MOLSYSVIEWER_JUPYTER_SETTINGS;
    let requests = 0;
    const server = createServer((request, response) => {
        assert.equal(request.url, '/api/sessions');
        assert.equal(request.headers.authorization, 'token PRIVATE_TOKEN');
        requests++;
        response.setHeader('Content-Type', 'application/json');
        response.end(JSON.stringify([{
            id: 'PRIVATE_SESSION', path: 'system.ipynb',
            kernel: {id: 'PRIVATE_KERNEL', execution_state: 'busy', connections: 1},
        }]));
    });
    try {
        await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
        const settings = join(directory, 'settings.json');
        await writeFile(settings, JSON.stringify({port: server.address().port, token: 'PRIVATE_TOKEN'}), {mode: 0o600});
        process.env.MOLSYSVIEWER_JUPYTER_SETTINGS = settings;
        const observer = initialCanvasSessionTrace({
            python: process.env.INITIAL_CANVAS_TEST_PYTHON,
            initial_canvas_attempt: 'synthetic-live-attempt',
        }, directory);
        observer.arm();
        await new Promise(resolve => setTimeout(resolve, 17000));
        await observer.finish('canvas_wait_failed');
        const raw = await readFile(join(directory, 'initial-canvas-sessions.json'), 'utf8');
        const result = JSON.parse(raw);
        assert.equal(requests, 2);
        assert.equal(result.attempt, 'synthetic-live-attempt');
        assert.equal(result.anchor, 'sampler_arm_before_run_click');
        assert.deepEqual(result.samples.map(row => row.stage), ['while_waiting', 'canvas_timeout']);
        assert.ok(result.samples.every(row => row.available && row.sessions[0].execution_state === 'busy'));
        assert.ok(result.samples[0].elapsed_ms >= 15000);
        assert.ok(!raw.includes('PRIVATE'));
    } finally {
        if (original === undefined) delete process.env.MOLSYSVIEWER_JUPYTER_SETTINGS;
        else process.env.MOLSYSVIEWER_JUPYTER_SETTINGS = original;
        await new Promise(resolve => server.close(resolve));
        await rm(directory, {recursive: true, force: true});
    }
});
