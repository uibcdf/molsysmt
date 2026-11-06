"""Translation controls sharing selection and result UI with System."""

from ._panel_widgets import RESULT_MARKUP, SELECTION_MARKUP, SHARED_JS

ESM = (
    SHARED_JS
    + r"""
export function render({model,el}) {
  const abort=new AbortController(),options={signal:abort.signal};
  const initial={source:'none',value:'',expression:'',indices:'',context:'current',structure_index:0};
  const defaults={dx:'0',dy:'0',dz:'0',unit:'angstrom',structures:'all',indices:'',effect:'update',title:''};
  let draft={...initial,...model.get('geometry_selection')},parameters={...defaults,...model.get('translation_parameters')};
  let context={},review=null,result=null,destinations=[],busy=false,sequence=0,alive=true,message='';
  let stamp=0,lastApply=0,lastApplyStamp=0;
  el.innerHTML=`<section class="msm-system" aria-label="Molecular geometry tools">
    <h2>Translate</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint">Move molecular coordinates by a displacement vector. To reposition the camera, use the canvas controls.</p>
    __SELECTION_EDITOR__
    <div data-transform><label>Translate structures<select data-scope aria-label="Translate structures"><option value="all">All structures</option><option value="current">Current structure</option><option value="indices">Structure indices</option></select></label>
      <label data-frames-label hidden>Structure indices<input data-frames aria-label="Translation structure indices" maxlength="4096" placeholder="2, 0"></label>
      <div class="msm-vector"><label>Δx<input data-dx aria-label="Translation x" type="text" inputmode="decimal" maxlength="64"></label><label>Δy<input data-dy aria-label="Translation y" type="text" inputmode="decimal" maxlength="64"></label><label>Δz<input data-dz aria-label="Translation z" type="text" inputmode="decimal" maxlength="64"></label></div>
      <label>Displacement unit<select data-unit aria-label="Displacement unit"><option value="angstrom">Å (angstrom)</option><option value="nm">nm</option></select></label>
      <label>Apply to<select data-effect aria-label="Translation destination"><option value="update">Current system</option><option value="result">Independent result</option></select></label>
      <label data-title-label hidden>Result name<input data-title aria-label="Result name" maxlength="200" placeholder="Optional name"></label>
      <p class="msm-hint" data-effect-hint></p>
    </div>
    <div data-review hidden><h3>Review translation</h3><p data-review-summary></p><p data-review-scope></p>
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
    q('context').textContent=!context.has_system?'Load a system in Studio > Load first.':context.n_atoms!==undefined?`${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} structures`:'Molecular data need explicit recovery.';
    for(const [key,field] of [['dx','dx'],['dy','dy'],['dz','dz'],['unit','unit'],['scope','structures'],['frames','indices'],['effect','effect'],['title','title']])if(document.activeElement!==q(key))q(key).value=parameters[field];
    const independent=parameters.effect==='result';
    q('frames-label').hidden=parameters.structures!=='indices';q('title-label').hidden=!independent;
    q('effect-hint').textContent=independent?'Create a copy of the whole system, changing only the selected atoms and structures. The source stays unchanged. Large trajectories need memory for a separate system and View. Scene decorations are not copied.':'Edit the current molecular data and update the scene. Scene Undo cannot restore these coordinates.';
    q('editor').hidden=!!review||!!result;q('transform').hidden=!!review||!!result;
    q('review').hidden=!review;q('preview').hidden=!!review||!!result;
    q('preview').disabled=busy||!context.can_review||draft.source==='none'||(independent&&!destinations.length);
    q('preview').textContent=busy?'Working…':'Review translation';q('confirm').disabled=busy;q('back').disabled=busy;
    for(const input of el.querySelectorAll('input,select'))input.disabled=busy;
    q('refresh').disabled=busy||['pending','sync_failed','editing','syncing','uncertain'].includes(context.state);
    if(review){
      q('review-summary').textContent=`Move ${review.n_atoms.toLocaleString()} atoms in ${review.n_structures} structures by [${parameters.dx}, ${parameters.dy}, ${parameters.dz}] ${parameters.unit==='angstrom'?'Å':'nm'}.`;
      q('review-scope').textContent=`Structures: ${review.structure_indices.join(', ')}${review.structures_truncated?'…':''}. Selection context: structure ${review.selection_structure}, reference chemical state.`;
      q('review-effect').textContent=(independent?'The result keeps every source atom and structure. The source is unchanged.':'The current system will change. Affected stored analyses may need recalculation. Scene Undo does not restore molecular coordinates.')+' The periodic box stays fixed; coordinates are not wrapped.';
      q('confirm').textContent=independent?'Create translated result':'Apply translation';
    }
    const fallback=['pending','sync_failed'].includes(context.state)?'Use Update view in the canvas to finish the pending update.':context.state==='uncertain'?'Replace the molecular system explicitly before editing.':'';
    q('status').textContent=message||fallback;
  }
  function changed(){stamp++;review=null;message='';model.set('geometry_selection',{...draft});model.set('translation_parameters',{...parameters});render();}
  function request(action){
    if(busy)return;
    const token=review?.token;busy=true;sequence++;
    if(action==='apply'){lastApply=sequence;lastApplyStamp=stamp;}
    else review=null;
    render();model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},parameters:{...parameters},...(token?{token}:{})}});
  }
  for(const [key,field] of [['dx','dx'],['dy','dy'],['dz','dz'],['frames','indices'],['title','title']])q(key).addEventListener('input',()=>{parameters[field]=q(key).value;changed();},options);
  for(const [key,field] of [['unit','unit'],['scope','structures'],['effect','effect']])q(key).addEventListener('change',()=>{parameters[field]=q(key).value;changed();},options);
  for(const [key,action] of [['preview','review'],['confirm','apply'],['back','back'],['refresh','refresh']])q(key).addEventListener('click',()=>request(action),options);
  function onState(msg){
    if(msg?.type==='presentation_closed'&&result?.id===msg.id){result=null;message='Result view closed.';if(!busy)request('refresh');else render();return;}
    if(msg?.type!=='state'||typeof msg.state?.request_id!=='number')return;
    if(msg.state.request_id<sequence){
      if(msg.state.request_id===lastApply&&stamp===lastApplyStamp&&msg.state.stage==='done'&&msg.state.context?.target_revision===context.target_revision){message=msg.state.message;render();}
      return;
    }
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
