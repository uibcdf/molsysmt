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
async function focusWhole(index){
 const surface=page.locator('[data-molsysviewer-canvas-output]').nth(index);
 await surface.locator('canvas').first().scrollIntoViewIfNeeded();
 const before=await page.evaluate(i=>({camera:window.__controllers[i].getCameraSnapshot(),sphere:window.__controllers[i].getStructureData().boundary.sphere}),index);
 await surface.locator('canvas').first().click({button:'right',position:{x:20,y:20}});
 await page.getByRole('menuitem',{name:'Focus All',exact:true}).click();
 await page.waitForFunction(i=>{
  const c=window.__controllers[i],camera=c.getCameraSnapshot(),sphere=c.getStructureData().boundary.sphere;
  return c.plugin.canvas3d.reprCount.value>0&&!c.plugin.canvas3d.camera.transition.inTransition&&camera?.target?.every(Number.isFinite)
   &&Math.hypot(...camera.target.map((v,j)=>v-sphere.center[j]))<sphere.radius+1;
 },index);
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 await writeFile(output+`/focus-${index}.json`,JSON.stringify({before,after:await page.evaluate(i=>({camera:window.__controllers[i].getCameraSnapshot(),sphere:window.__controllers[i].getStructureData().boundary.sphere,representations:window.__controllers[i].plugin.canvas3d.reprCount.value}),index)},null,2));
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
  await execute(cell);await page.waitForFunction(()=>window.__controllers?.[0]?.getStructureData()?.elementCount>0,null,{timeout:120000});
  await workspace(page);
  await focusWhole(0);
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


 const oracle=JSON.parse(await readFile(output+'/sequence-expected.json','utf8'));
 assert.equal(await page.evaluate(()=>window.__controllers[0].getStructureData().elementCount),oracle.n_atoms);
 await step('Reject a missing external reference without changing rendered coordinates',async()=>{
  await panel().locator('[data-task]').selectOption('sequence');
  await panel().getByRole('heading',{name:'Align components by sequence',exact:true}).waitFor();
  assert.equal(await panel().locator('[data-editor]').isVisible(),false);
  await panel().locator('[data-fit-reference-kind]').selectOption('file');
  await panel().locator('[data-fit-reference-file]').fill(oracle.reference_filename+'.missing');
  await panel().locator('[data-fit-reference-structure]').fill('4');
  await panel().locator('[data-fit-atoms]').fill('');
  await panel().locator('[data-fit-reference]').fill('');
  await panel().locator('[data-scope]').selectOption('indices');
  await panel().locator('[data-frames]').fill('2, 0, 2');
  await panel().locator('[data-preview]').click();
  await panel().locator('[data-status]').filter({hasText:/reference|file/i}).waitFor();
  await panel().locator('[data-preview]').waitFor({state:'visible'});
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__geometryBefore));
 });
 await step('Review unequal anchor populations and complete components then cancel without writes',async()=>{
  await panel().locator('[data-fit-reference-file]').fill(oracle.reference_filename);
  await panel().locator('[data-preview]').click();
  await panel().locator('[data-review]').waitFor({state:'visible'});
  const summary=await panel().locator('[data-review-summary]').innerText();
  assert.match(summary,new RegExp(`Align ${oracle.n_moving} atoms in complete source components across 2 structures`));
  assert.match(summary,/4 query anchors and 3 reference anchors/);
  assert.match(summary,/not a matched-pair count/);
  assert.ok(oracle.positional_counterfactual_nm>0.01);
  await panel().locator('[data-back]').click();
  await panel().locator('[data-preview]').waitFor({state:'visible'});
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__geometryBefore));
 });
 await step('Apply sequence and atom-name matching and verify actual Mol* coordinates',async()=>{
  await panel().locator('[data-preview]').click();await panel().locator('[data-confirm]').click();
  await panel().locator('[data-status]').filter({hasText:'Sequence-derived alignment applied. The view is up to date.'}).waitFor();
  await page.waitForFunction(expected=>{const now=window.__geometryPositions(0);return now?.length===expected.length&&now.every((xyz,i)=>xyz.every((v,j)=>Math.abs(v-expected[i][j])<1e-4));},oracle.source_angstrom[0]);
  await focusWhole(0);
  await page.evaluate(()=>window.__externalFittedSource=window.__geometryPositions(0));
 });
 await step('Create an independent result using another structure of the same external file',async()=>{
  await panel().locator('[data-fit-reference-structure]').fill('0');
  await panel().locator('[data-fit-atoms]').fill(JSON.stringify(oracle.query_atoms.slice().reverse().concat(oracle.query_atoms[0])));
  await panel().locator('[data-fit-reference]').fill(JSON.stringify(oracle.reference_atoms.slice().reverse().concat(oracle.reference_atoms[0])));
  await panel().locator('[data-scope]').selectOption('current');
  await panel().locator('[data-effect]').selectOption('result');
  await panel().locator('[data-title]').fill('Sequence alignment result');
  await panel().locator('[data-preview]').click();
  await panel().locator('[data-confirm]').filter({hasText:'Create sequence-aligned result'}).click();
  await panel().locator('[data-result]').waitFor({state:'visible'});
  await panel().locator('[data-show-notebook]').click();
  await page.waitForFunction(n=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===n,oracle.n_atoms);
  await page.waitForFunction(expected=>{const now=window.__geometryPositions(1);return now?.length===expected.length&&now.every((xyz,i)=>xyz.every((v,j)=>Math.abs(v-expected[i][j])<1e-4));},oracle.result_angstrom[0]);
  await focusWhole(1);
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__externalFittedSource));
  await page.screenshot({path:output+'/sequence-independent.png',fullPage:true});
 });
 await step('The external result retains its identity between notebook and independent window',async()=>{
  const opened=page.waitForEvent('popup');await panel().locator('[data-show-window]').click();
  const child=await opened;record(child);await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await panel().locator('[data-status]').filter({hasText:'Result opened in its own window.'}).waitFor();
  assert.equal(await child.title(),'Sequence alignment result');
  const closed=child.waitForEvent('close');await panel().locator('[data-show-notebook]').click();await closed;
  await panel().locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();
  assert.equal(await page.evaluate(()=>window.__controllers.length),2);
 });
 await step('Sequence population controls survive canvas and detached Studio popups',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();
  await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();
  const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();
  const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  await studio.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').click();
  await studio.locator('[data-molsysviewer-addon-panel-tab="geometry"]').click();
  await studio.getByRole('heading',{name:'Align components by sequence',exact:true}).waitFor();
  assert.equal(await studio.locator('[data-fit-reference-kind]').inputValue(),'file');
  assert.equal(await studio.locator('[data-fit-reference-file]').inputValue(),oracle.reference_filename);
  assert.equal(await studio.locator('[data-fit-atoms]').inputValue(),JSON.stringify(oracle.query_atoms.slice().reverse().concat(oracle.query_atoms[0])));
  assert.equal(await studio.locator('[data-fit-reference]').inputValue(),JSON.stringify(oracle.reference_atoms.slice().reverse().concat(oracle.reference_atoms[0])));
  assert.equal(await studio.locator('[data-fit-reference-structure]').inputValue(),'0');
  await studio.screenshot({path:output+'/sequence-studio.png'});await studio.close();await canvas.close();
 });
 await step('Python verifies all structures atoms units boxes coverage and the untouched reference file',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));
  await page.getByText('JUPYTER_SEQUENCE_ALIGN_NATIVE_OK 1',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Real local JupyterLab/ipykernel/AnyWidget, native sequence-derived component alignment with a sequence gap, permuted reference atoms, unequal populations, repeated source structures and an explicit unit policy, analytical rigid-transform oracles, independent Mol* results and detached Geometry controls. Not visible human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [index,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+index+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
