MODULE MODULE_COM

CONTAINS

  FUNCTION GEOMETRICAL_CENTER(coors,n_frames,n_atoms) RESULT(center)

    IMPLICIT NONE

    INTEGER, INTENT(IN)::n_atoms,n_frames
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
    DOUBLE PRECISION,DIMENSION(n_frames,3)::center

    DOUBLE PRECISION,DIMENSION(n_atoms)::weights

    weights(:)=1.0d0

    center=CENTER_OF_MASS(coors,weights,n_frames,n_atoms)

  END FUNCTION

  FUNCTION CENTER_OF_MASS(coors,weights,n_frames,n_atoms) RESULT(center)
 
    IMPLICIT NONE
 
    INTEGER,INTENT(IN)::n_atoms,n_frames
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
    DOUBLE PRECISION,DIMENSION(n_atoms),INTENT(IN)::weights
    DOUBLE PRECISION,DIMENSION(n_frames,3)::center
 
    INTEGER::ii,ll
    DOUBLE PRECISION::total_weight
 
    center(:,:)=0.0d0
    total_weight=SUM(weights)
 

    DO ll=1,n_frames
      DO ii=1,n_atoms
          center(ll,:)=center(ll,:)+weights(ii)*coors(ll,ii,:)
      END DO
      center(ll,:)=center(ll,:)/total_weight
    END DO
 
  END FUNCTION CENTER_OF_MASS

END MODULE MODULE_COM
 
