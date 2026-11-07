/** Actual pending-reader pointer/keyboard receiving in all three live hosts. */
import assert from 'node:assert/strict';
import {openMolecularPanel} from './jupyter_panel_controls.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const settings=process.env.MOLSYSVIEWER_JUPYTER_SETTINGS,output=dirname(resolve(settings));
const config=JSON.parse(await readFile(settings,'utf8'));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(index,p=page){
 await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
 await p.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index).locator('.cm-content').click();
 await p.getByRole('button',{name:/Run this cell and advance/}).click();
}
const workspace=p=>openMolecularPanel(p,'chemistry');
async function inspectPending(p,revision){
 const sheet=p.locator('[data-molsysviewer-system-sync="true"]');
 await sheet.evaluate(el=>{el.__readerInertBaseline=new Map(Array.from(el.parentElement.children).filter(x=>x!==el).map(x=>[x,x.inert]));});
 await execute(2*revision-1);await page.getByText('READER_PENDING '+revision,{exact:true}).waitFor();
 const reader=sheet.locator('[data-molsysviewer-sync-reader] .msm-chemistry');
 await reader.waitFor({state:'visible'});
 assert.match(await sheet.locator('p').first().innerText(),/scene remains paused/);
 assert.equal(await sheet.evaluate(el=>Array.from(el.parentElement.children).filter(x=>x!==el).every(x=>x.inert)),true);
 await reader.locator('[data-source]').selectOption('region');
 assert.equal(await reader.locator('[data-inspect]').isDisabled(),true);
 assert.match(await reader.locator('[data-status]').innerText(),/Update the scene before using its selection or regions/);
 await reader.locator('[data-source]').selectOption('indices');
 const input=reader.locator('[data-indices]');await input.click();await input.fill('');await p.keyboard.type('2,0,2');
 assert.equal(await input.inputValue(),'2,0,2');
 await reader.locator('[data-inspect]').focus();await p.keyboard.press('Enter');
 await reader.locator('[data-report-scope]').filter({hasText:'2 selected atoms'}).waitFor();
 await reader.locator('[data-report-heading]').focus();await p.keyboard.press('w');await p.keyboard.press('n');await p.keyboard.press('Escape');
 assert.equal(await reader.isVisible(),true);
 assert.equal(await reader.locator('[data-report]').isVisible(),true);
 await reader.locator('[data-change-inspection]').click();await reader.locator('[data-source]').selectOption('all');
 await reader.locator('[data-inspect]').click();await reader.locator('[data-report-scope]').filter({hasText:'3,983 selected atoms'}).waitFor();
 await reader.locator('[data-details] summary').click();await reader.locator('[data-next]').click();
 await reader.locator('[data-page-summary]').filter({hasText:'Rows 51–100'}).waitFor();
 await execute(2*revision);await page.getByText('READER_PENDING_UNCHANGED '+revision,{exact:true}).waitFor();
 await p.screenshot({path:output+'/pending-reader-'+revision+'.png',fullPage:true});
}
async function recover(p){
 const sheet=p.locator('[data-molsysviewer-system-sync="true"]');
 const identity=await sheet.locator('[data-molsysviewer-sync-reader] .msm-chemistry').elementHandle();
 await sheet.getByRole('button',{name:'Update view',exact:true}).click();await sheet.waitFor({state:'hidden'});
 assert.equal(await identity.evaluate(el=>el.isConnected&&!!el.closest('[data-molsysviewer-addon-widget-host]')),true);
 assert.equal(await sheet.locator('.msm-chemistry').count(),0);
 assert.equal(await sheet.evaluate(el=>Array.from(el.__readerInertBaseline).every(([node,inert])=>!node.isConnected||node.inert===inert)),true);
 assert.equal(await p.locator('.msm-chemistry').isVisible(),true);
 await identity.dispose();
}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/pending-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
 await baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first().filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();
 await execute(0,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);
 const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);
 await step('Mount actual Chemistry in the embedded TcTIM view',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/pending-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
  await page.locator('.jp-NotebookPanel:visible .jp-Cell').first().filter({hasText:'import molsysviewer as msv'}).waitFor();
  const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(0);
  await page.locator('canvas').waitFor();await workspace(page);
 });
 await step('Inspect and page current primary with real keys while embedded scene stays inert',()=>inspectPending(page,1));
 let canvas,studio;
 await step('Restore the same mounted panel after updating and open the canvas popup',async()=>{
  await recover(page);
  const source=page.locator('[data-molsysviewer-canvas-output]').first();
  await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();canvas=await opened;record(canvas);
  await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
 });
 await step('Inspect current primary from the paused live canvas popup',()=>inspectPending(canvas,2));
 await step('Restore canvas popup and mount Chemistry in detached Studio',async()=>{
  await recover(canvas);const opened=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();studio=await opened;record(studio);
  await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);
 });
 await step('Inspect and page current primary in detached paused Studio',()=>inspectPending(studio,3));
 await step('Restore detached Studio without recreating its panel and close popups',async()=>{await recover(studio);await studio.close();await canvas.close();});
 await step('Verify native molecular data revisions scene regions and result ownership',async()=>{
  await execute(7);await page.getByText('JUPYTER_PENDING_READERS_OK 3983',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');
 assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'New page error beyond the plain Jupyter baseline');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual Jupyter/AnyWidget/Mol*/canvas popup/detached Studio: pending native readers, real pointer/keyboard inputs, bounded pages, stale-scene sources disabled, exact reader DOM restored; three deliberate box edits only. Not human Qt acceptance.'};
 await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){
 await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));
 if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries()){await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());await p.screenshot({path:output+'/window-'+i+'-failure.png',fullPage:true});}
 console.error(error);process.exitCode=1;
}finally{if(browser)await browser.close();}
