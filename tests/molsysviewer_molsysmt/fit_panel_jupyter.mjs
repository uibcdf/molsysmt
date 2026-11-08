/** Independent results through actual Jupyter comms and the provider panel. */
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
 await openMolecularPanel(p,'geometry');
 await p.locator('[data-geometry-heading]').waitFor();
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
  await execute(cell);await page.waitForFunction(()=>window.__controllers?.[0]?.getStructureData()?.elementCount===62,null,{timeout:120000});
  await workspace(page);
  await page.evaluate(()=>{
   // Unit.conformation.position applies the unit's actual Mol* operator.
   // Native molecular payload indices are the model element indices here.
   window.__geometryPositions=index=>{
    const structure=window.__controllers[index]?.getStructureData();if(!structure)return null;
    const result=[];for(const unit of structure.units)for(const atom of unit.elements)result[atom]=Array.from(unit.conformation.position(atom,[0,0,0]));
    return result;
   };
   window.__geometryBefore=window.__geometryPositions(0);
  });
 });
 const panel=()=>page.locator('.msm-system').first();


 await step('Review explicit fitting atoms and cancel without changing rendered coordinates',async()=>{
  await panel().locator('[data-task]').selectOption('fit');await panel().getByRole('heading',{name:'Superpose structures',exact:true}).waitFor();
  await panel().getByRole('combobox',{name:'Atoms to move',exact:true}).waitFor({state:'visible'});
  await panel().locator('[data-source]').selectOption('indices');await panel().locator('[data-indices]').fill('0,1,2,3,4,5,6,7,8,9');
  await panel().locator('[data-fit-reference-structure]').fill('1');
  await panel().locator('summary').filter({hasText:'Fitting atoms and correspondence'}).click();
  await panel().locator('[data-fit-atoms]').fill("atom_name=='CA'");
  await panel().locator('[data-scope]').selectOption('indices');await panel().locator('[data-frames]').fill('2, 0');
  await panel().locator('[data-preview]').click();await panel().locator('[data-review]').waitFor({state:'visible'});
  assert.match(await panel().locator('[data-review-summary]').innerText(),/Superpose 10 moving atoms in 2 structures using 5 corresponding atom pairs and initial reference structure 1/);
  await panel().locator('[data-back]').click();await panel().locator('[data-preview]').waitFor({state:'visible'});
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__geometryBefore));
 });
 const oracle=JSON.parse(await readFile(output+'/fit-expected.json','utf8'));
 await step('Apply rigid superposition and compare actual Mol* positions with the independent SVD oracle',async()=>{
  await panel().locator('[data-preview]').click();await panel().locator('[data-confirm]').click();
  await panel().locator('[data-status]').filter({hasText:'Superposition applied. The view is up to date.'}).waitFor();
  await page.waitForFunction(expected=>{const now=window.__geometryPositions(0);return now?.length===62&&now.every((xyz,i)=>xyz.every((v,j)=>Math.abs(v-expected[i][j])<1e-4));},oracle.source_angstrom[0]);
  await page.evaluate(()=>window.__fittedSource=window.__geometryPositions(0));
 });
 await step('Create a separate result fitted to another explicit reference structure',async()=>{
  await panel().locator('[data-fit-reference-structure]').fill('2');await panel().locator('[data-scope]').selectOption('current');await panel().locator('[data-effect]').selectOption('result');
  await panel().locator('[data-title]').fill('Superposed result');await panel().locator('[data-preview]').click();
  await panel().locator('[data-confirm]').filter({hasText:'Create superposed result'}).click();await panel().locator('[data-result]').waitFor({state:'visible'});
  assert.match(await panel().locator('[data-result-provenance]').innerText(),/Superposed structures: 0/);
  await panel().locator('[data-show-notebook]').click();await page.waitForFunction(()=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===62);
  await page.waitForFunction(expected=>{const now=window.__geometryPositions(1);return now?.length===62&&now.every((xyz,i)=>xyz.every((v,j)=>Math.abs(v-expected[i][j])<1e-4));},oracle.result_angstrom[0]);
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__fittedSource));
  await page.screenshot({path:output+'/fit-independent.png',fullPage:true});
 });
 await step('The superposed result preserves its identity across window and notebook destinations',async()=>{
  const opened=page.waitForEvent('popup');await panel().locator('[data-show-window]').click();const child=await opened;record(child);
  await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await panel().locator('[data-status]').filter({hasText:'Result opened in its own window.'}).waitFor();
  assert.equal(await child.title(),'Superposed result');
  const closed=child.waitForEvent('close');await panel().locator('[data-show-notebook]').click();await closed;
  await panel().locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();assert.equal(await page.evaluate(()=>window.__controllers.length),2);
 });
 await step('Fitting references remain explicit in canvas and detached Studio popups',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();
  await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const tab=studio.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');await tab.waitFor({state:'visible'});await tab.click();
  await studio.locator('[data-molsysviewer-addon-panel-tab="geometry"]').click();await studio.getByRole('heading',{name:'Superpose structures',exact:true}).waitFor();
  assert.equal(await studio.locator('[data-fit-reference-structure]').inputValue(),'2');
  assert.equal(await studio.locator('[data-fit-atoms]').inputValue(),"atom_name=='CA'");
  await studio.screenshot({path:output+'/fit-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Python verifies every selected/unselected atom and structure against the independent oracle',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_FIT_NATIVE_OK 1',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 await step('Independent notebook Views bind saved-choice inputs to their own datalist',async()=>{
  await panel().locator('[data-new-result]').click();await panel().locator('[data-editor]').waitFor({state:'visible'});
  await panel().locator('[data-source]').selectOption('saved');await panel().locator('[data-name]').fill('chosen');
  const child=page.locator('[data-molsysviewer-canvas-output]').nth(1);
  await child.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  await child.getByTitle('Panel mode (N / W)',{exact:true}).click();
  const addons=child.locator('[data-molsysviewer-panel-stack-option="addons"], [data-molsysviewer-panel-stack-current="addons"]');if(await addons.count())await addons.click();
  await child.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').click();
  await child.locator('[data-molsysviewer-addon-panel-tab="system"]').click();
  await child.getByRole('heading',{name:'Remove atoms',exact:true}).waitFor();
  const association=await child.locator('.msm-system [data-name]').evaluate(input=>({own:input.list===input.closest('.msm-system').querySelector('datalist'),id:input.list?.id,ownId:input.closest('.msm-system').querySelector('datalist')?.id,names:Array.from(input.list?.options||[],option=>option.value)}));
  await writeFile(output+'/choice-association.json',JSON.stringify(association,null,2));
  assert.equal(association.own,true,'A saved-choice input must not resolve to a different View datalist');
  assert.ok(!association.names.includes('chosen'));
  const sourceNames=await panel().locator('[data-name]').evaluate(input=>Array.from(input.list?.options||[],option=>option.value));
  assert.ok(sourceNames.includes('chosen'));
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Real local JupyterLab/ipykernel/AnyWidget, native rigid fitting with explicit fitting/reference populations and reference structures, ordered structures, native numerical oracles, independent Mol* result and detached Geometry controls. Not visible human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [index,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+index+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
