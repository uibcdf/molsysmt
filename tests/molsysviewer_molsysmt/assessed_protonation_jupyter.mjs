/** Receive one assessed native decision through real Jupyter controls. */
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {openMolecularPanel,observeMolecularControllers} from './jupyter_panel_controls.mjs';
const settings=process.env.MOLSYSVIEWER_JUPYTER_SETTINGS,output=dirname(resolve(settings));
const config=JSON.parse(await readFile(settings,'utf8'));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
const checks=[],errors=[],baselineErrors=[];let browser,page,stage='start';
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(index,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();await p.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index).locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}
const panel=()=>page.locator('.msm-chemistry').first();
async function inspect(){await panel().locator('[data-inspect]').click();await panel().locator('[data-report]').waitFor();await panel().locator('[data-inspect]:enabled').waitFor();}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',e=>baselineErrors.push({error:String(e),stack:e.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/assessed-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 await baseline.locator('.jp-Cell').first().filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(0,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);page.on('pageerror',e=>errors.push({stage,error:String(e),stack:e.stack}));await observeMolecularControllers(page);
 await step('Inspect deposited villin hydrogens and exact whole-system assessment without modification',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/assessed-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  await page.locator('.jp-Cell').first().filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(0);
  await page.waitForFunction(()=>{const err=document.querySelector('.jp-OutputArea-error, .jp-RenderedText[data-mime-type="application/vnd.jupyter.stderr"]');if(err)throw new Error(err.textContent);return window.__controllers?.[0]?.getStructureData()?.elementCount===596;});
  await openMolecularPanel(page,'chemistry');await panel().locator('[data-task]').selectOption('protonation');await panel().locator('[data-assessment-ph]').fill('12');await inspect();
  assert.match(await panel().locator('[data-assessment-summary]').innerText(),/6 proposed H removals, not applied/);
  assert.equal(await panel().locator('[data-protonation-confirm]').isVisible(),false);await execute(1);await page.getByText('ASSESSED_SOURCE_SCENE_READY',{exact:true}).waitFor();
 });
 await step('Review and cancel the assessed managed edit before preparing its independent result',async()=>{
  await panel().locator('[data-protonation-review]').click();await panel().locator('[data-protonation-confirm]').waitFor();
  assert.match(await panel().locator('[data-protonation-confirm]').innerText(),/all structures/);
  await panel().locator('[data-protonation-back]').click();await panel().locator('[data-protonation-confirm]').waitFor({state:'hidden'});
  await panel().locator('[data-protonation-prepare]').click();await panel().locator('[data-preparation-result]').waitFor();
  assert.equal(await panel().locator('[data-report]').isVisible(),false);
  await execute(2);await page.getByText('ASSESSED_INDEPENDENT_OK 590',{exact:true}).waitFor();
 });
 await step('Present the independently owned native reconciliation without adopting it',async()=>{
  await panel().locator('[data-show-notebook]').click();await page.waitForFunction(()=>window.__controllers?.some(c=>c.getStructureData()?.elementCount===590));
  assert.equal(await page.evaluate(()=>window.__controllers[0].getStructureData().elementCount),596);
 });
 await step('Apply a newly inspected decision once through the managed atom map and scene coordinator',async()=>{
  await inspect();await panel().locator('[data-protonation-review]').click();await panel().locator('[data-protonation-confirm]').waitFor();
  await panel().locator('[data-protonation-apply]').click();await panel().locator('[data-status]').filter({hasText:/completed.*synchronized/}).waitFor();
  await page.waitForFunction(()=>window.__controllers[0].getStructureData()?.elementCount===590);
  assert.equal(await panel().locator('[data-report]').isVisible(),false);
  await execute(3);await page.getByText('ASSESSED_MANAGED_OK 590',{exact:true}).waitFor();
 });
 await step('Consume an assessed no-op without another molecular revision or fabricated chemistry',async()=>{
  await inspect();assert.match(await panel().locator('[data-assessment-summary]').innerText(),/0 proposed H removals/);
  await panel().locator('[data-protonation-review]').click();await panel().locator('[data-protonation-confirm]').waitFor();await panel().locator('[data-protonation-apply]').click();
  await panel().locator('[data-status]').filter({hasText:/completed.*synchronized/}).waitFor();assert.equal(await panel().locator('[data-report]').isVisible(),false);
 });
 await step('Verify exact coordinates all structure axes named observations and independent lifetime in Python',async()=>{
  await execute(4);await page.getByText('JUPYTER_ASSESSED_PROTONATION_OK 590',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(e=>baselineErrors.some(b=>fingerprint(e)===fingerprint(b))),'New browser error beyond plain Jupyter');
 const result={checks,errors,baseline_errors:baselineErrors,scope:'Actual Linux/Jupyter/Mol*/AnyWidget assessed native decision, Back, separate result, managed map and no-op, all structures and named analysis projection under pm policy. Not environmental pKa, human, installed or release qualification.'};
 await writeFile(output+'/full-result.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(page)await page.screenshot({path:output+'/failure.png',fullPage:true});console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
