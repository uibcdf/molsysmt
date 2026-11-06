/** Real Mol* controller + actual addon ESM + persistent native Python authority. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {writeFile} from 'node:fs/promises';

const here=dirname(fileURLToPath(import.meta.url));
const viewerRoot=process.env.MOLSYSVIEWER_ROOT;
if(!viewerRoot)throw Error('Set MOLSYSVIEWER_ROOT to the qualified Viewer checkout.');
const require=createRequire(resolve(viewerRoot,'molsysviewer/js/package.json'));
const {chromium}=require('playwright');
const worker=spawn(process.env.PYTHON || 'python',[resolve(here,'system_panel_bridge.py')],{cwd:resolve(here,'../..'),env:process.env});
const pending=new Map();let nextId=1,stderr='';
worker.stderr.on('data',b=>{stderr+=b;});
const ready=new Promise((resolve,reject)=>pending.set(0,{resolve,reject}));
createInterface({input:worker.stdout}).on('line',line=>{
 try {const r=JSON.parse(line),p=pending.get(r.id);if(!p)return;pending.delete(r.id);if(r.error)p.reject(Error(r.error));else p.resolve(r.result);}
 catch(e){for(const p of pending.values())p.reject(Error('Invalid native bridge output: '+line+'\n'+e));pending.clear();}
});
worker.on('exit',code=>{for(const p of pending.values())p.reject(Error('Native bridge exited '+code+'\n'+stderr));pending.clear();});
function rpc(data){return new Promise((resolve,reject)=>{const id=nextId++;pending.set(id,{resolve,reject});worker.stdin.write(JSON.stringify({id,...data})+'\n');});}
let browser;
const errors=[],checks=[];
try {
 const init=await ready;
 assert.equal(init.n_atoms,3983);
 browser=await chromium.launch({headless:true,executablePath:process.env.PW_CHROMIUM_BIN || '/usr/bin/google-chrome',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1200,height:900}});
 page.on('pageerror',e=>errors.push(String(e)));
 await page.exposeFunction('__nativeEvent',event=>rpc({events:[event]}));
 await page.setContent('<div id="root" style="width:1140px;height:850px"></div>');
 await page.addScriptTag({path:resolve(viewerRoot,'molsysviewer/js/tests/e2e/harness.bundle.js')});
 await page.evaluate(async init=>{
  window.__backendErrors=[];window.__backendQueue=Promise.resolve();
  const allowed=new Set(['panel_navigate','panel_unmount','addon_panel_action','addon_panel_state_changed','interaction_context_action']);
  const controller=await window.Harness.createController('root',undefined,event=>{
   if(!allowed.has(event.event))return;
   window.__backendQueue=window.__backendQueue.then(async()=>{
    const result=await window.__nativeEvent(event);
    for(const message of result.messages)await window.__controller.handleMessage(message);
   }).catch(e=>window.__backendErrors.push(String(e)));
  });
  await controller.handleMessage(init.payload);
  for(const message of init.messages)await controller.handleMessage(message);
 },init);
 await page.waitForFunction(()=>window.__controller.getStructureData()?.elementCount===3983);
 await page.locator('[data-molsysviewer-group-panel-toggle="true"]').click();
 const addonsTab=page.locator('[data-molsysviewer-panel-stack-option="addons"]');
 if(await addonsTab.isVisible())await addonsTab.click();
 await page.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').click();
 const panel=page.locator('.msm-system');
 await panel.waitFor({state:'visible'});
 assert.equal(await panel.evaluate(el=>getComputedStyle(el).display),'flex','Host CSS must survive the addon replacing its render content.');
 await page.waitForFunction(()=>document.querySelector('.msm-system [data-context]')?.textContent?.includes('3,983'));
 await panel.locator('[data-source]').selectOption('category');
 await panel.locator('[data-category]').selectOption('water');
 await panel.locator('[data-preview]').click();
 await panel.locator('[data-review]').waitFor({state:'visible'});
 assert.equal(await panel.locator('[data-remove-count]').innerText(),'165');
 assert.equal(await panel.locator('[data-keep-count]').innerText(),'3,818');
 if(process.env.MOLSYSVIEWER_PANEL_SCREENSHOT)await page.screenshot({path:process.env.MOLSYSVIEWER_PANEL_SCREENSHOT,fullPage:true});
 checks.push('Actual host workspace mounts addon ESM and native 1TCD review reports 165/3818 atoms.');
 await panel.locator('[data-confirm]').click();
 await page.waitForFunction(()=>window.__controller.getStructureData()?.elementCount===3818);
 await page.waitForFunction(()=>document.querySelector('.msm-system [data-context]')?.textContent?.includes('3,818'));
 let backend=await rpc({});
 assert.equal(backend.n_atoms,3818);assert.equal(backend.status.target_revision,1);
 checks.push('Real click-to-Python removal updates actual Mol* structure to 3818 atoms; native revision advances once.');
 await panel.locator('[data-category]').selectOption('ions');
 await panel.locator('[data-preview]').click();
 await page.waitForFunction(()=>document.querySelector('.msm-system [data-status]')?.textContent?.includes('Nothing to remove'));
 backend=await rpc({});assert.equal(backend.status.target_revision,1);
 checks.push('Zero ion matches remain a native no-op without another managed revision.');
 backend=await rpc({external_edit:true});
 assert.equal(backend.status.state,'pending');assert.equal(backend.n_atoms,3817);
 await page.evaluate(async messages=>{for(const m of messages)await window.__controller.handleMessage(m);},backend.messages);
 await page.getByRole('button',{name:/update view/i}).click();
 await page.waitForFunction(()=>window.__controller.getStructureData()?.elementCount===3817);
 await page.waitForFunction(()=>document.querySelector('.msm-system [data-context]')?.textContent?.includes('3,817'));
 backend=await rpc({});assert.equal(backend.status.state,'synchronized');assert.equal(backend.status.target_revision,2);
 checks.push('Host Update view reconciles a real pending edit; generic status event refreshes addon without repeating science.');
 await page.locator('[data-molsysviewer-addon-workspace-tab="core"]').click();
 await panel.waitFor({state:'detached'});
 assert.equal(await page.locator('style').evaluateAll(nodes=>nodes.filter(n=>n.textContent.includes('.msm-system')).length),0,'Unloaded panel CSS must not leak into other workspaces.');
 await page.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]').click();
 await panel.waitFor({state:'visible'});
 await page.waitForFunction(()=>document.querySelector('.msm-system [data-category]')?.value==='ions');
 assert.equal(await panel.evaluate(el=>getComputedStyle(el).display),'flex');
 assert.equal(await panel.locator('[data-review]').isVisible(),false);
 checks.push('Unmount/remount preserves the bounded draft and never restores an executable review token.');
 await page.evaluate(()=>window.__backendQueue);
 assert.deepEqual(await page.evaluate(()=>window.__backendErrors),[]);
 assert.deepEqual(errors,[]);
 const receipt={scope:'Local headless real Mol* + addon ESM + persistent Python/native source. Not a live Jupyter, visible Qt, popup or installed-artifact certificate.',checks,page_errors:errors,native_source:init.native_source};
 if(process.env.MOLSYSVIEWER_PANEL_RECEIPT)await writeFile(process.env.MOLSYSVIEWER_PANEL_RECEIPT,JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt,null,2));
 await page.evaluate(()=>window.__controller.dispose());
} finally {
 if(browser)await browser.close();
 worker.stdin.end();
 if(worker.exitCode===null){await new Promise(resolve=>{const t=setTimeout(()=>{worker.kill();resolve();},5000);worker.once('exit',()=>{clearTimeout(t);resolve();});});}
}
