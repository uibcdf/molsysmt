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

