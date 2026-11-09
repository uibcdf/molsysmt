/** Stored-chemistry inspection through actual Jupyter and popup controls. */
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
async function workspace(p){
 await openMolecularPanel(p,'chemistry');
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
 let expected;
 async function inspectAssessment(p,task){
  const widget=p.locator('.msm-chemistry').first();
  await widget.locator('[data-task]').selectOption(task);
  await widget.locator('[data-heading]').filter({hasText:task==='coverage'?'Assess exact-template coverage':task==='terminals'?'Inspect missing terminal atoms':'Assess reference-rule protonation'}).waitFor();
  if(task==='coverage')await widget.locator('[data-source]').selectOption('all');
  if(task==='protonation')await widget.locator('[data-assessment-ph]').fill('12');
  await widget.locator('[data-inspect]').click();await widget.locator('[data-report-heading]').filter({hasText:'report'}).waitFor();
  const details=widget.locator('[data-details]');if(!await details.evaluate(e=>e.open))await details.locator('summary').click();
  return widget;
 }
 async function table(widget){return widget.locator('[data-rows] tr').evaluateAll(rows=>rows.map(row=>Array.from(row.querySelectorAll('td'),cell=>cell.textContent)));}

 await step('Render bundled TcTIM and open Chemistry without starting an assessment',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/chemistry-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(cell);
  await page.locator('canvas').waitFor();await workspace(page);
  expected=JSON.parse(await readFile(output+'/assessment-expected.json','utf8'));
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
  const assessedCanvas=await inspectAssessment(canvas,'protonation');
  assert.match(await assessedCanvas.locator('[data-assessment-summary]').innerText(),new RegExp(`${expected.removed} proposed H removals, not applied`));
  await assessedCanvas.locator('[data-task]').selectOption('hydrogens');
  await assessedCanvas.locator('[data-heading]').filter({hasText:'Hydrogen inventory'}).waitFor();
  await assessedCanvas.locator('[data-inspect]').click();await assessedCanvas.locator('[data-report-scope]').filter({hasText:'3,983 selected atoms'}).waitFor();
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const tab=studio.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');await tab.waitFor({state:'visible'});await tab.click();
  await studio.locator('[data-molsysviewer-addon-panel-tab="chemistry"]').click();await studio.locator('.msm-chemistry').waitFor();
  await studio.locator('[data-inspect]').click();await studio.locator('[data-report-scope]').filter({hasText:'3,983 selected atoms'}).waitFor();
  await studio.screenshot({path:output+'/chemistry-studio-popup.png'});
  // Preserve all existing popup inspection assertions, then receive the new
  // whole-system reader independently on both actual endpoints.
  for(const host of [studio]){
   const widget=await inspectAssessment(host,'protonation');
   assert.match(await widget.locator('[data-assessment-summary]').innerText(),new RegExp(`${expected.removed} proposed H removals, not applied`));
   assert.equal(await widget.locator('[data-editor]').isVisible(),false);
  }
  await studio.screenshot({path:output+'/chemistry-assessment-studio.png'});
  await studio.locator('[data-clear]').click();await studio.locator('[data-report]').waitFor({state:'hidden'});await studio.close();await canvas.close();
 });
 await step('Inspect exact-template coverage with native source-group pages and unassessed scope',async()=>{
  const widget=await inspectAssessment(page,'coverage');
  const summary=await widget.locator('[data-assessment-summary]').innerText();
  assert.match(summary,new RegExp(`${expected.counts.assessed} assessed, ${expected.counts.incomplete} incomplete, ${expected.counts.unassessed} unassessed`));
  assert.equal((await table(widget)).length,50);
  assert.deepEqual((await table(widget))[0].slice(0,4),expected.coverage_first);
  await widget.locator('[data-next]').click();await widget.locator('[data-page-summary]').filter({hasText:'Rows 51–100'}).waitFor();
  assert.equal((await table(widget))[0][0],'50');
  await page.screenshot({path:output+'/chemistry-template-coverage.png',fullPage:true});
 });
 await step('Inspect missing terminal OXT on the whole system without certifying empty results',async()=>{
  const widget=await inspectAssessment(page,'terminals');
  assert.equal(await widget.locator('[data-editor]').isVisible(),false);
  assert.equal(await widget.locator('[data-chemical-state]').isVisible(),false);
  assert.deepEqual(await table(widget),expected.terminals);
  assert.match(await widget.locator('[data-assessment-summary]').innerText(),/empty result does not certify/);
  assert.equal(await widget.locator('[data-preparation]').isVisible(),false);
 });
 await step('Inspect a fixed-pKa removal decision without executing it or preparing a result',async()=>{
  const widget=await inspectAssessment(page,'protonation');
  assert.match(await widget.locator('[data-assessment-summary]').innerText(),new RegExp(`${expected.removed} proposed H removals, not applied`));
  assert.match(await widget.locator('[data-assessment-summary]').innerText(),new RegExp(`Native status: ${expected.status}`));
  assert.match(await widget.locator('[data-assessment-summary]').innerText(),new RegExp(`${expected.assessed} assessed groups; ${expected.unassessed} unassessed groups`));
  await widget.locator('[data-dataset]').selectOption('protonation_removals');
  if(expected.removal_rows.length)await widget.locator('[data-rows] tr').first().locator('td').first().filter({hasText:expected.removal_rows[0][0]}).waitFor();
  assert.deepEqual(await table(widget),expected.removal_rows);
  assert.equal(await widget.locator('[data-preparation-result]').isVisible(),false);
  await page.screenshot({path:output+'/chemistry-protonation-assessment.png',fullPage:true});
 });
 await step('Python verifies every source coordinate chemical domain scene and revision is unchanged',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_CHEMISTRY_UNCHANGED 3983',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual Jupyter/Mol*/AnyWidget stored-chemistry/hydrogen inventory plus exact-template, terminal OXT and fixed-pKa read-only assessments; bounded pages and both popup hosts. Synchronized source only; pending-state pointer/keyboard admission remains Viewer #304. Not human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
