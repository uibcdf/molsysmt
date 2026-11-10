/** Independent construction through actual Jupyter, both popup boundaries and native witnesses. */
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
const scope=p=>p===page?p.locator('[data-molsysviewer-canvas-output]').first():p;
const workspace=p=>openMolecularPanel(p,'chemistry',scope(p));
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/preparation-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);
 const panel=()=>page.locator('.msm-chemistry').first();
 const e=()=>scope(page).locator('.msm-chemistry');
 const field=(editor,key)=>editor.locator(`[data-construction="${key}"]`);
 async function task(editor,name){await editor.locator('[data-task]').selectOption(name);await editor.locator('[data-task]:enabled').waitFor();}
 async function prepare(editor,title){await editor.locator('[data-prepare]').click();await editor.locator('[data-result-heading]').filter({hasText:title}).waitFor();await editor.locator('[data-replace-review]:enabled').waitFor();assert.equal(await editor.locator('[data-replace-review]').isEnabled(),true);}
 async function present(editor){await editor.locator('[data-show-notebook]').click();await editor.locator('[data-status]').filter({hasText:/below|notebook|displayed|shown/i}).waitFor();}
 async function next(editor){await editor.locator('[data-new-result]').click();await editor.locator('[data-result]').waitFor({state:'hidden'});}
 await step('Construct an explicit peptide from an empty view without loading it implicitly',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/construction-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(cell);await page.locator('canvas').waitFor();await workspace(page);
  await task(e(),'peptide');assert.equal(await e().locator('[data-editor]').isVisible(),false);assert.match(await e().locator('[data-context]').innerText(),/No system is required/);await field(e(),'sequence').fill('AlaGly');await prepare(e(),'Constructed peptide');await present(e());await next(e());
 });
 await step('Build a typed water cell and deliberately adopt its independent copy',async()=>{
  await task(e(),'water_cell');await field(e(),'cell_length_unit').selectOption('angstrom');for(const key of ['cell_a','cell_b','cell_c'])await field(e(),key).fill('20');await prepare(e(),'Constructed water cell');assert.match(await e().locator('[data-result-summary]').innerText(),/804 atoms/);await present(e());
  await e().locator('[data-replace-review]').click();await e().locator('[data-replacement]').waitFor();await e().locator('[data-replace-back]').click();await e().locator('[data-replacement]').waitFor({state:'hidden'});await e().locator('[data-replace-review]').click();await e().locator('[data-replacement]').waitFor();await e().locator('[data-replace-apply]').click();await e().locator('[data-replace-unavailable]').filter({hasText:'has been loaded'}).waitFor();await next(e());
 });
 await step('Place seeded whole-water ions through the detached Studio opened from the canvas popup',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);const editor=studio.locator('.msm-chemistry').first();await task(editor,'ions');await field(editor,'n_cations').fill('2');await field(editor,'n_anions').fill('1');await field(editor,'random_seed').fill('19');await prepare(editor,'Ion placement');assert.match(await editor.locator('[data-result-summary]').innerText(),/798 atoms/);await present(editor);await next(editor);await studio.screenshot({path:output+'/construction-ions-studio.png'});await studio.close();await canvas.close();
 });
 await step('Choose a deposited assembly by name and preserve its independent geometry',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('CONSTRUCTION_ASSEMBLY_READY',{exact:true}).waitFor();await workspace(page);await task(e(),'bioassembly');assert.equal(await field(e(),'assembly_name').locator('option').count(),2);await field(e(),'assembly_name').selectOption('declared');await prepare(e(),'Biological assembly');assert.match(await e().locator('[data-result-summary]').innerText(),/1,608 atoms/);await present(e());await next(e());
 });
 await step('Solvate only the explicitly chosen prepared structure and keep the source unchanged',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('CONSTRUCTION_SOLVATION_READY',{exact:true}).waitFor();await workspace(page);await task(e(),'solvate');await field(e(),'clearance').fill('0.35 nm');await field(e(),'construction_forcefield').fill('AMBER14');await field(e(),'random_seed').fill('19');await prepare(e(),'Solvated system');await present(e());await page.screenshot({path:output+'/construction-solvation.png',fullPage:true});
 });
 await step('Verify all five independent molecular results and seeded ion coordinates in Python',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(3));await page.getByText('JUPYTER_CONSTRUCTION_NATIVE_OK',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual empty/loaded Jupyter construction with explicit peptide/water/ions/assembly/solvation, independent notebook results and both popup boundaries. Source overlay; not human Qt or installed artifact qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
