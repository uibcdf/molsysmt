MODULE MODULE_BONDS

CONTAINS

    SUBROUTINE COMPONENT_INDICES(atom_indices, n_atoms, n_bonds, comp_indices)
     
     
        INTEGER,DIMENSION(n_bonds,2),INTENT(IN)::atom_indices
        INTEGER,INTENT(IN)::n_bonds, n_atoms
        INTEGER,DIMENSION(n_atoms),INTENT(OUT)::comp_indices
    
        LOGICAL,DIMENSION(n_atoms):: visto
        INTEGER:: n_components
    
        INTEGER::ii, jj, label, label_out, atom_1, atom_2
    
        visto(:)=.FALSE.
        comp_indices(:)= (/ (ii, ii=1,n_atoms) /)
        n_components=0
    
        DO ii=1,n_bonds
    
            atom_1 = atom_indices(ii,1)+1
            atom_2 = atom_indices(ii,2)+1
    
            IF (visto(atom_1).eqv..FALSE.) THEN
    
                IF (visto(atom_2).eqv..FALSE.) THEN
    
                    label = atom_1
                    visto(atom_1)=.TRUE.
                    visto(atom_2)=.TRUE.
                    comp_indices(atom_1)=label
                    comp_indices(atom_2)=label
    
                ELSE
    
                    label = comp_indices(atom_2)
                    visto(atom_1)=.TRUE.
                    comp_indices(atom_1)=label
    
                END IF
    
            ELSE
    
                IF (visto(atom_2).eqv..FALSE.) THEN 
    
                    label = comp_indices(atom_1)
                    visto(atom_2)=.TRUE.
                    comp_indices(atom_2)=label
    
                ELSE
    
                    IF (comp_indices(atom_1).ne.comp_indices(atom_2)) THEN
    
                        label=comp_indices(atom_1)
                        label_out=comp_indices(atom_2)
    
                        WHERE (comp_indices==label_out)
    
                            comp_indices=label
    
                        END WHERE
    
                    END IF
    
                END IF
    
            END IF
    
        END DO
    
        visto(:)=.FALSE.
    
    
        DO ii=1,n_atoms
    
            IF (visto(ii).eqv..FALSE.) THEN
    
                label=comp_indices(ii)
    
                DO jj=1,n_atoms
    
                    IF (visto(jj).eqv..FALSE.) THEN
    
                        IF (comp_indices(jj)==label) THEN
    
                            comp_indices(jj)=n_components
                            visto(jj)=.TRUE.
    
                        END IF
    
                    END IF
    
                END DO
                    
                n_components = n_components+1
    
            END IF
    
        END DO
    
    END SUBROUTINE COMPONENT_INDICES

END MODULE MODULE_BONDS
