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
 await p.getByRole('heading',{name:'Translate',exact:true}).waitFor();
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


 await step('Review a native center-of-mass request under the explicit partial application policy',async()=>{
  await panel().locator('[data-task]').selectOption('center');await panel().getByRole('heading',{name:'Center',exact:true}).waitFor();
  await page.evaluate(()=>{window.__taskReplies=[];window.__errorPanelModel.on('msg:custom',msg=>{if(msg?.type==='state')window.__taskReplies.push({id:msg.state.request_id,stage:msg.state.stage,message:msg.state.message,revision:msg.state.context.target_revision,state:msg.state.context.state});});});
  await panel().locator('[data-source]').selectOption('indices');await panel().locator('[data-indices]').fill('0,1,2,3');
  await panel().locator('[data-center-kind]').selectOption('masses');await panel().locator('[data-preview]').click();await panel().locator('[data-review]').waitFor({state:'visible'});
 });
 await step('The native error remains visible after its automatic synchronized refresh',async()=>{
  await panel().locator('[data-confirm]').click();
  await page.waitForFunction(()=>window.__taskReplies.some(x=>x.stage==='error'));
  await page.waitForFunction(()=>{const error=window.__taskReplies.find(x=>x.stage==='error');return window.__taskReplies.some(x=>x.id>error.id&&x.state==='synchronized');});
  await page.waitForFunction(()=>/No standard units/.test(document.querySelector('.msm-system [data-status]')?.textContent||''));
  assert.equal(await panel().locator('[data-review]').isVisible(),false);
 });
 await step('Python verifies that the rejected native call did not mutate the system',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_NATIVE_ERROR_PRESERVED',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 await step('A new user choice clears the diagnostic and requires a new review',async()=>{
  await panel().locator('[data-center-kind]').selectOption('geometric');
  assert.equal(await panel().locator('[data-status]').innerText(),'');
  assert.equal(await panel().locator('[data-review]').isVisible(),false);
  await panel().locator('[data-preview]').click();await panel().locator('[data-review]').waitFor({state:'visible'});
  assert.equal(await panel().locator('[data-status]').innerText(),'');
  await panel().locator('[data-back]').click();await panel().locator('[data-review]').waitFor({state:'hidden'});
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Real local JupyterLab/ipykernel/AnyWidget, native centering rejection, actual synchronization/refresh notices and unchanged primary data. Not visible human Qt qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors,replies:page?await page.evaluate(()=>window.__taskReplies||[]):[]},null,2));if(browser){for(const [index,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+index+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
