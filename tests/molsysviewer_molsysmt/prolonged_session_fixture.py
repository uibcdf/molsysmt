"""Linux one-kernel receiving workload with actual cgroup resource observations.

Run via system_panel_jupyter.py --scenario prolonged-session. The workload uses
real native calculations, notebook widgets, coherent files and both popup types;
it does not qualify installed artifacts, hardware VRAM, macOS or human usage.
"""


def notebook_cells(prefix, output):
    setup = (
        prefix
        + """
import copy, gc, hashlib, json, os, time, uuid
import numpy as np
import psutil
from IPython.display import display
from molsysviewer.system_edits import SystemEditPendingError
puw=msm.pyunitwizard
_long_pid=os.getpid()
_long_birth=psutil.Process().create_time()
_long_identity=str(uuid.uuid4())
_long_cycle=0
_long_ledger=[]
"""
        + f"_long_output=Path({str(output)!r})\n"
        + """
def long_write():
    temporary=_long_output/'long-ledger.partial.json'
    temporary.write_text(json.dumps(_long_ledger,indent=2,allow_nan=False))
    temporary.replace(_long_output/'long-ledger.json')
def long_cgroup():
    relative=Path('/proc/self/cgroup').read_text().split('0::',1)[1].strip().lstrip('/')
    base=Path('/sys/fs/cgroup')/relative
    return {name:(base/name).read_text().strip() for name in ['cpu.max','cpu.stat','memory.max','memory.current','memory.peak','memory.events','pids.current']}
def long_check_identity():
    assert os.getpid()==_long_pid and psutil.Process().create_time()==_long_birth
    np.testing.assert_array_equal(puw.get_value(witness.molsys.structures.coordinates,to_unit='nm'),_witness_xyz)
def long_analysis_snapshot(value):
    return {name:np.asarray(getattr(value,name)).copy() for name in ['evaluated_structure_indices','occurrence_structures','occurrence_relations','relation_participant_offsets','participant_roles','participant_atom_offsets','participant_atoms']}
witness=msv.demo['1TCD']
assert witness.molsys.get_n_atoms()==3983
_witness_xyz=puw.get_value(witness.molsys.structures.coordinates,to_unit='nm').copy()
display(witness)
print('LONG_SETUP_READY')
"""
    )
    create = """
long_check_identity()
_long_cycle+=1
_long_started=time.perf_counter()
_long_cgroup_before=long_cgroup()
_source=msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],to_form='molsysmt.MolSys')
v=msv.new_view(_source)
del _source
assert v.molsys.get_n_atoms()==62 and v.molsys.structures.n_structures==5000
_expected_xyz=puw.get_value(v.molsys.structures.coordinates,to_unit='nm').copy()
_delta=puw.quantity([.01,0,0],'nm')
v.addons.molsysmt.structure.translate(selection=[0],structure_indices=[4999],translation=_delta,in_place=True)
_expected_xyz[4999,0]+=[.01,0,0]
np.testing.assert_allclose(puw.get_value(v.molsys.structures.coordinates,to_unit='nm'),_expected_xyz,rtol=1e-12,atol=1e-12)
_dist=v.addons.molsysmt.structure.get_distances(selection=[0],selection_2=[10],structure_indices='all',pairs=True,pbc=False,use_gpu=False)
_values=np.asarray(puw.get_value(_dist,to_unit='nm')).reshape(5000)
np.testing.assert_allclose(_values,np.linalg.norm(_expected_xyz[:,0]-_expected_xyz[:,10],axis=1),rtol=1e-12,atol=1e-12)
_context={'schema':'example.prolonged.distance@1','method':'molsysmt.structure.get_distances','parameters':{'selection':[0],'selection_2':[10],'pairs':True,'pbc':False},'units':{'native':'nm','displayed':'nm'},'source_translation':puw.QuantityRecord.from_quantity(_delta,field='example.prolonged.translation').to_dict(encoding='base64'),'managed_revision':v.addons.molsysmt.get_sync_status()['target_revision'],'raw_edits_observed':False}
v.trajectory_plot.show(_values,title='Native end-to-end control',y_label='Distance (nm)',observations=[_context])
v.shapes.add_sphere(center=puw.quantity(_expected_xyz[0].mean(axis=0),'nm'),radius='.1 nm',color='orange',tag='long-sphere')
v.active_selection.set([0,10])
_analysis=v.interactions.hbonds.get_buch_hbonds(name='long-hbonds',structure_indices='all',pbc=True)
assert _analysis.n_interactions>0
v.interactions.add('long-hbonds',tag='long-hbonds')
_expected_analysis=long_analysis_snapshot(_analysis)
_analysis_measurements={key:np.asarray(value).copy() for key,value in _analysis.measurements.items()}
_analysis_units=dict(_analysis.measure_units)
v.player.go_to_structure(4999)
(_long_output/'cycle-expected.json').write_text(json.dumps({'cycle':_long_cycle,'atoms':62,'structure':4999,'positions':{'0':(_expected_xyz[4999,0]*10).tolist(),'10':(_expected_xyz[4999,10]*10).tolist()}}))
display(v)
print(f'LONG_CREATED_{_long_cycle}')
"""
    windows = """
long_check_identity()
_before=v.export_state()
_status=v.addons.manager.system_edits.get_status()
try:
    v.addons.manager.system_edits.replace(v.molsys,expected_target=v.molsys,expected_revision=_status['target_revision']+1)
except SystemEditPendingError as error:
    assert 'changed after review' in str(error)
else:
    raise AssertionError('Stale replacement unexpectedly admitted')
assert v.export_state()==_before
np.testing.assert_allclose(puw.get_value(v.molsys.structures.coordinates,to_unit='nm'),_expected_xyz,rtol=1e-12,atol=1e-12)
v.player.go_to_structure(0)
print(f'LONG_WINDOWS_READY_{_long_cycle}')
"""
    recovery = """
long_check_identity()
assert v.player.index==1, v.player.index
_session_path=_long_output/f'cycle-{_long_cycle:02d}.msv'
await v.save_session_async(_session_path)
_expected_scene=copy.deepcopy(v.export_state())
_session_sha=hashlib.sha256(_session_path.read_bytes()).hexdigest()
v.close()
assert v.closed
v=msv.load_session(_session_path)
assert v.export_state()==_expected_scene
np.testing.assert_allclose(puw.get_value(v.molsys.structures.coordinates,to_unit='nm'),_expected_xyz,rtol=1e-12,atol=1e-12)
_analysis=v.interactions.get_analysis('long-hbonds')
for _key,_value in _expected_analysis.items():np.testing.assert_array_equal(getattr(_analysis,_key),_value)
assert set(_analysis.measurements)==set(_analysis_measurements)
for _key,_value in _analysis_measurements.items():np.testing.assert_array_equal(_analysis.measurements[_key],_value)
assert _analysis.measure_units==_analysis_units
assert v.trajectory_plot.records()[0]['series'][0]['observation']==_context
display(v)
print(f'LONG_RECOVERED_{_long_cycle}')
"""
    play = """
long_check_identity()
v.player.play(fps=10)
print(f'LONG_PLAYING_{_long_cycle}')
"""
    pause = """
v.player.pause()
v.player.go_to_structure(73)
print(f'LONG_PAUSED_{_long_cycle}')
"""
    close = """
long_check_identity()
assert v.player.index==73 and not v.player.is_playing
np.testing.assert_allclose(puw.get_value(v.molsys.structures.coordinates,to_unit='nm'),_expected_xyz,rtol=1e-12,atol=1e-12)
assert v.interactions.query('long-hbonds',structure_indices=[4999,0,73]).n_interactions==int(np.count_nonzero(np.isin(_expected_analysis['occurrence_structures'],[4999,0,73])))
_count=v.interactions.get_analysis('long-hbonds').n_interactions
v.close()
assert v.closed
v=None
_analysis=None
_dist=None
_values=None
_expected_xyz=None
_expected_analysis=None
_analysis_measurements=None
_expected_scene=None
_before=None
gc.collect()
_open=sum(1 for value in gc.get_objects() if isinstance(value,msv.MolSysView) and not value.closed)
_total=sum(1 for value in gc.get_objects() if isinstance(value,msv.MolSysView))
assert _open==1, (_open,_total)
_long_ledger.append({'cycle':_long_cycle,'cgroup_before':_long_cgroup_before,'cgroup_after':long_cgroup(),'kernel_identity':_long_identity,'kernel_pid':_long_pid,'kernel_birth':_long_birth,'seconds':time.perf_counter()-_long_started,'native_rss_mib':psutil.Process().memory_info().rss/2**20,'open_views':_open,'all_view_instances':_total,'interaction_occurrences':_count,'session_sha256':_session_sha,'session_bytes':_session_path.stat().st_size})
long_write()
print(f'LONG_CLOSED_{_long_cycle}')
"""
    final = """
long_check_identity()
witness.close()
assert witness.closed
print('LONG_ALL_COMPLETE',len(_long_ledger))
"""
    return [setup, create, windows, recovery, play, pause, close, final]
