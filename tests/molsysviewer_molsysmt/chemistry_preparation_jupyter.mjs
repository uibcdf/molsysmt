/** Native TcTIM preparation and reviewed adoption through actual Jupyter. */
import assert from 'node:assert/strict';
import {openMolecularPanel} from './jupyter_panel_controls.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const settings=process.env.MOLSYSVIEWER_JUPYTER_SETTINGS;
const output=dirname(resolve(settings));
const config=JSON.parse(await readFile(settings,'utf8'));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(cell,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();await cell.locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
const workspace=p=>openMolecularPanel(p,'chemistry');
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/preparation-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);
 const panel=()=>page.locator('.msm-chemistry').first();
 await step('Load actual TcTIM and explicitly prepare a separate heavy-atom result',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/preparation-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(cell);
  await page.locator('canvas').waitFor();await workspace(page);
  await panel().locator('[data-task]').selectOption('heavy');await panel().locator('[data-heading]').filter({hasText:'Add missing heavy atoms'}).waitFor();
  assert.equal(await panel().locator('[data-prepare]').isDisabled(),true);
  await panel().locator('[data-source]').selectOption('all');
  await panel().locator('[data-preparation-title]').fill('TcTIM heavy inspection');
  await panel().locator('[data-prepare]').click();
  await panel().locator('[data-result-summary]').filter({hasText:'3,983 atoms'}).waitFor();
  assert.match(await panel().locator('[data-scope]').innerText(),/every source structure/);
  assert.equal(await panel().locator('[data-replacement]').isVisible(),false);
 });
 await step('Present the independent result in the notebook and keep it while changing tasks',async()=>{
  await panel().locator('[data-show-notebook]').click();
  await page.locator('[data-molsysviewer-canvas-output]').nth(1).waitFor();
  await panel().locator('[data-new-result]').click();await panel().locator('[data-result]').waitFor({state:'hidden'});
  assert.equal(await page.locator('[data-molsysviewer-canvas-output]').count(),2);
  await panel().locator('[data-task]').selectOption('add_hydrogens');await panel().locator('[data-heading]').filter({hasText:'Add missing hydrogens'}).waitFor();
  assert.equal(await panel().locator('[data-editor]').isVisible(),false);
  assert.match(await panel().locator('[data-preparation-limits]').innerText(),/not environment-dependent pKa prediction/);
  await panel().locator('[data-preparation-title]').fill('TcTIM with hydrogens');
  await panel().locator('[data-prepare]').click();
  await panel().locator('[data-result-summary]').filter({hasText:'7,868 atoms'}).waitFor({timeout:180000});
  assert.match(await panel().locator('[data-missing-attributes]').innerText(),/b_factor/);
  assert.match(await panel().locator('[data-missing-attributes]').innerText(),/occupancy/);
 });
 await step('Review Back preserves the original TcTIM and its chemical domain',async()=>{
  await panel().locator('[data-replace-review]').click();await panel().locator('[data-replacement]').waitFor();
  assert.match(await panel().locator('[data-replacement]').innerText(),/current scene is reset/);
  await panel().locator('[data-replace-back]').click();await panel().locator('[data-replacement]').waitFor({state:'hidden'});
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));
  await page.getByText('PREPARATION_SOURCE_UNCHANGED',{exact:true}).waitFor();
 });
 await step('Apply the reviewed result and render its independent copy in the original canvas',async()=>{
  await panel().locator('[data-replace-review]').click();await panel().locator('[data-replacement]').waitFor();
  await panel().locator('[data-replace-apply]').click();
  await panel().locator('[data-context]').filter({hasText:'7,868 atoms'}).waitFor();
  await panel().locator('[data-replacement]').waitFor({state:'hidden'});
  assert.equal(await panel().locator('[data-replace-review]').isVisible(),false);
  assert.match(await panel().locator('[data-replace-unavailable]').innerText(),/has been loaded here/);
  await page.screenshot({path:output+'/chemistry-preparation-applied.png',fullPage:true});
 });
 await step('Inspect the adopted molecular data in the canvas popup and detached Studio',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  await canvas.locator('[data-task]').selectOption('hydrogens');await canvas.locator('[data-source]').selectOption('all');await canvas.locator('[data-inspect]').click();
  await canvas.locator('[data-report-scope]').filter({hasText:'7,868 selected atoms'}).waitFor();
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);
  await studio.locator('[data-task]').selectOption('hydrogens');await studio.locator('[data-source]').selectOption('all');await studio.locator('[data-inspect]').click();
  await studio.locator('[data-report-scope]').filter({hasText:'7,868 selected atoms'}).waitFor();
  await studio.screenshot({path:output+'/chemistry-preparation-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Python verifies one replacement, original preservation and independent result coordinates',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('JUPYTER_PREPARATION_NATIVE_OK 7868',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual TcTIM/Jupyter/Mol*/AnyWidget preparation, independent notebook result, heavy no-op 3983 atoms, hydrogen generation 7868 atoms, explicit losses, Back, conditional replacement and popup inspection. Source overlay; not human Qt or installed artifact qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
