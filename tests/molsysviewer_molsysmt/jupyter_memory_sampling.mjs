/** Private Chromium receiving measurements; never a process-memory estimate. */

async function taskBarrier(page) {
    await page.evaluate(() => new Promise(resolve => {
        const channel = new MessageChannel();
        channel.port1.onmessage = () => {
            channel.port1.onmessage = null;
            channel.port1.close();
            channel.port2.close();
            resolve();
        };
        channel.port2.postMessage(null);
    }));
}

function requireBytes(value, name) {
    if (!Number.isFinite(value) || value < 0) {
        throw new Error(`Unavailable or invalid memory measurement: ${name}`);
    }
    return value;
}

async function memoryWindow(page, cdp, phase, inspect, exposedGc) {
    const started = performance.now();
    const pageMeasurement = await page.evaluate(exposedGc => {
        if (exposedGc) {
            if (typeof globalThis.gc !== 'function') {
                throw new Error('This receiving method requires exposed Chromium GC');
            }
            globalThis.gc();
        }
        const memory = performance.memory;
        if (!memory) throw new Error('performance.memory is unavailable');
        return {
            timestamp_ms: performance.now(),
            used_js_heap_bytes: memory.usedJSHeapSize,
            total_js_heap_bytes: memory.totalJSHeapSize,
            js_heap_limit_bytes: memory.jsHeapSizeLimit,
        };
    }, exposedGc);
    for (const name of ['used_js_heap_bytes', 'total_js_heap_bytes', 'js_heap_limit_bytes']) {
        requireBytes(pageMeasurement[name], name);
    }
    const heap = await cdp.send('Runtime.getHeapUsage');
    requireBytes(heap.usedSize, 'Runtime.getHeapUsage.usedSize');
    requireBytes(heap.totalSize, 'Runtime.getHeapUsage.totalSize');
    const dom = await cdp.send('Memory.getDOMCounters');
    for (const [name, value] of Object.entries(dom)) {
        if (!Number.isSafeInteger(value) || value < 0) {
            throw new Error(`Unavailable or invalid DOM counter: ${name}`);
        }
    }
    for (const name of ['documents', 'nodes', 'jsEventListeners']) {
        if (!Object.hasOwn(dom, name)) throw new Error(`Missing DOM counter: ${name}`);
    }
    // The inspector must return primitive observations, never handles to subjects.
    const subjects = inspect ? await inspect(page) : null;
    return {
        phase,
        exposed_gc_before_page_metric: exposedGc,
        node_window_started_ms: started,
        node_window_finished_ms: performance.now(),
        page: pageMeasurement,
        cdp_heap: heap,
        cdp_dom: dom,
        subjects,
    };
}

export async function sampleRetirementMemory(page, cdp, {inspect = null} = {}) {
    const raw = await memoryWindow(page, cdp, 'same_task_exposed_gc', inspect, true);
    await taskBarrier(page);
    await taskBarrier(page);
    const afterTasks = await memoryWindow(page, cdp, 'after_two_tasks', inspect, false);
    // A subject inspection can itself keep WeakRef targets alive for its job.
    await taskBarrier(page);
    await cdp.send('HeapProfiler.collectGarbage');
    await taskBarrier(page);
    await cdp.send('HeapProfiler.collectGarbage');
    await taskBarrier(page);
    const afterCollection = await memoryWindow(page, cdp, 'after_cdp_collections', inspect, false);
    return {
        schema: 'molsysmt.jupyter_memory_sample@1',
        method: 'two_task_barriers_then_two_cdp_collections',
        cdp_collections: 2,
        metric_order: ['performance.memory', 'Runtime.getHeapUsage', 'Memory.getDOMCounters', 'subjects'],
        scope: 'Sequential API pairs within recorded windows; neither simultaneous instants nor RSS, GPU or complete process-family memory.',
        raw,
        after_tasks: afterTasks,
        after_collection: afterCollection,
    };
}
