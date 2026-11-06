/** Actual Jupyter transport receiving; run through system_panel_jupyter.py. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const settingsPath=process.env.MOLSYSVIEWER_JUPYTER_SETTINGS;
if(!settingsPath)throw Error('Set MOLSYSVIEWER_JUPYTER_SETTINGS to the isolated launcher settings.');
const out=dirname(resolve(settingsPath));
const config=JSON.parse(await readFile(settingsPath,'utf8'));
const root=config.viewer_root;
const require=createRequire(root+'/molsysviewer/js/package.json');
const {chromium}=require('playwright');
const errors=[],checks=[],baselineErrors=[];
let browser,page,stage='start';
async function step(label, action){stage=label;console.log('STEP '+label);await action();checks.push(label);}
async function controls(p){
 const surface=p.locator('.molsysviewer-controls');await surface.waitFor({state:'attached',timeout:120000});
 const hot=p.getByRole('button',{name:'Show canvas controls',exact:true});
 await hot.focus();await p.keyboard.press('Enter');
}
async function workspace(p){
 const toggle=p.getByTitle('Panel mode (N / W)',{exact:true});
 if(!await p.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').isVisible()){
  if(await toggle.count()){await controls(p);await toggle.click();}
 }
 const tab=p.locator('[data-molsysviewer-panel-stack-option="addons"]');
 if(!await p.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').isVisible()){await tab.waitFor({state:'visible'});await tab.click();}
 await p.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').click();
 await p.locator('.msm-system [data-context]').waitFor();
}
async function execute(p,cell){
 await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
 await cell.locator('.cm-content').click();
 await p.getByRole('button',{name:/Run this cell and advance/}).click();
}
const panel=p=>p.locator('.msm-system');
async function selected(p,source,value){
 await panel(p).locator('[data-source]').selectOption(source);
 const field=source==='category'?'category':source==='indices'?'indices':'expression';
 if(field==='category')await panel(p).locator('[data-category]').selectOption(value);
 else await panel(p).locator(`[data-${field}]`).fill(value);
 await panel(p).locator('[data-preview]').click();
}
const atoms=n=>page.waitForFunction(n=>window.__receivingControllers?.at(-1)?.getStructureData()?.elementCount===n,n);
try {
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',e=>baselineErrors.push({message:String(e),stack:e.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/receiving-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(baseline,plain);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});
 page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',e=>errors.push({stage,message:String(e),stack:e.stack}));record(page);
 await page.addInitScript(()=>{
  let runtime;window.__receivingControllers=[];window.__receivingDraws=0;window.__receivingStatusHistory=[];new MutationObserver(()=>{const e=document.querySelector('.msm-system [data-status]');if(e){const value=e.textContent+' | '+e.dataset.stage;if(window.__receivingStatusHistory.at(-1)!==value)window.__receivingStatusHistory.push(value);}}).observe(document,{childList:true,subtree:true,characterData:true});
  Object.defineProperty(window,'__molsysviewer_anywidget_runtime__',{configurable:true,get:()=>runtime,set(value){
   runtime=value;const C=value?.module?.MolSysViewerController;if(!C)return;
   const create=C.create;C.create=async function(...args){const c=await create.apply(this,args);window.__receivingControllers.push(c);c.plugin.canvas3d.didDraw.subscribe(()=>window.__receivingDraws++);return c;};
  }});
 });
 await step('Execute real notebook with source-pinned Python 3.14 kernel',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/receiving-system-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();
  await execute(page,cell);await atoms(3983);
  await page.waitForFunction(()=>window.__receivingDraws>0);
 });
 await step('Native review is 165 waters / 3818 retained; Back does not edit',async()=>{
  await workspace(page);await page.waitForFunction(()=>document.querySelector('.msm-system [data-context]')?.textContent?.includes('3,983'));
  assert.equal(await panel(page).evaluate(e=>getComputedStyle(e).display),'flex');
  await selected(page,'category','water');await panel(page).locator('[data-review]').waitFor();
  const layout=await panel(page).locator('.msm-stats > div').evaluateAll(nodes=>nodes.map(e=>{const dt=e.querySelector('dt'),dd=e.querySelector('dd'),a=dt.getBoundingClientRect(),b=dd.getBoundingClientRect();return {label:dt.textContent,dtFloat:getComputedStyle(dt).cssFloat,ddFloat:getComputedStyle(dd).cssFloat,labelBottom:a.bottom,valueTop:b.y,labelLeft:a.x,valueLeft:b.x};}));for(const row of layout){assert.equal(row.dtFloat,'none');assert.equal(row.ddFloat,'none');assert.ok(row.valueTop>=row.labelBottom,'Values must sit below their labels in real Jupyter');assert.ok(Math.abs(row.labelLeft-row.valueLeft)<1);}
  assert.equal(await panel(page).locator('[data-remove-count]').innerText(),'165');assert.equal(await panel(page).locator('[data-keep-count]').innerText(),'3,818');
  await writeFile(out+'/jupyter-stats-layout.json',JSON.stringify(await panel(page).locator('.msm-stats dt, .msm-stats dd').evaluateAll(nodes=>nodes.map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return{text:e.textContent,float:s.cssFloat,width:s.width,margin:s.margin,x:r.x,y:r.y,height:r.height};})),null,2));await page.screenshot({path:out+'/jupyter-review.png',fullPage:true});
  await panel(page).locator('[data-back]').click();await panel(page).locator('[data-review]').waitFor({state:'hidden'});await atoms(3983);
 });
 await step('Confirm traverses real widget comms, native edit and Mol* rendering',async()=>{
  await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-confirm]').click();await atoms(3818);
  await page.waitForFunction(()=>document.querySelector('.msm-system [data-status]')?.textContent?.includes('Selected atoms removed'));
 });
 await step('Empty ion selection and remount retain a bounded draft without a review',async()=>{
  await selected(page,'category','ions');await page.waitForFunction(()=>document.querySelector('.msm-system [data-status]')?.textContent?.includes('Nothing to remove'));
  await page.locator('[data-molsysviewer-addon-workspace-tab="core"]').click();await panel(page).waitFor({state:'detached'});
  await page.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').click();await panel(page).waitFor();
  await page.waitForFunction(()=>document.querySelector('.msm-system [data-category]')?.value==='ions');assert.equal(await panel(page).locator('[data-review]').isVisible(),false);
 });
 await step('Canvas popup and Studio popup share the actual Jupyter authority',async()=>{
  await selected(page,'indices','1');await panel(page).locator('[data-review]').waitFor();
  await controls(page);const opened=page.waitForEvent('popup');await page.getByTitle('Open popup',{exact:true}).click();
  const canvas=await opened;record(canvas);await canvas.locator('canvas').waitFor();await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  await canvas.waitForFunction(()=>document.querySelector('.msm-system [data-context]')?.textContent?.includes('3,818'));
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();
  const studio=await detached;record(studio);await studio.locator('[data-molsysviewer-panel-fullscreen="true"]').waitFor();await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);await panel(studio).waitFor();
  await canvas.getByTitle('Popout panel to external window',{exact:true}).waitFor({state:'hidden'});
  await selected(studio,'indices','0');await panel(studio).locator('[data-review]').waitFor();assert.equal(await panel(studio).locator('[data-remove-count]').innerText(),'1');
  await panel(studio).locator('[data-confirm]').click();await atoms(3817);
  await panel(page).locator('[data-review]').waitFor({state:'hidden'});
  await page.waitForFunction(()=>document.querySelector('.msm-system [data-context]')?.textContent?.includes('3,817'));
  await studio.screenshot({path:out+'/studio-popup.png',fullPage:true});
  await studio.close();await canvas.getByTitle('Popout panel to external window',{exact:true}).waitFor();
  await workspace(canvas);assert.equal(await panel(canvas).locator('[data-review]').isVisible(),false);await canvas.close();
 });
 await step('Kernel verifies actual inventory and exactly two managed edits',async()=>{
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1);await execute(page,cell);
  await page.getByText('JUPYTER_SYSTEM_NATIVE_OK 3817',{exact:true}).waitFor();
  assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
  await page.screenshot({path:out+'/jupyter-final.png',fullPage:true});
 });
 const fingerprint=e=>e.message+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(e=>baselineErrors.some(b=>fingerprint(b)===fingerprint(e))),'Viewer flow introduced a page error absent from the plain-notebook control');
 const receipt={baseline_errors:baselineErrors,scope:'Actual local JupyterLab server, ipykernel, anywidget/ipywidgets comms, real Mol* rendering and both popup lifecycles in headless Chromium. Not human visible Qt or installed-package qualification.',checks,errors,final_atoms:3817,managed_edits:2,python_source:config.contribution};
 await writeFile(out+'/full-result.json',JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt,null,2));
} catch(e){
 const failure={stage,error:String(e),errors,checks};console.log(JSON.stringify(failure,null,2));await writeFile(out+'/full-failure.json',JSON.stringify(failure,null,2)+'\n');
 if(browser){for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(out+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());}if(page){failure.status_history=await page.evaluate(()=>window.__receivingStatusHistory||[]);await writeFile(out+'/full-failure.json',JSON.stringify(failure,null,2)+'\n');await page.screenshot({path:out+'/full-failure.png',fullPage:true});await writeFile(out+'/full-failure-dom.txt',await page.locator('body').innerText());}process.exitCode=1;
} finally{if(browser)await browser.close();}
