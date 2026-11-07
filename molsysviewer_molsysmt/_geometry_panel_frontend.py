"""Coordinate task controls sharing selection and result UI with System."""

from ._panel_widgets import RESULT_MARKUP, SELECTION_MARKUP, SHARED_JS

ESM = (
    SHARED_JS
    + r"""
export function render({model,el}) {
  const abort=new AbortController(),options={signal:abort.signal};
  const initial={source:'none',value:'',expression:'',indices:'',context:'current',structure_index:0};
  const defaults={task:'translate',axes_expression:'',axes_type:'inertia',axes_weights:'uniform',axes_center:'preserve',axes_target:'cartesian',axes_basis:'1 0 0; 0 1 0; 0 0 1',ax:'0',ay:'0',az:'1',angle:'90',angle_unit:'degree',rotation_center_kind:'geometric',wrap_mode:'primary',wrap_compact:'component',ox:'0',oy:'0',oz:'0',origin_unit:'angstrom',fit_expression:'',fit_reference_expression:'',fit_reference_structure:'0',cx:'0',cy:'0',cz:'0',center_unit:'angstrom',center_kind:'geometric',source_expression:'',destination_kind:'point',target_expression:'',dx:'0',dy:'0',dz:'0',unit:'angstrom',structures:'all',indices:'',effect:'update',title:''};
  let draft={...initial,...model.get('geometry_selection')},parameters={...defaults,...model.get('translation_parameters')};
  let context={},review=null,result=null,destinations=[],busy=false,sequence=0,alive=true,message='';
  let stamp=0,requestStamp=0;
  el.innerHTML=`<section class="msm-system" aria-label="Molecular geometry tools">
    <label>Geometry task<select data-task aria-label="Geometry task"><option value="translate">Translate</option><option value="rotate">Rotate</option><option value="center">Center</option><option value="fit">Superpose structures</option><option value="axes">Align principal axes</option><option value="wrap">Wrap coordinates</option><option value="unwrap">Unwrap trajectory</option></select></label>
    <h2 data-geometry-heading>Translate</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint" data-purpose>Move molecular coordinates by a displacement vector. To reposition the camera, use the canvas controls.</p>
    __SELECTION_EDITOR__
    <div data-transform><label><span data-scope-caption>Translate structures</span><select data-scope aria-label="Translate structures"><option value="all">All structures</option><option value="current">Current structure</option><option value="indices">Structure indices</option></select></label>
      <label data-frames-label hidden>Structure indices<input data-frames aria-label="Translation structure indices" maxlength="4096" placeholder="2, 0"></label>
      <div data-principal hidden>
        <label>Moment definition<select data-axes-type aria-label="Principal-axis definition"><option value="inertia">Inertia tensor</option><option value="geometric">Geometric covariance</option></select></label>
        <label>Reference atom weights<select data-axes-weights aria-label="Principal-axis weights"><option value="uniform">Equal atom weights</option><option value="masses">Standard atomic masses</option></select></label>
        <label>Reference center<select data-axes-center aria-label="Principal-axis center"><option value="preserve">Keep initial reference center</option><option value="origin">Subtract initial reference center</option></select></label>
        <label>Target axes<select data-axes-target aria-label="Principal-axis target"><option value="cartesian">Molecular Cartesian axes</option><option value="custom">Explicit right-handed basis</option></select></label>
        <label data-axes-basis-row hidden>Target axes as three row vectors<input data-axes-basis aria-label="Target axis rows" maxlength="512" placeholder="1 0 0; 0 1 0; 0 0 1"></label>
        <details><summary>Atoms defining the principal axes</summary><label>MolSysMT reference expression<input data-axes-atoms aria-label="Principal-axis atom expression" maxlength="4096" placeholder="Empty uses every moving atom"></label><p class="msm-hint">The fixed reference population may differ from the moving atoms. Unselected reference atoms stay unchanged; their initial coordinates determine the transformation.</p></details>
        <p class="msm-hint">Native MolSysMT axes are ordered by increasing moment; inertia and covariance have different ordering. Axis signs are not unique and have no temporal continuity guarantee. Degenerate moments reject. Native validation checks the target basis and every processed structure before coordinate publication. The box stays fixed; coordinates are not periodically reconstructed.</p>
      </div>
      <div data-rotate hidden>
        <p class="msm-hint">The axis uses molecular Cartesian coordinates, independently of the camera. Positive angles follow the right-hand rule: +90° about +z maps +x to +y.</p>
        <div class="msm-vector"><label>Axis x<input data-ax aria-label="Rotation axis x" type="text" inputmode="decimal" maxlength="64"></label><label>Axis y<input data-ay aria-label="Rotation axis y" type="text" inputmode="decimal" maxlength="64"></label><label>Axis z<input data-az aria-label="Rotation axis z" type="text" inputmode="decimal" maxlength="64"></label></div>
        <label>Angle<input data-angle aria-label="Rotation angle" type="text" inputmode="decimal" maxlength="64"></label>
        <label>Angle unit<select data-angle-unit aria-label="Rotation angle unit"><option value="degree">Degrees</option><option value="radian">Radians</option></select></label>
        <label>Rotation center<select data-rotation-center-kind aria-label="Rotation center"><option value="geometric">Selected atoms’ geometric center in each structure</option><option value="origin">Coordinate origin</option><option value="point">Fixed point</option></select></label>
        <p class="msm-hint">The default center is unweighted and computed separately in each processed structure from stored coordinates. The box stays fixed; rotation neither wraps nor reconstructs periodic images. Periodic minimum-image distances can change.</p>
      </div>
      <div data-center hidden>
        <label>Source center<select data-center-kind aria-label="Source center"><option value="geometric">Geometric center</option><option value="masses">Center of mass</option></select></label>
        <details><summary>Reference atoms</summary><label>MolSysMT expression within the moving selection<input data-center-source aria-label="Source center expression" maxlength="4096" placeholder="Empty uses every moving atom"></label><p class="msm-hint">The source reference must be inside the moving selection. One fixed population is evaluated in the selection context.</p></details>
        <label>Destination<select data-destination aria-label="Center destination"><option value="point">Explicit point</option><option value="selection">Geometric center of a selection</option></select></label>
        <label data-target-row hidden>Target MolSysMT expression<input data-center-target aria-label="Target center expression" maxlength="4096" placeholder="atom_name=='CA'"></label>
        <p class="msm-hint">Centers are computed separately in each processed structure, from stored coordinates without periodic reconstruction. A target selection uses its initial geometric center.</p>
      </div>
      <div data-fit hidden>
        <label>Reference structure in this system<input data-fit-reference-structure aria-label="Reference structure index" type="text" inputmode="numeric" maxlength="64" placeholder="0"></label>
        <p class="msm-hint">By default, match the moving atoms to the same atom indices in the initial reference structure. The fit uses an unweighted rigid least-RMSD method (Kabsch, MolSysMT CPU). Coordinates are not reconstructed across periodic boundaries.</p>
        <details><summary>Fitting atoms and correspondence</summary>
          <label>Fit atom expression<input data-fit-atoms aria-label="Fit atom expression" maxlength="4096" placeholder="Empty uses every moving atom"></label>
          <label>Reference atom expression<input data-fit-reference aria-label="Reference atom expression" maxlength="4096" placeholder="Empty uses the same fit atom indices"></label>
          <p class="msm-hint">Expressions select fixed populations in ascending system-index order; atoms are paired by position, without sequence or atom-name matching. Fit atoms may lie outside the moving selection. Check chemical correspondence explicitly. At least three non-collinear pairs are required; geometry is checked before native writes.</p>
        </details>
      </div>
      <div data-wrap hidden>
        <label>Periodic placement<select data-wrap-mode aria-label="Periodic placement"><option value="primary">Primary box from origin</option><option value="centered">Primary box around center</option><option value="nearest">Nearest periodic image</option></select></label>
        <label>Keep together<select data-wrap-compact aria-label="Periodic grouping"><option value="component">Selected covalent components</option><option value="atom">Each atom separately</option></select></label>
        <p class="msm-hint">Components use provided bonds between selected atoms; no bonds are inferred. Their centers are placed in the chosen cell, so some atoms may extend outside it. Unselected atoms never move. Atomwise wrapping can split bonds across boundaries.</p>
      </div>
      <div data-periodic hidden>
        <p class="msm-hint" data-periodic-purpose></p>
        <details><summary>Periodic conventions and current support</summary><p class="msm-hint">Uses stored box vectors without changing them. This editor currently admits conventional lower-triangular box vectors; other orientations are rejected pending native support. Temporal unwrapping additionally requires an unchanged cell. It restores per-atom temporal continuity, not covalent reconstruction within one structure.</p></details>
      </div>
      <div class="msm-vector" data-point><label><span data-x-label>Δx</span><input data-dx aria-label="Translation x" type="text" inputmode="decimal" maxlength="64"></label><label><span data-y-label>Δy</span><input data-dy aria-label="Translation y" type="text" inputmode="decimal" maxlength="64"></label><label><span data-z-label>Δz</span><input data-dz aria-label="Translation z" type="text" inputmode="decimal" maxlength="64"></label></div>
      <label data-unit-row><span data-unit-caption>Displacement unit</span><select data-unit aria-label="Displacement unit"><option value="angstrom">Å (angstrom)</option><option value="nm">nm</option></select></label>
      <label>Apply to<select data-effect aria-label="Translation destination"><option value="update">Current system</option><option value="result">Independent result</option></select></label>
      <label data-title-label hidden>Result name<input data-title aria-label="Result name" maxlength="200" placeholder="Optional name"></label>
      <p class="msm-hint" data-effect-hint></p>
    </div>
    <div data-review hidden><h3 data-review-heading>Review translation</h3><p data-review-summary></p><p data-review-scope></p>
      <p class="msm-hint" data-review-effect></p>
      <div class="msm-actions"><button data-confirm>Apply translation</button><button data-back>Back</button></div>
    </div>
    __RESULT_CARD__
    <div class="msm-actions"><button data-preview>Review translation</button><button data-refresh>Refresh</button></div>
    <p class="msm-status" role="status" aria-live="polite" data-status></p>
  </section>`;
  const q=key=>el.querySelector(`[data-${key}]`);
  const whole=document.createElement('option');whole.value='all';whole.textContent='Whole system';q('source').options.add(whole,1);
  const renderSelection=selectionEditor(el,options,patch=>{Object.assign(draft,patch);changed();});
  const renderResult=resultCard(el,model,options,{result:()=>result,busy:()=>busy,request,
    update:(value,text)=>{busy=value;message=text;if(alive)render();}});
  function render(){
    renderSelection(draft,context);renderResult(result,context,destinations,busy);
    const principal=parameters.task==='axes',rotated=parameters.task==='rotate',centered=parameters.task==='center',fitted=parameters.task==='fit',wrapped=parameters.task==='wrap',unwrapped=parameters.task==='unwrap',periodic=wrapped||unwrapped;
    const [heading,label]=({translate:['Translate','translation'],rotate:['Rotate','rotation'],axes:['Align principal axes','principal-axis alignment'],center:['Center','centering'],fit:['Superpose structures','superposition'],wrap:['Wrap coordinates','periodic wrapping'],unwrap:['Unwrap trajectory','temporal unwrapping']})[parameters.task]||['Translate','translation'];
    q('task').value=parameters.task;q('geometry-heading').textContent=heading;
    const atomsCaption=wrapped?'Atoms to wrap':unwrapped?'Atoms to unwrap':fitted?'Atoms to move':'Choose atoms';
    q('selection-caption').textContent=atomsCaption;q('source').setAttribute('aria-label',atomsCaption);
    q('purpose').textContent=principal?'Orient the moving atoms using a fixed reference population and native principal axes. This changes molecular coordinates, not the camera.':rotated?'Rotate selected molecular coordinates about a specified system axis and center. The camera is unchanged.':wrapped?'Choose periodic images for selected molecular coordinates, using each structure’s stored box.':unwrapped?'Restore per-atom continuity in a deliberately ordered sequence of structures.':fitted?'Move the chosen atoms together to match an initial reference pose. Set fitting atoms separately in advanced controls.':centered?'Place a chosen center at an explicit destination by translating the selected atoms.':'Move molecular coordinates by a displacement vector. To reposition the camera, use the canvas controls.';
    q('scope-caption').textContent=principal?'Align structures':rotated?'Rotate structures':unwrapped?'Unwrap structures in time order':wrapped?'Wrap structures':fitted?'Superpose structures':centered?'Center structures':'Translate structures';q('review-heading').textContent='Review '+label;
    q('scope').setAttribute('aria-label',principal?'Align structures':rotated?'Rotate structures':unwrapped?'Unwrap structures in time order':wrapped?'Wrap structures':fitted?'Superpose structures':centered?'Center structures':'Translate structures');
    q('frames').setAttribute('aria-label',principal?'Principal-axis structure indices':rotated?'Rotation structure indices':periodic?'Periodic structure indices':fitted?'Superposition structure indices':centered?'Center structure indices':'Translation structure indices');
    q('unit').setAttribute('aria-label',rotated?'Rotation center unit':wrapped?'Periodic reference unit':centered?'Target point unit':'Displacement unit');
    q('effect').setAttribute('aria-label','Coordinate result destination');
    q('principal').hidden=!principal;q('axes-basis-row').hidden=parameters.axes_target!=='custom';q('rotate').hidden=!rotated;q('center').hidden=!centered;q('fit').hidden=!fitted;q('wrap').hidden=!wrapped;q('periodic').hidden=!periodic;q('point').hidden=principal||fitted||unwrapped||(rotated&&parameters.rotation_center_kind!=='point')||(centered&&parameters.destination_kind==='selection');q('unit-row').hidden=q('point').hidden;
    q('target-row').hidden=parameters.destination_kind!=='selection';
    q('unit-caption').textContent=rotated?'Rotation center unit':wrapped?'Periodic reference unit':centered?'Target point unit':'Displacement unit';
    q('periodic-purpose').textContent=unwrapped?'Requires at least two selected structures and one unchanged cell. Their supplied order is treated as temporal adjacency; skipped intervals or large displacements can make image recovery ambiguous.':'Primary boxes use fractional-coordinate placement. Nearest image chooses the closest Cartesian image to the reference point; these can differ for skew cells.';
    for(const axis of ['x','y','z']){const caption=rotated?'Center '+axis:wrapped?(parameters.wrap_mode==='primary'?'Origin ':parameters.wrap_mode==='centered'?'Cell center ':'Reference point ')+axis:centered?'Target '+axis:'Δ'+axis;q(axis+'-label').textContent=caption;q('d'+axis).setAttribute('aria-label',rotated?'Rotation center '+axis:wrapped?'Periodic reference '+axis:centered?'Target '+axis:'Translation '+axis);}
    q('context').textContent=!context.has_system?'Load a system in Studio > Load first.':context.n_atoms!==undefined?`${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} structures`:'Molecular data need explicit recovery.';
    for(const [key,field] of [['axes-type','axes_type'],['axes-weights','axes_weights'],['axes-center','axes_center'],['axes-target','axes_target'],['axes-basis','axes_basis'],['axes-atoms','axes_expression'],['ax','ax'],['ay','ay'],['az','az'],['angle','angle'],['angle-unit','angle_unit'],['rotation-center-kind','rotation_center_kind'],['wrap-mode','wrap_mode'],['wrap-compact','wrap_compact'],['fit-atoms','fit_expression'],['fit-reference','fit_reference_expression'],['fit-reference-structure','fit_reference_structure'],['dx',wrapped?'ox':(centered||rotated)?'cx':'dx'],['dy',wrapped?'oy':(centered||rotated)?'cy':'dy'],['dz',wrapped?'oz':(centered||rotated)?'cz':'dz'],['unit',wrapped?'origin_unit':(centered||rotated)?'center_unit':'unit'],['center-kind','center_kind'],['center-source','source_expression'],['destination','destination_kind'],['center-target','target_expression'],['scope','structures'],['frames','indices'],['effect','effect'],['title','title']])if(document.activeElement!==q(key))q(key).value=parameters[field];
    const independent=parameters.effect==='result';
    q('frames-label').hidden=parameters.structures!=='indices';q('title-label').hidden=!independent;
    q('effect-hint').textContent=independent?'Create a copy of the whole system, changing only the selected atoms and structures. The source stays unchanged. Large trajectories need memory for a separate system and View. Scene decorations are not copied.':'Edit the current molecular data and update the scene. Scene Undo cannot restore these coordinates.';
    q('editor').hidden=!!review||!!result;q('transform').hidden=!!review||!!result;
    q('review').hidden=!review;q('preview').hidden=!!review||!!result;
    const insufficientTemporal=unwrapped&&(context.n_structures<2||parameters.structures==='current');
    q('preview').disabled=busy||!context.can_review||draft.source==='none'||insufficientTemporal||(independent&&!destinations.length);
    q('preview').textContent=busy?'Working…':'Review '+label;q('confirm').disabled=busy;q('back').disabled=busy;
    for(const input of el.querySelectorAll('input,select'))input.disabled=busy;
    q('refresh').disabled=busy||['pending','sync_failed','editing','syncing','uncertain'].includes(context.state);
    if(review){
      q('review-summary').textContent=principal?`Align ${review.n_atoms.toLocaleString()} atoms in ${review.n_structures} structures using ${review.n_fit_atoms} reference atoms, ${parameters.axes_type==='inertia'?'inertia tensor':'geometric covariance'} and ${parameters.axes_weights==='masses'?'standard atomic masses':'equal atom weights'}. ${parameters.axes_center==='origin'?'Subtract':'Keep'} the initial reference center. Target: ${parameters.axes_target==='cartesian'?'molecular Cartesian axes':`row vectors ${parameters.axes_basis}`}. Native basis and moment checks run on confirmation.`:rotated?`Rotate ${review.n_atoms.toLocaleString()} atoms in ${review.n_structures} structures about molecular axis [${parameters.ax}, ${parameters.ay}, ${parameters.az}] by ${parameters.angle} ${parameters.angle_unit}. Center: ${parameters.rotation_center_kind==='geometric'?'selected atoms’ unweighted geometric center in each processed structure':parameters.rotation_center_kind==='origin'?'coordinate origin':`fixed point [${parameters.cx}, ${parameters.cy}, ${parameters.cz}] ${parameters.center_unit==='angstrom'?'Å':'nm'}`}.`:wrapped?`Wrap ${review.n_atoms.toLocaleString()} atoms in ${review.n_structures} structures. Placement: ${{primary:'primary box from origin',centered:'primary box around center',nearest:'nearest periodic image'}[parameters.wrap_mode]}. Reference: [${parameters.ox}, ${parameters.oy}, ${parameters.oz}] ${parameters.origin_unit==='angstrom'?'Å':'nm'}. ${parameters.wrap_compact==='component'?'Reconstruct selected bonded components and place their centers.':'Wrap each atom independently.'}`:unwrapped?`Unwrap ${review.n_atoms.toLocaleString()} atoms in temporal order ${review.structure_indices.join(' → ')}${review.structures_truncated?'…':''}. The first selected structure anchors continuity.`:fitted?`Superpose ${review.n_atoms.toLocaleString()} moving atoms in ${review.n_structures} structures using ${review.n_fit_atoms} corresponding atom pairs and initial reference structure ${review.reference_structure}. Rigid unweighted Kabsch fit; MolSysMT CPU. Chemical correspondence is user-declared.`:centered?`Center ${review.n_center_atoms} reference atoms (${parameters.center_kind==='masses'?'atomic masses':'geometric center'}) by moving ${review.n_atoms} atoms in ${review.n_structures} structures. Destination: ${parameters.destination_kind==='selection'?`initial geometric center of ${review.n_target_atoms} target atoms`:`[${parameters.cx}, ${parameters.cy}, ${parameters.cz}] ${parameters.center_unit==='angstrom'?'Å':'nm'}`}.`:`Move ${review.n_atoms.toLocaleString()} atoms in ${review.n_structures} structures by [${parameters.dx}, ${parameters.dy}, ${parameters.dz}] ${parameters.unit==='angstrom'?'Å':'nm'}.`;
      q('review-scope').textContent=`Structures: ${review.structure_indices.join(', ')}${review.structures_truncated?'…':''}. Selection context: structure ${review.selection_structure}, reference chemical state.`;
      q('review-effect').textContent=(independent?'The result keeps every source atom and structure. The source is unchanged.':'The current system will change. Affected stored analyses may need recalculation. Scene Undo does not restore molecular coordinates.')+(periodic?' Stored box vectors stay fixed. Only the selected structures change images. Unselected structures keep their original coordinates.':' The periodic box stays fixed; coordinates are not wrapped.');
      q('confirm').textContent=independent?(principal?'Create aligned result':rotated?'Create rotated result':wrapped?'Create wrapped result':unwrapped?'Create unwrapped result':fitted?'Create superposed result':centered?'Create centered result':'Create translated result'):(principal?'Apply principal-axis alignment':rotated?'Apply rotation':wrapped?'Apply wrapping':unwrapped?'Apply unwrapping':fitted?'Apply superposition':centered?'Apply centering':'Apply translation');
    }
    const fallback=['pending','sync_failed'].includes(context.state)?'Use Update view in the canvas to finish the pending update.':context.state==='uncertain'?'Replace the molecular system explicitly before editing.':'';
    q('status').textContent=message||(insufficientTemporal?'Choose at least two structures in their intended temporal order.':fallback);
  }
  function changed(){stamp++;review=null;message='';model.set('geometry_selection',{...draft});model.set('translation_parameters',{...parameters});render();}
  function request(action){
    if(busy)return;
    const token=review?.token;busy=true;sequence++;
    requestStamp=stamp;
    if(action!=='apply')review=null;
    render();model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},parameters:{...parameters},...(token?{token}:{})}});
  }
  q('task').addEventListener('change',()=>{parameters.task=q('task').value;changed();request('task');},options);
  for(const axis of ['x','y','z'])q('d'+axis).addEventListener('input',()=>{parameters[(parameters.task==='wrap'?'o':['center','rotate'].includes(parameters.task)?'c':'d')+axis]=q('d'+axis).value;changed();},options);
  for(const [key,field] of [['axes-basis','axes_basis'],['axes-atoms','axes_expression'],['ax','ax'],['ay','ay'],['az','az'],['angle','angle'],['fit-atoms','fit_expression'],['fit-reference','fit_reference_expression'],['fit-reference-structure','fit_reference_structure'],['center-source','source_expression'],['center-target','target_expression'],['frames','indices'],['title','title']])q(key).addEventListener('input',()=>{parameters[field]=q(key).value;changed();},options);
  for(const [key,field] of [['axes-type','axes_type'],['axes-weights','axes_weights'],['axes-center','axes_center'],['axes-target','axes_target'],['angle-unit','angle_unit'],['rotation-center-kind','rotation_center_kind'],['wrap-mode','wrap_mode'],['wrap-compact','wrap_compact'],['unit',null],['center-kind','center_kind'],['destination','destination_kind'],['scope','structures'],['effect','effect']])q(key).addEventListener('change',()=>{parameters[field||(parameters.task==='wrap'?'origin_unit':['center','rotate'].includes(parameters.task)?'center_unit':'unit')]=q(key).value;changed();},options);
  for(const [key,action] of [['preview','review'],['confirm','apply'],['back','back'],['refresh','refresh']])q(key).addEventListener('click',()=>request(action),options);
  function onState(msg){
    if(msg?.type==='presentation_closed'&&result?.id===msg.id){result=null;message='Result view closed.';if(!busy)request('refresh');else render();return;}
    if(msg?.type!=='state'||typeof msg.state?.request_id!=='number')return;
    if(msg.state.request_id<sequence)return;
    if(requestStamp!==stamp){busy=false;request('refresh');return;}
    const state=msg.state;busy=false;draft={...initial,...state.draft};parameters={...defaults,...state.parameters};context=state.context||{};review=state.review||null;result=state.result||null;destinations=state.destinations||[];message=state.message||'';render();
    if(review)q('confirm').focus();
  }
  function onContext(){review=null;if(!busy)request('refresh');else render();}
  function onSync(status){
    const refresh=status.state==='synchronized'&&(context.state!=='synchronized'||status.target_revision!==context.target_revision);
    context={...context,...status,can_review:status.state==='synchronized'&&!refresh?context.can_review:false};review=null;
    if(status.state!=='synchronized'){busy=false;message=status.reason||'Molecular data are updating.';render();}
    else if(refresh){busy=false;request('refresh');}else render();
  }
  model.on('msg:custom',onState);model.on('viewer:frame-changed',onContext);model.on('viewer:selection-changed',onContext);model.on('viewer:system-sync-changed',onSync);
  render();return()=>{alive=false;abort.abort();model.off('msg:custom',onState);model.off('viewer:frame-changed',onContext);model.off('viewer:selection-changed',onContext);model.off('viewer:system-sync-changed',onSync);review=null;el.replaceChildren();};
}
"""
)
ESM = ESM.replace("__SELECTION_EDITOR__", SELECTION_MARKUP).replace(
    "__RESULT_CARD__", RESULT_MARKUP
)
