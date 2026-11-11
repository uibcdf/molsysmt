/** Receive the inclusive native contact cutoff in an actual Jupyter canvas. */
import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import {dirname} from 'node:path';
import {observeMolecularControllers, openMolecularPanel} from './jupyter_panel_controls.mjs';

const settings = process.env.MOLSYSVIEWER_JUPYTER_SETTINGS;
const output = dirname(settings);
const config = JSON.parse(await readFile(settings, 'utf8'));
const {chromium} = createRequire(config.viewer_root + '/molsysviewer/js/package.json')('playwright');
const errors = [];
const baselineErrors = [];
const decisions = [];
let browser, page, stage = 'Jupyter startup';

async function openNotebook(filename, marker, pageErrors) {
  const notebook = await browser.newPage({viewport: {width: 1440, height: 1100}});
  notebook.setDefaultTimeout(30000);
  notebook.on('pageerror', error => pageErrors.push({stage, message: String(error), stack: error.stack}));
  await observeMolecularControllers(notebook);
  await notebook.goto(`http://127.0.0.1:${config.port}/lab/workspaces/contacts-${Date.now()}/tree/${filename}?token=${config.token}`, {waitUntil: 'domcontentloaded'});
  await notebook.locator('.jp-NotebookPanel:visible .jp-Cell').first().filter({hasText: marker}).waitFor();
  const dismiss = notebook.getByRole('button', {name: 'No', exact: true});
  if (await dismiss.isVisible()) await dismiss.click();
  return notebook;
}

async function notebookResult(notebook, marker) {
  await notebook.waitForFunction(pattern => {
    const expected = new RegExp(pattern);
    return document.querySelector('.jp-OutputArea-error')
      || [...document.querySelectorAll('.jp-OutputArea-output')].some(output => expected.test(output.textContent.trim()));
  }, marker.source);
  const outputErrors = await notebook.locator('.jp-OutputArea-error').allTextContents();
  assert.deepEqual(outputErrors, []);
}

async function execute(notebook, index) {
  await notebook.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
  await notebook.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index).locator('.cm-content').click();
  await notebook.getByRole('button', {name: /Run this cell and advance/}).click();
}

try {
  browser = await chromium.launch({
    headless: true,
    executablePath: config.chromium,
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  });
  const control = await openNotebook('plain.ipynb', 'PLAIN_JUPYTER_CONTROL_OK', baselineErrors);
  await execute(control, 0);
  await control.getByText('PLAIN_JUPYTER_CONTROL_OK 2', {exact: true}).waitFor();
  await control.close();

  stage = 'Open Analysis on the initialized canvas';
  page = await openNotebook('system.ipynb', 'import molsysviewer as msv', errors);
  await execute(page, 0);
  await page.locator('canvas').first().waitFor();
  await page.waitForFunction(() => window.__controllers[0]?.getStructureData()?.elementCount > 3);
  await openMolecularPanel(page, 'analysis');
  await execute(page, 1);
  await notebookResult(page, /^JUPYTER_CONTACTS_BASELINE$/);
  const panel = page.locator('.msm-analysis');
  await panel.locator('[data-task]').selectOption('contacts');
  await panel.locator('[data-first] [data-source]').selectOption('indices');
  await panel.locator('[data-first] [data-indices]').fill('0');
  await panel.locator('[data-second] [data-source]').selectOption('indices');
  await panel.locator('[data-second] [data-indices]').fill('1,2');
  const report = panel.locator('[data-report]');
  const summary = panel.locator('[data-report-summary]');

  for (const [unit, equal, below] of [
    ['nm', '0.5', '0.49999999999999994'],
    ['angstrom', '5', '4.999999999999999'],
    ['pm', '500', '499.99999999999994'],
  ]) {
    await panel.locator('[data-cutoff-unit]').selectOption(unit);
    for (const [cutoff, included] of [[equal, true], [below, false]]) {
      stage = `Evaluate ${cutoff} ${unit}`;
      await panel.locator('[data-cutoff]').fill(cutoff);
      await report.waitFor({state: 'hidden'});
      await panel.locator('[data-calculate]').click();
      await summary.filter({hasText: `distance <= ${cutoff} ${unit}`}).waitFor();
      const rows = await panel.locator('[data-rows] tr').evaluateAll(elements => elements.map(
        element => [...element.querySelectorAll('td')].map(cell => cell.textContent),
      ));
      assert.deepEqual(rows, [['0', '0', '1', String(included)], ['0', '0', '2', 'false']]);
      assert.match(await summary.innerText(), new RegExp(`${Number(included)} positive contacts among 2 evaluated pair occurrences`));
      assert.equal(await panel.locator('[data-add-live-distance]').isVisible(), false);
      decisions.push({cutoff, unit, included, rows});
    }
  }

  stage = 'Check the native system and scene after all calculations';
  await execute(page, 2);
  await notebookResult(page, /^JUPYTER_CONTACTS_UNCHANGED \d+$/);
  const fingerprint = error => error.message + '|' + (error.stack?.split('\n')[1] || '');
  assert.ok(errors.every(error => baselineErrors.some(control => fingerprint(error) === fingerprint(control))),
    'Analysis introduced a page error absent from the plain notebook');
  await writeFile(output + '/contacts-browser.json', JSON.stringify({decisions, errors, baselineErrors}, null, 2));
} catch (error) {
  console.error(stage, error);
  await page?.screenshot({path: output + '/contacts-failure.png'}).catch(() => {});
  await writeFile(output + '/contacts-browser.json', JSON.stringify({stage, decisions, errors, baselineErrors}, null, 2));
  process.exitCode = 1;
} finally {
  await browser?.close();
}
