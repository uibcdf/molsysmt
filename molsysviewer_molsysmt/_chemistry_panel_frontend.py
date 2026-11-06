"""Calm read-only chemistry reports with bounded, explicit source-index pages."""

from ._panel_widgets import SELECTION_MARKUP, SHARED_JS

ESM = (
    SHARED_JS
    + r"""
export function render({model,el}) {
  const abort=new AbortController(),options={signal:abort.signal};
  const initial={source:'none',value:'',expression:'',indices:'',context:'current',structure_index:0};
  const defaults={task:'chemistry',state_mode:'reference',state_index:'0'};
  let draft={...initial,...model.get('chemistry_selection')},parameters={...defaults,...model.get('chemistry_parameters')};
  let context={},report=null,page=null,busy=false,sequence=0,stamp=0,requestStamp=0,message='';
  const labels={atom_type:'Element',atom_id:'Atom ID',isotope:'Isotope',formal_charge:'Formal charge',atom_is_aromatic:'Atom aromaticity',n_unpaired_electrons:'Unpaired electrons',n_implicit_hydrogens:'Stored implicit H count',n_explicit_hydrogens:'Stored explicit H count',allows_implicit_hydrogens:'Implicit H permission',atom_stereochemistry:'Atom stereochemistry',bond_id:'Bond ID',bond_type:'Bond type',bond_order:'Bond order',bond_is_aromatic:'Bond aromaticity',bond_stereochemistry:'Bond stereochemistry',covalent_multiplicity:'Covalent multiplicity',coordinates:'Coordinates'};
  const label=name=>labels[name]||String(name).replaceAll('_',' ');
  el.innerHTML=`<section class="msm-system msm-chemistry" aria-label="Molecular chemistry tools">
    <label>Chemistry task<select data-task aria-label="Chemistry task"><option value="chemistry">Inspect stored chemistry</option><option value="hydrogens">Hydrogen inventory</option></select></label>
    <h2 data-heading>Inspect stored chemistry</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint" data-purpose></p>
    __SELECTION_EDITOR__
    <p class="msm-hint">The report uses the structure chosen in Selection context. One structure is inspected; other structures are not assessed.</p>
    <details><summary>Chemical state</summary>
      <label>Inspect chemical state<select data-state-mode aria-label="Inspect chemical state"><option value="reference">Reference state</option><option value="structure">State associated with the chosen structure</option><option value="index">State index</option></select></label>
      <label data-state-index-label hidden>Chemical state index<input data-state-index aria-label="Chemical state index" inputmode="numeric" maxlength="64"></label>
      <p class="msm-hint">Selections use the reference state. The report inspects these fixed atoms in the state chosen here. An absent or ambiguous state remains unassessed.</p>
    </details>
    <div class="msm-actions"><button data-inspect>Inspect chemistry</button><button data-refresh>Refresh</button><button data-clear hidden>Clear report</button></div>
    <p class="msm-status" role="status" aria-live="polite" data-status></p>
    <section data-report hidden aria-label="Chemistry report">
      <h3 data-report-heading tabindex="-1"></h3><button data-change-inspection>Change inspection</button><p data-report-scope></p><p class="msm-hint" data-state-summary></p>
      <p data-inventory-status></p><p class="msm-hint" data-count-convention></p><p class="msm-hint" data-connectivity></p>
      <details data-fields-section open><summary>Stored information</summary><div class="msm-table-scroll"><table><thead><tr><th>Field</th><th>Coverage</th><th>Present / total</th></tr></thead><tbody data-fields></tbody></table></div><p class="msm-hint">Presence describes stored information, not independent chemical validation. Partial, missing, unsupported and conflicting values remain distinct in the details.</p></details>
      <details data-issues-section open hidden><summary>Inventory issues</summary><ul data-issue-counts></ul></details>
      <details data-details><summary>Inspect source indices and values</summary>
        <label>Report table<select data-dataset aria-label="Report table"></select></label><p class="msm-hint" data-page-unit></p>
        <div class="msm-table-scroll"><table><thead data-columns></thead><tbody data-rows></tbody></table></div>
        <p class="msm-hint" data-page-summary></p><div class="msm-actions"><button data-previous>Previous page</button><button data-next>Next page</button></div>
        <p class="msm-hint">Indices refer to the source system. Long labels are shortened to 200 characters. The Python API returns the full native report.</p>
      </details>
      <details><summary>What was not assessed</summary><ul data-unassessed></ul><p class="msm-hint">This report does not prepare the system or certify readiness for a later calculation.</p></details>
      <details><summary>Report provenance and lifetime</summary><p data-provenance></p><p class="msm-hint">Only this mounted panel keeps the report in memory. Changing its inputs, source revision or structure context expires it. Clear report releases it; it does not delete molecular data. Reports are not stored in the scene or H5MSM.</p></details>
    </section>
  </section>`;
  const q=key=>el.querySelector(`[data-${key}]`);
  const whole=document.createElement('option');whole.value='all';whole.textContent='Whole system';q('source').options.add(whole,1);
  const renderSelection=selectionEditor(el,options,patch=>{Object.assign(draft,patch);changed();});
  function cell(tag,value){const node=document.createElement(tag);node.textContent=String(value);return node;}
  function tableRows(target,rows){target.replaceChildren(...rows.map(values=>{const tr=document.createElement('tr');tr.append(...values.map(x=>cell('td',x)));return tr;}));}
  function list(target,values){target.replaceChildren(...values.map(x=>cell('li',x)));}
  function render(){
    const hydrogen=parameters.task==='hydrogens';renderSelection(draft,context);
    q('task').value=parameters.task;q('heading').textContent=hydrogen?'Hydrogen inventory':'Inspect stored chemistry';
    q('purpose').textContent=hydrogen?'Inspect indexed hydrogen neighbors and separately stored hydrogen counts, without adding or removing atoms.':'Inspect stored atom, bond and coordinate information without completing or repairing chemistry.';
    q('context').textContent=!context.has_system?'Load a system in Studio > Load first.':context.n_atoms!==undefined?`${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} structures`:'Molecular data need explicit recovery.';
    q('state-mode').value=parameters.state_mode;q('state-index-label').hidden=parameters.state_mode!=='index';if(document.activeElement!==q('state-index'))q('state-index').value=parameters.state_index;
    const sceneSource=['current','saved','region'].includes(draft.source)&&context.state!=='synchronized';
    q('inspect').disabled=busy||!context.can_inspect||draft.source==='none'||sceneSource;
    q('inspect').textContent=busy?'Working…':hydrogen?'Inspect hydrogens':'Inspect chemistry';q('refresh').disabled=busy;q('clear').hidden=!report;q('clear').disabled=busy;
    for(const input of el.querySelectorAll('input,select'))input.disabled=busy;
    q('status').textContent=message||(sceneSource?'Update the scene before using its selection or regions.':['pending','sync_failed'].includes(context.state)?'The scene update is pending. Inspection reads the current molecular data; use Update view to synchronize the scene.':'');
    q('report').hidden=!report;
    if(report){
      q('report-heading').textContent=hydrogen?'Hydrogen inventory report':'Stored chemistry report';
      q('report-scope').textContent=`${report.n_atoms.toLocaleString()} selected atoms · ${report.structure_index===null?'no coordinate structures':`structure ${report.structure_index}`} · ${report.explicit_hydrogens.toLocaleString()} selected explicit H atoms`;
      q('state-summary').textContent=`Chemical state: ${report.chemical_state_index===null?'unresolved':report.chemical_state_index}${report.chemical_state_status?' · '+report.chemical_state_status:''}.`;
      q('inventory-status').textContent=hydrogen?'Native inventory status: '+report.status+'.':'';
      q('count-convention').textContent=hydrogen?report.count_convention:'';
      const c=report.connectivity;
      q('connectivity').textContent=c?`Declared connectivity: ${c.declared_completeness}. ${c.incident_bonds.toLocaleString()} bonds touch the selected atoms; ${c.crossing_bonds.toLocaleString()} cross the selection. Whole-state check: ${c.invalid_bonds.toLocaleString()} invalid/duplicate bonds among ${c.examined_bonds.toLocaleString()} examined bonds.`:'';
      q('fields-section').hidden=hydrogen;q('issues-section').hidden=!hydrogen;
      tableRows(q('fields'),(report.fields||[]).map(f=>[label(f.name)+(f.unit?' ('+f.unit+')':''),f.status,`${f.present} / ${f.total}`]));
      list(q('issue-counts'),(report.issue_counts||[]).map(x=>`${label(x.reason)}: ${x.count}`));
      list(q('unassessed'),report.unassessed_checks.map(label));
      q('provenance').textContent=`${report.method} · ${report.schema} · ${Object.entries(report.software).map(([k,v])=>k+' '+v).join(', ')} · molecular revision ${report.source_revision}.`;
      const selected=page?.dataset;
      q('dataset').replaceChildren(...report.datasets.map(d=>{const o=document.createElement('option');o.value=d.id;o.textContent=labels[d.id]||d.label;return o;}));q('dataset').value=selected;
      if(page){
        const tr=document.createElement('tr');tr.append(...page.columns.map(name=>cell('th',name)));q('columns').replaceChildren(tr);tableRows(q('rows'),page.rows);
        q('page-summary').textContent=page.total?`Rows ${page.offset+1}–${page.offset+page.rows.length} of ${page.total.toLocaleString()}.`:'No rows in this source population.';
        q('page-unit').textContent=page.unit?(page.dataset==='coordinates'?'Coordinate values are finite-position flags; source coordinates are assessed in nm.':'Declared unit: '+page.unit+'.'):'';
        q('previous').disabled=busy||!page.offset;q('next').disabled=busy||page.offset+page.rows.length>=page.total;
      }
    }
  }
  function changed(){stamp++;report=null;page=null;message='';model.set('chemistry_selection',{...draft});model.set('chemistry_parameters',{...parameters});render();}
  function request(action,extra={}){if(busy)return;busy=true;sequence++;requestStamp=stamp;render();model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},parameters:{...parameters},...extra}});}
  q('task').addEventListener('change',()=>{parameters.task=q('task').value;changed();request('task');},options);
  q('state-mode').addEventListener('change',()=>{parameters.state_mode=q('state-mode').value;changed();},options);
  q('state-index').addEventListener('input',()=>{parameters.state_index=q('state-index').value;changed();},options);
  q('change-inspection').addEventListener('click',()=>q('source').focus(),options);
  for(const [key,action] of [['inspect','inspect'],['refresh','refresh'],['clear','clear']])q(key).addEventListener('click',()=>request(action),options);
  function turn(dataset,offset){if(report)request('page',{report_id:report.id,dataset,offset});}
  q('dataset').addEventListener('change',()=>turn(q('dataset').value,0),options);
  q('previous').addEventListener('click',()=>turn(page.dataset,page.offset-page.page_size),options);
  q('next').addEventListener('click',()=>turn(page.dataset,page.offset+page.page_size),options);
  function onState(msg){
    if(msg?.type!=='state'||typeof msg.state?.request_id!=='number'||msg.state.request_id<sequence)return;
    if(requestStamp!==stamp){busy=false;request('refresh');return;}
    const state=msg.state;busy=false;draft={...initial,...state.draft};parameters={...defaults,...state.parameters};context=state.context||{};report=state.report||null;page=state.page||null;message=state.message||'';render();
    if(report&&state.stage==='report')q('report-heading').focus();
  }
  function onContext(){stamp++;report=null;page=null;if(!busy)request('refresh');else render();}
  function onSync(status){
    stamp++;report=null;page=null;context={...context,...status,can_inspect:!!context.has_system&&['synchronized','pending','sync_failed'].includes(status.state)};
    if(!busy)request('refresh');else render();
  }
  model.on('msg:custom',onState);model.on('viewer:frame-changed',onContext);model.on('viewer:selection-changed',onContext);model.on('viewer:system-sync-changed',onSync);
  render();return()=>{abort.abort();model.off('msg:custom',onState);model.off('viewer:frame-changed',onContext);model.off('viewer:selection-changed',onContext);model.off('viewer:system-sync-changed',onSync);report=null;page=null;el.replaceChildren();};
}
"""
)
ESM = ESM.replace("__SELECTION_EDITOR__", SELECTION_MARKUP)

CSS = r"""
.msm-chemistry [data-report]{display:flex;flex-direction:column;gap:12px}
.msm-chemistry .msm-table-scroll{max-width:100%;overflow:auto;margin-top:8px}
.msm-chemistry table{width:100%;border-collapse:collapse;font-size:12px;text-align:left}
.msm-chemistry th,.msm-chemistry td{padding:5px 7px;border-bottom:1px solid #596473;overflow-wrap:anywhere;vertical-align:top}
.msm-chemistry th{font-weight:600}.msm-chemistry ul{padding-left:20px;margin:8px 0}
"""
