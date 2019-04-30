


def add_loop (item, target_sequence=None, engine='modeller'):

    if engine=='modeller':

        from molmodmt import convert as _convert
        from molmodmt import sequence_alignment as _sequence_alignment
        import tempfile as _tempfile
        from os import remove as _remove
        import modeller as modeller
        import modeller.automodel as automodel

        seq_original = _convert(item, 'aminoacids1:seq')
        seq_aligned, _, _, _, _ = _sequence_alignment('aminoacids1:'+seq_original,
                                                      'aminoacids1:'+target_sequence)

        tmp_pdbfilename = _tempfile.NamedTemporaryFile(suffix=".pdb").name
        tmp_name = tmp_pdbfilename.split('/')[-1].split('.')[0]
        tmp_seqfilename = '/tmp/'+tmp_name+'.seq'
        tmp_alifilename = '/tmp/'+tmp_name+'.ali'

        _convert(item, tmp_pdbfilename)

        e = environ()
        e.io.atom_files_directory = ['.', '/tmp']
        m = model(e, file=tmp_pdbfilename)
        aln = alignment(e)
        aln.append_model(m, align_codes=tmp_name)
        aln.write(file=tmp_seqfilename)

        alifile = open(tmp_alifilename,'w')
        seqfile = open(tmp_seqfilename,'r')
        for _ in range(2):
            line= seqfile.readline()
            alifile.write(line)
        alifile.write(seq_aligned+'*')
        alifile.write('>P1,'+tmp_name+'_fill')
        alifile.write('sequence:::::::::')
        alifile.write(target_sequence+'*')
        alifile.close()
        seqfile.close()

        a = loopmodel(env, alnfile = tmp_alifilename, knowns = tmp_name, sequence = tmp_name+'_fill')
        a.starting_model = 1
        a.ending_model = 1

        a.loop.starting_model = 1
        a.loop.ending_model = 2
        a.loop.md_level = refine.fast

        a.make()

        _remove(tmp_pdbfilename)
        _remove(tmp_seqfilename)
        _remove(tmp_alifilename)

    elif engine=='pyrosetta':
        pass

    elif engine=='ensembler':
        pass

    pass
