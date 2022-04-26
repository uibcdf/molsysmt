acceptors=[
'atND1' ,   # N for HIS (presence of H determines if donor-acceptor)
'atNE2' ,   # N for HIS (presence of H determines if donor-acceptor) (Not in GLN)
'atO'   ,   # O for the main chain
'atOY'   ,   # O for the main chain (In ACEMD terminal)
'atOT1'   ,   # O for terminals
'atOT2'   ,   # O for terminals
'atOD1' ,   # O for ASN and ASP and HYP
'atOD2' ,   # O for ASP
'atOE1' ,   # O for GLN and GLU
'atOE2' ,   # O for GLU
'atOG'  ,   # O for SER
'atOG1' ,   # O for THR
'atOH'  ,   # O for TYR
'atOW'  ,   # O for WAT
'atSD'      # S for MET
]

acceptors_exception={
'atNE2' : { 'GLN' : [ 'Always'   , False ], 'HIS' : [ 'With H' , False ]},
'atSG'  : { 'CYH' : [ 'Always'   , True  ]},    ## Corregir esto!!!
'atND1' : { 'HIS' : [ 'With H', False ]}
}


