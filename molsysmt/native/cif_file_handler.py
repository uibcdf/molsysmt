
class CIFFileHandler():

    def __init__(self, filename, io_mode='r', closed=False):

        self.file = None

        if io_mode=='w':

            raise NotImplementedError

        elif io_mode=='r':

            self.file = open(filename, "r")

        else:

            raise NotImplementedError

        if closed:
            self.file.close()

    def parse(self):

        molecules = {}
        molecule = {}
        
        block = _read_block(self.file)
        while len(block):
            
            entry = _analysis_block(block)
        
            if entry[0]=='data':
        
                if len(molecule):
                    molecules[molecule['data']['data']]=molecule
                    molecule={}
            
            molecule[entry[0]]=entry[1]
            block = _read_block(self.file)
        
        molecules[molecule['data']['data']]=molecule
       
        return molecules

    def close(self):

        self.file.close()


def _read_block(fff):

    block=[]

    line = fff.readline()
    while line and not line.startswith('#'):
        if len(line.rstrip()):
            block.append(line.rstrip())
        line = fff.readline()

    return block


def _analysis_block(block):

    block_type = None
    block_dict = {}
    
    if block[0].startswith('data_'):

        block_type = 'data'
        block_dict = {'data': block[0][5:].rstrip()}
    
    elif block[0].startswith('loop_'):
        
        block_type = block[1].split('.')[0]

        suffix=len(block_type)+1
        
        fields = []
        values = []
        
        for ii in block[1:]:
            if ii.startswith(block_type):
                fields.append(ii[suffix:].split(' ')[0])
            else:
                values.append(ii.split())

        for field in fields:
            block_dict[field]=[]

        for aux in values:
            for field, value in zip(fields, aux):
                block_dict[field].append(value)

    else:

        block_type = block[0].split('.')[0]

        suffix=len(block_type)+1
        
        field = None
        value = None
        for ii in block:
            if ii.startswith(block_type):
                if field:
                    block_dict[field]=value
                field = ii[suffix:].split(' ')[0]
                value = ii.replace(block_type+'.'+field, '').strip()
            else:
                value += ii.strip()
    
    return block_type, block_dict

