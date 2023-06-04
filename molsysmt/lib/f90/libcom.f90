MODULE MODULE_COM

CONTAINS

  FUNCTION GEOMETRICAL_CENTER(coors, groups_indices, groups_atoms_indices, groups_starts,& 
                          n_structures, n_atoms, n_groups, n_groups_atoms) RESULT(center)

    IMPLICIT NONE

    INTEGER,INTENT(IN)::n_structures, n_atoms, n_groups, n_groups_atoms
    DOUBLE PRECISION,DIMENSION(n_structures,n_atoms,3),INTENT(IN)::coors
    INTEGER,DIMENSION(n_groups),INTENT(IN)::groups_indices
    INTEGER,DIMENSION(n_groups+1),INTENT(IN)::groups_starts
    INTEGER,DIMENSION(n_groups_atoms),INTENT(IN)::groups_atoms_indices
    DOUBLE PRECISION,DIMENSION(n_groups_atoms)::weights
    DOUBLE PRECISION,DIMENSION(n_structures, n_groups, 3)::center
 
    weights(:)=1.0d0

    center=CENTER_OF_MASS(coors, groups_indices, groups_atoms_indices, groups_starts, weights,& 
                          &n_structures, n_atoms, n_groups, n_groups_atoms)

  END FUNCTION

  FUNCTION CENTER_OF_MASS(coors, groups_indices, groups_atoms_indices, groups_starts, weights,& 
                          &n_structures, n_atoms, n_groups, n_groups_atoms) RESULT(center)
 
    IMPLICIT NONE
 
    INTEGER,INTENT(IN)::n_structures, n_atoms, n_groups, n_groups_atoms
    DOUBLE PRECISION,DIMENSION(n_structures,n_atoms,3),INTENT(IN)::coors
    INTEGER,DIMENSION(n_groups),INTENT(IN)::groups_indices
    INTEGER,DIMENSION(n_groups+1),INTENT(IN)::groups_starts
    INTEGER,DIMENSION(n_groups_atoms),INTENT(IN)::groups_atoms_indices
    DOUBLE PRECISION,DIMENSION(n_groups_atoms),INTENT(IN)::weights
    DOUBLE PRECISION,DIMENSION(n_structures, n_groups, 3)::center
 
    INTEGER::ii, jj, ll, atom_index
    DOUBLE PRECISION::total_weight
 
    center(:,:,:)=0.0d0

    DO ii=1,n_groups
        total_weight=0.0d0
        DO jj=groups_starts(ii)+1, groups_starts(ii+1)
            total_weight = total_weight+weights(jj)
        END DO
        DO jj=groups_starts(ii)+1, groups_starts(ii+1)
            atom_index = groups_atoms_indices(jj)+1
            DO ll=1,n_structures
                center(ll,ii,:)=center(ll,ii,:)+weights(jj)*coors(ll,atom_index,:)/total_weight
            END DO
        END DO
    END DO
 
  END FUNCTION CENTER_OF_MASS

END MODULE MODULE_COM
 
