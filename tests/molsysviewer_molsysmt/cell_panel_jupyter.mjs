/** Assigning physical cells through actual Jupyter and shared native authority. */
import assert from 'node:assert/strict';
import {openMolecularPanel,observeMolecularControllers} from './jupyter_panel_controls.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const settings=process.env.MOLSYSVIEWER_JUPYTER_SETTINGS,output=dirname(resolve(settings));
const config=JSON.parse(await readFile(settings,'utf8'));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(cell,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();await cell.locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
const panel=p=>p.locator('.msm-system').first();
async function fillCell(p,lengths,angles,lengthUnit='nm',angleUnit='degree'){
 const c=panel(p);await c.locator('[data-cell-length-unit]').selectOption(lengthUnit);await c.locator('[data-cell-angle-unit]').selectOption(angleUnit);
 for(const [i,key] of ['a','b','c'].entries())await c.locator(`[data-cell-${key}]`).fill(String(lengths[i]));
 for(const [i,key] of ['alpha','beta','gamma'].entries())await c.locator(`[data-cell-${key}]`).fill(String(angles[i]));
}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',e=>baselineErrors.push({error:String(e),stack:e.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/cell-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',e=>errors.push({stage,error:String(e),stack:e.stack}));record(page);await observeMolecularControllers(page);
 let expected;
 async function positionMatch(index){await page.waitForFunction(({index,expected})=>{const c=window.__controllers?.[index],structure=c?.getStructureData();if(!structure)return false;const positions=[];for(const unit of structure.units)for(const atom of unit.elements)positions[atom]=Array.from(unit.conformation.position(atom,[0,0,0]));return positions.length===62&&positions.every((xyz,i)=>xyz.every((v,j)=>Math.abs(v-expected[i][j])<1e-4));},{index,expected});}
 await step('Render the real source without a box and expose structure-level cell controls',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/cell-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const first=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await first.filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(first);
  await page.waitForFunction(()=>window.__controllers?.[0]?.getStructureData()?.elementCount===62,null,{timeout:120000});
  await openMolecularPanel(page,'geometry');await panel(page).locator('[data-task]').selectOption('cell');await panel(page).getByRole('heading',{name:'Assign periodic cell',exact:true}).waitFor();
  await page.waitForFunction(()=>document.querySelector('.msm-system [data-preview]')?.disabled===false);
  assert.equal(await panel(page).locator('[data-editor]').isVisible(),false);assert.equal(await panel(page).locator('[data-preview]').isEnabled(),true);
  expected=JSON.parse(await readFile(output+'/cell-expected.json','utf8')).coordinates_angstrom[0];await positionMatch(0);
 });
 await step('Reject partial initialization and nonphysical lengths before a review or write',async()=>{
  await panel(page).locator('[data-scope]').selectOption('indices');await panel(page).locator('[data-frames]').fill('2,0');await panel(page).locator('[data-preview]').click();
  await panel(page).locator('[data-status]').filter({hasText:'All structures'}).waitFor();assert.equal(await panel(page).locator('[data-review]').isVisible(),false);
  await panel(page).locator('[data-scope]').selectOption('all');await fillCell(page,[0,40,50],[90,90,90],'angstrom');await panel(page).locator('[data-preview]').click();
  await panel(page).locator('[data-status]').filter({hasText:/positive/}).waitFor();assert.equal(await panel(page).locator('[data-review]').isVisible(),false);await positionMatch(0);
 });
 await step('Review physical lengths and angles then Back without initializing boxes',async()=>{
  await fillCell(page,[30,40,50],[90,90,90],'angstrom');await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-review]').waitFor({state:'visible'});
  assert.match(await panel(page).locator('[data-review-summary]').innerText(),/30, 40, 50.*Å.*3 complete structures/);
  await panel(page).locator('[data-back]').click();await panel(page).locator('[data-review]').waitFor({state:'hidden'});
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_CELL_PREVIEW_OK 0',{exact:true}).waitFor();await positionMatch(0);
 });
 await step('Initialize all periodic cells through real comms without moving atoms',async()=>{
  await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-confirm]').click();await panel(page).locator('[data-status]').filter({hasText:'Periodic cell assigned. The view is up to date.'}).waitFor();
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('JUPYTER_CELL_ASSIGNED_OK 1',{exact:true}).waitFor();await positionMatch(0);
 });
 await step('Create an independent triclinic result and preserve its actual Cartesian positions',async()=>{
  await panel(page).locator('[data-effect]').selectOption('result');await panel(page).locator('[data-title]').fill('Cell proposal');await fillCell(page,[2,3,4],[90,90,60]);
  await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-confirm]').click();await panel(page).locator('[data-result-heading]').filter({hasText:'Cell proposal'}).waitFor();
  await panel(page).locator('[data-show-notebook]').click();await panel(page).locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();
  await page.waitForFunction(()=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===62);await positionMatch(0);await positionMatch(1);
 });
 await step('Move the cell result between notebook and window after exact acknowledgement',async()=>{
  const opened=page.waitForEvent('popup');await panel(page).locator('[data-show-window]').click();const child=await opened;record(child);await child.locator('canvas').waitFor();await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await panel(page).locator('[data-status]').filter({hasText:'Result opened in its own window.'}).waitFor();assert.equal(await child.title(),'Cell proposal');
  const closed=child.waitForEvent('close');await panel(page).locator('[data-show-notebook]').click();await closed;await panel(page).locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();await positionMatch(1);
  await panel(page).locator('[data-new-result]').click();await panel(page).locator('[data-cell]').waitFor({state:'visible'});
 });
 await step('Assign a selected structure through canvas and detached Studio authority',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await openMolecularPanel(canvas,'geometry');
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await openMolecularPanel(studio,'geometry');
  await panel(studio).locator('[data-task]').selectOption('cell');await panel(studio).locator('[data-effect]').selectOption('update');await panel(studio).locator('[data-scope]').selectOption('indices');await panel(studio).locator('[data-frames]').fill('1');await fillCell(studio,[6,7,8],[Math.PI/2,Math.PI/2,Math.PI/2],'nm','radian');
  await panel(studio).locator('[data-preview]').click();await panel(studio).locator('[data-confirm]').click();await panel(studio).locator('[data-status]').filter({hasText:'Periodic cell assigned. The view is up to date.'}).waitFor();
  await studio.screenshot({path:output+'/cell-studio-popup.png'});await studio.close();await canvas.close();await positionMatch(0);await positionMatch(1);
 });
 await step('Python verifies boxes coordinates chemical state independent ownership and exactly two edits',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(3));await page.getByText('JUPYTER_CELL_NATIVE_OK 2',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);await positionMatch(0);await positionMatch(1);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(e=>baselineErrors.some(b=>fingerprint(b)===fingerprint(e))),'A page error was introduced beyond the plain Jupyter control');
 await writeFile(output+'/full-result.json',JSON.stringify({checks,errors,baseline_errors:baselineErrors,scope:'Actual local Jupyter/ipykernel/AnyWidget comms, native physical-cell factory and managed setting, independent Mol* result, popup authority and unchanged Cartesian coordinates. Source only; not human Qt or installed qualification.'},null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());if(page)await page.screenshot({path:output+'/failure.png',fullPage:true});console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
