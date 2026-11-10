/** Explicit local refinement through actual Jupyter, Mol* and both popups. */
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
async function execute(cell,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();await cell.locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
const panel=p=>p.locator('.msm-system').first();
const positions=async p=>p.evaluate(()=>{const s=window.__controllers?.[0]?.getStructureData();if(!s)return null;const result=[];for(const u of s.units)for(const a of u.elements)result[a]=Array.from(u.conformation.position(a,[0,0,0]));return result;});
async function configure(p,effect){await openMolecularPanel(p,'geometry');const editor=panel(p);await editor.locator('[data-task]').selectOption('minimize');await editor.locator('[data-task]:enabled').waitFor();await editor.locator('[data-effect]').selectOption(effect);return editor;}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/refinement-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);await observeMolecularControllers(page);
 let initial,expected;
 await step('Review the explicit complete model and cancel without changing coordinates',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/refinement-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(cell);
  await page.waitForFunction(()=>{const error=document.querySelector('.jp-OutputArea-error');if(error)throw new Error(error.textContent);return window.__controllers?.[0]?.getStructureData()?.elementCount===62;},null,{timeout:120000});initial=await positions(page);expected=JSON.parse(await readFile(output+'/refinement-expected.json','utf8')).coordinates_angstrom;
  const p=await configure(page,'result');assert.equal(await p.locator('[data-editor]').isVisible(),false);assert.equal(await p.locator('[data-scope]').isVisible(),false);
  await p.locator('[data-preview]').click();await p.locator('[data-review]').waitFor();assert.match(await p.locator('[data-review-summary]').innerText(),/OpenMM L-BFGS on CPU/);
  assert.match(await p.locator('[data-mechanical-model]').innerText(),/AMBER14/);assert.match(await p.locator('[data-mechanical-model]').innerText(),/Stored in system/);assert.match(await p.locator('[data-mechanical-model]').innerText(),/MolSysMT default/);
  await p.locator('[data-back]').click();await p.locator('[data-preview]').waitFor();assert.deepEqual(await positions(page),initial);
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('REFINEMENT_SOURCE_UNCHANGED',{exact:true}).waitFor();
 });
 await step('Create one independent minimized result and present its actual molecular geometry',async()=>{
  const p=panel(page);await p.locator('[data-preview]').click();await p.locator('[data-confirm]').filter({hasText:'Create minimized result'}).click();await p.locator('[data-result]').waitFor();await p.locator('[data-minimization-result] summary').click();assert.match(await p.locator('[data-minimization-result-method]').innerText(),/OpenMM.*L-BFGS.*CPU/);assert.match(await p.locator('[data-minimization-result-model]').innerText(),/AMBER14/);assert.deepEqual(await positions(page),initial);
  await p.locator('[data-show-notebook]').click();await page.waitForFunction(()=>window.__controllers?.[1]?.getStructureData()?.elementCount===62);
  await page.waitForFunction(expected=>{const s=window.__controllers[1].getStructureData();return s.units.every(u=>Array.from(u.elements).every(a=>Array.from(u.conformation.position(a,[0,0,0])).every((v,j)=>Math.abs(v-expected[a][j])<.001)));},expected);
  await page.screenshot({path:output+'/refinement-independent.png',fullPage:true});
 });
 await step('Review from the canvas popup and apply local refinement from detached Studio',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  let p=await configure(canvas,'update');await p.locator('[data-preview]').click();await p.locator('[data-review]').waitFor();await p.locator('[data-back]').click();
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});p=await configure(studio,'update');await p.locator('[data-preview]').click();await p.locator('[data-review]').waitFor();await p.locator('[data-confirm]').filter({hasText:'Apply local minimization'}).click();await p.locator('[data-status]').filter({hasText:'Local minimization applied. The view is up to date.'}).waitFor();
  await page.waitForFunction(expected=>{const s=window.__controllers[0].getStructureData();return s.units.every(u=>Array.from(u.elements).every(a=>Array.from(u.conformation.position(a,[0,0,0])).every((v,j)=>Math.abs(v-expected[a][j])<.001)));},expected);
  await studio.screenshot({path:output+'/refinement-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Verify independent data ownership native chemistry energies and the single source edit',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('JUPYTER_REFINEMENT_NATIVE_OK',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(error=>baselineErrors.some(b=>fingerprint(error)===fingerprint(b))),'A new page error appeared beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual Jupyter/IPython/AnyWidget/Mol* source receiving: explicit model review/Back, independent result, both popup boundaries, managed current effect, independent OpenMM coordinates/energy and native chemistry. Not human or installed-package acceptance.'};await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
