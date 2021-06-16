MODULE MODULE_PBC

CONTAINS

SUBROUTINE PBC(vector,box,inv,ortho)
 
  IMPLICIT NONE
 
  DOUBLE PRECISION,DIMENSION(3),INTENT(INOUT)::vector
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box,inv
  DOUBLE PRECISION,DIMENSION(3)::vaux,vaux2
  INTEGER,INTENT(IN)::ortho
  INTEGER::ii,jj,kk
  DOUBLE PRECISION::x,L,Lhalf

  IF (ortho==1) THEN
     DO ii=1,3
        vector(ii)=vector(ii)-box(ii,ii)*ANINT(vector(ii)/box(ii,ii))
     END DO

  ELSE
     IF (.TRUE.) THEN
        !vaux(1)=inv(1,1)*vector(1)
        !vaux(2)=inv(2,1)*vector(1)+inv(2,2)*vector(2)
        !vaux(3)=inv(3,1)*vector(1)+inv(3,2)*vector(2)+inv(3,3)*vector(3)
        vaux(1)=inv(1,1)*vector(1)+inv(2,1)*vector(2)+inv(3,1)*vector(3)
        vaux(2)=                   inv(2,2)*vector(2)+inv(3,2)*vector(3)
        vaux(3)=                                      inv(3,3)*vector(3)
        vaux(1)=vaux(1)-NINT(vaux(1))*1.0
        vaux(2)=vaux(2)-NINT(vaux(2))*1.0
        vaux(3)=vaux(3)-NINT(vaux(3))*1.0
        vector(1)=box(1,1)*vaux(1)+box(2,1)*vaux(2)+box(3,1)*vaux(3)
        vector(2)=                 box(2,2)*vaux(2)+box(3,2)*vaux(3)
        vector(3)=                                  box(3,3)*vaux(3)
     ELSE
        L=1000000.0d0
        vaux2=0.0d0
        DO ii=-1,1,1
           DO jj=-1,1,1
              DO kk=-1,1,1
                 vaux(:)=vector(:)+ii*box(1,:)+jj*box(2,:)+kk*box(3,:)
                 x=(vaux(1)*vaux(1)+vaux(2)*vaux(2)+vaux(3)*vaux(3))
                 IF (L>x) THEN
                    vaux2=vaux
                    L=x
                 END IF
              END DO
           END DO
        END DO
        vector(:)=vaux2(:)
     END IF

  END IF
  
END SUBROUTINE PBC

!SUBROUTINE PBC_FRAMES(vector_frames,box,inv,ortho,nn)
!
!  IMPLICIT NONE
!
!  INTEGER,INTENT(IN)::nn,ortho
!  DOUBLE PRECISION,DIMENSION(nn,3),INTENT(INOUT)::vector_frames
!  DOUBLE PRECISION,DIMENSION(nn,3,3),INTENT(IN)::box,inv
!
!  INTEGER::ii
!  DOUBLE PRECISION,DIMENSION(3)::vect_aux
!
!  DO ii=1,nn
!     vect_aux(:)=vector_frames(ii,:)
!     CALL PBC(vect_aux,box(ii,:,:),inv(ii,:,:),ortho)
!     vector_frames(ii,:)=vect_aux(:)
!  END DO
!
!END SUBROUTINE PBC_FRAMES

SUBROUTINE PBC_TENSOR(tensor, box, inv, ortho, n_frames, n_atoms)

  IMPLICIT NONE

  INTEGER,INTENT(IN)::n_frames, n_atoms ,ortho
  DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(INOUT)::tensor
  DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box,inv

  INTEGER::ii,jj
  DOUBLE PRECISION,DIMENSION(3)::vect_aux

  DO ii=1,n_atoms
    DO jj=1,n_frames
        vect_aux(:)=tensor(jj,ii,:)
        CALL PBC(vect_aux,box(jj,:,:),inv(jj,:,:),ortho)
        tensor(jj,ii,:)=vect_aux(:)
    END DO
  END DO

END SUBROUTINE PBC_TENSOR


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



! SUBROUTINE COMPACT_PBC_STRUCTURE(pbc_opt,list_com,coors,box,ortho,numat_com,numat_glob,com)


!   IMPLICIT NONE

!   INTEGER,INTENT(IN)::pbc_opt,ortho,numat_com,numat_glob
!   DOUBLE PRECISION,DIMENSION(numat_glob,3),INTENT(IN)::coors
!   DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box
!   INTEGER,DIMENSION(numat_com),INTENT(IN)::list_com
!   DOUBLE PRECISION,DIMENSION(3),INTENT(OUT)::com

!   INTEGER::ii,jj,kk,nn
!   DOUBLE PRECISION,DIMENSION(:),ALLOCATABLE::pix,vect_aux,old_ref
!   DOUBLE PRECISION,DIMENSION(:,:),ALLOCATABLE::comaux
!   DOUBLE PRECISION::theta,pi
!   DOUBLE PRECISION::x,y,z,Lx,Ly,Lz


!   com=0.0d0

!   IF (pbc_opt==0) THEN

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

! END SUBROUTINE COMPACT_PBC_STRUCTURE


END MODULE MODULE_PBC
