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
  
  SUBROUTINE DISTANCE(diff_set,coors1,coors2,box,inv,ortho,&
          pbc_opt,n1,n2,matrix)
  !! No need to start arrays in 0
  
  IMPLICIT NONE
  INTEGER,INTENT(IN)::diff_set,pbc_opt,ortho
  INTEGER,INTENT(IN)::n1,n2
  DOUBLE PRECISION,DIMENSION(n1,3),INTENT(IN)::coors1
  DOUBLE PRECISION,DIMENSION(n2,3),INTENT(IN)::coors2
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box,inv
  DOUBLE PRECISION,DIMENSION(n1,n2),INTENT(OUT)::matrix
  
  INTEGER::ii,jj
  DOUBLE PRECISION::val_aux
  DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::vect,vect_aux,vect_aux2
  
  ALLOCATE(vect(3),vect_aux(3),vect_aux2(3))
  
  IF (diff_set==1) THEN
     
     DO ii=1,n1
        vect_aux=coors1(ii,:)
        DO jj=1,n2
           vect_aux2=coors2(jj,:)
           matrix(ii,jj)=DIST2POINTS(vect_aux,vect_aux2,box,inv,ortho,pbc_opt)
        END DO
     END DO
     
  ELSE
     
     DO ii=1,n1
        matrix(ii,ii)=0.0d0
        vect_aux=coors1(ii,:)
        DO jj=ii+1,n1
           vect_aux2=coors1(jj,:)
           val_aux=DIST2POINTS(vect_aux,vect_aux2,box,inv,ortho,pbc_opt)
           matrix(ii,jj)=val_aux
           matrix(jj,ii)=val_aux
        END DO
     END DO
     
  END IF
  
  DEALLOCATE(vect,vect_aux,vect_aux2)
 
  END SUBROUTINE DISTANCE

