"""Frontend for the qualified System task; the host supplies workspace chrome."""

ESM = r"""
export function render({model, el}) {
  const abort = new AbortController();
  const options = {signal: abort.signal};
  const initial = {source:'none', value:'', expression:'', indices:'', context:'current', structure_index:0};
  let draft = {...initial, ...(model.get('system_draft') || {})};
  let context = {}, review = null, sequence = 0, busy = false, stage = 'select', message = '';
  let draftStamp=0,lastRemove=0,lastRemoveStamp=0;
  el.innerHTML = `<section class="msm-system" aria-label="Molecular system tools">
    <h2>Remove atoms</h2><p class="msm-context" data-context>Loading system information…</p>
    <p class="msm-hint">Remove atoms from molecular data. To change visibility, use Regions.</p>
    <div data-editor><label>Choose atoms<select data-source aria-label="Choose atoms">
      <option value="none">Choose a selection…</option><option value="category">Molecular category</option>
      <option value="current">Current canvas selection</option><option value="saved">Saved selection</option>
      <option value="region">Region</option><option value="expression">Selection expression</option>
      <option value="indices">Atom indices</option></select></label>
    <label data-category-label hidden>Category<select data-category aria-label="Molecular category">
      <option value="">Choose a category…</option><option value="water">Water</option><option value="ions">Ions</option></select></label>
    <label data-name-label hidden>Name<input data-name aria-label="Saved selection or region name" maxlength="4096" list="msm-system-choices"></label>
    <datalist id="msm-system-choices"></datalist><p class="msm-hint" data-truncated hidden>Showing the first 200 names. You can enter any existing name.</p>
    <label data-expression-label hidden>MolSysMT expression<input data-expression aria-label="MolSysMT expression" maxlength="4096" placeholder="group_type=='water'"></label>
    <label data-indices-label hidden>Atom indices<input data-indices aria-label="Atom indices" maxlength="4096" placeholder="0, 2, 4"></label>
    <details><summary>Selection context</summary>
      <label>Evaluate selection in<select data-evaluate aria-label="Selection structure context"><option value="current">Current structure</option><option value="index">Structure index</option></select></label>
      <label data-index-label hidden>Structure index<input data-index aria-label="Structure index" type="number" min="0" step="1"></label>
      <p class="msm-hint">Expressions use the reference chemical state. Structure indices start at 0.</p>
    </details></div>
    <p class="msm-scope">Removing an atom removes it from every structure.</p>
    <div data-review hidden><h3>Review removal</h3><p class="msm-hint" data-review-selection></p><dl class="msm-stats">
      <div><dt>Remove</dt><dd data-remove-count></dd></div><div><dt>Keep</dt><dd data-keep-count></dd></div><div><dt>Structures</dt><dd data-structures></dd></div></dl>
      <p class="msm-hint" data-review-context></p>
      <p class="msm-hint">Saved selections and scene objects will be updated. Scene Undo cannot restore removed atoms.</p>
      <div class="msm-actions"><button data-confirm>Remove selected atoms</button><button data-back>Back</button></div>
    </div>
    <div class="msm-actions"><button data-preview>Review removal</button><button data-refresh>Refresh</button></div>
    <p class="msm-status" role="status" aria-live="polite" data-status></p>
  </section>`;
  const q = key => el.querySelector(`[data-${key}]`);
  const choicesId='msm-system-choices-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
  el.querySelector('datalist').id=choicesId;q('name').setAttribute('list',choicesId);
  function render() {
    q('context').textContent = !context.has_system ? 'Load a system in Studio > Load first.' :
      context.n_atoms !== undefined ? `${context.n_atoms.toLocaleString()} atoms · ${context.n_structures} ${context.n_structures===1?'structure':'structures'}` : 'Molecular data need explicit recovery.';
    q('source').value = draft.source;
    q('category').value = draft.value;
    for (const [key, value] of [['name', draft.value], ['expression',draft.expression], ['indices',draft.indices], ['evaluate',draft.context], ['index',draft.structure_index]]) {
      if (document.activeElement !== q(key)) q(key).value = value;
    }
    q('category-label').hidden = draft.source !== 'category';
    q('name-label').hidden = !['saved','region'].includes(draft.source);
    q('expression-label').hidden = draft.source !== 'expression';q('indices-label').hidden = draft.source !== 'indices';
    q('index-label').hidden = draft.context !== 'index';
    q('truncated').hidden = !context.choices_truncated || !['saved','region'].includes(draft.source);
    const names = draft.source === 'saved' ? context.saved || [] : context.regions || [];
    el.querySelector('datalist').replaceChildren(...names.map(name => {const o=document.createElement('option');o.value=name;return o;}));
    for (const input of el.querySelectorAll('input, select')) input.disabled = busy;
    q('review').hidden = !review;q('editor').hidden=!!review;
    q('preview').hidden = !!review;
    q('preview').disabled = busy || !context.can_review || draft.source === 'none';
    q('preview').textContent = busy ? 'Working…' : 'Review removal';
    q('refresh').disabled = ['pending','sync_failed','editing','syncing','uncertain'].includes(context.state);q('back').disabled=busy;q('confirm').disabled=busy;
    if (review) {
      const label=draft.source==='category' ? (draft.value==='water'?'Water':'Ions') : draft.source==='current'?'Current canvas selection':draft.source==='expression'?'Expression: '+draft.expression:draft.source==='indices'?'Atom indices: '+draft.indices:draft.source+': '+draft.value;
      q('review-selection').textContent=label.length>220?label.slice(0,220)+'…':label;
      q('remove-count').textContent = review.remove_atoms.toLocaleString();q('keep-count').textContent = review.keep_atoms.toLocaleString();q('structures').textContent = review.n_structures.toLocaleString();
      q('confirm').textContent = `Remove ${review.remove_atoms.toLocaleString()} ${review.remove_atoms===1?'atom':'atoms'}`;
      q('review-context').textContent = `Selection context: structure ${review.selection_structure}; reference state. ` + (review.n_groups == null ? 'Group membership is incomplete.' : `${review.n_groups} groups selected.`);
    }
    const fallback = ['pending','sync_failed'].includes(context.state) ? 'Use Update view in the canvas to finish the pending update.' : context.state==='uncertain' ? 'Use explicit system replacement to recover before editing.' : context.state==='unavailable' ? 'This host needs an update for managed molecular editing.' : '';
    q('status').textContent = message || fallback;
    q('status').dataset.stage=stage;
  }
  function persist() {model.set('system_draft', {...draft});}
  function changed() {draftStamp++;review=null;message='';stage='select';persist();render();}
  function request(action) {
    if (busy && action!=='refresh') return;
    const token=review?.token;busy=true;sequence++;
    if(action==='remove'){lastRemove=sequence;lastRemoveStamp=draftStamp;}
    if(action!=='remove')review=null;
    render();
    model.send({type:'action',id:action,payload:{request_id:sequence,draft:{...draft},...(token?{token}:{})}});
  }
  q('source').addEventListener('change',()=>{draft.source=q('source').value;draft.value='';changed();},options);
  q('category').addEventListener('change',()=>{draft.value=q('category').value;changed();},options);
  for (const [key, field] of [['name','value'],['expression','expression'],['indices','indices']]) q(key).addEventListener('input',()=>{draft[field]=q(key).value;changed();},options);
  q('evaluate').addEventListener('change',()=>{draft.context=q('evaluate').value;changed();},options);
  q('index').addEventListener('input',()=>{draft.structure_index=Number(q('index').value);changed();},options);
  for(const [key,action] of [['preview','review'],['confirm','remove'],['back','back'],['refresh','refresh']])q(key).addEventListener('click',()=>request(action),options);
  function onState(msg) {
    if(msg?.type!=='state' || typeof msg.state?.request_id!=='number')return;
    if(msg.state.request_id < sequence){
      if(msg.state.request_id===lastRemove && draftStamp===lastRemoveStamp && msg.state.stage==='done' && msg.state.context?.target_revision===context.target_revision){message=msg.state.message;render();}
      return;
    }
    const state=msg.state;busy=false;draft={...initial,...state.draft};context=state.context || {};review=state.review || null;stage=state.stage;message=state.message || '';render();
    if(review)q('confirm').focus();else if(['done','error','sync_required'].includes(stage))q('status').setAttribute('tabindex','-1');
  }
  function onContextChange(){review=null;if(!busy)request('refresh');else render();}
  function onSystemSync(status){
    const refresh=status.state==='synchronized' && (context.state!=='synchronized' || status.target_revision!==context.target_revision);
    context={...context,...status,can_review:status.state==='synchronized' && !refresh ? context.can_review : false};review=null;
    if(status.state!=='synchronized'){busy=false;message=status.reason || 'Molecular data are updating. Use the canvas update control if needed.';render();}
    else if(refresh){busy=false;request('refresh');}
    else render();
  }
  model.on('msg:custom',onState);model.on('viewer:frame-changed',onContextChange);model.on('viewer:selection-changed',onContextChange);model.on('viewer:system-sync-changed',onSystemSync);
  render();
  return () => {abort.abort();model.off('msg:custom',onState);model.off('viewer:frame-changed',onContextChange);model.off('viewer:selection-changed',onContextChange);model.off('viewer:system-sync-changed',onSystemSync);review=null;el.replaceChildren();};
}
"""

