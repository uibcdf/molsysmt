/** Signed rotations through real Jupyter, Mol* vertices and independent popups. */
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
  const hot=p.getByRole('button',{name:'Show canvas controls',exact:true});await hot.focus();await p.keyboard.press('Enter');
  await toggle.click();
 }
 if(!await tab.isVisible()){const addons=p.locator('[data-molsysviewer-panel-stack-option="addons"]');await addons.waitFor({state:'visible'});await addons.click();}
 await tab.waitFor({state:'visible'});
 await tab.click();await p.locator('[data-molsysviewer-addon-panel-tab="geometry"]').click();await p.locator('[data-geometry-heading]').waitFor();
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


 await step('Review a molecular-axis rotation and cancel without changing Mol* vertices',async()=>{
  await panel().locator('[data-task]').selectOption('rotate');await panel().getByRole('heading',{name:'Rotate',exact:true}).waitFor();
  await panel().locator('[data-source]').selectOption('indices');await panel().locator('[data-indices]').fill('0,1,2,3,4,5,6,7,8,9,2');
  assert.equal(await panel().locator('[data-rotation-center-kind]').inputValue(),'geometric');
  assert.equal(await panel().locator('[data-angle-unit]').inputValue(),'degree');
  await panel().locator('[data-scope]').selectOption('indices');await panel().locator('[data-frames]').fill('2, 0');
  await panel().locator('[data-preview]').click();await panel().locator('[data-review]').waitFor({state:'visible'});
  assert.match(await panel().locator('[data-review-summary]').innerText(),/Rotate 10 atoms in 2 structures.*molecular axis.*90 degree.*each processed structure/);
  assert.match(await panel().locator('[data-review-scope]').innerText(),/Structures: 2, 0/);
  await panel().locator('[data-back]').click();await panel().locator('[data-preview]').waitFor({state:'visible'});
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__geometryBefore));
 });
 await step('Apply a signed quarter turn about each structure centroid and inspect actual vertices',async()=>{
  await panel().locator('[data-preview]').click();await panel().locator('[data-confirm]').click();
  await panel().locator('[data-status]').filter({hasText:'Rotation applied. The view is up to date.'}).waitFor();
  await page.waitForFunction(()=>{
   const now=window.__geometryPositions(0),before=window.__geometryBefore;if(!now||!before)return false;
   const center=[0,1,2].map(j=>before.slice(0,10).reduce((sum,xyz)=>sum+xyz[j],0)/10);
   return now.length===62&&now.every((xyz,i)=>xyz.every((v,j)=>{
    const expected=i>=10||j===2?before[i][j]:j===0?center[0]-(before[i][1]-center[1]):center[1]+(before[i][0]-center[0]);
    return Math.abs(v-expected)<1e-4;
   }));
  });
  await page.evaluate(()=>window.__rotatedSource=window.__geometryPositions(0));
 });
 await step('Create an independent negative-radian rotation about a unit-bearing fixed point',async()=>{
  await panel().locator('[data-rotation-center-kind]').selectOption('point');
  await panel().locator('[data-dx]').fill('1');await panel().locator('[data-dy]').fill('-2');await panel().locator('[data-dz]').fill('3');
  await panel().locator('[data-unit]').selectOption('angstrom');
  await panel().locator('[data-angle]').fill(String(-Math.PI/2));await panel().locator('[data-angle-unit]').selectOption('radian');
  await panel().locator('[data-scope]').selectOption('current');await panel().locator('[data-effect]').selectOption('result');
  await panel().locator('[data-title]').fill('Rotated result');await panel().locator('[data-preview]').click();
  await panel().locator('[data-confirm]').filter({hasText:'Create rotated result'}).click();await panel().locator('[data-result]').waitFor({state:'visible'});
  assert.match(await panel().locator('[data-result-provenance]').innerText(),/Rotated structures: 0/);
  await panel().locator('[data-show-notebook]').click();await page.waitForFunction(()=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===62);
  await page.waitForFunction(()=>{
   const source=window.__rotatedSource,result=window.__geometryPositions(1);
   return result?.length===62&&result.every((xyz,i)=>xyz.every((v,j)=>{
    const expected=i>=10||j===2?source[i][j]:j===0?1+(source[i][1]+2):-2-(source[i][0]-1);
    return Math.abs(v-expected)<1e-4;
   }));
  });
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__rotatedSource));
  await page.screenshot({path:output+'/rotate-independent.png',fullPage:true});
 });
 await step('The rotated result keeps its identity across window and notebook destinations',async()=>{
  const opened=page.waitForEvent('popup');await panel().locator('[data-show-window]').click();const child=await opened;record(child);
  await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await panel().locator('[data-status]').filter({hasText:'Result opened in its own window.'}).waitFor();
  assert.equal(await child.title(),'Rotated result');
  const closed=child.waitForEvent('close');await panel().locator('[data-show-notebook]').click();await closed;
  await panel().locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();assert.equal(await page.evaluate(()=>window.__controllers.length),2);
 });
 await step('Rotation axis angle and fixed point survive canvas and Studio popups',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();
  await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const studioTab=studio.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');await studioTab.waitFor({state:'visible'});await studioTab.click();
  await studio.locator('[data-molsysviewer-addon-panel-tab="geometry"]').click();await studio.getByRole('heading',{name:'Rotate',exact:true}).waitFor();
  assert.equal(await studio.locator('[data-az]').inputValue(),'1');
  assert.equal(await studio.locator('[data-angle]').inputValue(),String(-Math.PI/2));
  assert.equal(await studio.locator('[data-angle-unit]').inputValue(),'radian');
  assert.equal(await studio.locator('[data-rotation-center-kind]').inputValue(),'point');
  assert.equal(await studio.locator('[data-dy]').inputValue(),'-2');
  await studio.screenshot({path:output+'/rotate-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Python verifies every selected and unselected atom and structure',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_ROTATE_NATIVE_OK 1',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Real local JupyterLab/ipykernel/AnyWidget, native axis-angle rotation with per-structure centroids and fixed point, ordered structures, independent signed quarter-turn numerical oracles, independent Mol* result and detached Geometry controls. Not visible human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [index,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+index+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
