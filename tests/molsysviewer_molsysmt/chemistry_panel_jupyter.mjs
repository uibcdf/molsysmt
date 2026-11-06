/** Stored-chemistry inspection through actual Jupyter and popup controls. */
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
 const toggle=p.getByTitle('Panel mode (N / W)',{exact:true});
 if(!await tab.isVisible()&&await toggle.count()){
  const hot=p.getByRole('button',{name:'Show canvas controls',exact:true});await hot.focus();await p.keyboard.press('Enter');await toggle.click();
 }
 if(!await tab.isVisible()){const addons=p.locator('[data-molsysviewer-panel-stack-option="addons"]');await addons.waitFor({state:'visible'});await addons.click();}
 await tab.waitFor({state:'visible'});await tab.click();await p.locator('[data-molsysviewer-addon-panel-tab="chemistry"]').click();
 await p.locator('.msm-chemistry').waitFor();
}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/chemistry-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);
 const panel=()=>page.locator('.msm-chemistry').first();
 await step('Render bundled TcTIM and open Chemistry without starting an assessment',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/chemistry-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(cell);
  await page.locator('canvas').waitFor();await workspace(page);
  assert.equal(await panel().locator('[data-report]').isVisible(),false);
  assert.equal(await panel().locator('[data-inspect]').isDisabled(),true);
 });
 await step('Inspect actual stored fields with distinct present partial and missing coverage',async()=>{
  await panel().locator('[data-source]').selectOption('all');await panel().locator('[data-inspect]').click();
  await panel().locator('[data-report-heading]').filter({hasText:'Stored chemistry report'}).waitFor();
  assert.match(await panel().locator('[data-report-scope]').innerText(),/3,983 selected atoms.*structure 0/);
  const formal=panel().locator('[data-fields] tr').filter({hasText:'Formal charge'});assert.match(await formal.innerText(),/missing/);
  const order=panel().locator('[data-fields] tr').filter({hasText:'Bond order'});assert.match(await order.innerText(),/partial/);
  assert.match(await panel().locator('[data-state-summary]').innerText(),/Chemical state: 0.*resolved/);
  await page.screenshot({path:output+'/chemistry-fields.png',fullPage:true});
 });
 await step('Read bounded source-index pages without recalculating the molecular system',async()=>{
  await panel().locator('[data-details] summary').click();
  assert.equal(await panel().locator('[data-rows] tr').count(),50);
  assert.equal(await panel().locator('[data-rows] tr').first().locator('td').first().innerText(),'0');
  await panel().locator('[data-next]').click();await panel().locator('[data-page-summary]').filter({hasText:'Rows 51–100'}).waitFor();
  assert.equal(await panel().locator('[data-rows] tr').first().locator('td').first().innerText(),'50');
  await panel().locator('[data-dataset]').selectOption('formal_charge');await panel().locator('[data-page-unit]').filter({hasText:'elementary_charge'}).waitFor();
  assert.equal(await panel().locator('[data-rows] tr').first().locator('td').nth(1).innerText(),'Unknown');
 });
 await step('Inspect a duplicate numeric selection and expose unassessed scientific checks',async()=>{
  await panel().locator('[data-change-inspection]').click();
  await panel().locator('[data-source]').selectOption('indices');await panel().locator('[data-indices]').fill('2,0,2');
  assert.equal(await panel().locator('[data-report]').isVisible(),false);
  await panel().locator('[data-inspect]').click();await panel().locator('[data-report-scope]').filter({hasText:'2 selected atoms'}).waitFor();
  await panel().locator('summary').filter({hasText:'What was not assessed'}).click();
  assert.match(await panel().locator('[data-unassessed]').innerText(),/valence/);
  assert.match(await panel().locator('[data-unassessed]').innerText(),/protonation/);
 });
 await step('Keep unknown hydrogen counts distinct from zero and indexed atoms',async()=>{
  await panel().locator('[data-task]').selectOption('hydrogens');await panel().locator('[data-heading]').filter({hasText:'Hydrogen inventory'}).waitFor();
  await panel().locator('[data-source]').selectOption('all');await panel().locator('[data-inspect]').click();
  await panel().locator('[data-inventory-status]').filter({hasText:'unassessed'}).waitFor();
  const details=panel().locator('[data-details]');if(!await details.evaluate(e=>e.open))await details.locator('summary').click();
  assert.equal(await panel().locator('[data-rows] tr').first().locator('td').nth(2).innerText(),'Unknown');
  assert.equal(await panel().locator('[data-rows] tr').first().locator('td').nth(3).innerText(),'Unknown');
  assert.match(await panel().locator('[data-count-convention]').innerText(),/-1 is unknown/);
 });
 await step('Use the same native reports and clear only panel data in both popup hosts',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  await canvas.locator('[data-inspect]').click();await canvas.locator('[data-report-scope]').filter({hasText:'3,983 selected atoms'}).waitFor();
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const tab=studio.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');await tab.waitFor({state:'visible'});await tab.click();
  await studio.locator('[data-molsysviewer-addon-panel-tab="chemistry"]').click();await studio.locator('.msm-chemistry').waitFor();
  await studio.locator('[data-inspect]').click();await studio.locator('[data-report-scope]').filter({hasText:'3,983 selected atoms'}).waitFor();
  await studio.screenshot({path:output+'/chemistry-studio-popup.png'});
  await studio.locator('[data-clear]').click();await studio.locator('[data-report]').waitFor({state:'hidden'});await studio.close();await canvas.close();
 });
 await step('Python verifies every source coordinate chemical domain scene and revision is unchanged',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_CHEMISTRY_UNCHANGED 3983',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual Jupyter/Mol*/AnyWidget stored-chemistry and hydrogen inventory, bounded pages, native coverage and both popup hosts. Synchronized source only; pending-state pointer/keyboard admission remains Viewer #304. Not human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
