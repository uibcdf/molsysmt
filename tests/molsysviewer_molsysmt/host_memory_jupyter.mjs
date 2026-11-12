/** Default-host notebook execution baseline; no molecular views or imports. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile, writeFile} from 'node:fs/promises';
import {dirname} from 'node:path';
import {isDeepStrictEqual} from 'node:util';
import {sampleRetirementMemory} from './jupyter_memory_sampling.mjs';

const config = JSON.parse(await readFile(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS, 'utf8'));
const output = dirname(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS);
const {chromium} = createRequire(config.viewer_root + '/molsysviewer/js/package.json')('playwright');
const groups = config.host_memory_groups;
assert.ok(Number.isInteger(groups) && groups >= 1 && groups <= 7);
let browser;
const result = {schema: 'molsysmt.jupyter_host_memory@1', outcome: 'in_progress', groups, samples: []};
async function readHostConfig(page) {
    return page.evaluate(() => {
        const config = JSON.parse(document.querySelector('#jupyter-config-data').textContent);
        return Object.fromEntries(['appVersion', 'appName', 'disabledExtensions'].map(name => [name, config[name] ?? null]));
    });
}
async function readToolbarSettings(page) {
    return page.evaluate(async () => {
        const response = await fetch('/lab/api/settings/@jupyterlab/cell-toolbar-extension:plugin');
        if (!response.ok) return {available: false, status: response.status};
        const value = await response.json();
        return {available: true, version: value.version, raw: value.raw,
            schema_defaults: Object.fromEntries(Object.entries(value.schema?.properties ?? {}).map(([name, property]) => [name, property.default ?? null]))};
    });
}
try {
    browser = await chromium.launch({
        headless: true, executablePath: config.chromium,
        args: ['--no-sandbox', '--enable-precise-memory-info', '--js-flags=--expose-gc'],
    });
    const page = await browser.newPage({viewport: {width: 1500, height: 1200}});
    page.setDefaultTimeout(30000);
    const errors = [];
    page.on('pageerror', error => errors.push({name: error.name, message: error.message}));
    await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/host-memory-${Date.now()}/tree/system.ipynb?token=${config.token}`, {waitUntil: 'domcontentloaded'});
    const cell = index => page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index);
    await cell(0).filter({hasText: '_host_forbidden='}).waitFor();
    const no = page.getByRole('button', {name: 'No', exact: true});
    if (await no.isVisible()) await no.click();
    async function execute(index, marker) {
        await page.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
        await cell(index).locator('.cm-content').click();
        await page.getByRole('button', {name: /Run this cell and advance/}).click();
        await page.waitForFunction(marker => document.querySelector('.jp-OutputArea-error')
            || [...document.querySelectorAll('.jp-OutputArea-output')].some(node => node.textContent.trim() === marker), marker);
        assert.equal(await page.locator('.jp-OutputArea-error').count(), 0, 'Host-only cell failed');
        await page.getByText(marker, {exact: true}).waitFor();
        await page.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
    }
    const cdp = await page.context().newCDPSession(page);
    result.browser = await cdp.send('Browser.getVersion');
    result.host_page_config = await readHostConfig(page);
    result.cell_toolbar_settings = await readToolbarSettings(page);
    await execute(0, 'HOST_MEMORY_READY');
    result.samples.push({executions: 0, memory: await sampleRetirementMemory(page, cdp)});
    let executions = 0;
    for (let group = 0; group < groups; group++) {
        for (let index = 0; index < 3; index++) {
            executions++;
            await execute(1, 'HOST_MEMORY_EXECUTED ' + executions);
        }
        result.samples.push({executions, memory: await sampleRetirementMemory(page, cdp)});
        await writeFile(output + '/host-memory-progress.json', JSON.stringify(result, null, 2));
    }
    await execute(2, 'HOST_MEMORY_COMPLETE');
    result.kernel = JSON.parse(await readFile(output + '/host-kernel.json', 'utf8'));
    assert.equal(result.kernel.executions, groups * 3);
    assert.deepEqual(result.kernel.initial_forbidden_imports, []);
    assert.deepEqual(result.kernel.final_forbidden_imports, []);
    result.page_errors = errors;
    result.host_page_config_after = await readHostConfig(page);
    result.cell_toolbar_settings_after = await readToolbarSettings(page);
    result.settings_changed = !isDeepStrictEqual(result.cell_toolbar_settings, result.cell_toolbar_settings_after)
        || !isDeepStrictEqual(result.host_page_config, result.host_page_config_after);
    assert.equal(result.settings_changed, false, 'Host settings changed during the baseline');
    result.outcome = 'passed';
    result.scope = 'Default-host toolbar execution/clear-output baseline with no molecular/AnyWidget kernel imports. Not extension-ablation, retaining-chain attribution or long molecular-campaign acceptance.';
    await cdp.detach();
    await writeFile(output + '/full-result.json', JSON.stringify(result, null, 2));
} catch (error) {
    result.outcome = 'failed';
    result.error = {name: error.name, message: error.message};
    await writeFile(output + '/host-memory-failure.json', JSON.stringify(result, null, 2));
    process.exitCode = 1;
} finally {
    await browser?.close();
}
