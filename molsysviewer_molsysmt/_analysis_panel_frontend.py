"""Explicit populations and bounded native geometry/conformation reports."""

from ._panel_widgets import SELECTION_MARKUP, SHARED_JS

ESM = (
    SHARED_JS
    + r"""
export function render({model,el}) {
  const abort=new AbortController(),options={signal:abort.signal};
  const initial={source:'none',value:'',expression:'',indices:'',context:'current',structure_index:0};
  const defaults={task:'distances',relation:'between',pairing:'cartesian',first_endpoint:'atoms',second_endpoint:'atoms',structures:'current',indices:'',pbc:false,neighbor_mode:'cutoff',cutoff:'0.35',cutoff_unit:'nm',count:'5',reference_structure:'0',reference_population:'same',weighting:'uniform',atom_tuples:'',angle_unit:'degrees'};
  let draft={...initial,...model.get('analysis_selection')},second={...initial,...model.get('analysis_selection_2')},parameters={...defaults,...model.get('analysis_parameters')};
  let context={},report=null,page=null,busy=false,sequence=0,stamp=0,requestStamp=0,message='',retirement=0;
  let selectedRow=null,pendingAction='',sceneRequest=0,sceneNotice='';
  const sceneActions=new Set(['select_participants','focus_participants','add_live_distance','add_structure_plot']);
  const angularTasks=new Set(['angles','torsions']);
  const conformations=new Set(['rmsd','least_rmsd','gyration','rmsf']);
  const headings={vectors:'Vectors',angles:'Angles',torsions:'Torsions',distances:'Distances',minimum:'Minimum distance',maximum:'Maximum distance',neighbors:'Neighbor search',rmsd:'RMSD without superposition',least_rmsd:'RMSD after optimal superposition',gyration:'Radius of gyration',rmsf:'Atomic fluctuations (RMSF)'};
  el.innerHTML=`<section class="msm-system msm-analysis" aria-label="Molecular analysis tools">
    <label>Analysis task<select data-task aria-label="Analysis task"><optgroup label="Distances and neighborhoods"><option value="distances">Distances</option><option value="minimum">Minimum distance</option><option value="maximum">Maximum distance</option><option value="neighbors">Neighbor search</option></optgroup><optgroup label="Vectors and angles"><option value="vectors">Vectors</option><option value="angles">Angles (atom triplets)</option><option value="torsions">Torsions (atom quartets)</option></optgroup><optgroup label="Conformations"><option value="rmsd">RMSD without superposition</option><option value="least_rmsd">RMSD after optimal superposition</option><option value="gyration">Radius of gyration</option><option value="rmsf">Atomic fluctuations (RMSF)</option></optgroup></select></label>
    <h2 data-heading>Distances</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint" data-purpose></p>
    <label data-relation-label>Populations<select data-relation aria-label="Analysis populations"><option value="between">Between two populations</option><option value="within">Within one population</option></select></label>
    <div data-reference-settings hidden><label>Reference structure index<input data-reference-structure aria-label="RMSD reference structure index" inputmode="numeric" maxlength="64" value="0"></label><label>Reference atoms<select data-reference-population aria-label="RMSD reference population"><option value="same">Same source atom indices as the query</option><option value="second">Choose a separate reference population</option></select></label><p class="msm-hint">The reference is a stored structure of this system. Atoms correspond by their supplied order, including repeated indices; equal counts do not establish chemical identity. No sequence or name matching is inferred.</p></div>
    <div data-angular-settings hidden>
      <label><span data-tuples-label>Atom triplets</span><textarea data-atom-tuples aria-label="Atom-index tuples (JSON)" maxlength="16384" rows="3" placeholder="[[0, 1, 2], [2, 3, 4]]"></textarea></label>
      <label>Display angular unit<select data-angle-unit aria-label="Angular display unit"><option value="degrees">degrees</option><option value="radians">radians</option></select></label>
      <label class="msm-checkbox"><input type="checkbox" data-angular-pbc>Use periodic minimum images when a box is available</label>
    </div>
    <details data-first open><summary data-first-label>First population</summary>__SELECTION_EDITOR__</details>
    <details data-second open><summary data-second-label>Second population</summary>__SELECTION_EDITOR__</details>
    <p class="msm-hint" data-population-help>Each selection is resolved in its stated reference-state context. Those fixed atoms are used in every requested structure; this is not a different selection in each structure.</p>
    <label data-weighting-label hidden>Gyration weighting<select data-weighting aria-label="Gyration weighting"><option value="uniform">Uniform atom weights</option><option value="masses">Standard atomic masses (IUPAC 2021)</option></select></label>
    <details data-distance-settings><summary>Endpoints and calculation settings</summary>
      <label>First endpoint<select data-first-endpoint aria-label="First endpoint"><option value="atoms">Individual atoms</option><option value="geometric">Geometric center of the population</option><option value="mass">Mass-weighted center of the population</option></select></label>
      <label data-second-endpoint-label>Second endpoint<select data-second-endpoint aria-label="Second endpoint"><option value="atoms">Individual atoms</option><option value="geometric">Geometric center of the population</option><option value="mass">Mass-weighted center of the population</option></select></label>
      <label data-pairing-label>Compare<select data-pairing aria-label="Analysis pairing"><option value="cartesian">Every first endpoint with every second endpoint</option><option value="paired">Corresponding endpoints, in supplied order</option></select></label>
      <label class="msm-checkbox"><input type="checkbox" data-pbc>Use periodic minimum-image distances when a box is available</label>
      <p class="msm-hint">Centers use the provided coordinates; split periodic molecules are not reconstructed. Periodic atom distances do not make a simple center a whole-molecule center.</p>
    </details>
    <label>Calculate structures<select data-structures aria-label="Analysis structures"><option value="current">Current structure</option><option value="all">All structures</option><option value="indices">Structure indices, in order</option></select></label>
    <label data-structure-indices-label hidden>Structure indices<input data-structure-indices aria-label="Analysis structure indices" maxlength="4096" placeholder="2, 0, 2"></label>
    <div data-neighbor-settings hidden>
      <label>Find neighbors by<select data-neighbor-mode aria-label="Neighbor criterion"><option value="cutoff">Distance cutoff, inclusive</option><option value="count">Number of nearest neighbors</option></select></label>
      <div class="msm-vector" data-cutoff-settings><label>Cutoff<input data-cutoff aria-label="Neighbor cutoff" inputmode="decimal" maxlength="64"></label><label>Length unit<select data-cutoff-unit aria-label="Neighbor cutoff unit"><option value="nm">nm</option><option value="angstrom">Å</option><option value="pm">pm</option></select></label></div>
      <label data-count-label hidden>Neighbors per first endpoint<input data-count aria-label="Neighbor count" inputmode="numeric" maxlength="64"></label>
    </div>
    <p class="msm-hint" data-pair-scope></p>
    <details><summary>Calculation size and resources</summary><p class="msm-hint" data-resources>A full distance matrix grows as structures × first endpoints × second endpoints. Only 50 rows are sent to the browser at a time. Native calculation, coordinates and indexing may still need substantial memory. Flat distance matrices request MolSysMT block mode and may use temporary disk storage; centers, corresponding pairs, extrema and nearest-count searches retain their native resource behavior. There is no universal RAM limit or cancellation contract in this panel.</p></details>
    <div class="msm-actions"><button data-calculate>Calculate</button><button data-refresh>Refresh</button><button data-clear hidden>Clear result</button></div>
    <p class="msm-status" role="status" aria-live="polite" data-status></p>
    <section data-report hidden aria-label="Analysis result"><h3 data-report-heading tabindex="-1"></h3><p data-report-summary></p><p class="msm-hint" data-periodicity></p>
      <div class="msm-table-scroll"><table><thead data-columns></thead><tbody data-rows></tbody></table></div>
      <p class="msm-hint" data-page-summary></p><div class="msm-actions" data-pagination><button data-previous>Previous page</button><button data-next>Next page</button></div>
      <div class="msm-actions" role="group" aria-label="Scene actions for selected result"><button data-select-participants>Select participants</button><button data-focus-participants>Focus participants</button><button data-add-live-distance>Add live distance</button></div>
      <div data-plot-actions hidden><div class="msm-actions"><button data-add-structure-plot>Add trajectory plot</button></div><p class="msm-hint" data-plot-limit></p></div>
      <p class="msm-hint" data-scene-help>Choose a result row to use its participants in the scene. Focus and live distances use the visible structure; they do not navigate to the calculated structure. A live distance follows the loaded trajectory and may calculate values for every loaded structure.</p>
      <p class="msm-hint" data-live-distance-limit hidden></p>
      <details><summary>Method, source and result lifetime</summary><p data-provenance></p><p class="msm-hint" data-lifetime>Atom and structure indices refer to the source system. Centers refer to the stated populations, not invented atom indices. Distances are displayed in nm with nine significant digits; Python returns the full native values. This mounted panel keeps the result, including any native temporary storage. Clear, changed inputs/source or leaving the panel releases it. Raw external edits are not automatically observed. Calculating does not change the scene or store the result in H5MSM. Deliberately added live distances belong to core Measures and remain after clearing this report.</p></details>
    </section>
  </section>`;
  const q=key=>el.querySelector(`[data-${key}]`);
  for(const key of ['first','second']){const select=q(key).querySelector('[data-source]');const option=document.createElement('option');option.value='all';option.textContent='Whole system';select.options.add(option,1);}
  const firstEditor=selectionEditor(q('first'),options,patch=>{Object.assign(draft,patch);changed();});
  const secondEditor=selectionEditor(q('second'),options,patch=>{Object.assign(second,patch);changed();});
  function cell(tag,value){const node=document.createElement(tag);node.textContent=String(value);return node;}
  function keepRow(nextReport,nextPage){
    if(selectedRow&&(!nextReport||!nextPage||selectedRow.id!==nextReport.id||selectedRow.index<nextPage.offset||selectedRow.index>=nextPage.offset+nextPage.rows.length))selectedRow=null;
    report=nextReport;page=nextPage;
  }
  function render(){
    const angular=angularTasks.has(parameters.task),vector=parameters.task==='vectors',conformation=conformations.has(parameters.task),rmsd=['rmsd','least_rmsd'].includes(parameters.task),between=angular?false:conformation?(rmsd&&parameters.reference_population==='second'):parameters.relation==='between',neighbors=parameters.task==='neighbors';
    q('task').value=parameters.task;q('heading').textContent=headings[parameters.task];
    q('purpose').textContent=conformation?({rmsd:'Compare positions with one explicit reference structure, including translation and rotation.',least_rmsd:'Calculate the minimum RMSD after an optimal rigid superposition. No fit is applied to molecular coordinates.',gyration:'Measure the spread of the chosen atoms around their geometric or mass-weighted center in each structure.',rmsf:'Measure each atom’s fluctuation about its mean position over the requested structures. Input coordinates are not aligned automatically; use Geometry first when alignment is intended.'}[parameters.task]+' MolSysMT CPU calculation; molecular data and the scene are unchanged.'):neighbors?'Find neighboring endpoints in each chosen structure, keeping zero matches distinct from an uncalculated result.':parameters.task==='minimum'?'Find the closest pair in each chosen structure. Ties keep the first local pair in native order.':parameters.task==='maximum'?'Find the farthest pair in each chosen structure. Ties keep the first local pair in native order.':'Calculate distances between the chosen endpoints without changing coordinates or the scene.';
    q('context').textContent=!context.has_system?'Load a system in Studio > Load first.':context.n_atoms!==undefined?`${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} structures`:'Molecular data need explicit recovery.';
    firstEditor(draft,context);secondEditor(second,context);q('second').hidden=!between;q('first').hidden=angular;q('population-help').hidden=angular;
    q('angular-settings').hidden=!angular;q('atom-tuples').value=parameters.atom_tuples;q('angle-unit').value=parameters.angle_unit;q('angular-pbc').checked=parameters.pbc;q('tuples-label').textContent=parameters.task==='angles'?'Ordered atom triplets (JSON)':'Ordered atom quartets (JSON)';q('atom-tuples').placeholder=parameters.task==='angles'?'[[0, 1, 2], [2, 3, 4]]':'[[0, 1, 2, 3], [2, 3, 4, 5]]';
    q('first-label').textContent=conformation?'Atoms to analyze':'First population';q('second-label').textContent=conformation?'Reference atoms, in correspondence order':'Second population';
    q('relation-label').hidden=conformation||angular;q('distance-settings').hidden=conformation||angular;q('reference-settings').hidden=!rmsd;q('weighting-label').hidden=parameters.task!=='gyration';
    q('reference-population').value=parameters.reference_population;q('weighting').value=parameters.weighting;
    if(document.activeElement!==q('reference-structure'))q('reference-structure').value=parameters.reference_structure;
    q('relation').value=parameters.relation;q('first-endpoint').value=parameters.first_endpoint;q('second-endpoint').value=parameters.second_endpoint;q('second-endpoint-label').hidden=!between;
    q('pairing-label').hidden=neighbors||!between;q('pairing').value=parameters.pairing;q('pbc').checked=parameters.pbc;
    q('structures').value=parameters.structures;q('structure-indices-label').hidden=parameters.structures!=='indices';
    q('neighbor-settings').hidden=!neighbors;q('neighbor-mode').value=parameters.neighbor_mode;q('cutoff-settings').hidden=parameters.neighbor_mode!=='cutoff';q('count-label').hidden=parameters.neighbor_mode!=='count';q('cutoff-unit').value=parameters.cutoff_unit;
    for(const [key,value] of [['structure-indices',parameters.indices],['cutoff',parameters.cutoff],['count',parameters.count]])if(document.activeElement!==q(key))q(key).value=value;
    q('pair-scope').textContent=conformation?'Use the stored nonperiodic coordinates: no wrapping, whole-molecule reconstruction or preparation is inferred. Requested structure order and repeated occurrences are retained. RMSF repeats contribute repeatedly to its average.':neighbors?(between?'The explicit target population can include the query atoms; zero-distance matches are retained.':'Within one population, native self matches are excluded. Neighbor rows are directed and sorted by distance; local tie order is preserved.'):between?(parameters.pairing==='paired'?'Corresponding endpoints require equal counts. Atom order and repeated occurrences are preserved.':'The Cartesian product includes every first/second endpoint pair, including overlaps.'):'The full within-population matrix includes self distances and both directions. These are numerical pairs, not unique physical interactions.';
    q('resources').textContent=conformation?'Only 50 source-index rows cross to the browser at a time. Calculations and coordinates may still need substantial memory; native execution policies remain in force. This panel does not promise a universal RAM bound or cancellation. RMSD/gyration return one value per requested structure; RMSF returns one value per selected atom.':'A full distance matrix grows as structures × first endpoints × second endpoints. Only 50 rows are sent to the browser at a time. Flat distance matrices request native block mode and may use temporary disk storage. Centers, corresponding pairs, extrema and nearest-count searches retain native resource behavior; no universal RAM bound or cancellation is promised.';
    if(vector){q('purpose').textContent='Calculate directed vectors from the first endpoint to the second in molecular Cartesian axes, independently of the camera. Molecular data and the scene are unchanged.';q('pair-scope').textContent+=' Vector rows contain X, Y and Z components; no scalar or arrow is substituted.';q('resources').textContent='A vector matrix has three components per pair. Only 50 source-index rows cross to the browser at a time. Native block mode may retain temporary disk output; coordinate/center preparation and full results still have their native RAM costs. There is no universal RAM bound or cancellation.';}
    if(angular){q('purpose').textContent=parameters.task==='angles'?'Calculate native angles for ordered atom triplets; the middle atom is the vertex. No bonds or chemistry are inferred.':'Calculate signed native torsions for ordered atom quartets. Atom order determines the convention; no named chemical dihedrals are inferred.';q('pair-scope').textContent='Enter a JSON list of source atom-index tuples. Tuple order and repeated tuples are retained in every requested structure. Native undefined observations are displayed as undefined, not repaired.';q('resources').textContent='Only 50 observations cross to the browser at a time. The native angular API currently gathers selected coordinates and returns the complete angular array in memory; this panel adds no out-of-core or universal RAM guarantee. Prefer a small explicit structure scope for large systems.';}
    const sceneSource=(angular?[]:[draft,...(between?[second]:[])]).some(d=>['current','saved','region'].includes(d.source))&&context.state!=='synchronized';
    q('calculate').disabled=busy||!context.can_calculate||(!angular&&draft.source==='none')||(between&&second.source==='none')||sceneSource;
    q('calculate').textContent=busy&&pendingAction==='calculate'?'Calculating…':'Calculate';q('refresh').disabled=busy;q('clear').hidden=!report;q('clear').disabled=busy;
    for(const input of el.querySelectorAll('input,select,textarea'))input.disabled=busy;
    q('status').textContent=sceneNotice||message||(sceneSource?'Update the scene before using its selection or regions.':['pending','sync_failed'].includes(context.state)?'The scene update is pending. This calculation reads current molecular data; use Update view to synchronize the scene.':'');
    const chosen=!!report&&!!selectedRow&&selectedRow.id===report.id;
    for(const [key,action] of [['select-participants','select_participants'],['focus-participants','focus_participants'],['add-live-distance','add_live_distance']])q(key).disabled=busy||!chosen||context.state!=='synchronized'||(action==='add_live_distance'&&!!report?.live_distance_unavailable);
    q('add-live-distance').textContent=busy&&pendingAction==='add_live_distance'?'Adding live distance…':'Add live distance';
    q('add-live-distance').hidden=conformation||angular||vector;q('live-distance-limit').hidden=conformation||angular||vector||!report?.live_distance_unavailable;q('live-distance-limit').textContent=report?.live_distance_unavailable||'';
    q('plot-actions').hidden=!conformation||!report;q('add-structure-plot').disabled=busy||!report||context.state!=='synchronized'||!!report?.plot_unavailable;q('plot-limit').textContent=report?.plot_unavailable||'A core trajectory plot links one evaluated value to each loaded structure. It remains after clearing this report.';
    q('scene-help').textContent=conformation?'Choose a result row to select or focus its analyzed atoms. RMSF rows refer to one atom averaged across the stated structures. Focus uses the visible structure without navigating or fitting it. Deliberately added plots belong to core Plots; clicking a point navigates the corresponding structure.':'Choose a result row to use its participants in the scene. Focus and live distances use the visible structure; they do not navigate to the calculated structure. A live distance follows the loaded trajectory.';
    if(angular||vector)q('scene-help').textContent='Choose a result row to select or focus its actual participant atoms in the visible structure. These actions do not navigate to the observation structure or change molecular data. No live distance, vector arrow, angular Measure or plot is created.';
    q('report').hidden=!report;
    if(report){
      q('report-heading').textContent=headings[parameters.task]+' result';q('report-summary').textContent=conformation?`${report.rows.toLocaleString()} ${report.result_axis==='atom'?'atom':'structure'} values · ${report.first_atoms.toLocaleString()} atom occurrences · structure indices ${report.structure_indices.join(', ')}${report.structures_truncated?'…':''}${report.reference_structure_index===null?'':` · reference structure ${report.reference_structure_index}`}.`:`${report.rows.toLocaleString()} ${report.rows===1?'row':'rows'} · ${report.first_atoms.toLocaleString()} first-population ${report.first_atoms===1?'atom':'atoms'} · ${report.second_atoms.toLocaleString()} second-population ${report.second_atoms===1?'atom':'atoms'} · ${report.structure_count===1?'structure':'structures'} ${report.structure_indices.join(', ')}${report.structures_truncated?'…':''}.`;
      q('periodicity').textContent=conformation?'Nonperiodic stored-coordinate analysis; no molecular or scene changes.':report.periodic?'Periodic minimum-image distances requested with a stored box.':report.requested_pbc?'Periodic distances were requested, but no stored box is available. Native nonperiodic distances are shown.':'Nonperiodic distances.';
      q('provenance').textContent=`${report.method} · MolSysMT ${report.software.molsysmt} · molecular revision ${report.source_revision}${report.disk_backed?' · native temporary disk storage':''}.`;
      q('lifetime').textContent=conformation?'Values are displayed in nm with nine significant digits. Python retains full native precision/units. RMSD reference pairing follows supplied order; optimal-superposition RMSD does not fit the source. RMSF is atom-indexed and does not align its input. This mounted report expires on changed inputs/source or unmount; raw external writes are not observed. Calculation does not store a generic result in H5MSM. Core plots are separate scene objects and remain after Clear.':'Atom and structure indices refer to the source system. Centers retain their stated populations. Distances are displayed in nm with nine significant digits; Python returns full native values. Clear, changed inputs/source or leaving this mounted panel releases its result and temporary storage. Raw external edits are not observed. Calculation does not change the scene or store this result in H5MSM. Deliberately added live distances remain in core Measures.';
      if(angular||vector){
        if(angular)q('report-summary').textContent=`${report.rows.toLocaleString()} angular observations · ${report.tuple_count} ordered tuples · structure indices ${report.structure_indices.join(', ')}${report.structures_truncated?'…':''}.`;
        q('periodicity').textContent=report.periodic?'Periodic minimum-image geometry with a stored box.':report.requested_pbc?'Periodic geometry was requested without a stored box. Native nonperiodic geometry is shown.':'Nonperiodic geometry.';
        q('lifetime').textContent=(angular?`Angles are displayed in ${report.unit}. Undefined native values remain undefined; they are not zero observations. `:'Vectors point from first to second endpoint; Cartesian X/Y/Z are displayed in nm. Centers use supplied coordinates, without reconstructing split periodic molecules. ')+ 'The browser shows nine significant digits; Python retains complete native values and units. Source/tuple/structure order is preserved. This mounted result expires on changed inputs/source or unmount. Raw external writes are not observed. Calculation neither edits molecular data nor stores the report or geometry in H5MSM.';
      }
      if(page){const tr=document.createElement('tr');tr.append(cell('th','Choose'),...page.columns.map(x=>cell('th',x)));q('columns').replaceChildren(tr);q('rows').replaceChildren(...page.rows.map((values,index)=>{
        const row=document.createElement('tr'),choice=document.createElement('th'),radio=document.createElement('input'),position=page.offset+index;
        choice.scope='row';radio.type='radio';radio.name='analysis-row-'+report.id;radio.dataset.resultRow=String(position);radio.setAttribute('aria-label',`Select result row ${position+1}`);radio.checked=chosen&&selectedRow.index===position;radio.disabled=busy||context.state!=='synchronized';
        choice.append(radio);row.append(choice,...values.map(x=>cell('td',x)));return row;
      }));q('page-summary').textContent=page.total?`Rows ${page.offset+1}–${page.offset+page.rows.length} of ${page.total.toLocaleString()}.`:'No matching neighbors in the evaluated scope.';q('pagination').hidden=page.total<=page.page_size;q('previous').disabled=busy||!page.offset;q('next').disabled=busy||page.offset+page.rows.length>=page.total;}
    }
  }
  function changed(){const previous=report;stamp++;report=null;page=null;selectedRow=null;sceneNotice='';message='';model.set('analysis_selection',{...draft});model.set('analysis_selection_2',{...second});model.set('analysis_parameters',{...parameters});
    // Release a potentially large previous result on the first input change.
    // This housekeeping request must not disable typing or restore older inputs.
    if(previous){retirement=++sequence;model.send({type:'action',id:'clear',payload:{request_id:retirement,draft:{...draft},second:{...second},parameters:{...parameters}}});}
    render();}
  function request(action,extra={}){if(busy)return;busy=true;pendingAction=action;sequence++;requestStamp=stamp;if(sceneActions.has(action)){sceneRequest=sequence;sceneNotice='';}else if(action!=='refresh')sceneNotice='';render();model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},second:{...second},parameters:{...parameters},...extra}});}
  q('task').addEventListener('change',()=>{parameters.task=q('task').value;if(parameters.task==='neighbors')parameters.pairing='cartesian';changed();request('task');},options);
  for(const [key,name,event] of [['relation','relation','change'],['first-endpoint','first_endpoint','change'],['second-endpoint','second_endpoint','change'],['pairing','pairing','change'],['structures','structures','change'],['structure-indices','indices','input'],['neighbor-mode','neighbor_mode','change'],['cutoff','cutoff','input'],['cutoff-unit','cutoff_unit','change'],['count','count','input']])q(key).addEventListener(event,()=>{parameters[name]=q(key).value;if(name==='relation'&&parameters.relation==='within')parameters.pairing='cartesian';changed();},options);
  q('atom-tuples').addEventListener('input',()=>{parameters.atom_tuples=q('atom-tuples').value;changed();},options);
  q('angle-unit').addEventListener('change',()=>{parameters.angle_unit=q('angle-unit').value;changed();},options);
  q('angular-pbc').addEventListener('change',()=>{parameters.pbc=q('angular-pbc').checked;changed();},options);
  q('pbc').addEventListener('change',()=>{parameters.pbc=q('pbc').checked;changed();},options);
  for(const [key,name,event] of [['reference-structure','reference_structure','input'],['reference-population','reference_population','change'],['weighting','weighting','change']])q(key).addEventListener(event,()=>{parameters[name]=q(key).value;changed();},options);
  q('add-structure-plot').addEventListener('click',()=>{if(report)request('add_structure_plot',{report_id:report.id});},options);
  for(const [key,action] of [['calculate','calculate'],['refresh','refresh'],['clear','clear']])q(key).addEventListener('click',()=>request(action),options);
  q('rows').addEventListener('change',event=>{
    const radio=event.target.closest('input[data-result-row]');
    if(!radio||!report||busy||context.state!=='synchronized')return;
    const index=Number(radio.dataset.resultRow);selectedRow={id:report.id,index};sceneNotice='';render();
    q('rows').querySelector(`[data-result-row="${index}"]`)?.focus({preventScroll:true});
  },options);
  q('previous').addEventListener('click',()=>{selectedRow=null;request('page',{report_id:report.id,offset:page.offset-page.page_size});},options);
  q('next').addEventListener('click',()=>{selectedRow=null;request('page',{report_id:report.id,offset:page.offset+page.page_size});},options);
  for(const [key,action] of [['select-participants','select_participants'],['focus-participants','focus_participants'],['add-live-distance','add_live_distance']])q(key).addEventListener('click',()=>{if(selectedRow&&report)request(action,{report_id:report.id,row_index:selectedRow.index});},options);
  function onState(msg){
    if(msg?.type!=='state'||typeof msg.state?.request_id!=='number')return;
    const s=msg.state;
    if(retirement&&s.request_id===retirement){retirement=0;if(s.stage==='error')message=s.message||'Could not release the previous result.';render();return;}
    if(s.request_id<sequence)return;
    // A scene selection can change context before its acknowledgement arrives.
    // Preserve only that action's notice, then refresh without restoring stale drafts.
    if(sceneRequest===s.request_id){sceneNotice=s.message||'';sceneRequest=0;}
    if(requestStamp!==stamp){busy=false;pendingAction='';request('refresh');return;}
    busy=false;pendingAction='';draft={...initial,...s.draft};second={...initial,...s.second};parameters={...defaults,...s.parameters};context=s.context||{};keepRow(s.report||null,s.page||null);message=s.message||'';render();if(report&&s.stage==='report')q('report-heading').focus();
  }
  function onContext(){stamp++;report=null;page=null;if(!busy&&context.can_calculate)request('refresh');else render();}
  function onSync(status){stamp++;sequence++;busy=false;pendingAction='';sceneRequest=0;sceneNotice='';report=null;page=null;selectedRow=null;context={...context,...status,can_calculate:!!context.has_system&&context.n_structures>0&&['synchronized','pending','sync_failed'].includes(status.state)};if(context.can_calculate)request('refresh');else render();}
  model.on('msg:custom',onState);model.on('viewer:frame-changed',onContext);model.on('viewer:selection-changed',onContext);model.on('viewer:system-sync-changed',onSync);render();
  return()=>{abort.abort();model.off('msg:custom',onState);model.off('viewer:frame-changed',onContext);model.off('viewer:selection-changed',onContext);model.off('viewer:system-sync-changed',onSync);report=null;page=null;el.replaceChildren();};
}
"""
)
ESM = ESM.replace("__SELECTION_EDITOR__", SELECTION_MARKUP)

CSS = r"""
.msm-analysis textarea{width:100%;box-sizing:border-box;min-height:74px;font:inherit;color:inherit;background:transparent;border:1px solid #596473;border-radius:4px;padding:6px}
.msm-analysis [data-report]{display:flex;flex-direction:column;gap:12px}
.msm-analysis details[data-first],.msm-analysis details[data-second]{border:1px solid #596473;border-radius:7px;padding:9px}
.msm-analysis .msm-checkbox{display:flex;flex-direction:row;align-items:center;gap:8px}.msm-analysis .msm-checkbox input{width:auto}
.msm-analysis .msm-table-scroll{max-width:100%;overflow:auto}
.msm-analysis table{width:100%;border-collapse:collapse;font-size:12px;text-align:left}
.msm-analysis th,.msm-analysis td{padding:5px 7px;border-bottom:1px solid #596473;overflow-wrap:anywhere;vertical-align:top}
.msm-analysis input[type="radio"]{width:auto;min-width:0}
"""
