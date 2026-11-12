/** Actual retained/released object and backing-buffer controls, without Jupyter. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {sampleRetirementMemory} from './jupyter_memory_sampling.mjs';

const output = resolve(process.argv[2]);
const viewer = process.env.MOLSYSVIEWER_ROOT;
assert.ok(viewer, 'MOLSYSVIEWER_ROOT is required');
const {chromium} = createRequire(viewer + '/molsysviewer/js/package.json')('playwright');
let browser;
const result = {schema: 'molsysmt.memory_sampler_controls@1', outcome: 'in_progress'};
try {
    browser = await chromium.launch({
        headless: true,
        executablePath: process.env.PW_CHROMIUM_BIN || '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--enable-precise-memory-info', '--js-flags=--expose-gc'],
    });
    const page = await browser.newPage();
    page.setDefaultTimeout(15000);
    await page.setContent('<!doctype html><title>Memory sampling controls</title><p>Independent controls</p>');
    const cdp = await page.context().newCDPSession(page);
    result.browser = await cdp.send('Browser.getVersion');
    result.creation_job = await page.evaluate(() => {
        const witness = {data: new Uint8Array(4 * 1024 * 1024)};
        witness.data[0] = 37;
        const retained = {data: new Uint8Array(8 * 1024 * 1024)};
        globalThis.__memoryControlWitness = witness;
        globalThis.__memoryControlRetained = retained;
        globalThis.__memoryControlRefs = Object.fromEntries(
            Object.entries({witness, retained}).map(([name, value]) => [name, {
                object: new WeakRef(value), buffer: new WeakRef(value.data.buffer),
            }]),
        );
        // No ordinary strong local reference survives this nested scope.
        globalThis.__memoryControlRefs.retired = (() => {
            const value = {data: new Uint8Array(8 * 1024 * 1024)};
            return {object: new WeakRef(value), buffer: new WeakRef(value.data.buffer)};
        })();
        globalThis.gc();
        return Object.fromEntries(Object.entries(globalThis.__memoryControlRefs).map(([name, refs]) => [
            name, {object_alive: !!refs.object.deref(), buffer_alive: !!refs.buffer.deref()},
        ]));
    });
    for (const row of Object.values(result.creation_job)) {
        assert.deepEqual(row, {object_alive: true, buffer_alive: true});
    }
    const inspect = page => page.evaluate(() => Object.fromEntries(
        Object.entries(globalThis.__memoryControlRefs).map(([name, refs]) => [
            name, {object_alive: !!refs.object.deref(), buffer_alive: !!refs.buffer.deref()},
        ]),
    ));
    result.before_release = await sampleRetirementMemory(page, cdp, {inspect});
    const first = result.before_release.after_collection.subjects;
    assert.deepEqual(first.retired, {object_alive: false, buffer_alive: false});
    assert.deepEqual(first.retained, {object_alive: true, buffer_alive: true});
    assert.deepEqual(first.witness, {object_alive: true, buffer_alive: true});
    await page.evaluate(() => { delete globalThis.__memoryControlRetained; });
    result.after_release = await sampleRetirementMemory(page, cdp, {inspect});
    const last = result.after_release.after_collection.subjects;
    assert.deepEqual(last.retained, {object_alive: false, buffer_alive: false});
    assert.deepEqual(last.retired, {object_alive: false, buffer_alive: false});
    assert.deepEqual(last.witness, {object_alive: true, buffer_alive: true});
    const beforeBacking = result.before_release.after_collection.cdp_heap.backingStorageSize;
    const afterBacking = result.after_release.after_collection.cdp_heap.backingStorageSize;
    assert.ok(Number.isFinite(beforeBacking) && Number.isFinite(afterBacking),
        'This explicit Chromium control requires the CDP backing-storage metric');
    result.released_backing_bytes = beforeBacking - afterBacking;
    assert.ok(result.released_backing_bytes >= 7 * 1024 * 1024,
        'Releasing the eight-MiB control must reduce observed backing storage');
    result.witness_value = await page.evaluate(() => globalThis.__memoryControlWitness.data[0]);
    assert.equal(result.witness_value, 37);
    const element = await page.evaluateHandle(() => {
        const node = document.createElement('div');
        node.payload = new Uint8Array(8 * 1024 * 1024);
        globalThis.__memoryHandleRefs = {object: new WeakRef(node), buffer: new WeakRef(node.payload.buffer)};
        return node;
    });
    const inspectHandle = page => page.evaluate(() => ({
        object_alive: !!globalThis.__memoryHandleRefs.object.deref(),
        buffer_alive: !!globalThis.__memoryHandleRefs.buffer.deref(),
    }));
    try {
        result.handle_retained = await sampleRetirementMemory(page, cdp, {inspect: inspectHandle});
        assert.deepEqual(result.handle_retained.after_collection.subjects, {object_alive: true, buffer_alive: true});
    } finally {
        await element.dispose();
    }
    result.handle_disposed = await sampleRetirementMemory(page, cdp, {inspect: inspectHandle});
    assert.deepEqual(result.handle_disposed.after_collection.subjects, {object_alive: false, buffer_alive: false});
    result.outcome = 'passed';
    result.scope = 'Chromium method/controls only; no molecular package, widget, Jupyter host or long-campaign acceptance.';
    await cdp.detach();
} catch (error) {
    result.outcome = 'failed';
    result.error = {name: error.name, message: error.message};
    process.exitCode = 1;
} finally {
    await browser?.close();
    await writeFile(output, JSON.stringify(result, null, 2));
}
