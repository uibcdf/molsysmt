MODULE MODULE_GEOMETRY

USE MODULE_PBC
USE MODULE_MATH
USE MODULE_COM

CONTAINS

  FUNCTION DIST2POINTS(point1,point2,box,inv,ortho,pbc_opt) RESULT (valdist)
      
    IMPLICIT NONE    
    INTEGER, INTENT(IN)::ortho,pbc_opt
    DOUBLE PRECISION,DIMENSION(3),INTENT(IN)::point1,point2
    DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box,inv
    DOUBLE PRECISION::valdist
    DOUBLE PRECISION,DIMENSION(3)::vect_aux
    
    vect_aux(:)=point1(:)-point2(:)
    IF (pbc_opt==1) THEN
        CALL PBC (vect_aux,box,inv,ortho)
    END IF
    valdist=sqrt(dot_product(vect_aux(:),vect_aux(:)))

  END FUNCTION DIST2POINTS
  
  SUBROUTINE DISTANCE(diff_set,coors1,coors2,box,inv,ortho,&
          pbc_opt,n1,n2,n_frames,matrix)
  
  IMPLICIT NONE
  INTEGER,INTENT(IN)::diff_set,pbc_opt,ortho
  INTEGER,INTENT(IN)::n1,n2,n_frames
  DOUBLE PRECISION,DIMENSION(n_frames,n1,3),INTENT(IN)::coors1
  DOUBLE PRECISION,DIMENSION(n_frames,n2,3),INTENT(IN)::coors2
  DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box,inv
  DOUBLE PRECISION,DIMENSION(n_frames,n1,n2),INTENT(OUT)::matrix
  
  INTEGER::ii,jj,kk
  DOUBLE PRECISION::val_aux
  DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::vect,vect_aux,vect_aux2
  DOUBLE PRECISION,DIMENSION(:,:),ALLOCATABLE::tmp_box,tmp_inv

  ALLOCATE(vect(3),vect_aux(3),vect_aux2(3))
  ALLOCATE(tmp_box(3,3),tmp_inv(3,3))

  IF (diff_set==1) THEN
    DO kk=1,n_frames
      tmp_box=box(kk,:,:)
      tmp_inv=inv(kk,:,:)
      DO ii=1,n1
         vect_aux=coors1(kk,ii,:)
         DO jj=1,n2
            vect_aux2=coors2(kk,jj,:)
            matrix(kk,ii,jj)=DIST2POINTS(vect_aux,vect_aux2,tmp_box,tmp_inv,ortho,pbc_opt)
         END DO
      END DO
    END DO
  ELSE
    DO kk=1,n_frames
      tmp_box=box(kk,:,:)
      tmp_inv=inv(kk,:,:)
      DO ii=1,n1
         matrix(kk,ii,ii)=0.0d0
         vect_aux=coors1(kk,ii,:)
         DO jj=ii+1,n1
            vect_aux2=coors1(kk,jj,:)
            val_aux=DIST2POINTS(vect_aux,vect_aux2,tmp_box,tmp_inv,ortho,pbc_opt)
            matrix(kk,ii,jj)=val_aux
            matrix(kk,jj,ii)=val_aux
         END DO
      END DO
    END DO
  END IF
  
  DEALLOCATE(vect,vect_aux,vect_aux2)
  DEALLOCATE(tmp_box,tmp_inv)
 
  END SUBROUTINE DISTANCE

  FUNCTION RADIUS_OF_GYRATION (coors,weights,n_frames,n_atoms) RESULT(Rg)

    IMPLICIT NONE    
    INTEGER, INTENT(IN)::n_frames,n_atoms
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
    DOUBLE PRECISION,DIMENSION(n_atoms),INTENT(IN)::weights
    DOUBLE PRECISION,DIMENSION(n_frames)::Rg

    INTEGER::ii,jj
    DOUBLE PRECISION,DIMENSION(n_frames,3)::com
    DOUBLE PRECISION,DIMENSION(3)::vect_aux
    DOUBLE PRECISION::total_weight
    DOUBLE PRECISION::val_aux

    Rg(:) = 0.0d0
    com = CENTER_OF_MASS(coors,weights,n_frames,n_atoms)
    total_weight=SUM(weights)

    DO ii=1,n_frames
        val_aux=0.0d0
        DO jj=1,n_atoms
            vect_aux = coors(ii,jj,:)-com(ii,:)
            Rg(ii)=Rg(ii)+weights(jj)*dot_product(vect_aux,vect_aux)
        END DO
    END DO

    Rg(:)=Rg(:)/total_weight
    Rg(:)=sqrt(Rg(:))

  END FUNCTION

END MODULE MODULE_GEOMETRY
 
