#################################
######## Charge

charge={}

charge={
'itNA': +1.0,
'itK': +1.0,
'itCL': -1.0
}


#################################
######## Donor - Acceptor

### Donors

donors=[
'atN'   ,   # N for the main chain
'atNT'  ,   # N for the main chain (in ACEMD terminal)
'atNE'  ,   # N for ARG
'atNH1' ,   # N for ARG
'atNH2' ,   # N for ARG
'atNE1' ,   # N for TRP
'atNE2' ,   # N for HIS and GLN (presence of H determines if donor)
'atND1' ,   # N for HIS (presence of H determines if donor)
'atND2' ,   # N for ASN
'atNZ'  ,   # N for LYS
'atOG'  ,   # O for SER
'atOH'  ,   # O for TYR
'atOW'  ,   # O for WAT
'atOG1' ,   # O for THR
'atSG'      # S for CYS
]

donors_exception={
'atNE2' : { 'HIS' : [ 'Without H' , False ]},
'atND1' : { 'HIS' : [ 'Without H' , False ]},
'atOD1' : { 'HYP' : [ 'Always' , True ]}
}
# !! y que pasa con las ASPH?



### Acceptors

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


## Y que pasa con los terminales?
