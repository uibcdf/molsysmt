/** Native properties and source-indexed reports through actual Jupyter and both popups. */
import assert from 'node:assert/strict';
import {openMolecularPanel,observeMolecularControllers,molecularReceivingSnapshot} from './jupyter_panel_controls.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const config=JSON.parse(await readFile(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS,'utf8'));
const output=dirname(resolve(process.env.MOLSYSVIEWER_JUPYTER_SETTINGS));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
async function step(name,action){stage=name;console.log('STEP '+name);await action();checks.push(name);}
async function execute(index,p=page){await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();const cell=p.locator('.jp-NotebookPanel:visible .jp-Cell').nth(index);await cell.locator('.cm-content').click();await p.getByRole('button',{name:/Run this cell and advance/}).click();}

let expected;
const panel=p=>p.locator('.msm-analysis').first();
const close=(a,b)=>assert.ok(Math.abs(a-b)<=Math.max(1e-9,5e-9*Math.abs(b)),`${a} versus ${b}`);
async function rows(e){return e.locator('[data-rows] tr').evaluateAll(nodes=>nodes.map(tr=>Array.from(tr.querySelectorAll('td'),td=>{const text=td.textContent;return text!==''&&Number.isFinite(Number(text))?Number(text):text;})));}
async function prepare(p,task){if(!await panel(p).isVisible())await openMolecularPanel(p,'analysis');const e=panel(p);if(await e.locator('[data-family="property"]').getAttribute('aria-pressed')!=='true')await e.locator('[data-family="property"]').click();await e.locator('[data-task]:enabled').waitFor();await e.locator('[data-task]').selectOption(task);await e.locator('[data-task]:enabled').waitFor();await e.locator('[data-first] [data-source]').selectOption('indices');await e.locator('[data-first] [data-indices]').fill('20,10,6,20');return e;}
async function calculate(e,success=true){await e.locator('[data-calculate]').click();await e.locator('[data-calculate]:enabled').waitFor();if(success)await e.locator('[data-report]').waitFor();else await e.locator('[data-status]').filter({hasText:/\S/}).waitFor();}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/property-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await baseline.locator('.jp-Cell').first().filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(0,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);await observeMolecularControllers(page);

 await step('Open native properties without an implicit calculation and inspect source atom masses',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/property-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await page.locator('.jp-Cell').first().filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(0);
  await page.waitForFunction(()=>{const err=document.querySelector('.jp-OutputArea-error');if(err)throw new Error(err.textContent);return window.__controllers?.[0]?.getStructureData()?.elementCount===62;});
  expected=JSON.parse(await readFile(output+'/property-expected.json','utf8'));
  const e=await prepare(page,'mass');assert.equal(await e.locator('[data-family="property"]').getAttribute('aria-pressed'),'true');assert.equal(await e.locator('[data-report]').isVisible(),false);assert.equal(await e.locator('[data-relation-label]').isVisible(),false);assert.equal(await e.locator('[data-structures]').isVisible(),false);
  await calculate(e);const r=await rows(e);assert.deepEqual(r.map(r=>r[0]),expected.atoms);r.forEach((row,i)=>close(row[2],expected.mass[i]));assert.equal(await e.locator('[data-add-live-distance]').isVisible(),false);
 });
 await step('Inspect complete group tables and deliberate participant actions without preparing chemistry',async()=>{
  for(const task of ['reference_charge','hydrophobicity','polarity']){const e=await prepare(page,task);await calculate(e);assert.deepEqual((await rows(e)).map(r=>r[0]),expected.groups);if(task==='reference_charge')assert.match(await e.locator('[data-periodicity]').innerText(),/not stored formal/);}
  const e=panel(page);await e.locator('[data-result-row="0"]').check();await e.locator('[data-select-participants]').click();await e.locator('[data-status]').filter({hasText:'Selected'}).waitFor();
  await page.waitForFunction(atoms=>JSON.stringify(window.__controllers[0].currentActiveSelection.atom_indices.slice().sort((a,b)=>a-b))===JSON.stringify(atoms.slice().sort((a,b)=>a-b)),expected.group_members);
  await e.locator('[data-focus-participants]').click();await e.locator('[data-status]').filter({hasText:'Focused participant atoms'}).waitFor();assert.equal(await page.evaluate(()=>window.__controllers[0].trajectory.getTrajectoryState().currentFrame),0);
  await e.locator('[data-first] [data-indices]').fill('0,6');await calculate(e,false);assert.match(await e.locator('[data-status]').innerText(),/ACE/);assert.equal(await e.locator('[data-report]').isVisible(),false);
 });
 await step('Inspect sequence projection and source graph reports with exact source indices',async()=>{
  let e=await prepare(page,'sequence');await e.locator('[data-first] [data-indices]').fill('0,20,6');await calculate(e);const r=await rows(e);assert.deepEqual(r.map(r=>r[2]),['omitted by native projection','A','A']);
  for(const task of ['bonds','blocks','rings']){e=await prepare(page,task);await e.locator('[data-first] [data-source]').selectOption('all');await calculate(e,task!=='rings');if(task==='blocks')assert.equal((await rows(e))[0][1],62);if(task==='rings')assert.match(await e.locator('[data-status]').innerText(),/Bond chemistry columns are missing/);}
 });
 await step('Page fifty source rows and inspect nonconsecutive repeated SASA structures with explicit units',async()=>{
  let e=await prepare(page,'mass');await e.locator('[data-first] [data-source]').selectOption('all');await calculate(e);assert.equal(await e.locator('[data-rows] tr').count(),50);await e.locator('[data-next]').click();await e.locator('[data-page-summary]').filter({hasText:'Rows 51–62'}).waitFor();assert.equal((await rows(e))[0][0],50);
  e=await prepare(page,'sasa');await e.locator('[data-structures]').selectOption('indices');await e.locator('[data-structure-indices]').fill('2,0,2');await e.locator('[data-probe-radius]').fill('140');await e.locator('[data-probe-unit]').selectOption('pm');await calculate(e);const r=await rows(e);assert.deepEqual(r.map(r=>r[0]),[2,2,2,2,0,0,0,0,2,2,2,2]);assert.deepEqual(r.map(r=>r[1]),[...expected.atoms,...expected.atoms,...expected.atoms]);r.forEach((row,i)=>close(row[2],expected.sasa.flat()[i]));assert.match(await e.locator('[data-columns]').innerText(),/nm²/);assert.match(await e.locator('[data-periodicity]').innerText(),/including solvent/);
 });
 let canvas,studio;
 await step('Inspect observed DSSP codes with exact group and repeated structure correspondence',async()=>{
  const e=await prepare(page,'secondary_structure');await e.locator('[data-first] [data-indices]').fill('0,20,10,6,20');await e.locator('[data-secondary-mode]').selectOption('full');await e.locator('[data-structures]').selectOption('indices');await e.locator('[data-structure-indices]').fill('2,0,2');await calculate(e);
  const expectedRows=[2,0,2].flatMap((f,i)=>expected.ss_groups.map((g,j)=>[f,g,"'"+expected.dssp_full[i][j]+"'"]));assert.deepEqual(await rows(e),expectedRows);assert.ok(expected.dssp_full.flat().includes('NA'));const provenance=e.locator('details').filter({hasText:'Method, source and result lifetime'});if(!await provenance.evaluate(node=>node.open))await provenance.locator('summary').click();assert.match(await e.locator('[data-provenance]').innerText(),/MDTraj/);assert.match(await e.locator('[data-periodicity]').innerText(),/not sequence prediction/);
  await e.locator('[data-result-row="0"]').check();await e.locator('[data-select-participants]').click();await e.locator('[data-status]').filter({hasText:'Selected'}).waitFor();assert.equal(await page.evaluate(()=>window.__controllers[0].trajectory.getTrajectoryState().currentFrame),0);
 });
 await step('Receive independent property reports in canvas and detached Studio popups',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  let e=await prepare(canvas,'mass');await calculate(e);(await rows(e)).forEach((row,i)=>close(row[2],expected.mass[i]));
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});e=await prepare(studio,'sequence');await calculate(e);assert.deepEqual((await rows(e)).map(r=>r[2]),['A','A']);await studio.screenshot({path:output+'/property-studio-popup.png'});await studio.close();await canvas.close();
 });
 await step('Receive known caffeine ring sets and reject a partial ring without editing the source',async()=>{
  await execute(1);await page.getByText('PROPERTY_CAFFEINE_READY 24',{exact:true}).waitFor();await page.waitForFunction(()=>window.__controllers[0].getStructureData()?.elementCount===24);
  const e=await prepare(page,'rings');await e.locator('[data-first] [data-source]').selectOption('all');await calculate(e);assert.deepEqual((await rows(e)).map(r=>r[2]).sort(),['1, 2, 3, 4, 5','4, 5, 6, 8, 9, 11'].sort());await e.locator('[data-first] [data-source]').selectOption('indices');await e.locator('[data-first] [data-indices]').fill('1,2,3');await calculate(e,false);assert.equal(await e.locator('[data-report]').isVisible(),false);assert.match(await e.locator('[data-status]').innerText(),/ring/i);
  await execute(2);await page.getByText('JUPYTER_PROPERTIES_NATIVE_OK',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);await page.screenshot({path:output+'/property-native-final.png',fullPage:true});
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(error=>baselineErrors.some(b=>fingerprint(error)===fingerprint(b))),'A new page error appeared beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,receiving_state:await molecularReceivingSnapshot(page),scope:'Actual Jupyter/AnyWidget/Mol* native properties, source maps, paging, participant actions, ten native tasks including categorical DSSP and both popups. No human or installed qualification.'};await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors,receiving_state:page?await molecularReceivingSnapshot(page).catch(()=>({unavailable:true})):null},null,2));if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries()){await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());await p.screenshot({path:output+'/window-'+i+'-failure.png',fullPage:true});}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
