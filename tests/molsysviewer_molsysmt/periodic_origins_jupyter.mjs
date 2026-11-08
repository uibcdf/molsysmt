/** Receiving small physical origins across application unit policies. */
import assert from 'node:assert/strict';
import {openMolecularPanel,observeMolecularControllers} from './jupyter_panel_controls.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const output=dirname(resolve(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS));
const config=JSON.parse(await readFile(output+'/settings.json','utf8'));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(cell,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();await cell.locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
const panel=p=>p.locator('.msm-system').first();
async function request(p,origin,unit='angstrom',effect='update'){
 const c=panel(p);await c.locator('[data-task]').selectOption('wrap');await c.getByRole('heading',{name:'Wrap coordinates',exact:true}).waitFor();
 await c.locator('[data-source]').selectOption('saved');await c.locator('[data-name]').fill('chosen');await c.locator('[data-wrap-mode]').selectOption('primary');await c.locator('[data-wrap-compact]').selectOption('atom');
 await c.locator('[data-unit]').selectOption(unit);await c.locator('[data-dx]').fill(origin);await c.locator('[data-dy]').fill('0');await c.locator('[data-dz]').fill('0');
 await c.locator('[data-scope]').selectOption('indices');await c.locator('[data-frames]').fill('2,0');await c.locator('[data-effect]').selectOption(effect);
}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',e=>baselineErrors.push({error:String(e),stack:e.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/origin-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',e=>errors.push({stage,error:String(e),stack:e.stack}));record(page);await observeMolecularControllers(page);
 let oracle;
 async function positionMatch(index,expected){await page.waitForFunction(({index,expected})=>{const structure=window.__controllers?.[index]?.getStructureData();if(!structure)return false;const positions=[];for(const unit of structure.units)for(const atom of unit.elements)positions[atom]=Array.from(unit.conformation.position(atom,[0,0,0]));return positions.length===62&&positions.every((xyz,i)=>xyz.every((v,j)=>Math.abs(v-expected[i][j])<1e-4));},{index,expected});}
 await step('Render a boundary-sensitive source under the declared application unit policy',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/origin-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const first=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await first.filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(first);
  await page.waitForFunction(()=>window.__controllers?.[0]?.getStructureData()?.elementCount===62,null,{timeout:120000});await openMolecularPanel(page,'geometry');
  oracle=JSON.parse(await readFile(output+'/origins-expected.json','utf8'));await positionMatch(0,oracle.before_angstrom[0]);
  for(const key of ['positive_angstrom','negative_angstrom'])assert.ok(Math.max(...oracle[key][0].flatMap((xyz,i)=>xyz.map((v,j)=>Math.abs(v-oracle.zero_origin_angstrom[0][i][j]))))>29,'The fixture must reject replacing the physical origin with zero');
 });
 await step('Review a small positive origin and Back without changing rendered coordinates',async()=>{
  await request(page,'0.0001');await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-review]').waitFor({state:'visible'});assert.match(await panel(page).locator('[data-review-summary]').innerText(),/2 atoms in 2 structures/);
  await panel(page).locator('[data-back]').click();await panel(page).locator('[data-review]').waitFor({state:'hidden'});await positionMatch(0,oracle.before_angstrom[0]);
 });
 await step('Apply the small positive angstrom input and verify the nonzero-origin image',async()=>{
  await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-confirm]').click();await panel(page).locator('[data-status]').filter({hasText:'Periodic wrapping applied. The view is up to date.'}).waitFor();await positionMatch(0,oracle.positive_angstrom[0]);
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_ORIGINS_POSITIVE_OK 1',{exact:true}).waitFor();
 });
 await step('Compute the negative-origin independent result without altering the source',async()=>{
  await request(page,'-0.0001','angstrom','result');await panel(page).locator('[data-title]').fill('Small-origin result');await panel(page).locator('[data-preview]').click();await panel(page).locator('[data-confirm]').click();await panel(page).locator('[data-result]').waitFor({state:'visible'});
  await panel(page).locator('[data-show-notebook]').click();await panel(page).locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();await page.waitForFunction(()=>window.__controllers?.length===2&&window.__controllers[1].getStructureData()?.elementCount===62);await positionMatch(0,oracle.positive_angstrom[0]);await positionMatch(1,oracle.negative_angstrom[0]);
 });
 await step('Preserve the same negative-origin result across acknowledged window ownership',async()=>{
  const opened=page.waitForEvent('popup');await panel(page).locator('[data-show-window]').click();const child=await opened;record(child);await child.locator('#molsysviewer-loading').waitFor({state:'hidden'});await panel(page).locator('[data-status]').filter({hasText:'Result opened in its own window.'}).waitFor();assert.equal(await child.title(),'Small-origin result');
  const closed=child.waitForEvent('close');await panel(page).locator('[data-show-notebook]').click();await closed;await panel(page).locator('[data-status]').filter({hasText:'Result shown below'}).waitFor();await positionMatch(1,oracle.negative_angstrom[0]);await panel(page).locator('[data-new-result]').click();
 });
 await step('Apply the same physical negative origin in nm through detached Studio',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await openMolecularPanel(canvas,'geometry');
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await openMolecularPanel(studio,'geometry');
  await request(studio,'-0.00001','nm');await panel(studio).locator('[data-preview]').click();await panel(studio).locator('[data-confirm]').click();await panel(studio).locator('[data-status]').filter({hasText:'Periodic wrapping applied. The view is up to date.'}).waitFor();await studio.screenshot({path:output+'/small-origin-studio.png'});await studio.close();await canvas.close();await positionMatch(0,oracle.negative_angstrom[0]);await positionMatch(1,oracle.negative_angstrom[0]);
 });
 await step('Verify every native structure source effect box chemistry coverage and unchanged unit policy',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('JUPYTER_ORIGINS_NATIVE_OK 2',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(e=>baselineErrors.some(b=>fingerprint(b)===fingerprint(e))),'A page error was introduced beyond the plain Jupyter control');
 await writeFile(output+'/full-result.json',JSON.stringify({checks,errors,baseline_errors:baselineErrors,standard:oracle.standard,scope:'Small positive and negative physical origins distinguished from zero, actual Mol* images, native analytical controls, nonconsecutive structures, current/independent effects and both popup authorities. Source only; not human Qt or installed qualification.'},null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());if(page)await page.screenshot({path:output+'/failure.png',fullPage:true});console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
