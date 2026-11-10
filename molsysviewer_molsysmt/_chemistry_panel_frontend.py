"""Calm read-only chemistry reports with bounded, explicit source-index pages."""

from ._panel_widgets import RESULT_MARKUP, SELECTION_MARKUP, SHARED_JS

ESM = (
    SHARED_JS
    + r"""
export function render({model,el}) {
  const abort=new AbortController(),options={signal:abort.signal};
  const initial={source:'none',value:'',expression:'',indices:'',context:'current',structure_index:0};
  const defaults={task:'chemistry',state_mode:'reference',state_index:'0',hydrogen_mode:'pH',engine:'MolSysMT',pH:'7.4',attribute_policy:'strict',title:'',inference_method:'supported_group_templates',bond_cutoff:'2 angstroms',n_cap:'none',c_cap:'none',keep_ids:'no',charge_method:'gasteiger_marsili',forcefield:'',water_model:'',expected_charge:''};
  let draft={...initial,...model.get('chemistry_selection')},parameters={...defaults,...model.get('chemistry_parameters')};
  let context={},report=null,page=null,busy=false,sequence=0,stamp=0,requestStamp=0,message='',pendingAction='';
  let result=null,replacement=null,canReplace=false,replacementSupported=false,destinations=[],alive=true,protonationReview=null,canApplyProtonation=false,canPrepareProtonation=false;
  const labels={atom_type:'Element',atom_id:'Atom ID',isotope:'Isotope',formal_charge:'Formal charge',atom_is_aromatic:'Atom aromaticity',n_unpaired_electrons:'Unpaired electrons',n_implicit_hydrogens:'Stored implicit H count',n_explicit_hydrogens:'Stored explicit H count',allows_implicit_hydrogens:'Implicit H permission',atom_stereochemistry:'Atom stereochemistry',bond_id:'Bond ID',bond_type:'Bond type',bond_order:'Bond order',bond_is_aromatic:'Bond aromaticity',bond_stereochemistry:'Bond stereochemistry',covalent_multiplicity:'Covalent multiplicity',coordinates:'Coordinates'};
  const label=name=>labels[name]||String(name).replaceAll('_',' ');
  const repairs={
    infer_bonds:{title:'Infer covalent bonds',purpose:'Apply the chosen bounded template and observed-H policy to a separate system.',scope:'Both candidate endpoints must be selected. One chosen structure supplies peptide geometry; all source structures are retained.',limits:'Experimental native template composition; unsupported groups remain excluded. No arbitrary ligand, water, metal or disulfide distance fallback, no inferred bond orders or protonation. Existing declarations are retained; changed connectivity invalidates output interaction coverage.'},
    add_bonds:{title:'Add missing bonds',purpose:'Apply the native group-template and distance heuristic with an explicit cutoff.',scope:'Both endpoints must be selected. The chosen source structure supplies geometry; all source structures are retained.',limits:'MolSysMT legacy distance/template heuristic, distinct from bounded covalent inference. No bond orders or chemical completeness certificate. Inspect the separate result before adoption.'},
    terminal_cappings:{title:'Complete terminal atoms and caps',purpose:'Complete native terminal atoms and optionally attach explicitly named peptide caps.',scope:'Selected atoms identify source peptide/protein components. Native completion may also repair missing heavy atoms. All source structures are retained; indices and IDs may change.',limits:'MolSysMT templates, explicit pH approximation and cap names. No biological-terminus inference or minimization. Native legacy conversion may omit attributes; review diagnostics and the result attribute summary.'},
    remove_hydrogens:{title:'Remove reference-rule hydrogens',purpose:'Remove H atoms inconsistent with the native reference-name inventory and explicit pH approximation.',scope:'Whole system and all structures. The reference rules decide atom removal across the shared axis; the atom editor and chemical-state picker do not choose a population.',limits:'Fixed free-amino-acid pKa rules, not environment-dependent pKa prediction. Unsupported groups remain unassessed, not certified. Deposited hydrogens may be evidence; inspect Assess reference-rule protonation before preparing this separate result.'},
    autodock_types:{title:'Assign AutoDock atom types',purpose:'Attach explicitly named AutoDock4 chemical-environment labels to a separate system.',scope:'Whole system, exactly one nonempty prepared chemical state. Structure-associated state uses the visible frame. All source coordinates and structures are retained.',limits:'Experimental autodock4 / chemical_environment profile, requiring complete graph and H inventory; optional RDKit. No hidden H addition, charge calculation or full force-field parameterization. Mechanical assignments are not stored by H5MSM 0.5.'},
    partial_charges:{title:'Assign partial charges',purpose:'Attach a complete atom-aligned charge assignment using the explicitly chosen model.',scope:'Whole system, exactly one prepared chemical state. Structure-associated state uses the visible frame. The expected total is a full-system declaration, never a selected-fragment charge.',limits:'Gasteiger–Marsili requires prepared chemistry and RDKit; force-field charges require the named model and OpenMM templates. No automatic chemical repair or full parameterization. Existing analyses retain snapshots; recalculate those depending on these parameters. Mechanical assignments are not stored by H5MSM 0.5.'},
  };
  el.innerHTML=`<section class="msm-system msm-chemistry" aria-label="Molecular chemistry tools">
    <label>Chemistry task<select data-task aria-label="Chemistry task"><optgroup label="Inspect"><option value="chemistry">Inspect stored chemistry</option><option value="hydrogens">Hydrogen inventory</option><option value="coverage">Assess exact-template coverage</option><option value="terminals">Inspect missing terminal atoms</option><option value="protonation">Assess reference-rule protonation</option></optgroup><optgroup label="Prepare a separate system"><option value="heavy">Add missing heavy atoms</option><option value="add_hydrogens">Add missing hydrogens</option><option value="infer_bonds">Infer covalent bonds</option><option value="add_bonds">Add missing bonds</option><option value="terminal_cappings">Complete terminal atoms and caps</option><option value="remove_hydrogens">Remove reference-rule hydrogens</option><option value="autodock_types">Assign AutoDock atom types</option><option value="partial_charges">Assign partial charges</option></optgroup></select></label>
    <h2 data-heading>Inspect stored chemistry</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint" data-purpose></p>
    __SELECTION_EDITOR__
    <p class="msm-hint" data-scope>The report uses the structure chosen in Selection context. One structure is inspected; other structures are not assessed.</p>
    <details data-chemical-state><summary>Chemical state</summary>
      <label>Inspect chemical state<select data-state-mode aria-label="Inspect chemical state"><option value="reference">Reference state</option><option value="structure">State associated with the chosen structure</option><option value="index">State index</option></select></label>
      <label data-state-index-label hidden>Chemical state index<input data-state-index aria-label="Chemical state index" inputmode="numeric" maxlength="64"></label>
      <p class="msm-hint">Selections use the reference state. The report inspects these fixed atoms in the state chosen here. An absent or ambiguous state remains unassessed.</p>
    </details>
    <label data-assessment-ph-label hidden>Assessment pH<input data-assessment-ph aria-label="Assessment pH" inputmode="decimal" maxlength="64"></label>
    <div data-preparation hidden>
      <label data-hydrogen-mode-label>Hydrogen method<select data-hydrogen-mode aria-label="Hydrogen method"><option value="pH">Template-based pH approximation</option><option value="fixed_chemical_state">Prepared chemical state (RDKit)</option></select></label>
      <label data-engine-label>Engine<select data-engine aria-label="Preparation engine"><option value="MolSysMT">MolSysMT</option><option value="PDBFixer">PDBFixer (optional)</option><option value="OpenMM">OpenMM (optional)</option></select></label>
      <label data-ph-label>pH<input data-ph aria-label="Preparation pH" inputmode="decimal" maxlength="64"></label>
      <label data-attribute-label>Attributes without values for new atoms<select data-attribute-policy aria-label="Preparation attribute policy"><option value="strict">Stop if attributes would be lost</option><option value="intersection">Allow omission with native diagnostics</option></select></label>
      <label data-inference-method-label hidden>Inference method<select data-inference-method aria-label="Covalent inference method"><option value="supported_group_templates">Supported group templates · exact H names</option><option value="supported_group_templates_with_hydrogen_aliases">Supported group templates · explicit H-name aliases</option></select></label>
      <label data-bond-cutoff-label hidden>Maximum bond distance (include length unit)<input data-bond-cutoff aria-label="Maximum bond distance" maxlength="128"></label>
      <div data-capping-fields hidden><label>N-terminal cap<select data-n-cap aria-label="N-terminal cap"><option value="none">No added cap · complete terminal atoms</option><option value="ACE">ACE</option></select></label><label>C-terminal cap<select data-c-cap aria-label="C-terminal cap"><option value="none">No added cap · complete terminal atoms</option><option value="NME">NME</option><option value="NHE">NHE</option><option value="NH2">NH2</option></select></label><label>Native ID policy<select data-keep-ids aria-label="Capping ID policy"><option value="no">Regenerate IDs</option><option value="yes">Retain native IDs</option></select></label></div>
      <div data-charge-fields hidden><label>Charge model<select data-charge-method aria-label="Charge model"><option value="gasteiger_marsili">Gasteiger–Marsili · RDKit</option><option value="forcefield">Named force field · OpenMM</option></select></label><label data-forcefield-label>Force field<input data-forcefield aria-label="Charge force field" maxlength="200" placeholder="Required for force-field charges"></label><label data-water-model-label>Water model<input data-water-model aria-label="Charge water model" maxlength="200" placeholder="Optional named water templates"></label><label>Expected whole-system charge (elementary charge)<input data-expected-charge aria-label="Expected whole-system charge" maxlength="64" placeholder="Integer; leave empty to use complete formal charges"></label></div>
      <p class="msm-hint" data-preparation-limits></p>
      <label>Result name<input data-preparation-title aria-label="Preparation result name" maxlength="200" placeholder="Optional name"></label>
      <p class="msm-hint">Preparation creates an independent system and materializes molecular data in memory. It keeps the source unchanged. Native warnings remain in the Python output. A prepared result is not a readiness certificate.</p>
      <button data-prepare>Prepare separate system</button>
    </div>
    __RESULT_CARD__
    <section data-preparation-result hidden><details><summary>Preparation method and source</summary><p data-preparation-provenance></p></details><p class="msm-hint" data-missing-attributes></p>
      <button data-replace-review>Use in this view…</button><p class="msm-hint" data-replace-unavailable></p>
      <div data-replacement hidden><h3 tabindex="-1" data-replacement-heading>Replace the current system?</h3>
        <p>The prepared result will replace the complete molecular system. The current scene is reset: regions, selections, shapes and other scene objects are not transferred. Scene Undo cannot restore this replacement.</p>
        <p class="msm-hint">A separate copy is loaded; the result view remains independent. Copying may materialize the full result. Replacement is refused if the source or reviewed result has changed through managed edits.</p>
        <div class="msm-actions"><button data-replace-apply>Replace system</button><button data-replace-back>Back</button></div>
      </div>
    </section>
    <div class="msm-actions"><button data-inspect>Inspect chemistry</button><button data-refresh>Refresh</button><button data-clear hidden>Clear report</button></div>
    <p class="msm-status" role="status" aria-live="polite" data-status></p>
    <section data-report hidden aria-label="Chemistry report">
      <h3 data-report-heading tabindex="-1"></h3><button data-change-inspection>Change inspection</button><p data-report-scope></p><p class="msm-hint" data-state-summary></p>
      <p data-inventory-status></p><p class="msm-hint" data-count-convention></p><p class="msm-hint" data-connectivity></p>
      <p class="msm-hint" data-assessment-summary hidden></p>
      <section data-protonation-actions hidden>
        <p class="msm-hint">Apply this same inspected decision once. Only the listed hydrogen atoms are removed, across every source structure. Unsupported groups stay unassessed. This adds no hydrogens, charges or environmental pKa prediction.</p>
        <button data-protonation-prepare>Prepare separate system from this assessment</button>
        <button data-protonation-review>Apply assessed H removal here…</button>
        <section data-protonation-confirm hidden>
          <h4 data-protonation-review-heading tabindex="-1">Apply assessed H removal to the current system?</h4>
          <p>The listed source atoms will be removed from all structures. The native atom map remaps selections, regions and named analyses; observations involving removed atoms are removed without recalculation. The native operation is performed once. If projection fails, retry only Update view.</p>
          <button data-protonation-apply>Apply assessed H removal</button><button data-protonation-back>Back</button>
        </section>
      </section>
      <details data-assessment-attribution hidden><summary>Scientific reference identifiers</summary><p class="msm-hint" data-assessment-references></p></details>
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
  const renderResult=resultCard(el,model,options,{result:()=>result,busy:()=>busy,request,update:(value,text)=>{busy=value;message=text;if(alive)render();}});
  function cell(tag,value){const node=document.createElement(tag);node.textContent=String(value);return node;}
  function tableRows(target,rows){target.replaceChildren(...rows.map(values=>{const tr=document.createElement('tr');tr.append(...values.map(x=>cell('td',x)));return tr;}));}
  function list(target,values){target.replaceChildren(...values.map(x=>cell('li',x)));}
  function render(){
    const assessment=['coverage','terminals','protonation'].includes(parameters.task),whole=['terminals','protonation'].includes(parameters.task),protonation=parameters.task==='protonation',hydrogen=parameters.task==='hydrogens',heavy=parameters.task==='heavy',addH=parameters.task==='add_hydrogens',repair=repairs[parameters.task],prepare=heavy||addH||!!repair,selectedRepair=['infer_bonds','add_bonds','terminal_cappings'].includes(parameters.task),assignment=['autodock_types','partial_charges'].includes(parameters.task),fixed=addH&&parameters.hydrogen_mode==='fixed_chemical_state';renderSelection(draft,context);
    q('task').value=parameters.task;q('heading').textContent=heavy?'Add missing heavy atoms':addH?'Add missing hydrogens':hydrogen?'Hydrogen inventory':'Inspect stored chemistry';
    q('purpose').textContent=heavy?'Complete selected groups using the explicitly chosen native engine. Unassessed groups remain distinct from completed groups.':addH?'Add hydrogen atoms to a separate complete system, without removing existing hydrogens.':hydrogen?'Inspect indexed hydrogen neighbors and separately stored hydrogen counts, without adding or removing atoms.':'Inspect stored atom, bond and coordinate information without completing or repairing chemistry.';
    q('context').textContent=!context.has_system?'Load a system in Studio > Load first.':context.n_atoms!==undefined?`${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} structures`:'Molecular data need explicit recovery.';
    q('state-mode').value=parameters.state_mode;q('state-index-label').hidden=parameters.state_mode!=='index';if(document.activeElement!==q('state-index'))q('state-index').value=parameters.state_index;
    q('editor').hidden=addH||whole||(repair&&!selectedRepair);q('chemical-state').hidden=(prepare&&!fixed&&!assignment&&parameters.task!=='infer_bonds')||whole;q('assessment-ph-label').hidden=!protonation;if(document.activeElement!==q('assessment-ph'))q('assessment-ph').value=parameters.pH;
    q('scope').textContent=heavy?'The selection is evaluated in its chosen structure and reference state. The selected groups are completed across every source structure. Atom indices may change.':addH?'The complete system is prepared; no atom selection or visible-structure extraction is applied. This panel requires one source structure.':'The report uses the structure chosen in Selection context. One structure is inspected; other structures are not assessed.';
    q('preparation').hidden=!prepare||!!result;q('hydrogen-mode-label').hidden=!addH;q('hydrogen-mode').value=parameters.hydrogen_mode;
    q('engine-label').hidden=fixed||!!repair;q('engine').value=parameters.engine;for(const option of q('engine').options)option.disabled=heavy&&option.value==='OpenMM';
    q('ph-label').hidden=(!addH||fixed)&&!['terminal_cappings','remove_hydrogens'].includes(parameters.task);q('attribute-label').hidden=!!repair||(addH&&!fixed);q('attribute-policy').value=parameters.attribute_policy;
    for(const [key,value] of [['ph',parameters.pH],['preparation-title',parameters.title]])if(document.activeElement!==q(key))q(key).value=value;
    q('preparation-limits').textContent=heavy?'Template placement is an estimate, not refinement. Unsupported gaps or conflicting chemistry may remain unassessed; inspect native diagnostics. PDBFixer requires the omission policy. New atoms have no inferred force-field parameters.':fixed?'Requires one isolated, fully prepared component and chemical state with explicit connectivity, charges and hydrogen inventory. RDKit places local hydrogens on the existing pose. No protonation choice, minimization or periodic reconstruction is performed.':'Uses fixed free-amino-acid pKa thresholds, not environment-dependent pKa prediction. Existing hydrogens are retained. The native legacy route may discard attributes; it does not provide the strict attribute policy. Review diagnostics and inspect the result.';
    if(repair){q('heading').textContent=repair.title;q('purpose').textContent=repair.purpose;q('scope').textContent=repair.scope;q('preparation-limits').textContent=repair.limits;}
    q('inference-method-label').hidden=parameters.task!=='infer_bonds';q('bond-cutoff-label').hidden=parameters.task!=='add_bonds';q('capping-fields').hidden=parameters.task!=='terminal_cappings';q('charge-fields').hidden=parameters.task!=='partial_charges';q('forcefield-label').hidden=parameters.charge_method!=='forcefield';q('water-model-label').hidden=parameters.charge_method!=='forcefield';
    for(const [key,name] of [['inference-method','inference_method'],['bond-cutoff','bond_cutoff'],['n-cap','n_cap'],['c-cap','c_cap'],['keep-ids','keep_ids'],['charge-method','charge_method'],['forcefield','forcefield'],['water-model','water_model'],['expected-charge','expected_charge']])if(document.activeElement!==q(key))q(key).value=parameters[name];
    q('prepare').disabled=busy||!context.can_review||(selectedRepair&&draft.source==='none')||(heavy&&(draft.source==='none'||(parameters.engine==='PDBFixer'&&parameters.attribute_policy==='strict')))||(addH&&context.n_structures!==1);
    q('prepare').textContent=busy?'Preparing…':'Prepare separate system';
    renderResult(result,context,destinations,busy||!context.can_review);q('preparation-result').hidden=!result;
    if(result){
      const p=result.parameters;
      const method=p.task?`${repairs[p.task].title} · ${p.method||p.engine||'MolSysMT'} · ${p.scope==='whole_system'?'whole system':p.selected_atoms+' selected atoms'}`:result.operation.endsWith('heavy_atoms')?`Heavy-atom completion · ${p.engine} · ${p.selected_groups} selected groups · all source structures`:p.mode==='fixed_chemical_state'?`Hydrogen completion · prepared chemical state ${p.chemical_state} · RDKit · structure 0`:`Hydrogen completion · pH ${p.pH} · ${p.engine} · whole system, structure 0`;
      const extra=p.task?[
        p.chemical_state!==undefined?`Chemical state ${p.chemical_state}`:'',p.selection_structure!==undefined?`selection context structure ${p.selection_structure}`:'',
        p.pH!==undefined?`pH ${p.pH}`:'',p.N_terminal!==undefined?`N cap ${p.N_terminal||'none'}`:'',p.C_terminal!==undefined?`C cap ${p.C_terminal||'none'}`:'',
        p.max_bond_length?`bond distance ${p.max_bond_length}`:'',p.typing_scheme?`typing scheme ${p.typing_scheme}`:'',p.forcefield?`force field ${p.forcefield}`:'',p.water_model?`water model ${p.water_model}`:'',
        p.expected_total_charge!==undefined?`expected whole-system charge ${p.expected_total_charge===null?'from complete formal charges':p.expected_total_charge+' elementary charge'}`:'',
        p.selected_groups!==undefined?`${p.selected_groups} selected groups; native source-component scope`:'',p.report_schema?`native report ${p.report_schema}`:'',
      ].filter(Boolean).join(' · '):'';
      q('preparation-provenance').textContent=`${method}. ${extra?extra+'. ':''} MolSysMT ${result.software.molsysmt}; ${result.source_atoms.toLocaleString()} source atoms, molecular revision ${result.source_revision}.`;
      q('missing-attributes').textContent=result.missing_attributes.length?'Source attributes unavailable in this result: '+result.missing_attributes.join(', ')+(result.attributes_truncated?'…':'')+'.':'No source attribute names became unavailable. This does not prove preservation of every value or chemical interpretation.';
      q('replace-review').disabled=busy||!canReplace;q('replace-review').hidden=!!replacement||!!result.adopted;
      q('replace-unavailable').textContent=result.adopted?'This result has been loaded here. Its separate view remains independent.':canReplace?'':!replacementSupported?'Update MolSysViewer to a qualified host for reviewed replacement.':'The source changed or needs recovery. The separate result is still available; prepare again before replacing the current system.';
    }
    q('replacement').hidden=!replacement;q('replace-apply').disabled=busy||!canReplace;q('replace-back').disabled=busy;
    const sceneSource=!whole&&['current','saved','region'].includes(draft.source)&&context.state!=='synchronized';
    q('inspect').hidden=prepare;q('inspect').disabled=busy||!context.can_inspect||(!whole&&draft.source==='none')||sceneSource;
    q('inspect').textContent=busy?'Working…':hydrogen?'Inspect hydrogens':'Inspect chemistry';q('refresh').disabled=busy;q('clear').hidden=!report;q('clear').disabled=busy;
    for(const input of el.querySelectorAll('input,select'))input.disabled=busy;
    q('status').textContent=message||(sceneSource?'Update the scene before using its selection or regions.':['pending','sync_failed'].includes(context.state)?'The scene update is pending. Inspection reads the current molecular data; use Update view to synchronize the scene.':'');
    if(assessment){
      const titles={coverage:'Assess exact-template coverage',terminals:'Inspect missing terminal atoms',protonation:'Assess reference-rule protonation'};
      q('heading').textContent=titles[parameters.task];
      q('purpose').textContent=protonation?'Inspect the existing fixed-pKa name-inventory decision. This is an approximation, not environment-dependent pKa prediction or a chemical-state choice. Inspection changes nothing. The explicit actions apply this same decision once to the current system or to a separate result.':whole?'Inspect the native whole-system C-terminal OXT name check. Stored backbone connectivity and capping evidence define native chain ends; ambiguous chemistry remains unassessed. This is not a complete terminal-chemistry assessment.':'Compare the whole groups containing selected atoms against exact supported native templates. Missing, unexpected, ambiguous and unsupported chemistry remain distinct.';
      q('scope').textContent=whole?'Whole current molecular system, independent of the atom editor and visible structure. No coordinates or scene are changed.': 'Each selected atom contributes its complete source group. One chosen structure and chemical state are assessed. Group indices refer to the source, not a renumbered selection.';
      q('inspect').textContent=busy?'Working…':'Inspect without changing';
    }
    q('report').hidden=!report;
    q('protonation-actions').hidden=!protonation||!report;
    q('protonation-prepare').disabled=busy||!canPrepareProtonation;
    q('protonation-review').disabled=busy||!canApplyProtonation;
    q('protonation-confirm').hidden=!protonationReview||!report;
    q('protonation-apply').disabled=busy||!canApplyProtonation;
    q('protonation-back').disabled=busy;
    q('assessment-summary').hidden=!assessment;q('assessment-attribution').hidden=!protonation||!report;
    if(report&&assessment){
      q('report-heading').textContent=q('heading').textContent+' report';
      q('report-scope').textContent=whole?`${report.group_count.toLocaleString()} ${protonation?'source groups':'groups with missing terminal atoms'} · whole system`:`${report.group_count.toLocaleString()} source groups · ${report.structure_index===null?'no coordinate structures':`structure ${report.structure_index}`}`;
      q('state-summary').textContent=parameters.task==='terminals'?'Inventory/name-based terminal check; no chemical-state selection.':`Chemical state: ${report.chemical_state_index===null?'unresolved':report.chemical_state_index}.`;
      q('assessment-summary').textContent=protonation?`Native status: ${report.status}; pH ${report.pH}. ${report.removed_atoms} proposed H removals, not applied. ${report.assessed_groups} assessed groups; ${report.unassessed_groups} unassessed groups; ${report.unassessed_states} unassessed states; ${report.unassigned_atoms} unassigned atoms. Coverage complete: ${report.coverage_complete}.`:whole?'Only missing OXT names are returned; an empty result does not certify complete termini or unsupported groups.':`Native group coverage: ${report.counts.assessed} assessed, ${report.counts.incomplete} incomplete, ${report.counts.unassessed} unassessed. This is template comparison, not validation of all chemistry.`;
      q('assessment-references').textContent=protonation?report.attribution.join(', ')+(report.attribution_truncated?'…':''):'';
      q('inventory-status').textContent='';q('count-convention').textContent='';q('connectivity').textContent='';q('fields-section').hidden=true;q('issues-section').hidden=true;
      list(q('unassessed'),report.unassessed_checks.map(label));
      q('provenance').textContent=`${report.method} · ${report.schema} · MolSysMT ${report.software.molsysmt} · molecular revision ${report.source_revision}. Full native arrays stay in Python; only 50 rows are sent per page. Reports expire on changed inputs/source or unmount; raw external writes are not observed. No report or executable decision is stored in sessions or H5MSM.`;
      q('dataset').replaceChildren(...report.datasets.map(d=>{const o=document.createElement('option');o.value=d.id;o.textContent=d.label;return o;}));q('dataset').value=page?.dataset;
      if(page){const tr=document.createElement('tr');tr.append(...page.columns.map(name=>cell('th',name)));q('columns').replaceChildren(tr);tableRows(q('rows'),page.rows);q('page-summary').textContent=page.total?`Rows ${page.offset+1}–${page.offset+page.rows.length} of ${page.total.toLocaleString()}.`:'No rows returned for this check; unsupported or unassessed chemistry is not certified.';q('page-unit').textContent='';q('previous').disabled=busy||!page.offset;q('next').disabled=busy||page.offset+page.rows.length>=page.total;}
    }
    if(report&&!assessment){
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
  function changed(){stamp++;report=null;page=null;replacement=null;protonationReview=null;canApplyProtonation=canPrepareProtonation=false;message='';model.set('chemistry_selection',{...draft});model.set('chemistry_parameters',{...parameters});render();}
  function request(action,extra={}){if(busy)return;pendingAction=action;busy=true;sequence++;requestStamp=stamp;render();model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},parameters:{...parameters},...extra}});}
  q('task').addEventListener('change',()=>{parameters.task=q('task').value;changed();request('task');},options);
  q('state-mode').addEventListener('change',()=>{parameters.state_mode=q('state-mode').value;changed();},options);
  q('state-index').addEventListener('input',()=>{parameters.state_index=q('state-index').value;changed();},options);
  for(const [key,name,event] of [['hydrogen-mode','hydrogen_mode','change'],['engine','engine','change'],['ph','pH','input'],['attribute-policy','attribute_policy','change'],['preparation-title','title','input']])q(key).addEventListener(event,()=>{parameters[name]=q(key).value;changed();},options);
  for(const [key,name,event] of [['inference-method','inference_method','change'],['bond-cutoff','bond_cutoff','input'],['n-cap','n_cap','change'],['c-cap','c_cap','change'],['keep-ids','keep_ids','change'],['charge-method','charge_method','change'],['forcefield','forcefield','input'],['water-model','water_model','input'],['expected-charge','expected_charge','input']])q(key).addEventListener(event,()=>{parameters[name]=q(key).value;changed();},options);
  q('assessment-ph').addEventListener('input',()=>{parameters.pH=q('assessment-ph').value;changed();},options);
  q('prepare').addEventListener('click',()=>request('prepare'),options);
  q('replace-review').addEventListener('click',()=>request('replacement.review'),options);
  q('replace-apply').addEventListener('click',()=>request('replacement.apply',{token:replacement?.token}),options);
  for(const [key,action] of [['protonation-review','protonation.review'],['protonation-back','protonation.back'],['protonation-prepare','protonation.prepare'],['protonation-apply','protonation.apply']])q(key).addEventListener('click',()=>request(action,{report_id:report?.id,token:protonationReview}),options);
  q('replace-back').addEventListener('click',()=>request('replacement.back'),options);
  q('change-inspection').addEventListener('click',()=>q('source').focus(),options);
  for(const [key,action] of [['inspect','inspect'],['refresh','refresh'],['clear','clear']])q(key).addEventListener('click',()=>request(action),options);
  function turn(dataset,offset){if(report)request('page',{report_id:report.id,dataset,offset});}
  q('dataset').addEventListener('change',()=>turn(q('dataset').value,0),options);
  q('previous').addEventListener('click',()=>turn(page.dataset,page.offset-page.page_size),options);
  q('next').addEventListener('click',()=>turn(page.dataset,page.offset+page.page_size),options);
  function onState(msg){
    if(msg?.type==='presentation_closed'&&result?.id===msg.id){result=null;replacement=null;if(!busy)request('refresh');else render();return;}
    if(msg?.type!=='state'||typeof msg.state?.request_id!=='number'||msg.state.request_id<sequence)return;
    if(requestStamp!==stamp){busy=false;request('refresh');return;}
    const state=msg.state;busy=false;pendingAction='';draft={...initial,...state.draft};parameters={...defaults,...state.parameters};context=state.context||{};report=state.report||null;page=state.page||null;result=state.result||null;replacement=state.replacement||null;canReplace=!!state.can_replace;replacementSupported=!!state.replacement_supported;destinations=state.destinations||[];protonationReview=state.protonation_review||null;canApplyProtonation=!!state.can_apply_protonation;canPrepareProtonation=!!state.can_prepare_protonation;message=state.message||'';render();
    if(report&&state.stage==='report')q('report-heading').focus();
    if(replacement)q('replacement-heading').focus();if(protonationReview)q('protonation-review-heading').focus();
  }
  function onContext(){if(busy&&pendingAction==='protonation.apply'){report=null;page=null;protonationReview=null;canApplyProtonation=canPrepareProtonation=false;render();return;}stamp++;report=null;page=null;protonationReview=null;canApplyProtonation=canPrepareProtonation=false;if(!busy&&context.can_inspect)request('refresh');else render();}
  function onSync(status){
    if(busy&&pendingAction==='protonation.apply'){
      // Its coordinator notifications describe the request still in flight.
      // Retire the consumed review, but keep its own completion/error response.
      context={...context,...status,can_inspect:!!context.has_system&&['synchronized','pending','sync_failed'].includes(status.state),can_review:!!context.has_system&&context.n_structures>0&&status.state==='synchronized'};
      report=null;page=null;protonationReview=null;canApplyProtonation=canPrepareProtonation=false;render();return;
    }
    // Busy-state requests have no host admission and therefore no reply.
    // Retire older responses and start a fresh read only in an admitted state.
    stamp++;sequence++;busy=false;report=null;page=null;replacement=null;protonationReview=null;canApplyProtonation=canPrepareProtonation=false;canReplace=false;context={...context,...status,can_inspect:!!context.has_system&&['synchronized','pending','sync_failed'].includes(status.state),can_review:!!context.has_system&&context.n_structures>0&&status.state==='synchronized'};
    if(context.can_inspect)request('refresh');else render();
  }
  model.on('msg:custom',onState);model.on('viewer:frame-changed',onContext);model.on('viewer:selection-changed',onContext);model.on('viewer:system-sync-changed',onSync);
  render();return()=>{alive=false;abort.abort();model.off('msg:custom',onState);model.off('viewer:frame-changed',onContext);model.off('viewer:selection-changed',onContext);model.off('viewer:system-sync-changed',onSync);report=null;page=null;result=null;replacement=null;el.replaceChildren();};
}
"""
)
ESM = ESM.replace("__SELECTION_EDITOR__", SELECTION_MARKUP)
ESM = ESM.replace("__RESULT_CARD__", RESULT_MARKUP)

CSS = r"""
.msm-chemistry [data-report]{display:flex;flex-direction:column;gap:12px}
.msm-chemistry [data-preparation],.msm-chemistry [data-preparation-result]{display:flex;flex-direction:column;gap:12px}
.msm-chemistry [data-replacement]{padding:12px;border:1px solid #596473;border-radius:7px}
.msm-chemistry .msm-table-scroll{max-width:100%;overflow:auto;margin-top:8px}
.msm-chemistry table{width:100%;border-collapse:collapse;font-size:12px;text-align:left}
.msm-chemistry th,.msm-chemistry td{padding:5px 7px;border-bottom:1px solid #596473;overflow-wrap:anywhere;vertical-align:top}
.msm-chemistry th{font-weight:600}.msm-chemistry ul{padding-left:20px;margin:8px 0}
"""
