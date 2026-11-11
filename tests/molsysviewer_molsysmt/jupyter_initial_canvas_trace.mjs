/** First-canvas observations from the real widget and Mol* controller for #615. */
import { execFile } from 'node:child_process';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

export async function installInitialCanvasTrace(page, expectedAtoms, attempt) {
    await page.addInitScript(expectedAtoms => {
        let cell, target, controller, runTime, attempt, sceneSubscription, drawSubscription;
        const marks = {};
        let observerErrors = 0;

        const mark = name => {
            if (runTime !== undefined && marks[name] === undefined) {
                marks[name] = performance.now() - runTime;
            }
        };
        const observe = action => {
            try {
                action();
            } catch {
                observerErrors++;
            }
        };
        const release = () => {
            sceneSubscription?.unsubscribe();
            drawSubscription?.unsubscribe();
            sceneSubscription = drawSubscription = undefined;
        };
        const readScene = () => {
            if (controller.canvasHost?.querySelector('canvas')?.isConnected) mark('canvas_connected');
            if (controller.getStructureData()?.elementCount === expectedAtoms) mark('scene_registered');
        };
        const belongsToCell = element => {
            for (let node = element; node; node = node.parentElement ?? node.getRootNode()?.host) {
                if (node === cell) return true;
            }
            return false;
        };

        window.__initialCanvasTrace = {
            arm(initialCell, label) {
                cell = initialCell;
                attempt = label;
                runTime = performance.now();
                if (window.__molsysviewer_anywidget_runtime__) mark('runtime_available');
            },
            runtimeAvailable() {
                mark('runtime_available');
            },
            runClicked() {
                mark('run_clicked');
            },
            controllerStarted(element) {
                observe(() => {
                    if (!cell || target || !element.parentElement?.hasAttribute('data-molsysviewer-canvas-output')) return;
                    // AnyWidget can start rendering before attaching its output to the cell.
                    target = element;
                    mark('widget_mount_started');
                });
            },
            controllerReady(created, element) {
                observe(() => {
                    if (element !== target || controller) return;
                    controller = created;
                    mark('controller_ready');
                    const canvas = controller.plugin.canvas3d;
                    readScene();
                    if (!canvas) return;
                    sceneSubscription = controller.plugin.state.data.events.changed.subscribe(() => observe(readScene));
                    let subscribed = false;
                    drawSubscription = canvas.didDraw.subscribe(() => {
                        // BehaviorSubject emits its cached value during subscribe.
                        if (!subscribed) return;
                        observe(() => {
                            readScene();
                            if (marks.scene_registered === undefined || !controller.canvasHost?.isConnected) return;
                            if (canvas.reprCount.value <= 0 || canvas.boundingSphereVisible.radius <= 0) return;
                            mark('first_native_draw');
                            release();
                        });
                    });
                    subscribed = true;
                    mark('draw_observer_armed');
                });
            },
            finish() {
                const canvas = target?.querySelector('canvas');
                if (canvas?.isConnected) mark('canvas_connected');
                const rect = canvas?.getBoundingClientRect();
                let observedAtoms = null;
                observe(() => { observedAtoms = controller?.getStructureData()?.elementCount ?? null; });
                const data = {
                    attempt,
                    anchor: 'observer_arm_before_run_click',
                    run_epoch_ms: runTime === undefined ? null : performance.timeOrigin + runTime,
                    run_clicked_epoch_ms: marks.run_clicked === undefined ? null
                        : performance.timeOrigin + runTime + marks.run_clicked,
                    elapsed_ms: runTime === undefined ? null : performance.now() - runTime,
                    marks: { ...marks },
                    expected_atoms: expectedAtoms,
                    observed_atoms: observedAtoms,
                    belongs_to_initial_cell: target ? belongsToCell(target) : null,
                    canvas: rect ? {
                        connected: canvas.isConnected,
                        x: rect.x, y: rect.y, width: rect.width, height: rect.height,
                    } : null,
                    viewport: { width: innerWidth, height: innerHeight, visible: !document.hidden },
                    output_errors: cell?.querySelectorAll('.jp-OutputArea-error').length ?? null,
                    observer_errors: observerErrors,
                };
                release();
                cell = target = controller = undefined;
                return data;
            },
        };
    }, expectedAtoms);
    return async (cell, button) => {
        try {
            await cell.evaluate(
                (element, label) => window.__initialCanvasTrace?.arm(element, label),
                attempt,
                { timeout: 750 },
            );
            await button.evaluate(element => element.addEventListener(
                'click', () => window.__initialCanvasTrace?.runClicked(), { once: true, capture: true },
            ), undefined, { timeout: 750 });
        } catch {
            // A missing observer does not alter the Run or canvas verdict.
        }
    };
}

/** Sample the existing authenticated session endpoint while the browser is connected. */
export function initialCanvasSessionTrace(config, output) {
    let started, timer, halfway;
    const runner = fileURLToPath(new URL('./system_panel_jupyter.py', import.meta.url));
    async function sample(stage) {
        const elapsed_ms = performance.now() - started;
        try {
            const {stdout} = await promisify(execFile)(
                config.python, [runner, '--sample-initial-canvas-sessions'],
                {timeout: 2500, maxBuffer: 65536},
            );
            return {stage, elapsed_ms, ...JSON.parse(stdout)};
        } catch {
            return {stage, elapsed_ms, available: false, reason: 'sampler_unavailable'};
        }
    }
    function arm() {
        started = performance.now();
        timer = setTimeout(() => { halfway = sample('while_waiting'); }, 15000);
    }
    async function finish(outcome) {
        clearTimeout(timer);
        const samples = await Promise.all([
            halfway ?? {
                stage: 'while_waiting',
                available: false,
                reason: started === undefined ? 'run_unavailable' : 'checkpoint_not_reached',
            },
            outcome === 'canvas_wait_failed' ? sample('canvas_timeout') : null,
        ]);
        try {
            await writeFile(output + '/initial-canvas-sessions.json', JSON.stringify({
                attempt: config.initial_canvas_attempt,
                anchor: 'sampler_arm_before_run_click',
                anchor_epoch_ms: started === undefined ? null : performance.timeOrigin + started,
                outcome,
                samples: samples.filter(Boolean),
            }, null, 2));
        } catch {
            console.warn('Could not write live Jupyter session diagnostics');
        }
    }
    return {arm, finish};
}

/** Persist before retiring the browser, while preserving the original test verdict. */
export async function saveInitialCanvasTrace(page, path, outcome) {
    let timer;
    const capture = page.evaluate(() => window.__initialCanvasTrace?.finish()).catch(() => null);
    try {
        const trace = await Promise.race([
            capture,
            new Promise(resolve => { timer = setTimeout(() => resolve(null), 750); }),
        ]);
        await writeFile(path, JSON.stringify({
            schema: 'molsysviewer.initial_canvas_trace@1',
            outcome,
            capture: trace ? (trace.attempt ? 'available' : 'unarmed') : 'unavailable',
            trace: trace ?? null,
        }, null, 2));
    } catch {
        console.warn('Could not write initial canvas diagnostic');
    } finally {
        clearTimeout(timer);
    }
}
