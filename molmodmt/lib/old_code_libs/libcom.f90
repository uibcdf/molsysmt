MODULE MODULE_COM

USE MODULE_PBC

CONTAINS

  FUNCTION WEIGHTED_CENTER(coors,weights,natoms,nframes) RESULT(com)
 
    IMPLICIT NONE
 
    INTEGER,INTENT(IN)::natoms,nframes
    DOUBLE PRECISION,DIMENSION(nframes,natoms,3),INTENT(IN)::coors
    DOUBLE PRECISION,DIMENSION(natoms),INTENT(IN)::weights
    DOUBLE PRECISION,DIMENSION(nframes,3)::com
 
    INTEGER::ii,ll
    DOUBLE PRECISION::total_weight
 
    com(:,:)=0.0d0
    total_weight=SUM(weights)
 

    DO ll=1,nframes
      DO ii=1,natoms
          com(ll,:)=com(ll,:)+weights(ii)*coors(ll,ii,:)
      END DO
      com(ll,:)=com(ll,:)/total_weight
    END DO

 
  END FUNCTION WEIGHTED_CENTER


! SUBROUTINE UNBOUNDED_CENTER_3DPBC(pbc_opt,coors,box,ortho,com)


!   IMPLICIT NONE

!   INTEGER,INTENT(IN)::pbc_opt,ortho,numat_com,numat_glob
!   DOUBLE PRECISION,DIMENSION(numat,3),INTENT(IN)::coors
!   DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box
!   DOUBLE PRECISION,DIMENSION(3),INTENT(OUT)::com

!   INTEGER::ii,jj,kk,nn
!   DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::pix,vect_aux,old_ref
!   DOUBLE PRECISION,DIMENSION(:,:),ALLOCATABLE::comaux
!   DOUBLE PRECISION::theta,pi
!   DOUBLE PRECISION::x,y,z,Lx,Ly,Lz


!   com=0.0d0

!   IF (pbc_opt==0) THEN

!      print 'This function is called with PBC... are you sure you want to apply this?'
!      DO ii=1,numat_com
!         jj=list_com(ii)+1
!         com(:)=com(:)+coors(jj,:)
!      END DO
!      com(:)=com(:)/(numat_com*1.0d0)

!   ELSE

!      IF (ortho==1) THEN

! ! Bai, Linge; Breen, David (2008). "Calculating Center of Mass in an Unbounded 2D Environment".
! ! Journal of Graphics, GPU, and Game Tools 13 (4): 53–60. doi:10.1080/2151237X.2008.10129266

!         ALLOCATE(comaux(3,2),vect_aux(3),pix(3),old_ref(3))
!         comaux=0.0d0
!         vect_aux=0.0d0
!         pi=3.1415926535897931*2.0d0
!         DO ii=1,3
!            pix(ii)=box(ii,ii)/pi
!         END DO
        
!         DO ii=1,numat_com
!            jj=list_com(ii)+1
!            DO kk=1,3
!               theta=coors(jj,kk)/pix(kk)
!               comaux(kk,1)=comaux(kk,1)+pix(kk)*dcos(theta)
!               comaux(kk,2)=comaux(kk,2)+pix(kk)*dsin(theta)
!            END DO
!         END DO
        
!         comaux(:,:)=comaux(:,:)/(numat_com*1.0d0)
        
!         theta=3.1415926535897931

!         DO ii=1,3
!            com(ii)=datan2(-comaux(ii,2),-comaux(ii,1))+theta
!            com(ii)=pix(ii)*com(ii)
!         END DO

!         DEALLOCATE(comaux,pix)

!         ! Recompute com with new reference

!         old_ref=com
!         com=0.0d0
!         Lx=box(1,1) 
!         Ly=box(2,2) 
!         Lz=box(3,3) 
!         vect_aux(1)=(Lx/2.0d0)-old_ref(1)
!         vect_aux(2)=(Ly/2.0d0)-old_ref(2)
!         vect_aux(3)=(Lz/2.0d0)-old_ref(3)


!         DO ii=1,numat_com
!            jj=list_com(ii)+1
!            x=coors(jj,1)+vect_aux(1) 
!            y=coors(jj,2)+vect_aux(2) 
!            z=coors(jj,3)+vect_aux(3) 
!            IF (x<0.0d0) THEN
!               nn=CEILING(abs(x)/Lx)
!               x=x+nn*Lx
!            ELSE IF (x>=Lx) THEN
!               nn=INT(x/Lx)
!               x=x-nn*Lx
!            END IF
!            IF (y<0.0d0) THEN
!               nn=CEILING(abs(y)/Ly)
!               y=y+nn*Ly
!            ELSE IF (y>=Ly) THEN
!               nn=INT(y/Ly)
!               y=y-nn*Ly
!            END IF
!            IF (z<0.0d0) THEN
!               nn=CEILING(abs(z)/Lz)
!               z=z+nn*Lz
!            ELSE IF (z>=Lz) THEN
!               nn=INT(z/Lz)
!               z=z-nn*Lz
!            END IF
!            x=x-vect_aux(1)
!            y=y-vect_aux(2)
!            z=z-vect_aux(3)
!            com(:)=com(:)+(/x,y,z/)
!         END DO

!         com=com/(numat_com*1.0d0)

!         x=com(1)
!         y=com(2)
!         z=com(3)

!         IF (x<0.0d0) THEN
!            nn=CEILING(abs(x)/Lx)
!            x=x+nn*Lx
!         ELSE IF (x>=Lx) THEN
!            nn=INT(x/Lx)
!            x=x-nn*Lx
!         END IF
!         IF (y<0.0d0) THEN
!            nn=CEILING(abs(y)/Ly)
!            y=y+nn*Ly
!         ELSE IF (y>=Ly) THEN
!            nn=INT(y/Ly)
!            y=y-nn*Ly
!         END IF
!         IF (z<0.0d0) THEN
!            nn=CEILING(abs(z)/Lz)
!            z=z+nn*Lz
!         ELSE IF (z>=Lz) THEN
!            nn=INT(z/Lz)
!            z=z-nn*Lz
!         END IF

!         com(:)=(/x,y,z/)

!         DEALLOCATE(vect_aux,old_ref)

!      ELSE

!         print*,'Function not implemented for not orthorhombic unit cells.'

!      END IF

!   END IF

! END SUBROUTINE UNBOUNDED_CENTER_3DPBC


END MODULE MODULE_COM
