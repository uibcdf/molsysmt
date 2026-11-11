/** Native Analysis through actual Jupyter, with independent coordinate oracles. */
import assert from 'node:assert/strict';
import {openMolecularPanel,observeMolecularControllers} from './jupyter_panel_controls.mjs';
import {installInitialCanvasTrace,saveInitialCanvasTrace} from './jupyter_initial_canvas_trace.mjs';
import {createRequire} from 'node:module';
import {readFile,writeFile,appendFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
const settings=process.env.MOLSYSVIEWER_JUPYTER_SETTINGS;
const output=dirname(resolve(settings)),config=JSON.parse(await readFile(settings,'utf8'));
const {chromium}=createRequire(config.viewer_root+'/molsysviewer/js/package.json')('playwright');
let browser,page,stage='start';const checks=[],errors=[],baselineErrors=[];
const campaignStarted=performance.now();
async function step(name,action){stage=name;await appendFile(output+'/step-timings.jsonl',JSON.stringify({stage,phase:'start',elapsed_ms:performance.now()-campaignStarted})+'\n');console.log('STEP '+name);await action();checks.push(name);await appendFile(output+'/step-timings.jsonl',JSON.stringify({stage,phase:'complete',elapsed_ms:performance.now()-campaignStarted})+'\n');}
async function execute(cell,p=page,beforeRun){
 await p.getByText(/Isolated molecular tools receiving\s*\|\s*Idle/).waitFor();
 await cell.locator('.cm-content').click();
 await beforeRun?.(cell);
 await p.getByRole('button',{name:/Run this cell and advance/}).click();
}
const workspace=p=>openMolecularPanel(p,'analysis');
async function populations(panel){await panel.locator('[data-first] [data-source]').selectOption('indices');await panel.locator('[data-first] [data-indices]').fill('0,2');await panel.locator('[data-second] [data-source]').selectOption('indices');await panel.locator('[data-second] [data-indices]').fill('3,5,7');}
async function numericRows(panel){return panel.locator('[data-rows] tr').evaluateAll(rows=>rows.map(row=>[...row.querySelectorAll('td')].map(cell=>Number(cell.textContent))));}
function displayed(actual,expected){assert.ok(actual===Number(expected.toPrecision(9)),`${actual} differs from the nine-significant-digit independent observation ${expected}`);}
function close(actual,expected){assert.ok(Math.abs(actual-expected)<1e-8,`${actual} differs from independent coordinate reference ${expected}`);}
async function chooseRow(panel,index=0){const radio=panel.locator(`[data-result-row="${index}"]`);await radio.focus();await panel.page().keyboard.press('Space');assert.equal(await radio.isChecked(),true);}
async function configureDistance(p,{first='0,2',second='3,5,7',centers=false}={}){
 await p.bringToFront();await workspace(p);const panel=p.locator('.msm-analysis');await panel.locator('[data-task]').selectOption('distances');
 for(const [side,text] of [['first',first],['second',second]]){await panel.locator(`[data-${side}] [data-source]`).selectOption('indices');await panel.locator(`[data-${side}] [data-indices]`).fill(text);}
 const settings=panel.locator('details:has([data-first-endpoint])');if(await settings.getAttribute('open')===null)await settings.locator('summary').click();
 await panel.locator('[data-first-endpoint]').selectOption(centers?'geometric':'atoms');await panel.locator('[data-second-endpoint]').selectOption(centers?'geometric':'atoms');
 return panel;
}
async function calculateRows(panel){await panel.locator('[data-calculate]').click();await panel.locator('[data-report-heading]').filter({hasText:'Distances result'}).waitFor();}
async function addLive(panel){await chooseRow(panel);await panel.locator('[data-add-live-distance]').click();const status=panel.locator('[data-status]');await status.filter({hasText:'Added live distance'}).waitFor();const match=/Added live distance (\S+) in Measures/.exec(await status.innerText());assert.ok(match);return match[1];}
async function renderedDistance(p,tag,points,participants){
 await p.bringToFront();
 if(!await p.evaluate(()=>!!window.Harness))await p.addScriptTag({path:config.viewer_root+'/molsysviewer/js/tests/e2e/harness.bundle.js'});
 await p.waitForFunction(({tag,points,participants})=>{
  const c=window.__controllers?.at(-1);if(!c)return false;const actual=window.Harness.inspectMeasurementGeometry(c,tag);
  return JSON.stringify(actual.participants)===JSON.stringify(participants)&&actual.geometry.some(g=>g.kind==='text')&&actual.geometry.every(g=>g.points.every((point,i)=>point.every((v,j)=>Math.abs(v-points[i][j])<1e-4))&&(g.kind!=='text'||g.labelAnchor.every((v,j)=>Math.abs(v-(points[0][j]+points[1][j])/2)<1e-4)));
 },{tag,points,participants});
 const geometry=await p.evaluate(tag=>window.Harness.inspectMeasurementGeometry(window.__controllers.at(-1),tag),tag);
 const expected=Math.hypot(...points[0].map((v,j)=>v-points[1][j]));
 for(const g of geometry.geometry){const value=/Distance\s+(-?\d+(?:\.\d+)?)/.exec(g.label);assert.ok(value,g.label);assert.ok(Math.abs(Number(value[1])-expected)<0.011);}
}
async function conformationPanel(p,task,scope='indices'){
 await p.bringToFront();await workspace(p);const panel=p.locator('.msm-analysis').first();
 await panel.locator('[data-task]').selectOption(task);
 await panel.locator('[data-first] [data-source]').selectOption('indices');await panel.locator('[data-first] [data-indices]').fill('4,0,2,4');
 const context=panel.locator('[data-first] details');if(await context.getAttribute('open')===null)await context.locator('summary').click();await context.locator('[data-evaluate]').selectOption('index');await context.locator('[data-index]').fill('0');
 await panel.locator('[data-structures]').selectOption(scope);if(scope==='indices')await panel.locator('[data-structure-indices]').fill('2,0,2');
 if(['rmsd','least_rmsd'].includes(task))await panel.locator('[data-reference-structure]').fill('1');
 await panel.locator('[data-calculate]').click();await panel.locator('[data-report]').waitFor({state:'visible'});return panel;
}
async function verifyPlot(p,task,expected){
 const card=p.locator(`[data-molsysviewer-datacard^="molsysmt-${task}-"]`).first();await card.waitFor({state:'visible'});
 const svg=card.locator('svg:has(polyline)');const points=await svg.locator('polyline').evaluate(node=>(node.getAttribute('points')||'').split(/\s+/).map(point=>point.split(',').map(Number)));
 assert.equal(points.length,3);assert.ok(points[0][0]<points[1][0]&&points[1][0]<points[2][0]);
 const [lo,hi]=[expected.indexOf(Math.min(...expected)),expected.indexOf(Math.max(...expected))];assert.ok(Math.abs(expected[hi]-expected[lo])>1e-12);
 for(let i=0;i<3;i++)assert.ok(Math.abs((points[i][1]-points[lo][1])/(points[hi][1]-points[lo][1])-(expected[i]-expected[lo])/(expected[hi]-expected[lo]))<1e-6);
 const text=await card.textContent();assert.match(text,/Structure index/);assert.match(text,/Length \(nm\)/);return {card,svg,points};
}
async function clickPlotPoint(svg,values){
 const position=await svg.evaluate((node,values)=>{const point=node.createSVGPoint();point.x=values[0];point.y=values[1];const screen=point.matrixTransform(node.getScreenCTM()),rect=node.getBoundingClientRect();return {x:screen.x-rect.left,y:screen.y-rect.top};},values);
 await svg.click({position});
}
try{
 browser=await chromium.launch({headless:true,executablePath:config.chromium,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const baseline=await browser.newPage();baseline.on('pageerror',error=>baselineErrors.push({error:String(error),stack:error.stack}));await baseline.goto(`http://127.0.0.1:${config.port}/lab/workspaces/analysis-plain-${Date.now()}/tree/plain.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});const plain=baseline.locator('.jp-NotebookPanel:visible .jp-Cell').first();await plain.filter({hasText:'PLAIN_JUPYTER_CONTROL_OK'}).waitFor();await execute(plain,baseline);await baseline.getByText('PLAIN_JUPYTER_CONTROL_OK 2',{exact:true}).waitFor();await baseline.close();
 page=await browser.newPage({viewport:{width:1440,height:1100}});page.setDefaultTimeout(30000);const record=p=>p.on('pageerror',error=>errors.push({stage,error:String(error),stack:error.stack}));record(page);const panel=()=>page.locator('.msm-analysis').first();let expected;
 await observeMolecularControllers(page);
 const armInitialCanvasTrace=await installInitialCanvasTrace(page,3983);
 await step('Load TcTIM and open Analysis without calculating implicitly',async()=>{
  let outcome='run_unavailable';
  try {
   await page.goto(`http://127.0.0.1:${config.port}/lab/workspaces/analysis-${Date.now()}/tree/system.ipynb?token=${config.token}`,{waitUntil:'domcontentloaded'});
   const cell=page.locator('.jp-NotebookPanel:visible .jp-Cell').first();
   await cell.filter({hasText:'import molsysviewer as msv'}).waitFor();
   const no=page.getByRole('button',{name:'No',exact:true});
   if(await no.isVisible())await no.click();
   await execute(cell,page,armInitialCanvasTrace);
   outcome='canvas_wait_failed';
   await page.locator('canvas').waitFor();
   outcome='canvas_visible';
   await workspace(page);
  } finally {
   await saveInitialCanvasTrace(page,output+'/initial-canvas.json',outcome);
  }
  assert.equal(await panel().locator('[data-calculate]').isDisabled(),true);
  assert.equal(await panel().locator('[data-report]').isVisible(),false);
  expected=JSON.parse(await readFile(output+'/analysis-expected.json','utf8'));
 });
 await step('Calculate explicit atom populations and verify native distances against coordinates',async()=>{
  await populations(panel());await panel().locator('[data-calculate]').click();await panel().locator('[data-report-heading]').filter({hasText:'Distances result'}).waitFor();const rows=await numericRows(panel());assert.equal(rows.length,6);assert.deepEqual(rows.map(r=>r.slice(0,3)),[[0,0,3],[0,0,5],[0,0,7],[0,2,3],[0,2,5],[0,2,7]]);rows.forEach((r,i)=>close(r[3],expected.distances[i]));assert.match(await panel().locator('[data-columns]').innerText(),/Distance \(nm\)/);
 });
 await step('Inspect native minimum and maximum without changing molecular data',async()=>{
  for(const task of ['minimum','maximum']){await panel().locator('[data-task]').selectOption(task);await panel().locator('[data-calculate]').click();await panel().locator('[data-report-heading]').filter({hasText:task==='minimum'?'Minimum distance result':'Maximum distance result'}).waitFor();const rows=await numericRows(panel());assert.equal(rows.length,1);close(rows[0][3],expected[task]);}
 });
 await step('Inspect evaluated-empty neighbors and explicit nearest-count results',async()=>{
  await panel().locator('[data-task]').selectOption('neighbors');await panel().locator('[data-cutoff]').fill('0');await panel().locator('[data-calculate]').click();await panel().locator('[data-page-summary]').filter({hasText:'No matching neighbors in the evaluated scope'}).waitFor();assert.equal(await panel().locator('[data-rows] tr').count(),0);await panel().locator('[data-neighbor-mode]').selectOption('count');await panel().locator('[data-count]').fill('1');await panel().locator('[data-calculate]').click();await panel().locator('[data-report-summary]').filter({hasText:'2 rows'}).waitFor();const rows=await numericRows(panel());rows.forEach((r,i)=>close(r[3],Math.min(...expected.distances.slice(i*3,i*3+3))));
 });
 await step('Page through TcTIM source indices without transferring the complete result',async()=>{
  await panel().locator('[data-task]').selectOption('distances');await panel().locator('[data-first] [data-source]').selectOption('all');await panel().locator('[data-second] [data-indices]').fill('3');await panel().locator('[data-calculate]').click();await panel().locator('[data-report-summary]').filter({hasText:'3,983 rows'}).waitFor();assert.equal(await panel().locator('[data-rows] tr').count(),50);await panel().locator('[data-next]').click();await panel().locator('[data-page-summary]').filter({hasText:'Rows 51–100'}).waitFor();const rows=await numericRows(panel());assert.equal(rows[0][1],50);close(rows[0][3],expected.page51);await page.screenshot({path:output+'/analysis-paged.png',fullPage:true});
 });
 await step('Use independent Analysis panels in canvas popup and detached Studio',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);await populations(canvas.locator('.msm-analysis'));await canvas.locator('[data-calculate]').click();await canvas.locator('[data-report-summary]').filter({hasText:'6 rows'}).waitFor();const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);await populations(studio.locator('.msm-analysis'));await studio.locator('[data-task]').selectOption('minimum');await studio.locator('[data-calculate]').click();await studio.locator('[data-report-heading]').filter({hasText:'Minimum distance result'}).waitFor();close((await numericRows(studio.locator('.msm-analysis')))[0][3],expected.minimum);await studio.screenshot({path:output+'/analysis-studio-popup.png'});await studio.locator('[data-clear]').click();await studio.locator('[data-report]').waitFor({state:'hidden'});await studio.close();await canvas.close();
 });
 await step('Python verifies every molecular coordinate chemical domain and scene object unchanged',async()=>{await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(1));await page.getByText('JUPYTER_ANALYSIS_UNCHANGED 3983',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);});
 await step('Select participants and focus the visible structure without losing the row acknowledgement',async()=>{
  const p=await configureDistance(page);await calculateRows(p);assert.equal(await p.locator('[data-pagination]').isVisible(),false);assert.equal(await p.locator('[data-select-participants]').isDisabled(),true);await chooseRow(p);
  await p.locator('[data-select-participants]').click();await p.locator('[data-status]').filter({hasText:'Selected 2 participant atoms'}).waitFor();
  await page.waitForFunction(()=>JSON.stringify(window.__controllers[0].currentActiveSelection.atom_indices.slice().sort((a,b)=>a-b))==='[0,3]');
  await p.locator('[data-focus-participants]').click();await p.locator('[data-status]').filter({hasText:'Focused participant atoms'}).waitFor();
  // Core focus encloses atomic spheres, rather than taking an arithmetic mean.
  // Independently require both source positions/radii plus the requested 4 Å
  // margin, and a local radius that cannot pass by keeping the whole-system view.
  await page.waitForFunction(points=>{
   const c=window.__controllers[0],camera=c.getCameraSnapshot(),radii=[];for(const u of c.getStructureData().units)for(const i of u.elements)if([0,3].includes(i))radii.push(u.conformation.r(i));
   if(radii.length!==2)return false;
   const maximum=Math.hypot(...points[0].map((v,j)=>v-points[1][j]))+Math.max(...radii)+4;
   return c.trajectory.getTrajectoryState().currentFrame===0&&camera.radius<=maximum+1e-4&&points.every((point,i)=>Math.hypot(...point.map((v,j)=>v-camera.target[j]))+radii[i]+4<=camera.radius+1e-4);
  },expected.focus_points_angstrom).catch(async error=>{
   const diagnostic=await page.evaluate(()=>{const c=window.__controllers[0],s=c.getStructureData(),atoms=[];for(const u of s.units)for(const i of u.elements)if([0,3].includes(i))atoms.push({index:i,position:Array.from(u.conformation.position(i,[0,0,0])),radius:u.conformation.r(i)});return {camera:c.getCameraSnapshot(),atoms,visibility:document.visibilityState};});
   await writeFile(output+'/focus-diagnostic.json',JSON.stringify({expected_points:expected.focus_points_angstrom,...diagnostic},null,2));throw error;
  });
  assert.equal(await p.locator('[data-result-row="0"]').isChecked(),true);
 });
 await step('Mass-weighted observations retain participant actions and explain the disabled live conversion',async()=>{
  const p=await configureDistance(page);await p.locator('[data-first-endpoint]').selectOption('mass');await calculateRows(p);await chooseRow(p);
  assert.equal(await p.locator('[data-add-live-distance]').isDisabled(),true);assert.equal(await p.locator('[data-select-participants]').isEnabled(),true);assert.equal(await p.locator('[data-focus-participants]').isEnabled(),true);assert.match(await p.locator('[data-live-distance-limit]').innerText(),/mass-weighted/);
 });
 await step('Create a centroid Measure from TcTIM and preserve its actual geometry after Clear',async()=>{
  const p=await configureDistance(page,{centers:true});await calculateRows(p);const tag=await addLive(p);await renderedDistance(page,tag,expected.center_points_angstrom,[0,2,3,5,7]);
  await p.locator('[data-clear]').click();await p.locator('[data-report]').waitFor({state:'hidden'});await renderedDistance(page,tag,expected.center_points_angstrom,[0,2,3,5,7]);
  await page.screenshot({path:output+'/analysis-live-source.png',fullPage:true});
 });
 await step('Create core Measures through canvas and detached Studio popups with mirrored geometry',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').first();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  const p=await configureDistance(canvas,{centers:true});await calculateRows(p);const tag=await addLive(p);await renderedDistance(canvas,tag,expected.center_points_angstrom,[0,2,3,5,7]);await renderedDistance(page,tag,expected.center_points_angstrom,[0,2,3,5,7]);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const s=await configureDistance(studio,{centers:true});await calculateRows(s);await chooseRow(s);await s.locator('[data-select-participants]').click();await s.locator('[data-status]').filter({hasText:'Selected 5 participant atoms'}).waitFor();await s.locator('[data-focus-participants]').click();await s.locator('[data-status]').filter({hasText:'Focused participant atoms'}).waitFor();const third=await addLive(s);
  await renderedDistance(canvas,third,expected.center_points_angstrom,[0,2,3,5,7]);await renderedDistance(page,third,expected.center_points_angstrom,[0,2,3,5,7]);await studio.screenshot({path:output+'/analysis-live-studio-popup.png'});await studio.close();await canvas.close();
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(2));await page.getByText('JUPYTER_ANALYSIS_SCENE_OK 3',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 await step('A repeated-population live Measure uses the visible structure and follows a real ensemble',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(3));await page.waitForFunction(()=>window.__controllers.length===2&&window.__controllers[1].getStructureData()?.elementCount===62);
  const ensemble=JSON.parse(await readFile(output+'/analysis-ensemble-expected.json','utf8'));const p=await configureDistance(page,{centers:true,first:'4,0,4',second:'5,2'});
  for(const side of ['first','second']){const details=p.locator(`[data-${side}] details`);await details.locator('summary').click();await details.locator('[data-evaluate]').selectOption('index');await details.locator('[data-index]').fill('0');}
  await p.locator('[data-structures]').selectOption('indices');await p.locator('[data-structure-indices]').fill('2,0,2');await calculateRows(p);const rows=await numericRows(p);assert.deepEqual(rows.map(r=>r[0]),[2,0,2]);close(rows[0][3],ensemble.distances_nm[2]);
  const tag=await addLive(p);assert.match(await p.locator('[data-status]').innerText(),/row remains in structure 2/);assert.equal(await page.evaluate(()=>window.__controllers[1].trajectory.getTrajectoryState().currentFrame),0);await renderedDistance(page,tag,ensemble.points_angstrom[0],[4,0,4,5,2]);
  for(const index of [1,2]){await page.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');await page.locator('[data-molsysviewer-trajectory-step="next"]').click();await page.waitForFunction(index=>window.__controllers[1].trajectory.getTrajectoryState().currentFrame===index,index);await renderedDistance(page,tag,ensemble.points_angstrom[index],[4,0,4,5,2]);}
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(4));await page.getByText('JUPYTER_ANALYSIS_ENSEMBLE_OK 3',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 let conformations;
 await step('Prepare independent conformation references from the unchanged real ensemble',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(5));await page.getByText('JUPYTER_CONFORMATION_ORACLES_OK 3',{exact:true}).waitFor();conformations=JSON.parse(await readFile(output+'/conformation-expected.json','utf8'));
 });
 await step('Inspect RMSD optimal RMSD gyration and atom-indexed RMSF with explicit source axes',async()=>{
  for(const task of ['rmsd','least_rmsd','gyration','rmsf']){
   const p=await conformationPanel(page,task),rows=await numericRows(p),axis=task==='rmsf'?[4,0,2,4]:[2,0,2],values=task==='rmsf'?conformations[task]:axis.map(index=>conformations[task][index]);
   assert.deepEqual(rows.map(row=>row[0]),axis);rows.forEach((row,i)=>close(row[1],values[i]));assert.equal(await p.locator('[data-distance-settings]').isVisible(),false);assert.equal(await p.locator('[data-add-live-distance]').isVisible(),false);assert.equal(await p.locator('[data-add-structure-plot]').isDisabled(),true);
   if(task==='rmsf')assert.match(await p.locator('[data-plot-limit]').innerText(),/not indexed by one scalar per structure/);
  }
 });
 await step('Add a correctly indexed core plot retain it after Clear and navigate by its actual point',async()=>{
  const p=await conformationPanel(page,'gyration','all');assert.equal(await p.locator('[data-add-structure-plot]').isEnabled(),true);await p.locator('[data-add-structure-plot]').click();await p.locator('[data-status]').filter({hasText:'Added a trajectory plot'}).waitFor();
  const {svg,points}=await verifyPlot(page,'gyration',conformations.gyration);await p.locator('[data-clear]').click();await p.locator('[data-report]').waitFor({state:'hidden'});
  // Studio legitimately overlaps canvas cards. Close it through the ordinary
  // toolbar before the pointer action; never force a click through the overlay.
  const canvasOutput=page.locator('[data-molsysviewer-canvas-output]').last();await canvasOutput.scrollIntoViewIfNeeded();await canvasOutput.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');await canvasOutput.getByTitle('Panel mode (N / W)',{exact:true}).click();await p.waitFor({state:'hidden'});
  await clickPlotPoint(svg,points[1]);await page.waitForFunction(()=>window.__controllers.at(-1).trajectory.getTrajectoryState().currentFrame===1);
  await page.screenshot({path:output+'/conformation-core-plot.png',fullPage:true});
 });
 await step('Inspect and adopt conformational results through both real popup boundaries',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').last();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  // The popup owns its Studio layout independently of the source. As with the
  // primary canvas, use the normal toolbar to uncover the plot before clicking.
  const popupPanel=canvas.locator('[data-molsysviewer-addons-panel="true"]');
  if(await popupPanel.isVisible()){
   await canvas.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await canvas.keyboard.press('Enter');await canvas.getByTitle('Panel mode (N / W)',{exact:true}).click();await popupPanel.waitFor({state:'hidden'});
  }
  const graph=await verifyPlot(canvas,'gyration',conformations.gyration);await clickPlotPoint(graph.svg,graph.points[2]);await canvas.waitForFunction(()=>window.__controllers.at(-1).trajectory.getTrajectoryState().currentFrame===2);await page.waitForFunction(()=>window.__controllers.at(-1).trajectory.getTrajectoryState().currentFrame===2);
  const rmsf=await conformationPanel(canvas,'rmsf');const rows=await numericRows(rmsf);rows.forEach((row,i)=>close(row[1],conformations.rmsf[i]));
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const rmsd=await conformationPanel(studio,'rmsd','all');await rmsd.locator('[data-add-structure-plot]').click();await rmsd.locator('[data-status]').filter({hasText:'Added a trajectory plot'}).waitFor();await verifyPlot(canvas,'rmsd',conformations.rmsd);await verifyPlot(page,'rmsd',conformations.rmsd);await rmsd.locator('[data-clear]').click();await rmsd.locator('[data-report]').waitFor({state:'hidden'});await verifyPlot(canvas,'rmsd',conformations.rmsd);await studio.screenshot({path:output+'/conformation-studio-popup.png'});await studio.close();await canvas.close();
 });
 let geometryExpected;
 await step('Inspect directed vector components and repeated source structures against coordinates',async()=>{
  geometryExpected=JSON.parse(await readFile(output+'/geometry-expected.json','utf8'));
  const p=await configureDistance(page,{first:'4,0',second:'5,2'});
  await p.locator('[data-task]').selectOption('vectors');await p.locator('[data-heading]').filter({hasText:'Vectors'}).waitFor();
  await p.locator('[data-structures]').selectOption('indices');await p.locator('[data-structure-indices]').fill('0,2,0');
  await p.locator('[data-calculate]').click();await p.locator('[data-report-heading]').filter({hasText:'Vectors result'}).waitFor();
  const rows=await numericRows(p);assert.equal(rows.length,12);assert.deepEqual(rows.map(r=>r[0]),[0,0,0,0,2,2,2,2,0,0,0,0]);
  for(let i=0;i<rows.length;i++)for(let axis=0;axis<3;axis++)displayed(rows[i][3+axis],geometryExpected.vectors[i][axis]);
  assert.match(await p.locator('[data-columns]').innerText(),/X \(nm\)[\s\S]*Y \(nm\)[\s\S]*Z \(nm\)/);
  assert.equal(await p.locator('[data-add-live-distance]').isVisible(),false);
  await page.screenshot({path:output+'/analysis-vector-components.png'});
 });
 await step('Inspect ordered atom-triplet angles with explicit angular display units',async()=>{
  const p=page.locator('.msm-analysis');await p.locator('[data-task]').selectOption('angles');await p.locator('[data-angular-settings]').waitFor({state:'visible'});
  assert.equal(await p.locator('[data-first]').isVisible(),false);assert.equal(await p.locator('[data-second]').isVisible(),false);
  await p.locator('[data-atom-tuples]').fill(JSON.stringify(geometryExpected.triplets));await p.locator('[data-angle-unit]').selectOption('degrees');
  await p.locator('[data-calculate]').click();await p.locator('[data-report-heading]').filter({hasText:'Angles result'}).waitFor();
  let rows=await numericRows(p);assert.deepEqual(rows.map(r=>r[0]),[0,0,2,2,0,0]);
  for(let i=0;i<rows.length;i++){assert.deepEqual(rows[i].slice(1,4),geometryExpected.triplets[i%2]);displayed(rows[i][4],geometryExpected.angles_degrees[i]);}
  await p.locator('[data-angle-unit]').selectOption('radians');await p.locator('[data-calculate]').click();await p.locator('[data-report-heading]').filter({hasText:'Angles result'}).waitFor();rows=await numericRows(p);
  for(let i=0;i<rows.length;i++)displayed(rows[i][4],geometryExpected.angles_degrees[i]*Math.PI/180);
  assert.equal(await p.locator('[data-add-live-distance]').isVisible(),false);
  await page.screenshot({path:output+'/analysis-triplet-angles.png'});
 });
 await step('Inspect signed quartet torsions and deliberate participant actions without navigating',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').last();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});await workspace(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});await workspace(studio);
  const p=studio.locator('.msm-analysis');await p.locator('[data-task]').selectOption('torsions');await p.locator('[data-heading]').filter({hasText:'Torsions'}).waitFor();
  await p.locator('[data-atom-tuples]').fill(JSON.stringify(geometryExpected.quartets));await p.locator('[data-angle-unit]').selectOption('degrees');
  await p.locator('[data-calculate]').click();await p.locator('[data-report-heading]').filter({hasText:'Torsions result'}).waitFor();
  const rows=await numericRows(p);for(let i=0;i<rows.length;i++){assert.deepEqual(rows[i].slice(1,5),geometryExpected.quartets[i%2]);displayed(rows[i][5],geometryExpected.torsions_degrees[i]);}
  await chooseRow(p);await p.locator('[data-select-participants]').click();await p.locator('[data-status]').filter({hasText:'Selected 4 participant atoms'}).waitFor();
  await page.waitForFunction(()=>JSON.stringify(window.__controllers[1].currentActiveSelection.atom_indices.slice().sort((a,b)=>a-b))==='[0,2,4,5]');
  await p.locator('[data-focus-participants]').click();await p.locator('[data-status]').filter({hasText:'Focused participant atoms in visible structure 2'}).waitFor();
  assert.equal(await page.evaluate(()=>window.__controllers[1].trajectory.getTrajectoryState().currentFrame),2);
  await studio.screenshot({path:output+'/analysis-signed-torsions.png'});await studio.close();await canvas.close();
 });
 let pcaExpected;
 async function pcaPanel(target){
  const p=await configureDistance(target,{first:'4,0,2,4',second:'5,2'});
  await p.locator('[data-task]').selectOption('pca');await p.locator('[data-heading]').filter({hasText:'Principal component analysis'}).waitFor();
  await p.locator('[data-structures]').selectOption('indices');await p.locator('[data-structure-indices]').fill('2,0,2');
  await p.locator('[data-pca-weighting]').selectOption('custom');await p.locator('[data-pca-weights]').fill(JSON.stringify(pcaExpected.weights));
  await p.locator('[data-calculate]').click();await p.locator('[data-report-heading]').filter({hasText:'Principal component analysis'}).waitFor();
  const rows=await numericRows(p);assert.equal(rows.length,12);rows.forEach((row,i)=>{assert.equal(row[0],i+1);close(row[1],pcaExpected.values[i]);});
  assert.ok((await p.locator('[data-columns]').innerText()).includes('Eigenvalue (nm²)'));
  assert.equal(await p.locator('[data-add-structure-plot]').isDisabled(),true);return p;
 }
 async function coefficients(p){
  await p.locator('[data-pca-component]').fill('1');await p.locator('[data-show-component]').click();
  await p.locator('[data-columns]').filter({hasText:'Coefficient (dimensionless)'}).waitFor();
  const rows=await p.locator('[data-rows] tr').evaluateAll(rows=>rows.map(row=>[...row.querySelectorAll('td')].map(cell=>cell.textContent)));
  assert.equal(rows.length,12);
  const vector=rows.map((r,i)=>{assert.deepEqual(r.slice(0,4),['1','XYZ'[Math.floor(i/4)],String(i%4),String(pcaExpected.atoms[i%4])]);return Number(r[4]);});
  close(vector.reduce((sum,v)=>sum+v*v,0),1);
  pcaExpected.covariance.forEach((row,i)=>close(row.reduce((sum,v,j)=>sum+v*vector[j],0),pcaExpected.values[0]*vector[i]));
 }
 await step('Inspect weighted PCA eigenvalues and source-indexed coefficients without a trajectory projection',async()=>{
  pcaExpected=JSON.parse(await readFile(output+'/pca-expected.json','utf8'));
  const p=await pcaPanel(page);await coefficients(p);
  await p.locator('[data-show-spectrum]').click();await p.locator('[data-columns]').filter({hasText:'Eigenvalue (nm²)'}).waitFor();
  await p.locator('summary').filter({hasText:'Method, source and result lifetime'}).click();
  assert.match(await p.locator('[data-lifetime]').innerText(),/signs and bases|signs.*not unique/i);
  await page.screenshot({path:output+'/analysis-pca-spectrum.png'});
 });
 await step('Inspect PCA through both popups and deliberately select coefficient participants without moving coordinates',async()=>{
  const source=page.locator('[data-molsysviewer-canvas-output]').last();await source.getByRole('button',{name:'Show canvas controls',exact:true}).focus();await page.keyboard.press('Enter');
  const opened=page.waitForEvent('popup');await source.getByTitle('Open popup',{exact:true}).click();const canvas=await opened;record(canvas);await canvas.locator('#molsysviewer-loading').waitFor({state:'hidden'});
  await pcaPanel(canvas);
  const detached=canvas.waitForEvent('popup');await canvas.getByTitle('Popout panel to external window',{exact:true}).click();const studio=await detached;record(studio);await studio.locator('#molsysviewer-loading').waitFor({state:'detached'});
  const p=await pcaPanel(studio);await coefficients(p);await p.getByRole('radio',{name:'Select result row 4',exact:true}).check();
  await p.locator('[data-select-participants]').click();await p.locator('[data-status]').filter({hasText:'Selected 1 participant atoms'}).waitFor();
  await page.waitForFunction(()=>JSON.stringify(window.__controllers[1].currentActiveSelection.atom_indices)==='[4]');
  await p.locator('[data-focus-participants]').click();await p.locator('[data-status]').filter({hasText:'Focused participant atoms in visible structure 2'}).waitFor();
  assert.equal(await page.evaluate(()=>window.__controllers[1].trajectory.getTrajectoryState().currentFrame),2);
  await studio.screenshot({path:output+'/analysis-pca-popup-coefficients.png'});await studio.close();await canvas.close();
 });
 await step('Python verifies retained native data separate plots and deliberate structure navigation',async()=>{
  await execute(page.locator('.jp-NotebookPanel:visible .jp-Cell').nth(6));await page.getByText('JUPYTER_CONFORMATION_SCENE_OK 2',{exact:true}).waitFor();assert.equal(await page.locator('.jp-OutputArea-error').count(),0);
 });
 const fingerprint=e=>e.error+'|'+(e.stack?.split('\n')[1]||'');assert.ok(errors.every(error=>baselineErrors.some(baseline=>fingerprint(error)===fingerprint(baseline))),'A page error was introduced beyond the plain Jupyter control');const receipt={checks,errors,baseline_errors:baselineErrors,scope:'Actual TcTIM and real three-structure ensemble in Jupyter/Mol*/AnyWidget: native geometric/conformational queries, bounded source-index pages, explicit participant and core Measure/plot adoption from source and both popups. Independent numerical, actual geometry/text/plot-axis and molecular-invariance checks, including duplicate participants, atom-versus-structure axes, frozen observations versus deliberate navigation and mass-weighted live-distance refusal. Not human Qt or installed qualification.'};await writeFile(output+'/full-result.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
}catch(error){await writeFile(output+'/full-failure.json',JSON.stringify({stage,error:String(error),checks,errors},null,2));if(browser){for(const [i,p] of browser.contexts().flatMap(c=>c.pages()).entries())await writeFile(output+'/window-'+i+'-failure-dom.txt',await p.locator('body').innerText());}if(page){await page.screenshot({path:output+'/failure.png',fullPage:true});await writeFile(output+'/failure-dom.txt',await page.locator('body').innerText());}console.error(error);process.exitCode=1;}
finally{if(browser)await browser.close();}
