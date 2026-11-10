/** Explicit chemical repair/assignments through actual Jupyter and both popups. */
import assert from 'node:assert/strict';
import {openMolecularPanel,observeMolecularControllers} from './jupyter_panel_controls.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const config=JSON.parse(await readFile(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS,'utf8'));
const output=dirname(resolve(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(index,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();const cell=p.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index);await cell.locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
const panel=p=>p.locator('.msm-chemistry').first();
async function prepare(p,task){if(!await panel(p).isVisible())await openMolecularPanel(p,'chemistry');const e=panel(p);await e.locator('[data-task]').selectOption(task);await e.locator('[data-task]:enabled').waitFor();if(await e.locator('[data-editor]').isVisible())await e.locator('[data-source]').selectOption('all');await e.locator('[data-preparation-title]').fill('repair-'+task);return e;}
async function result(e){await e.locator('[data-prepare]').click();await e.locator('[data-result]').waitFor();assert.equal(await e.locator('[data-replacement]').isVisible(),false);}
async function verify(index,task){await execute(index);await page.getByText('NATIVE_REPAIR_OK '+task,{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/repair-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await baseline.locator('.jp-Cell').first().filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(0,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);await observeMolecularControllers(page);
 await step('Prepare explicit covalent inference and geometric bond repair without changing the source',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/repair-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await page.locator('.jp-Cell').first().filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(0);
  await page.waitForFunction(()=>{const err=document.querySelector('.jp-OutputArea-error');if(err)throw new Error(err.textContent);return window.__controllers?.[0]?.getStructureData()?.elementCount>0;});
  let e=await prepare(page,'infer_bonds');assert.match(await e.locator('[data-preparation-limits]').innerText(),/No arbitrary ligand/);await result(e);await verify(1,'infer_bonds');await e.locator('[data-new-result]').click();await e.locator('[data-result]').waitFor({state:'hidden'});
  e=await prepare(page,'add_bonds');await e.locator('[data-bond-cutoff]').fill('2 angstroms');await result(e);await verify(2,'add_bonds');await e.locator('[data-new-result]').click();await e.locator('[data-result]').waitFor({state:'hidden'});
 });
 await step('Prepare explicit caps review Back and present a separate native result',async()=>{
  const e=await prepare(page,'terminal_cappings');await e.locator('[data-n-cap]').selectOption('ACE');await e.locator('[data-c-cap]').selectOption('NME');await result(e);await verify(3,'terminal_cappings');
  await e.locator('[data-preparation-result] summary').click();assert.match(await e.locator('[data-preparation-provenance]').innerText(),/N cap ACE.*C cap NME/);
  await e.locator('[data-replace-review]').click();await e.locator('[data-replacement]').waitFor();await e.locator('[data-replace-back]').click();await e.locator('[data-replacement]').waitFor({state:'hidden'});
  await e.locator('[data-show-notebook]').click();await page.waitForFunction(()=>window.__controllers?.[1]?.getStructureData()?.elementCount>40);await e.locator('[data-new-result]').click();await e.locator('[data-result]').waitFor({state:'hidden'});await page.screenshot({path:output+'/repair-caps-independent.png',fullPage:true});
 });
 await step('Remove only native reference-rule hydrogens in an independent output',async()=>{
  const e=await prepare(page,'remove_hydrogens');assert.equal(await e.locator('[data-editor]').isVisible(),false);assert.match(await e.locator('[data-preparation-limits]').innerText(),/not environment-dependent pKa/);await result(e);await verify(4,'remove_hydrogens');await e.locator('[data-new-result]').click();await e.locator('[data-result]').waitFor({state:'hidden'});
  await execute(5);await page.getByText('METHANOL_REPLACEMENT_READY 6',{exact:true}).waitFor();await page.waitForFunction(()=>window.__controllers[0].getStructureData()?.elementCount===6);
 });
 let canvas,studio;
 await step('Assign explicit AutoDock4 chemical-environment labels from the canvas popup',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  const e=await prepare(canvas,'autodock_types');assert.equal(await e.locator('[data-editor]').isVisible(),false);assert.match(await e.locator('[data-preparation-limits]').innerText(),/H5MSM 0.5/);await result(e);await verify(6,'autodock_types');await e.locator('[data-new-result]').click();await e.locator('[data-result]').waitFor({state:'hidden'});
 });
 await step('Reject a contradictory charge declaration then assign the explicit charge model in detached Studio',async()=>{
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const e=await prepare(studio,'partial_charges');await e.locator('[data-expected-charge]').fill('9');await e.locator('[data-prepare]').click();await e.locator('[data-status]').filter({hasText:/charge|Charge/}).waitFor();assert.equal(await e.locator('[data-result]').isVisible(),false);
  await e.locator('[data-expected-charge]').fill('0');await result(e);await verify(7,'partial_charges');await e.locator('[data-preparation-result] summary').click();assert.match(await e.locator('[data-preparation-provenance]').innerText(),/gasteiger_marsili.*0 elementary charge/);await studio.screenshot({path:output+'/repair-charges-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Verify native outputs independent ownership preserved sources and retained presented result',async()=>{await execute(8);await page.getByText('JUPYTER_REPAIR_NATIVE_OK 6',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);});
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(error=>baselineErrors.some(b=>fingerprint(error)===fingerprint(b))),'A new page error appeared beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual Jupyter/AnyWidget/Mol* source receiving for six native chemistry tasks, independent outputs, reviewed Back, a retained presented cap result, native validation errors and both popups. No human or installed-artifact acceptance.'};await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries()){await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());await p.screenshot({path:output+'/window-'+i+'-failure.png',fullPage:true});}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
