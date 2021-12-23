def is_file_fasta(item):

    output = False

    if type(item)==str:
        output = item.endswith('.fasta')

    return output

