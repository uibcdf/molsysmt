/** Independent results through actual Jupyter comms and the provider panel. */
import assert from 'node:assert/strict';
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
async function workspace(p){
 const tab=p.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');
 if(!await tab.isVisible()){
  const hot=p.getByRole('button',{name:'Show canvas controls',exact:true});await hot.focus();await p.keyboard.press('Enter');
  await p.getByTitle('Panel mode (N / W)',{exact:true}).click();
  const addons=p.locator('[data-molsysviewer-panel-stack-option="addons"]');if(!await tab.isVisible())await addons.click();
 }
 await tab.click();await p.locator('.msm-system').waitFor();
}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/results-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);
 await page.addInitScript(()=>{let runtime;window.__controllers=[];Object.defineProperty(window,'__molsysviewer_anywidget_runtime__',{configurable:true,get:()=>runtime,set(value){runtime=value;const C=value?.module?.MolSysViewerController;if(!C)return;const create=C.create;C.create=async function(...args){const c=await create.apply(this,args);window.__controllers.push(c);return c;};}});});
 await step('Render the source through the real notebook presentation surface',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/results-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();
  await execute(cell);await page.waitForFunction(()=>window.__controllers?.[0]?.getStructureData()?.elementCount===62,{timeout:120000});
  await workspace(page);
 });
 const panel=()=>page.locator('.msm-system').first();
 await step('Extract ordered nonconsecutive structures without editing the source',async()=>{
  await panel().locator('[data-task]').selectOption('extract');await panel().locator('[data-heading]').filter({hasText:'Extract subset'}).waitFor();
  await panel().locator('[data-source]').selectOption('indices');await panel().locator('[data-indices]').fill('2, 4, 6');
  await panel().locator('[data-structure-scope]').selectOption('indices');await panel().locator('[data-result-indices]').fill('2, 0');
  await panel().locator('[data-result-title]').fill('Subset review');await panel().locator('[data-create-result]').click();
  await panel().locator('[data-result]').waitFor({state:'visible'});assert.match(await panel().locator('[data-result-summary]').innerText(),/3 atoms.*2 structures/);
  await panel().locator('[data-show-notebook]').click();
  await page.waitForFunction(()=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===3);
  assert.equal(await page.locator('[data-molsysviewer-result]').count(),1);
  await page.screenshot({path:output+'/notebook-result.png',fullPage:true});
 });
 await step('Copy opens a separate live View in an external window without recomputing',async()=>{
  await panel().locator('[data-task]').selectOption('copy');await panel().locator('[data-heading]').filter({hasText:'Copy system'}).waitFor();
  await panel().locator('[data-result-title]').fill('Copy review');await panel().locator('[data-create-result]').click();await panel().locator('[data-result-heading]').filter({hasText:'Copy review'}).waitFor();
  const popup=page.waitForEvent('popup');await panel().locator('[data-show-window]').click();const child=await popup;
  record(child);await child.locator('canvas').waitFor();await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await page.waitForFunction(()=>window.__controllers.length===3&&window.__controllers[2].getStructureData()?.elementCount===62);
  assert.equal(await child.title(),'Copy review');
  await panel().locator('[data-show-window]').click();assert.equal(browser.contexts()[0].pages().length,2);
  await child.screenshot({path:output+'/independent-window.png'});
 });
 await step('Detached Studio can open and close an independent result without closing its source',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();
  await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);
  const controls=studio.locator('.msm-system');await controls.locator('[data-task]').selectOption('copy');await controls.locator('[data-heading]').filter({hasText:'Copy system'}).waitFor();
  await controls.locator('[data-result-title]').fill('Temporary result');await controls.locator('[data-create-result]').click();await controls.locator('[data-result-heading]').filter({hasText:'Temporary result'}).waitFor();
  const resultOpened=browser.contexts()[0].waitForEvent('page');await controls.locator('[data-show-window]').click();const independent=await resultOpened;record(independent);
  await independent.locator('canvas').waitFor();await independent.locator('#molsysviewer-loading').waitFor({state:'hidden'});assert.equal(await independent.title(),'Temporary result');
  await independent.close();await studio.close();await canvas.close();
  await page.waitForFunction(()=>document.querySelectorAll('[data-molsysviewer-result]').length===2);
 });
 await step('Python recovers both Views and source closure preserves them',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_INDEPENDENT_RESULTS_OK 2',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
  assert.equal(browser.contexts()[0].pages().length,2);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Real local JupyterLab/ipykernel/AnyWidget, ordered native extraction, independent Mol* Views, notebook and browser-window presentation including detached Studio. Not visible human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
