MODULE MODULE_GEOMETRY

USE MODULE_MATH
USE MODULE_PBC
!USE MODULE_COM
USE MODULE_BOX

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

  FUNCTION ANG3VECTS (vec1,vec2,vec3) RESULT (ang)
  
    IMPLICIT NONE
    
    DOUBLE PRECISION,dimension(3),intent(in)::vec1,vec2,vec3
    DOUBLE PRECISION::ang
    DOUBLE PRECISION,dimension(3)::aux1,aux2,aux3
    DOUBLE PRECISION::cosa
    integer::signo
    double precision::pi
  
    cosa=0.0d0
    signo=0
    ang=0.0d0
    pi=3.14159265358979
    
    aux1=0.0d0
    aux2=0.0d0
    
    CALL PRODUCT_VECT(vec1,vec2,aux1)
    CALL PRODUCT_VECT(vec2,vec3,aux2)
    
    cosa=(aux1(1)*aux2(1)+aux1(2)*aux2(2)+aux1(3)*aux2(3))/(sqrt(dot_product(aux1,aux1))*sqrt(dot_product(aux2,aux2)))
  
    IF (cosa>=1.0d0) THEN 
       cosa=1.0d0
    END IF
    IF (cosa<=-1.0d0) THEN 
       cosa=-1.0d0
    END IF
  
    cosa=(DACOS(cosa))*(180.0d0/pi)

    IF (cosa>180.0d0) THEN
        print*,'ERROR: ANGLE > 180.0 DEGREES'
        STOP
    END IF
  
    aux3=0.0d0
    
    CALL PRODUCT_VECT(aux1,aux2,aux3)
    
    IF ( dot_product(aux3,vec2) <= 0.0d0 ) THEN
       signo=-1
    ELSE
       signo=+1
    END IF
  
    ang=cosa*signo
  
  END FUNCTION ANG3VECTS


  SUBROUTINE DISTANCE(diff_set, coors1, coors2, box, ortho, pbc_opt, n1, n2, n_frames, matrix)
  
  IMPLICIT NONE
  INTEGER,INTENT(IN):: diff_set, ortho, pbc_opt, n1, n2, n_frames
  DOUBLE PRECISION,DIMENSION(n_frames,n1,3),INTENT(IN)::coors1
  DOUBLE PRECISION,DIMENSION(n_frames,n2,3),INTENT(IN)::coors2
  DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box
  DOUBLE PRECISION,DIMENSION(n_frames,n1,n2),INTENT(OUT)::matrix

  DOUBLE PRECISION,DIMENSION(n_frames,3,3)::inv
  
  INTEGER::ii,jj,kk
  DOUBLE PRECISION::val_aux
  DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::vect,vect_aux,vect_aux2
  DOUBLE PRECISION,DIMENSION(:,:),ALLOCATABLE::tmp_box,tmp_inv

  ALLOCATE(vect(3),vect_aux(3),vect_aux2(3))
  ALLOCATE(tmp_box(3,3),tmp_inv(3,3))

  inv=0.0d0
  IF (pbc_opt==1) THEN
    CALL BOX2INVBOX (box, inv, n_frames)
  END IF

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
  
  SUBROUTINE DISTANCE_PAIRS(coors1, coors2, box, ortho, pbc_opt, n1, n2, n_frames, matrix)
  
  IMPLICIT NONE
  INTEGER,INTENT(IN):: ortho, pbc_opt, n1, n2, n_frames
  DOUBLE PRECISION,DIMENSION(n_frames,n1,3),INTENT(IN)::coors1
  DOUBLE PRECISION,DIMENSION(n_frames,n2,3),INTENT(IN)::coors2
  DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box
  DOUBLE PRECISION,DIMENSION(n_frames,n1),INTENT(OUT)::matrix

  DOUBLE PRECISION,DIMENSION(n_frames,3,3)::inv
  
  INTEGER::ii,kk
  DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::vect,vect_aux,vect_aux2
  DOUBLE PRECISION,DIMENSION(:,:),ALLOCATABLE::tmp_box,tmp_inv

  ALLOCATE(vect(3),vect_aux(3),vect_aux2(3))
  ALLOCATE(tmp_box(3,3),tmp_inv(3,3))

  inv=0.0d0
  IF (pbc_opt==1) THEN
    CALL BOX2INVBOX (box, inv, n_frames)
  END IF

  DO kk=1,n_frames
    tmp_box=box(kk,:,:)
    tmp_inv=inv(kk,:,:)
    DO ii=1,n1
      vect_aux=coors1(kk,ii,:)
      vect_aux2=coors2(kk,ii,:)
      matrix(kk,ii)=DIST2POINTS(vect_aux,vect_aux2,tmp_box,tmp_inv,ortho,pbc_opt)
    END DO
  END DO
  
  DEALLOCATE(vect,vect_aux,vect_aux2)
  DEALLOCATE(tmp_box,tmp_inv)
 
  END SUBROUTINE DISTANCE_PAIRS


  !FUNCTION RADIUS_OF_GYRATION (coors,weights,n_frames,n_atoms) RESULT(Rg)

  !  IMPLICIT NONE    
  !  INTEGER, INTENT(IN)::n_frames,n_atoms
  !  DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
  !  DOUBLE PRECISION,DIMENSION(n_atoms),INTENT(IN)::weights
  !  DOUBLE PRECISION,DIMENSION(n_frames)::Rg

  !  INTEGER::ii,jj
  !  DOUBLE PRECISION,DIMENSION(n_frames,3)::com
  !  DOUBLE PRECISION,DIMENSION(3)::vect_aux
  !  DOUBLE PRECISION::total_weight
  !  DOUBLE PRECISION::val_aux

  !  Rg(:) = 0.0d0
  !  com = CENTER_OF_MASS(coors,weights,n_frames,n_atoms)
  !  total_weight=SUM(weights)

  !  DO ii=1,n_frames
  !      val_aux=0.0d0
  !      DO jj=1,n_atoms
  !          vect_aux = coors(ii,jj,:)-com(ii,:)
  !          Rg(ii)=Rg(ii)+weights(jj)*dot_product(vect_aux,vect_aux)
  !      END DO
  !  END DO

  !  Rg(:)=Rg(:)/total_weight
  !  Rg(:)=sqrt(Rg(:))

  !END FUNCTION

  SUBROUTINE TRANSLATE(coors, shifts, frame_indices, n_atoms, n_frames, n_frame_indices)
 
    IMPLICIT NONE
    INTEGER,INTENT(IN)::n_frames, n_atoms, n_frame_indices
    DOUBLE PRECISION,DIMENSION(n_frames, n_atoms, 3),INTENT(INOUT)::coors
    DOUBLE PRECISION,DIMENSION(n_frame_indices, 3),INTENT(IN)::shifts
    INTEGER,DIMENSION(n_frame_indices),INTENT(IN)::frame_indices
    INTEGER::ii,jj,frame_index

    DO ii=1,n_frame_indices
      frame_index = frame_indices(ii)+1
      DO jj=1,n_atoms
          coors(frame_index,jj,:)=coors(frame_index,jj,:)+shifts(ii,:)
      END DO
    END DO

  END SUBROUTINE

  SUBROUTINE DIHEDRAL_ANGLES (angs, coors, box, ortho, pbc_opt, quartets, n_angs, n_atoms, n_frames)

    INTEGER,INTENT(IN)::ortho, n_atoms, n_angs, pbc_opt, n_frames
    INTEGER,DIMENSION(n_angs,4),INTENT(IN)::quartets
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(IN)::coors
    DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(n_frames,n_angs),INTENT(OUT)::angs

    DOUBLE PRECISION,DIMENSION(n_frames,3,3)::inv
    DOUBLE PRECISION,DIMENSION(3,3)::tmp_box,tmp_inv
    INTEGER::ii,jj
    INTEGER::atom1,atom2,atom3,atom4
    DOUBLE PRECISION,DIMENSION(3)::vect1,vect2,vect3
    
    inv=0.0d0
    IF (pbc_opt==1) THEN
        CALL BOX2INVBOX (box, inv, n_frames)
    END IF

    DO jj=1,n_frames
        tmp_box=box(jj,:,:)
        tmp_inv=inv(jj,:,:)
        DO ii=1,n_angs
            atom1=quartets(ii,1)+1
            atom2=quartets(ii,2)+1
            atom3=quartets(ii,3)+1
            atom4=quartets(ii,4)+1
            vect1=coors(jj,atom2,:)-coors(jj,atom1,:)
            vect2=coors(jj,atom3,:)-coors(jj,atom2,:)
            vect3=coors(jj,atom4,:)-coors(jj,atom3,:)
            IF (pbc_opt==1) THEN
                CALL PBC (vect1,tmp_box,tmp_inv,ortho)
                CALL PBC (vect2,tmp_box,tmp_inv,ortho)
                CALL PBC (vect3,tmp_box,tmp_inv,ortho)
            END IF
            angs(jj,ii)=ANG3VECTS(vect1,vect2,vect3)
        END DO
    END DO

END SUBROUTINE DIHEDRAL_ANGLES

END MODULE MODULE_GEOMETRY
 
