MODULE MODULE_GEOMETRY

USE MODULE_PBC
USE MODULE_MATH

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
  
  !SUBROUTINE DISTANCE_titj(diff_set,coors1,coors2,box,inv,ortho,&
  !                         pbc_opt,n1,n2,nframes,matrix)
  ! Esta por implementar, pero sería con tiempos cruzados.

  SUBROUTINE DISTANCE_titi(diff_set,coors1,coors2,box,inv,ortho,&
          pbc_opt,n1,n2,nframes,matrix)
  
  IMPLICIT NONE
  INTEGER,INTENT(IN)::diff_set,pbc_opt,ortho
  INTEGER,INTENT(IN)::n1,n2,nframes
  DOUBLE PRECISION,DIMENSION(nframes,n1,3),INTENT(IN)::coors1
  DOUBLE PRECISION,DIMENSION(nframes,n2,3),INTENT(IN)::coors2
  DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box,inv
  DOUBLE PRECISION,DIMENSION(nframes,n1,n2),INTENT(OUT)::matrix
  
  INTEGER::ii,jj,kk
  DOUBLE PRECISION::val_aux
  DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::vect,vect_aux,vect_aux2
  DOUBLE PRECISION,DIMENSION(:,:),ALLOCATABLE::tmp_box,tmp_inv

  ALLOCATE(vect(3),vect_aux(3),vect_aux2(3))
  ALLOCATE(tmp_box(3,3),tmp_inv(3,3))

  !OPEN(unit = 500, file = "salida.fortran")
  !WRITE(500,*)"SI ENTRA"
  !WRITE(500,*)diff_set
  !CLOSE(500)

  IF (diff_set==1) THEN
    DO kk=1,nframes
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
    DO kk=1,nframes
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
 
  END SUBROUTINE DISTANCE_titi

END MODULE MODULE_GEOMETRY
