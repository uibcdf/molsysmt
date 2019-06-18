MODULE MODULE_COM

CONTAINS

  FUNCTION GEOMETRICAL_CENTER(coors, atoms_indices_serialized, atoms_series_starts, frame_indices,& 
                              n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frame_indices) RESULT(center)

    IMPLICIT NONE

    INTEGER,INTENT(IN)::n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frame_indices
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
    INTEGER,DIMENSION(n_atoms_indices),INTENT(IN)::atoms_indices_serialized
    INTEGER,DIMENSION(n_atoms_series+1),INTENT(IN)::atoms_series_starts
    INTEGER,DIMENSION(n_frame_indices),INTENT(IN)::frame_indices
    DOUBLE PRECISION,DIMENSION(n_atoms_indices)::weights
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms_series,3)::center
 

    weights(:)=1.0d0

    center=CENTER_OF_MASS(coors, atoms_indices_serialized, atoms_series_starts, weights, frame_indices,& 
                          n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frame_indices)

  END FUNCTION

  FUNCTION CENTER_OF_MASS(coors, atoms_indices_serialized, atoms_series_starts, weights, frame_indices,& 
                          n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frame_indices) RESULT(center)
 
    IMPLICIT NONE
 
    INTEGER,INTENT(IN)::n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frame_indices
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
    INTEGER,DIMENSION(n_atoms_indices),INTENT(IN)::atoms_indices_serialized
    INTEGER,DIMENSION(n_atoms_series+1),INTENT(IN)::atoms_series_starts
    DOUBLE PRECISION,DIMENSION(n_atoms_indices),INTENT(IN)::weights
    INTEGER,DIMENSION(n_frame_indices),INTENT(IN)::frame_indices
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms_series,3)::center
 
    INTEGER::ii,jj,ll,frame_index,atom_index
    DOUBLE PRECISION::total_weight
 
    center(:,:,:)=0.0d0

    DO ii=1,n_atoms_series
        total_weight=0.0d0
        DO jj=atoms_series_starts(ii)+1,atoms_series_starts(ii+1)
            total_weight = total_weight+weights(jj)
        END DO
        DO jj=atoms_series_starts(ii)+1,atoms_series_starts(ii+1)
            atom_index = atoms_indices_serialized(jj)+1
            DO ll=1,n_frame_indices
                frame_index=frame_indices(ll)+1
                center(ll,ii,:)=center(ll,ii,:)+weights(jj)*coors(frame_index,atom_index,:)/total_weight
            END DO
        END DO
    END DO
 
  END FUNCTION CENTER_OF_MASS

END MODULE MODULE_COM
 
