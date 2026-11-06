"""Explicit populations and bounded native distance-family reports."""

from ._panel_widgets import SELECTION_MARKUP, SHARED_JS

ESM = (
    SHARED_JS
    + r"""
export function render({model,el}) {
  const abort=new AbortController(),options={signal:abort.signal};
  const initial={source:'none',value:'',expression:'',indices:'',context:'current',structure_index:0};
  const defaults={task:'distances',relation:'between',pairing:'cartesian',first_endpoint:'atoms',second_endpoint:'atoms',structures:'current',indices:'',pbc:false,neighbor_mode:'cutoff',cutoff:'0.35',cutoff_unit:'nm',count:'5'};
  let draft={...initial,...model.get('analysis_selection')},second={...initial,...model.get('analysis_selection_2')},parameters={...defaults,...model.get('analysis_parameters')};
  let context={},report=null,page=null,busy=false,sequence=0,stamp=0,requestStamp=0,message='',retirement=0;
  const headings={distances:'Distances',minimum:'Minimum distance',maximum:'Maximum distance',neighbors:'Neighbor search'};
  el.innerHTML=`<section class="msm-system msm-analysis" aria-label="Molecular analysis tools">
    <label>Analysis task<select data-task aria-label="Analysis task"><option value="distances">Distances</option><option value="minimum">Minimum distance</option><option value="maximum">Maximum distance</option><option value="neighbors">Neighbor search</option></select></label>
    <h2 data-heading>Distances</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint" data-purpose></p>
    <label>Populations<select data-relation aria-label="Analysis populations"><option value="between">Between two populations</option><option value="within">Within one population</option></select></label>
    <details data-first open><summary>First population</summary>__SELECTION_EDITOR__</details>
    <details data-second open><summary>Second population</summary>__SELECTION_EDITOR__</details>
    <p class="msm-hint">Each selection is resolved in its stated reference-state context. Those fixed atoms are used in every requested structure; this is not a different selection in each structure.</p>
    <details><summary>Endpoints and calculation settings</summary>
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
    <details><summary>Calculation size and resources</summary><p class="msm-hint">A full distance matrix grows as structures × first endpoints × second endpoints. Only 50 rows are sent to the browser at a time. Native calculation, coordinates and indexing may still need substantial memory. Flat distance matrices request MolSysMT block mode and may use temporary disk storage; centers, corresponding pairs, extrema and nearest-count searches retain their native resource behavior. There is no universal RAM limit or cancellation contract in this panel.</p></details>
    <div class="msm-actions"><button data-calculate>Calculate</button><button data-refresh>Refresh</button><button data-clear hidden>Clear result</button></div>
    <p class="msm-status" role="status" aria-live="polite" data-status></p>
    <section data-report hidden aria-label="Analysis result"><h3 data-report-heading tabindex="-1"></h3><p data-report-summary></p><p class="msm-hint" data-periodicity></p>
      <div class="msm-table-scroll"><table><thead data-columns></thead><tbody data-rows></tbody></table></div>
      <p class="msm-hint" data-page-summary></p><div class="msm-actions"><button data-previous>Previous page</button><button data-next>Next page</button></div>
      <details><summary>Method, source and result lifetime</summary><p data-provenance></p><p class="msm-hint">Atom and structure indices refer to the source system. Centers refer to the stated populations, not invented atom indices. Distances are displayed in nm with nine significant digits; Python returns the full native values. This mounted panel keeps the result, including any native temporary storage. Clear, changed inputs/source or leaving the panel releases it. Raw external edits are not automatically observed. Results do not change the scene and are not stored automatically in H5MSM.</p></details>
    </section>
  </section>`;
  const q=key=>el.querySelector(`[data-${key}]`);
  for(const key of ['first','second']){const select=q(key).querySelector('[data-source]');const option=document.createElement('option');option.value='all';option.textContent='Whole system';select.options.add(option,1);}
  const firstEditor=selectionEditor(q('first'),options,patch=>{Object.assign(draft,patch);changed();});
  const secondEditor=selectionEditor(q('second'),options,patch=>{Object.assign(second,patch);changed();});
  function cell(tag,value){const node=document.createElement(tag);node.textContent=String(value);return node;}
  function render(){
    const between=parameters.relation==='between',neighbors=parameters.task==='neighbors';
    q('task').value=parameters.task;q('heading').textContent=headings[parameters.task];
    q('purpose').textContent=neighbors?'Find neighboring endpoints in each chosen structure, keeping zero matches distinct from an uncalculated result.':parameters.task==='minimum'?'Find the closest pair in each chosen structure. Ties keep the first local pair in native order.':parameters.task==='maximum'?'Find the farthest pair in each chosen structure. Ties keep the first local pair in native order.':'Calculate distances between the chosen endpoints without changing coordinates or the scene.';
    q('context').textContent=!context.has_system?'Load a system in Studio > Load first.':context.n_atoms!==undefined?`${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} structures`:'Molecular data need explicit recovery.';
    firstEditor(draft,context);secondEditor(second,context);q('second').hidden=!between;
    q('relation').value=parameters.relation;q('first-endpoint').value=parameters.first_endpoint;q('second-endpoint').value=parameters.second_endpoint;q('second-endpoint-label').hidden=!between;
    q('pairing-label').hidden=neighbors||!between;q('pairing').value=parameters.pairing;q('pbc').checked=parameters.pbc;
    q('structures').value=parameters.structures;q('structure-indices-label').hidden=parameters.structures!=='indices';
    q('neighbor-settings').hidden=!neighbors;q('neighbor-mode').value=parameters.neighbor_mode;q('cutoff-settings').hidden=parameters.neighbor_mode!=='cutoff';q('count-label').hidden=parameters.neighbor_mode!=='count';q('cutoff-unit').value=parameters.cutoff_unit;
    for(const [key,value] of [['structure-indices',parameters.indices],['cutoff',parameters.cutoff],['count',parameters.count]])if(document.activeElement!==q(key))q(key).value=value;
    q('pair-scope').textContent=neighbors?(between?'The explicit target population can include the query atoms; zero-distance matches are retained.':'Within one population, native self matches are excluded. Neighbor rows are directed and sorted by distance; local tie order is preserved.'):between?(parameters.pairing==='paired'?'Corresponding endpoints require equal counts. Atom order and repeated occurrences are preserved.':'The Cartesian product includes every first/second endpoint pair, including overlaps.'):'The full within-population matrix includes self distances and both directions. These are numerical pairs, not unique physical interactions.';
    const sceneSource=[draft,...(between?[second]:[])].some(d=>['current','saved','region'].includes(d.source))&&context.state!=='synchronized';
    q('calculate').disabled=busy||!context.can_calculate||draft.source==='none'||(between&&second.source==='none')||sceneSource;
    q('calculate').textContent=busy?'Calculating…':'Calculate';q('refresh').disabled=busy;q('clear').hidden=!report;q('clear').disabled=busy;
    for(const input of el.querySelectorAll('input,select'))input.disabled=busy;
    q('status').textContent=message||(sceneSource?'Update the scene before using its selection or regions.':['pending','sync_failed'].includes(context.state)?'The scene update is pending. This calculation reads current molecular data; use Update view to synchronize the scene.':'');
    q('report').hidden=!report;
    if(report){
      q('report-heading').textContent=headings[parameters.task]+' result';q('report-summary').textContent=`${report.rows.toLocaleString()} ${report.rows===1?'row':'rows'} · ${report.first_atoms.toLocaleString()} first-population ${report.first_atoms===1?'atom':'atoms'} · ${report.second_atoms.toLocaleString()} second-population ${report.second_atoms===1?'atom':'atoms'} · ${report.structure_count===1?'structure':'structures'} ${report.structure_indices.join(', ')}${report.structures_truncated?'…':''}.`;
      q('periodicity').textContent=report.periodic?'Periodic minimum-image distances requested with a stored box.':report.requested_pbc?'Periodic distances were requested, but no stored box is available. Native nonperiodic distances are shown.':'Nonperiodic distances.';
      q('provenance').textContent=`${report.method} · MolSysMT ${report.software.molsysmt} · molecular revision ${report.source_revision}${report.disk_backed?' · native temporary disk storage':''}.`;
      if(page){const tr=document.createElement('tr');tr.append(...page.columns.map(x=>cell('th',x)));q('columns').replaceChildren(tr);q('rows').replaceChildren(...page.rows.map(values=>{const row=document.createElement('tr');row.append(...values.map(x=>cell('td',x)));return row;}));q('page-summary').textContent=page.total?`Rows ${page.offset+1}–${page.offset+page.rows.length} of ${page.total.toLocaleString()}.`:'No matching neighbors in the evaluated scope.';q('previous').disabled=busy||!page.offset;q('next').disabled=busy||page.offset+page.rows.length>=page.total;}
    }
  }
  function changed(){const previous=report;stamp++;report=null;page=null;message='';model.set('analysis_selection',{...draft});model.set('analysis_selection_2',{...second});model.set('analysis_parameters',{...parameters});
    // Release a potentially large previous result on the first input change.
    // This housekeeping request must not disable typing or restore older inputs.
    if(previous){retirement=++sequence;model.send({type:'action',id:'clear',payload:{request_id:retirement,draft:{...draft},second:{...second},parameters:{...parameters}}});}
    render();}
  function request(action,extra={}){if(busy)return;busy=true;sequence++;requestStamp=stamp;render();model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},second:{...second},parameters:{...parameters},...extra}});}
  q('task').addEventListener('change',()=>{parameters.task=q('task').value;if(parameters.task==='neighbors')parameters.pairing='cartesian';changed();request('task');},options);
  for(const [key,name,event] of [['relation','relation','change'],['first-endpoint','first_endpoint','change'],['second-endpoint','second_endpoint','change'],['pairing','pairing','change'],['structures','structures','change'],['structure-indices','indices','input'],['neighbor-mode','neighbor_mode','change'],['cutoff','cutoff','input'],['cutoff-unit','cutoff_unit','change'],['count','count','input']])q(key).addEventListener(event,()=>{parameters[name]=q(key).value;if(name==='relation'&&parameters.relation==='within')parameters.pairing='cartesian';changed();},options);
  q('pbc').addEventListener('change',()=>{parameters.pbc=q('pbc').checked;changed();},options);
  for(const [key,action] of [['calculate','calculate'],['refresh','refresh'],['clear','clear']])q(key).addEventListener('click',()=>request(action),options);
  q('previous').addEventListener('click',()=>request('page',{report_id:report.id,offset:page.offset-page.page_size}),options);
  q('next').addEventListener('click',()=>request('page',{report_id:report.id,offset:page.offset+page.page_size}),options);
  function onState(msg){if(msg?.type!=='state'||typeof msg.state?.request_id!=='number')return;if(retirement&&msg.state.request_id===retirement){retirement=0;if(msg.state.stage==='error')message=msg.state.message||'Could not release the previous result.';render();return;}if(msg.state.request_id<sequence)return;if(requestStamp!==stamp){busy=false;request('refresh');return;}const s=msg.state;busy=false;draft={...initial,...s.draft};second={...initial,...s.second};parameters={...defaults,...s.parameters};context=s.context||{};report=s.report||null;page=s.page||null;message=s.message||'';render();if(report&&s.stage==='report')q('report-heading').focus();}
  function onContext(){stamp++;report=null;page=null;if(!busy&&context.can_calculate)request('refresh');else render();}
  function onSync(status){stamp++;sequence++;busy=false;report=null;page=null;context={...context,...status,can_calculate:!!context.has_system&&context.n_structures>0&&['synchronized','pending','sync_failed'].includes(status.state)};if(context.can_calculate)request('refresh');else render();}
  model.on('msg:custom',onState);model.on('viewer:frame-changed',onContext);model.on('viewer:selection-changed',onContext);model.on('viewer:system-sync-changed',onSync);render();
  return()=>{abort.abort();model.off('msg:custom',onState);model.off('viewer:frame-changed',onContext);model.off('viewer:selection-changed',onContext);model.off('viewer:system-sync-changed',onSync);report=null;page=null;el.replaceChildren();};
}
"""
)
ESM = ESM.replace("__SELECTION_EDITOR__", SELECTION_MARKUP)

CSS = r"""
.msm-analysis [data-report]{display:flex;flex-direction:column;gap:12px}
.msm-analysis details[data-first],.msm-analysis details[data-second]{border:1px solid #596473;border-radius:7px;padding:9px}
.msm-analysis .msm-checkbox{display:flex;flex-direction:row;align-items:center;gap:8px}.msm-analysis .msm-checkbox input{width:auto}
.msm-analysis .msm-table-scroll{max-width:100%;overflow:auto}
.msm-analysis table{width:100%;border-collapse:collapse;font-size:12px;text-align:left}
.msm-analysis th,.msm-analysis td{padding:5px 7px;border-bottom:1px solid #596473;overflow-wrap:anywhere;vertical-align:top}
"""
