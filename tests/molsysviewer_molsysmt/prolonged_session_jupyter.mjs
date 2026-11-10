/** One scientific kernel, weak controller observation, real notebook and popups. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const config=JSON.parse(await readFile(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS,'utf8'));
const output=dirname(resolve(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
const cycles=Number(process.env.MSV_LONG_CYCLES??30),activeSeconds=Number(process.env.MSV_LONG_ACTIVE_SECONDS??30);
assert.ok(Number.isInteger(cycles)&&cycles>0&&cycles<=30&&activeSeconds>=.5&&activeSeconds<=90);
let browser,page,stage='start';const errors=[],baselineErrors=[],records=[],started=Date.now();
const cell=(i,p=page)=>p.locator('.jp-NotebookPanel:visible .jp-Cell').nth(i);
const surface=i=>cell(i).locator('[data-molsysviewer-canvas-output]').first();
async function execute(i,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();await cell(i,p).locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
async function marker(s){await page.waitForFunction(s=>document.querySelector('.jp-OutputArea-error')||[...document.querySelectorAll('.jp-OutputArea-output')].some(n=>n.textContent.trim()===s),s);assert.equal(await page.locator('.jp-OutputArea-error').count(),0,'Notebook cell reported a Python exception');await page.getByText(s,{exact:true}).waitFor();}
async function controls(p,scope=p){await scope.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await p.keyboard.press('Enter');}
async function installObservation(p){
 await p.addInitScript(()=>{
  window.__longRefs=[];
  let runtime;
  Object.defineProperty(window,'__molsysviewer_anywidget_runtime__',{configurable:true,get:()=>runtime,set(value){
   runtime=value;const C=value?.module?.MolSysViewerController;if(!C||C.create.__longWrapped)return;
   const create=C.create;const wrapped=async function(...args){const c=await create.apply(this,args);window.__longRefs.push(new WeakRef(c));
    const original=c.trajectory.setTrajectoryFrame;c.trajectory.setTrajectoryFrame=function(...parameters){const trace=window.__longFrameTrace??=[];const row={viewer_id:c.initOptions?.model?.get('runtime_viewer_id'),requested:typeof parameters[0]==='number'?parameters[0]:parameters[0]?.index,before:c.trajectory.getTrajectoryState().currentFrame,at:performance.now()};trace.push(row);if(trace.length>4096)trace.shift();const result=original.apply(this,parameters);Promise.resolve(result).then(value=>{row.result=value;row.after=c.trajectory.getTrajectoryState().currentFrame;},error=>{row.error=error.name;});return result;};return c;};wrapped.__longWrapped=true;C.create=wrapped;
  }});
  const open=window.open.bind(window);
  window.open=(...args)=>{
   const win=open(...args);if(!win)return win;const append=win.Node.prototype.appendChild;
   win.Node.prototype.appendChild=function(node){
    if(node.tagName==='SCRIPT'&&node.textContent.includes('await boot(module)'))node.textContent=node.textContent.replace('await boot(module)',`const create=module.MolSysViewerController.create;module.MolSysViewerController.create=async function(...args){const c=await create.apply(this,args);window.__longRefs=[...(window.__longRefs||[]),new WeakRef(c)];return c;};await boot(module)`);
    return append.call(this,node);
   };return win;
  };
 });
}
async function bind(p,i,viewerId){
 if(p===page){await surface(i).scrollIntoViewIfNeeded();const handle=await surface(i).elementHandle();await p.waitForFunction(({root,viewerId})=>{
  const c=(window.__longRefs??[]).map(r=>r.deref()).find(c=>c?.canvasHost?.isConnected&&root.contains(c.canvasHost)&&(!viewerId||c.initOptions?.model?.get('runtime_viewer_id')===viewerId));
  if(c){window.__longActive=c;return true;}return false;
 },{root:handle,viewerId});}
 else await p.waitForFunction(()=>{const c=(window.__longRefs??[]).map(r=>r.deref()).find(c=>c?.canvasHost?.isConnected);if(c){window.__longActive=c;return true;}return false;});
}
async function frame(p,index){await p.waitForFunction(index=>window.__longActive?.trajectory.getTrajectoryState().currentFrame===index,index);}
const recordPage=p=>p.on('pageerror',e=>errors.push({stage,error:String(e),stack:e.stack}));
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--enable-precise-memory-info','--js-flags=--expose-gc']});
 const plain=await browser.newPage();plain.on('pageerror',e=>baselineErrors.push({error:String(e),stack:e.stack}));await plain.goto(`http://127.0.0.1:${config.port}/lab/workspaces/long-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await plain.locator('.jp-Cell').first().filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(0,plain);await plain.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await plain.close();
 page=await browser.newPage({viewport:{width:1500,height:1200}});page.setDefaultTimeout(30000);recordPage(page);await installObservation(page);
 await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/long-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await cell(0).filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(0);await marker('LONG_SETUP_READY');await surface(0).locator('canvas').waitFor();await bind(page,0,JSON.parse(await readFile(output+'/witness-expected.json','utf8')).viewer_id);
 const witnessInitialization=await page.evaluate(async()=>{
  const c=window.__longActive,canvas=c.plugin.canvas3d;const before=canvas.camera.getSnapshot(),initialAtoms=c.getStructureData()?.elementCount??0;
  const snapshot=await new Promise((resolve,reject)=>{let subscription,requested=false;const timer=setTimeout(()=>{subscription?.unsubscribe();reject(new Error('Witness did not complete its initial molecular framing'));},30000);
   subscription=canvas.didDraw.subscribe(()=>{if(!requested)return;const s=canvas.camera.getSnapshot(),radius=canvas.boundingSphere.radius*(canvas.props.sceneRadiusFactor??1);
    if(c.getStructureData()?.elementCount!==3983||canvas.camera.transition.inTransition||radius<=0||Math.abs(s.radiusMax-radius)/radius>=.1)return;
    clearTimeout(timer);subscription.unsubscribe();resolve(s);
   });requested=true;canvas.requestDraw();
  });
  window.__longWitness=c;const s=snapshot;window.__longWitnessCamera=JSON.stringify({position:s.position,target:s.target,up:s.up,fov:s.fov,mode:s.mode});delete window.__longActive;return {initial_atoms:initialAtoms,before,after:snapshot,criterion:'Actual completed native draw, 3983 loaded atoms, native initial-fit radius and no active camera transition'};
 });await writeFile(output+'/witness-initialization.json',JSON.stringify(witnessInitialization,null,2));
 for(let n=1;n<=cycles;n++){
  const cycleStart=Date.now(),cycleStages=[];const stamp=()=>{cycleStages.push({phase:stage,elapsed_ms:Date.now()-cycleStart});console.log('PHASE '+stage);};stage='cycle '+n+' load/edit/calculate';stamp();console.log('CYCLE '+n+' create');await execute(1);await marker('LONG_CREATED_'+n);await surface(1).locator('canvas').waitFor();const expected=JSON.parse(await readFile(output+'/cycle-expected.json','utf8'));await bind(page,1,expected.viewer_id);await frame(page,4999);await page.waitForFunction(expected=>{
   const c=window.__longActive,s=c?.getStructureData();if(s?.elementCount!==expected.atoms)return false;const found={};for(const u of s.units)for(const a of u.elements){const k=u.model.atomicHierarchy.atomSourceIndex.value(a);if(Object.hasOwn(expected.positions,k))found[k]=Array.from(u.conformation.position(a,[0,0,0]));}
   return Object.entries(expected.positions).every(([k,v])=>found[k]?.every((x,i)=>x===Math.fround(v[i])));
  },expected);
  stage='cycle '+n+' stale rejection and windows';stamp();await execute(2);await marker('LONG_WINDOWS_READY_'+n);await frame(page,0);await controls(page,surface(1));const opened=page.waitForEvent('popup');await surface(1).getByTitle('Open popup',{exact:true}).click();const canvas=await opened;recordPage(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await bind(canvas);await frame(canvas,0);
  await controls(canvas);const next=canvas.locator('[data-molsysviewer-trajectory-step="next"]');await next.focus();await canvas.keyboard.press('Enter');await frame(canvas,1);await frame(page,1);
  await controls(canvas);const toggle=canvas.getByTitle('Panel mode (N / W)',{exact:true});if(!await canvas.getByTitle('Popout panel to external window',{exact:true}).isVisible())await toggle.click();const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;recordPage(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await studio.close();await canvas.close();
  stage='cycle '+n+' coherent save/recovery';stamp();await execute(3);await marker('LONG_RECOVERED_'+n);const recovered=JSON.parse(await readFile(output+'/cycle-recovered.json','utf8'));assert.equal(recovered.structure,1);await surface(3).locator('canvas').waitFor();await bind(page,3,recovered.viewer_id);await frame(page,1);
  
  await execute(4);await marker('LONG_PLAYING_'+n);await surface(3).scrollIntoViewIfNeeded();await bind(page,3,recovered.viewer_id);await page.waitForFunction(()=>window.__longActive.trajectory.getTrajectoryState().isPlaying);
  await page.evaluate(()=>{const c=window.__longActive,state={started:performance.now(),lastDraw:0,draws:0,frames:new Set()};let listening=false;state.subscription=c.plugin.canvas3d.didDraw.subscribe(()=>{if(!listening)return;state.lastDraw=performance.now();state.draws++;state.frames.add(c.trajectory.getTrajectoryState().currentFrame);});listening=true;window.__longPlayback=state;});stage='cycle '+n+' active playback';stamp();
  await page.waitForFunction(seconds=>{const s=window.__longPlayback;return s.lastDraw-s.started>=seconds*1000&&s.frames.size>=2&&window.__longActive.trajectory.getTrajectoryState().isPlaying;},activeSeconds,{timeout:(activeSeconds+30)*1000});
  const activity=await page.evaluate(()=>{const s=window.__longPlayback;s.subscription.unsubscribe();const row={seconds:(performance.now()-s.started)/1000,draws:s.draws,distinct_frames:s.frames.size};delete window.__longPlayback;return row;});
  stage='cycle '+n+' pause/final check';stamp();await execute(5);await marker('LONG_PAUSED_'+n);await frame(page,73);await execute(6);await marker('LONG_CLOSED_'+n);
  const diagnostic=await page.evaluate(()=>{const w=window.__longWitness,s=w.plugin.canvas3d.camera.getSnapshot();const camera=JSON.stringify({position:s.position,target:s.target,up:s.up,fov:s.fov,mode:s.mode});if(camera!==window.__longWitnessCamera)throw new Error('Independent witness camera changed '+JSON.stringify({before:JSON.parse(window.__longWitnessCamera),after:JSON.parse(camera)}));delete window.__longActive;globalThis.gc?.();window.__longRefs=window.__longRefs.filter(r=>r.deref());return {gc_exposed:typeof globalThis.gc==='function',js_heap_bytes:performance.memory?.usedJSHeapSize??null,observed_controllers:window.__longRefs.length,controller_lifetimes:window.__longRefs.map(r=>{const c=r.deref();return {disposed:c?.disposed??null,connected:c?.canvasHost?.isConnected??false,atoms:c?.getStructureData()?.elementCount??null};}),connected_controllers:window.__longRefs.filter(r=>r.deref()?.canvasHost?.isConnected).length};});
  records.push({cycle:n,stages:cycleStages,seconds:(Date.now()-cycleStart)/1000,activity,...diagnostic});await writeFile(output+'/browser-cycles.json',JSON.stringify(records,null,2));console.log('CYCLE '+n+' passed '+JSON.stringify(records.at(-1)));
 }
 stage='final cleanup';await execute(7);await marker('LONG_ALL_COMPLETE '+cycles);const native=JSON.parse(await readFile(output+'/long-ledger.json','utf8'));assert.equal(native.length,cycles);assert.equal(new Set(native.map(r=>r.kernel_identity)).size,1);assert.equal(new Set(native.map(r=>r.kernel_pid+':'+r.kernel_birth)).size,1);
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(e=>baselineErrors.some(b=>fingerprint(e)===fingerprint(b))));
 const blocks=[];for(let start=0;start<cycles;start+=10)blocks.push({first_cycle:start+1,last_cycle:Math.min(cycles,start+10),seconds:records.slice(start,start+10).reduce((sum,r)=>sum+r.seconds,0)});
 const result={cycles,active_seconds_per_cycle:activeSeconds,seconds:(Date.now()-started)/1000,blocks,records,native,errors,baseline_errors:baselineErrors,scope:'One unchanged scientific Jupyter kernel, real source APIs/widgets/Mol*, both popups, coherent session recovery and independent witness. Active playback is observed by native draws and changing structures, not idle waits. Automated source receiving only.'};await writeFile(output+'/full-result.json',JSON.stringify(result,null,2));console.log(JSON.stringify({cycles,result:'passed',seconds:result.seconds,blocks}));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),stack:error.stack,records,errors,frame_trace:page&&!page.isClosed()?await page.evaluate(()=>window.__longFrameTrace??[]).catch(()=>null):null,native_observation:page&&!page.isClosed()?await page.evaluate(()=>{const c=window.__longActive,s=window.__longPlayback,r=c?.canvasHost?.getBoundingClientRect();return {trajectory:c?.trajectory?.getTrajectoryState(),disposed:c?.disposed,connected:c?.canvasHost?.isConnected,rect:r?{x:r.x,y:r.y,width:r.width,height:r.height}:null,viewport:{width:innerWidth,height:innerHeight},playback:s?{draws:s.draws,distinct_frames:s.frames.size,seconds:(performance.now()-s.started)/1000,last_draw_seconds:(s.lastDraw-s.started)/1000}:null};}).catch(()=>null):null},null,2));if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries()){try{await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());await p.screenshot({path:output+'/window-'+i+'-failure.png',fullPage:true});}catch{}}
 console.error('FAIL '+stage+' '+(error.name??'Error')+'; original diagnostics retained privately');process.exitCode=1;
}finally{if(browser)await browser.close();}
