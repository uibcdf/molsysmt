/** Native properties and source-indexed reports through actual Jupyter and both popups. */
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


let expected;
const panel=p=>p.locator('.msm-analysis').first();
async function prepare(p,task='mass',population='all'){
 if(!await panel(p).isVisible())await openMolecularPanel(p,'analysis');const e=panel(p),family=['mass','sasa'].includes(task)?'property':'structure';
 if(await e.locator(`[data-family="${family}"]`).getAttribute('aria-pressed')!=='true')await e.locator(`[data-family="${family}"]`).click();await e.locator('[data-task]:enabled').waitFor();await e.locator('[data-task]').selectOption(task);await e.locator('[data-task]:enabled').waitFor();await e.locator('[data-first] [data-source]').selectOption(population);if(population==='indices')await e.locator('[data-first] [data-indices]').fill('20,10,6,20');return e;
}
async function calculate(e){await e.locator('[data-calculate]').click();await e.locator('[data-calculate]:enabled').waitFor();await e.locator('[data-report]').waitFor();}
async function colors(p,wanted){await p.waitForFunction(wanted=>{
 const c=window.__controllers?.[0];if(!c)return false;const s=c.getStructureData();if(!s||s.elementCount!==wanted.length)return false;
 const refs=Array.from(c.state.globalReprs||[]);const r=refs.map(ref=>c.plugin.state.data.cells.get(ref)?.obj?.data?.repr).find(r=>r?.theme?.color?.color);
 if(!r)return false;return wanted.every((value,i)=>{const unit=s.units.find(u=>Array.from(u.elements).includes(i));return unit&&Number(r.theme.color.color({kind:'element-location',structure:s,unit,element:i},false))===value;});
 },wanted);}
