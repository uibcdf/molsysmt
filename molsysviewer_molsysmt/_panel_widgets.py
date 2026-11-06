"""Reusable controls for selection and explicit independent-result presentation."""

SELECTION_MARKUP = r"""    <div data-editor><label>Choose atoms<select data-source aria-label="Choose atoms">
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
"""
RESULT_MARKUP = r"""    <div data-result hidden><h3 data-result-heading></h3><p data-result-summary></p><p class="msm-hint" data-result-provenance></p>
      <div class="msm-actions"><button data-show-notebook>Show in notebook</button><button data-show-window>Open in new window</button><button data-new-result>Create another result</button><button data-discard-result>Close result</button></div>
      <details><summary>Python reference</summary><code data-result-handle></code></details>
    </div>
"""
SHARED_JS = r"""
function selectionEditor(el, options, onChange) {
  const q=key=>el.querySelector(`[data-${key}]`);
  const choicesId='msm-task-choices-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
  el.querySelector('datalist').id=choicesId;q('name').setAttribute('list',choicesId);
  q('source').addEventListener('change',()=>onChange({source:q('source').value,value:''}),options);
  q('category').addEventListener('change',()=>onChange({value:q('category').value}),options);
  for(const [key,field] of [['name','value'],['expression','expression'],['indices','indices']])q(key).addEventListener('input',()=>onChange({[field]:q(key).value}),options);
  q('evaluate').addEventListener('change',()=>onChange({context:q('evaluate').value}),options);
  q('index').addEventListener('input',()=>onChange({structure_index:Number(q('index').value)}),options);
  return (draft,context)=>{
    q('source').value=draft.source;q('category').value=draft.value;
    for(const [key,value] of [['name',draft.value],['expression',draft.expression],['indices',draft.indices],['evaluate',draft.context],['index',draft.structure_index]])if(document.activeElement!==q(key))q(key).value=value;
    q('category-label').hidden=draft.source!=='category';q('name-label').hidden=!['saved','region'].includes(draft.source);
    q('expression-label').hidden=draft.source!=='expression';q('indices-label').hidden=draft.source!=='indices';q('index-label').hidden=draft.context!=='index';
    q('truncated').hidden=!context.choices_truncated||!['saved','region'].includes(draft.source);
    const names=draft.source==='saved'?context.saved||[]:context.regions||[];
    el.querySelector('datalist').replaceChildren(...names.map(name=>{const o=document.createElement('option');o.value=name;return o;}));
  };
}
function resultCard(el,model,options,access) {
  const q=key=>el.querySelector(`[data-${key}]`);
  async function present(destination){
    const result=access.result();if(access.busy()||!result)return;
    access.update(true,'Opening result…');
    try{const notice=await model.present_view(result.id,destination);access.update(false,notice||(destination==='notebook'?'Result shown below the original canvas.':'Result opened in its own window.'));}
    catch(error){access.update(false,String(error.message||error));}
  }
  q('show-notebook').addEventListener('click',()=>present('notebook'),options);
  q('show-window').addEventListener('click',()=>present('window'),options);
  q('discard-result').addEventListener('click',()=>access.request('result.discard'),options);
  q('new-result').addEventListener('click',()=>access.request('result.new'),options);
  return (result,context,destinations,busy)=>{
    q('result').hidden=!result;
    if(result){
      q('result-heading').textContent=result.title;
      q('result-summary').textContent=`${result.n_atoms.toLocaleString()} ${result.n_atoms===1?'atom':'atoms'} · ${result.n_structures.toLocaleString()} ${result.n_structures===1?'structure':'structures'}`;
      q('result-provenance').textContent=(result.affected_structures?`${result.effect_label||'Translated'} structures: ${result.affected_structures.join(', ')}${result.affected_truncated?'…':''}. All source structures retained.`:`Source structures, in order: ${result.structure_indices.join(', ')}${result.structures_truncated?'…':''}.`)+(context.target_revision!==result.source_revision?' The source has changed since this result was created.':'');
      q('result-handle').textContent=`view.addons.manager.presentations.get(${JSON.stringify(result.id)})`;
    }
    for(const [key,destination] of [['show-notebook','notebook'],['show-window','window']]){q(key).hidden=!destinations.includes(destination);q(key).disabled=busy;}
    q('discard-result').disabled=busy;q('new-result').disabled=busy;
  };
}
"""
