/** Private weak native owners for the notebook's real molecular controls. */
import assert from 'node:assert/strict';

export async function installNativeLifetimeObservation(page) {
    await page.addInitScript(() => {
        globalThis.__longNativeRows = [];
    });
}

export async function registerNativeSnapshot(page, {label, witness = false}) {
    return page.evaluate(({label, witness}) => {
        const controller = witness ? window.__longWitness : window.__longActive;
        const structure = controller?.getStructureData();
        const model = structure?.model;
        const axes = model?.atomicConformation;
        if (!structure || !model || !axes) throw new Error('Native molecular snapshot is not ready');
        const targets = {controller, structure, model};
        const buffers = new Set();
        const signature = {atoms: structure.elementCount, axes: []};
        for (const name of ['x', 'y', 'z']) {
            const axis = axes[name];
            if (!ArrayBuffer.isView(axis)) throw new Error(`Native coordinate axis ${name} has no backing view`);
            targets[name] = axis;
            buffers.add(axis.buffer);
            signature.axes.push({name, length: axis.length, sum: axis.reduce((total, value) => total + value, 0)});
        }
        const row = {
            label, witness, signature,
            targets: Object.fromEntries(Object.entries(targets).map(([name, value]) => [name, new WeakRef(value)])),
            buffers: [...buffers].map(buffer => ({bytes: buffer.byteLength, ref: new WeakRef(buffer)})),
        };
        if (witness) {
            // Intentional positive owner, not an inferred natural retention policy.
            window.__longRetainedWitnessNative = structure;
            window.__longWitnessNativeSignature = JSON.stringify(signature);
        }
        window.__longNativeRows.push(row);
        return {label, witness, signature, buffer_bytes: row.buffers.map(entry => entry.bytes)};
    }, {label, witness});
}

export async function receiveNativeDisposal(page) {
    const ready = await page.waitForFunction(() => window.__longNativeRows
        .filter(row => !row.witness).every(row => {
            const controller = row.targets.controller.deref();
            return !controller || (controller.disposed && !controller.canvasHost?.isConnected);
        }));
    await ready.dispose();
}

export async function inspectNativeLifetimes(page) {
    return page.evaluate(() => {
        const current = window.__longWitness.getStructureData();
        const axes = current.model.atomicConformation;
        const signature = {atoms: current.elementCount, axes: ['x', 'y', 'z'].map(name => ({
            name, length: axes[name].length, sum: axes[name].reduce((total, value) => total + value, 0),
        }))};
        return {
            witness_data_unchanged: JSON.stringify(signature) === window.__longWitnessNativeSignature,
            rows: window.__longNativeRows.map(row => ({
                label: row.label, witness: row.witness, atoms: row.signature.atoms,
                targets: Object.fromEntries(Object.entries(row.targets).map(([name, ref]) => [name, !!ref.deref()])),
                buffers: row.buffers.map(entry => ({bytes: entry.bytes, alive: !!entry.ref.deref()})),
            })),
        };
    });
}

export function assertNativeRetirement(sample, cycle) {
    const observed = sample.after_collection.subjects;
    assert.equal(observed.witness_data_unchanged, true, 'Independent molecular witness data changed');
    assert.equal(observed.rows.length, 3, 'Receive one witness and both notebook molecular snapshots');
    assert.deepEqual(observed.rows.map(row => row.label), ['witness', `cycle-${cycle}-created`, `cycle-${cycle}-recovered`]);
    for (const row of observed.rows) {
        assert.equal(row.atoms, row.witness ? 3983 : 62);
        assert.deepEqual(Object.keys(row.targets), ['controller', 'structure', 'model', 'x', 'y', 'z']);
        for (const [name, alive] of Object.entries(row.targets)) {
            assert.equal(alive, row.witness, `${row.label}/${name} has unexpected reachability`);
        }
        assert.ok(row.buffers.length > 0 && row.buffers.every(buffer => buffer.bytes > 0));
        for (const buffer of row.buffers) {
            assert.equal(buffer.alive, row.witness, `${row.label}/backing buffer has unexpected reachability`);
        }
    }
}

export async function retireObservedRows(page) {
    await page.evaluate(() => {
        window.__longNativeRows = window.__longNativeRows.filter(row => row.witness);
    });
}