async function verifyContext(card){
 const details=card.locator('[data-molsysviewer-plot-context]'),summary=details.locator('summary');
 await summary.focus();await summary.press('Enter');
 const raw=details.locator('[data-molsysviewer-series-observation="0"]');await raw.waitFor();
 const record=JSON.parse(await raw.innerText()),context=record.context;
 assert.equal(context.schema,'molsysmt.figure_observation@1');assert.equal(context.method,'molsysmt.physchem.get_sasa');
 assert.equal(context.units.displayed,'nm**2');assert.deepEqual(record.original_observation_rows,[0,1,2]);
 const expanded=context.arguments.selection.runs.flatMap(([start,step,count])=>Array.from({length:count},(_,i)=>start+i*step));
 assert.deepEqual(expanded,[20,10,6,20]);assert.equal(context.projection.index,20);
 assert.equal(context.source.correspondence,'declared_not_authenticated');assert.equal(context.source.raw_edits_observed,false);
 assert.ok(context.software.molsysmt);await summary.press('Enter');return context;
}
async function verifyPlot(p,expected){const card=p.locator('[data-molsysviewer-datacard^="molsysmt-report-"]').last();await card.waitFor();const svg=card.locator('svg:has(polyline)'),points=await svg.locator('polyline').evaluate(n=>n.getAttribute('points').split(/\s+/).map(s=>s.split(',').map(Number)));assert.equal(points.length,3);const low=expected.indexOf(Math.min(...expected)),high=expected.indexOf(Math.max(...expected));assert.notEqual(low,high);for(let i=0;i<3;i++)assert.ok(Math.abs((points[i][1]-points[low][1])/(points[high][1]-points[low][1])-(expected[i]-expected[low])/(expected[high]-expected[low]))<1e-6);await verifyContext(card);return {card,svg,points};}
async function point(svg,xy){const position=await svg.evaluate((n,v)=>{const p=n.createSVGPoint();p.x=v[0];p.y=v[1];const s=p.matrixTransform(n.getScreenCTM()),b=n.getBoundingClientRect();return{x:s.x-b.left,y:s.y-b.top};},xy);await svg.click({position});}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));
 await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/visual-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await baseline.locator('.jp-Cell').first().filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(0,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);await observeMolecularControllers(page);


 await step('Apply explicitly dimensioned mass colors through the existing Whole owner',async()=>{
  await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/visual-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});await page.locator('.jp-Cell').first().filter({hasText:'import molsysviewer as msv'}).waitFor();const no=page.getByRole('button',{name:'No',exact:true});if(await no.isVisible())await no.click();await execute(0);await page.waitForFunction(()=>{const e=document.querySelector('.jp-OutputArea-error');if(e)throw new Error(e.textContent);return window.__controllers?.[0]?.getStructureData()?.elementCount===62;});expected=JSON.parse(await readFile(output+'/visual-expected.json','utf8'));
  const e=await prepare(page);await calculate(e);await e.locator('[data-result-row="0"]').check();await e.locator('[data-color-actions] summary').click();await e.locator('[data-color-palette]').selectOption('blue_red');await e.locator('[data-color-range]').selectOption('manual');await e.locator('[data-color-minimum]').fill('0');await e.locator('[data-color-maximum]').fill('20');assert.match(await e.locator('[data-color-unit]').innerText(),/dalton/);await e.locator('[data-apply-report-colors]').click();await e.locator('[data-status]').filter({hasText:'Colored Whole'}).waitFor();await colors(page,expected.whole_colors);await e.locator('[data-clear]').click();await e.locator('[data-report]').waitFor({state:'hidden'});await colors(page,expected.whole_colors);
 });
 let svg,points;
 await step('Plot one SASA output through every source structure without changing the color snapshot',async()=>{
  const e=await prepare(page,'sasa','indices');await e.locator('[data-structures]').selectOption('all');await calculate(e);await e.locator('[data-result-row="0"]').check();await e.locator('[data-selected-plot-actions] summary').click();await e.locator('[data-add-result-plot]').click();await e.locator('[data-status]').filter({hasText:'selected observation'}).waitFor();({svg,points}=await verifyPlot(page,expected.sasa));assert.match(await svg.locator('..').innerText(),/nm\*\*2/);await e.locator('[data-clear]').click();await e.locator('[data-report]').waitFor({state:'hidden'});await colors(page,expected.whole_colors);await verifyPlot(page,expected.sasa);
  const canvasOutput=page.locator('[data-molsysviewer-canvas-output]').first();await canvasOutput.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');await canvasOutput.getByTitle('Panel mode (N / W)',{exact:true}).click();await e.waitFor({state:'hidden'});await point(svg,points[1]);await page.waitForFunction(()=>window.__controllers[0].trajectory.getTrajectoryState().currentFrame===1);await colors(page,expected.whole_colors);
 });
 let canvas,studio;
 await step('Receive unchanged native colors and explicit selected series in the canvas popup',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await colors(canvas,expected.whole_colors);
  const e=await prepare(canvas,'sasa','indices');await e.locator('[data-structures]').selectOption('all');await calculate(e);await e.locator('[data-result-row="0"]').check();await e.locator('[data-selected-plot-actions] summary').click();await e.locator('[data-add-result-plot]').click();await e.locator('[data-status]').filter({hasText:'selected observation'}).waitFor();await verifyPlot(canvas,expected.sasa);await verifyPlot(page,expected.sasa);
 });
 await step('Refuse incomplete Whole coloring in detached Studio without changing either canvas',async()=>{
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});const e=await prepare(studio,'mass','indices');await calculate(e);await e.locator('[data-result-row="0"]').check();await e.locator('[data-color-actions] summary').click();await e.locator('[data-apply-report-colors]').click();await e.locator('[data-status]').filter({hasText:'does not cover every atom'}).waitFor();await colors(page,expected.whole_colors);await colors(canvas,expected.whole_colors);assert.equal(await e.locator('[data-report]').isVisible(),true);
  const calculation=await prepare(studio,'sasa','indices');await calculation.locator('[data-structures]').selectOption('all');await calculate(calculation);
  await calculation.locator('[data-result-row="0"]').check();await calculation.locator('[data-selected-plot-actions] summary').click();await calculation.locator('[data-add-result-plot]').click();await calculation.locator('[data-status]').filter({hasText:'selected observation'}).waitFor();
  await calculation.locator('[data-clear]').click();await calculation.locator('[data-report]').waitFor({state:'hidden'});
  await verifyPlot(page,expected.sasa);await verifyPlot(canvas,expected.sasa);await studio.screenshot({path:output+'/visual-studio-popup.png'});await studio.close();await canvas.close();
 });

 await step('Adopt atomic RMSF as an explicit length-color snapshot without an invented trajectory axis',async()=>{
  const e=await prepare(page,'rmsf','all');await e.locator('[data-structures]').selectOption('all');await calculate(e);await e.locator('[data-result-row="0"]').check();const details=e.locator('[data-color-actions]');if(!await e.locator('[data-color-palette]').isVisible())await details.locator('summary').click();await e.locator('[data-color-palette]').selectOption('viridis');await e.locator('[data-color-range]').selectOption('auto');assert.match(await e.locator('[data-color-unit]').innerText(),/nm/);await e.locator('[data-apply-report-colors]').click();await e.locator('[data-status]').filter({hasText:'Colored Whole'}).waitFor();await colors(page,expected.rmsf_colors);assert.equal(await e.locator('[data-selected-plot-actions]').isVisible(),false);await e.locator('[data-clear]').click();await e.locator('[data-report]').waitFor({state:'hidden'});await colors(page,expected.rmsf_colors);
 });
 await step('Verify preserved scientific source and separate retained core colors and plots',async()=>{await execute(1);await page.getByText('JUPYTER_VISUAL_ADOPTION_NATIVE_OK',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);await page.screenshot({path:output+'/visual-final.png',fullPage:true});});
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(error=>baselineErrors.some(b=>fingerprint(error)===fingerprint(b))),'A new page error appeared beyond the plain Jupyter control');
 const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual Jupyter/AnyWidget/Mol* scalar colors through native representation themes in both canvases, explicit source series with real point navigation, both popups and source preservation. No human or installed acceptance.'};await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser)for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries()){await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());await p.screenshot({path:output+'/window-'+i+'-failure.png',fullPage:true});}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
