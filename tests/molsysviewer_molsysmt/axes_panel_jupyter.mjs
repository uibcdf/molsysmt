/** Principal-axis tensor invariants through real Jupyter and Mol* vertices. */
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


 await page.evaluate(()=>{
  window.__principalCheck=(index,oracle)=>{
   const now=window.__geometryPositions(index),before=oracle.before_angstrom;
   if(!now||now.length!==62)return false;
   const close=(a,b,tol=1e-4)=>Math.abs(a-b)<tol;
   if(!now.slice(8).every((xyz,i)=>xyz.every((v,j)=>close(v,before[i+8][j]))))return false;
   const weights=oracle.weights,total=weights.reduce((a,b)=>a+b,0);
   const center=[0,1,2].map(j=>now.slice(0,8).reduce((sum,xyz,i)=>sum+weights[i]*xyz[j],0)/total);
   if(!center.every((v,j)=>close(v,oracle.target_center_angstrom[j])))return false;
   const projected=now.slice(0,8).map(xyz=>oracle.basis.map(row=>row.reduce((sum,v,j)=>sum+v*(xyz[j]-center[j]),0)));
   for(let a=0;a<3;a++)for(let b=0;b<3;b++){
    const moment=projected.reduce((sum,xyz,i)=>sum+weights[i]*xyz[a]*xyz[b],0)/total;
    if(!close(moment,a===b?oracle.target_variances_angstrom2[a]:0,1e-3))return false;
   }
   for(let a=0;a<8;a++)for(let b=0;b<8;b++){
    const dist=(x,y)=>Math.hypot(...x.map((v,j)=>v-y[j]));
    if(!close(dist(now[a],now[b]),dist(before[a],before[b])))return false;
   }
   const volume=xyz=>{
    const [a,b,c]=[1,2,3].map(i=>xyz[i].map((v,j)=>v-xyz[0][j]));
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]);
   };
   return close(volume(now),volume(before),1e-3);
  };
 });
 await step('Review principal-axis options and cancel without copying or moving the system',async()=>{
  await panel().locator('[data-task]').selectOption('axes');await panel().getByRole('heading',{name:'Align principal axes',exact:true}).waitFor();
  await panel().locator('[data-source]').selectOption('indices');await panel().locator('[data-indices]').fill('0,1,2,3,4,5,6,7,2');
  assert.equal(await panel().locator('[data-axes-type]').inputValue(),'inertia');
  assert.equal(await panel().locator('[data-axes-weights]').inputValue(),'uniform');
  await panel().locator('[data-scope]').selectOption('indices');await panel().locator('[data-frames]').fill('2, 0');
  await panel().locator('[data-preview]').click();await panel().locator('[data-review]').waitFor({state:'visible'});
  assert.match(await panel().locator('[data-review-summary]').innerText(),/Align 8 atoms in 2 structures using 8 reference atoms.*inertia tensor.*equal atom weights/);
  assert.match(await panel().locator('[data-review-scope]').innerText(),/Structures: 2, 0/);
  await panel().locator('[data-back]').click();await panel().locator('[data-preview]').waitFor({state:'visible'});
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__geometryBefore));
 });
 await step('Apply inertia alignment and compare actual Mol* vertices with independent tensor invariants',async()=>{
  await panel().locator('[data-preview]').click();await panel().locator('[data-confirm]').click();
  await panel().locator('[data-status]').filter({hasText:'Principal-axis alignment applied. The view is up to date.'}).waitFor();
  const oracle=JSON.parse(await readFile(output+'/axes-source-oracle.json','utf8'));
  await page.waitForFunction(oracle=>window.__principalCheck(0,oracle),oracle);
  assert.notDeepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__geometryBefore));
  await page.evaluate(()=>window.__axesSource=window.__geometryPositions(0));
 });
 await step('Capture the unchanged source reference for a distinct mass-weighted result',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_AXES_REFERENCE_OK',{exact:true}).waitFor();
 });
 await step('Create a centered covariance result in explicit row axes and inspect its actual geometry',async()=>{
  await panel().locator('[data-axes-type]').selectOption('geometric');await panel().locator('[data-axes-weights]').selectOption('masses');
  await panel().locator('[data-axes-center]').selectOption('origin');await panel().locator('[data-axes-target]').selectOption('custom');
  await panel().locator('[data-axes-basis]').fill('0 1 0; 0 0 1; 1 0 0');
  await panel().locator('[data-scope]').selectOption('current');await panel().locator('[data-effect]').selectOption('result');
  await panel().locator('[data-title]').fill('Principal-axis result');await panel().locator('[data-preview]').click();
  await panel().locator('[data-confirm]').filter({hasText:'Create aligned result'}).click();await panel().locator('[data-result]').waitFor({state:'visible'});
  assert.match(await panel().locator('[data-result-provenance]').innerText(),/Aligned structures: 0/);
  await panel().locator('[data-show-notebook]').click();await page.waitForFunction(()=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===62);
  const oracle=JSON.parse(await readFile(output+'/axes-result-oracle.json','utf8'));
  await page.waitForFunction(oracle=>window.__principalCheck(1,oracle),oracle);
  assert.deepEqual(await page.evaluate(()=>window.__geometryPositions(0)),await page.evaluate(()=>window.__axesSource));
  await page.screenshot({path:output+'/axes-independent.png',fullPage:true});
 });
 await step('The principal-axis result keeps its identity across window and notebook destinations',async()=>{
  const opened=page.waitForEvent('popup');await panel().locator('[data-show-window]').click();const child=await opened;record(child);
  await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await panel().locator('[data-status]').filter({hasText:'Result opened in its own window.'}).waitFor();
  assert.equal(await child.title(),'Principal-axis result');
  const closed=child.waitForEvent('close');await panel().locator('[data-show-notebook]').click();await closed;
  await panel().locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();assert.equal(await page.evaluate(()=>window.__controllers.length),2);
 });
 await step('Principal-axis definitions weights and target rows survive both popup boundaries',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();
  await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const studioTab=studio.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');await studioTab.waitFor({state:'visible'});await studioTab.click();
  await studio.locator('[data-molsysviewer-addon-panel-tab="geometry"]').click();await studio.getByRole('heading',{name:'Align principal axes',exact:true}).waitFor();
  assert.equal(await studio.locator('[data-axes-type]').inputValue(),'geometric');
  assert.equal(await studio.locator('[data-axes-weights]').inputValue(),'masses');
  assert.equal(await studio.locator('[data-axes-center]').inputValue(),'origin');
  assert.equal(await studio.locator('[data-axes-target]').inputValue(),'custom');
  assert.equal(await studio.locator('[data-axes-basis]').inputValue(),'0 1 0; 0 0 1; 1 0 0');
  await studio.screenshot({path:output+'/axes-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Python verifies every selected and unselected atom and structure',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('JUPYTER_AXES_NATIVE_OK 1',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Real local JupyterLab/ipykernel/AnyWidget, native principal-axis alignment with distinct weights/tensors/centers/bases, ordered structures, independent covariance and proper-rigid numerical invariants, independent Mol* result and detached Geometry controls. Not visible human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [index,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+index+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
