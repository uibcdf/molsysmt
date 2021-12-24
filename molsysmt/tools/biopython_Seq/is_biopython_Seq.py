def is_biopython_Seq(item):

    try:
        output = (item.__class__.__name__=='Seq') and (item.__class__.__module__=='Bio.Seq')
    except:
        output = False

    return output

