import pandas as pd
import numpy  as np



class _AtomDB():

    _utype = 'AtomDB'

    def __init__(self,attributes=None,number_atoms=None):

        self.attribute_names=[attr['name'] for attr in attributes]
        self.df=pd.DataFrame(columns=self.attribute_names,index=number_atoms)

    def add_atom(self,atom=None):
        
        index=self.df.shape[0]
        if atom.index:
            if atom.index != index:
                print 'error'
        else:
            atom.index=index

        new_row=[]
        for attr in self.attribute_names:
            try:
                new_row.append(getattr(atom,attr).value)
            except:
                new_row.append(getattr(atom,attr))

        self.df.loc[index]=new_row
        del(new_row)

        ## esto puede estar mucho mejor... se pueden poner los atributos directamente? se pueden comparar en el df cantidades (value,unity)?