CSS = """
.msm-system{display:flex;flex-direction:column;gap:12px;padding:10px;color:#eef1f5;font:13px/1.5 system-ui,sans-serif}
.msm-system h2,.msm-system h3{margin:0;font-size:16px;font-weight:600}.msm-system h3{font-size:14px}
.msm-system p{margin:0}.msm-system [data-editor]{display:flex;flex-direction:column;gap:12px}.msm-system label{display:flex;flex-direction:column;gap:5px}.msm-system input,.msm-system select{box-sizing:border-box;width:100%;min-width:0;padding:8px;border:1px solid #596473;border-radius:6px;background:rgba(255,255,255,.04);color:inherit;font:inherit}.msm-system option{background:#252c35;color:#eef1f5}
.msm-system button{padding:7px 10px;border:1px solid #667282;border-radius:6px;background:rgba(255,255,255,.09);color:inherit;font:inherit;cursor:pointer}.msm-system button:disabled{opacity:.45;cursor:default}.msm-system [data-preview]{background:#d0dcec;color:#1d2633}.msm-system [data-confirm]{background:#dfc099;color:#29231d;font-weight:600}
.msm-system :focus-visible{outline:2px solid #a6c5eb;outline-offset:2px}.msm-system .msm-context,.msm-system .msm-hint{font-size:12px;color:#b9c4d3}.msm-system details{font-size:12px}.msm-system summary{cursor:pointer}.msm-system details label{margin-top:10px}.msm-system .msm-scope,.msm-system [data-review]{padding:10px;border:1px solid #596473;border-radius:7px}.msm-system [data-review]>*+*{margin-top:10px}.msm-system .msm-actions{display:flex;gap:7px;flex-wrap:wrap}.msm-system .msm-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:10px 0}.msm-system dt{font-size:11px;color:#b9c4d3}.msm-system dd{margin:3px 0 0;font-size:18px;font-variant-numeric:tabular-nums}.msm-system .msm-status{min-height:20px}.msm-system [hidden]{display:none!important}
"""
