MODULE MODULE_BOX

CONTAINS


  !! This function is not used by gro, xtc and trr
  
  !! box(1,1) = v1_x, box(1,2) = v1_y, box(1,3) = v1_z
  !! box(2,1) = v2_x, box(2,2) = v2_y, box(2,3) = v2_z
  !! box(3,1) = v3_x, box(3,2) = v3_y, box(3,3) = v3_z
  
  !! Para gromacs:
  !!
  !! box(1,1) = v1_x, box(1,2) = 0,    box(1,3) = 0
  !! box(2,1) = v2_x, box(2,2) = v2_y, box(2,3) = 0
  !! box(3,1) = v3_x, box(3,2) = v3_y, box(3,3) = v3_z
  !!
  !! cell(1,1)= v1_x, cell(1,2)= alpha cell(1,3)= beta
  !! cell(2,1)= 0,    cell(2,2)= v2_y, cell(2,3)= gamma
  !! cell(3,1)= 0,    cell(3,2)= 0,    cell(3,3)= v3_z
  
  SUBROUTINE BOX2INVBOX (box,invbox,nframes)
  
    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(OUT)::invbox
  
    invbox=0.0d0
  
    invbox(:,1,1)=1.0d0/box(:,1,1)
    invbox(:,2,2)=1.0d0/box(:,2,2)
    invbox(:,3,3)=1.0d0/box(:,3,3)
  
    invbox(:,2,1)=-box(:,2,1)/(box(:,1,1)*box(:,2,2))
    invbox(:,3,1)=(box(:,2,1)*box(:,3,2)-box(:,3,1)*box(:,2,2))/(box(:,1,1)*box(:,2,2)*box(:,3,3))
    invbox(:,3,2)=-box(:,3,2)/(box(:,2,2)*box(:,3,3))
  
  END SUBROUTINE BOX2INVBOX
  
  SUBROUTINE CELL2BOX (cell,box,volume,ortho,nframes)
  
    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    INTEGER::ii
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(INOUT)::cell
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(OUT)::box
    DOUBLE PRECISION,DIMENSION(nframes),INTENT(OUT)::volume
    INTEGER,INTENT(OUT)::ortho
    DOUBLE PRECISION::alpha,beta,gamm,x,y,z
    DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
  
    DO ii=1,nframes
  
      ortho=0
      box=0.0d0
      alpha=cell(ii,1,2)
      beta=cell(ii,1,3)
      gamm=cell(ii,2,3)
      x=cell(ii,1,1)
      y=cell(ii,2,2)
      z=cell(ii,3,3)
  
      box(ii,1,1)=x
      IF ((alpha==90.0d0).and.(beta==90.0d0).and.(gamm==90.0d0)) THEN
         box(ii,2,2)=y
         box(ii,3,3)=z
         volume(ii)=x*y*z
         ortho=1
      ELSE IF ((alpha==0.0d0).and.(beta==0.0d0).and.(gamm==0.0d0)) THEN
         cell(ii,1,2)=90.0d0
         cell(ii,1,3)=90.0d0
         cell(ii,2,3)=90.0d0
         box(ii,2,2)=y
         box(ii,3,3)=z
         volume(ii)=x*y*z
         ortho=1
      ELSE
         alpha=alpha/fact_pi_div_180
         beta=beta/fact_pi_div_180
         gamm=gamm/fact_pi_div_180
         box(ii,2,1)=y*cos(gamm)
         box(ii,2,2)=y*sin(gamm)  ! sqrt(y**2-box(2,2)**2)
         box(ii,3,1)=z*cos(beta)
         box(ii,3,2)=z*(cos(alpha)-cos(beta)*cos(gamm))/sin(gamm) 
         box(ii,3,3)=sqrt(z*z-box(ii,3,1)**2-box(ii,3,2)**2)
         volume(ii)=box(ii,1,1)*box(ii,2,2)*box(ii,3,3)
      END IF
  
    END DO
  END SUBROUTINE CELL2BOX
  
  !! This function is used by gro, xtc and trr
  SUBROUTINE BOX2CELL (box,cell,volume,ortho,nframes)
  
    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    INTEGER::ii
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(OUT)::cell
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes),INTENT(OUT)::volume
    INTEGER,INTENT(OUT)::ortho
    DOUBLE PRECISION::x,y,z
    DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
  
    ortho=0
    cell=0.0d0
    volume=0.0d0
  
    DO ii=1,nframes 
  
      IF ((box(ii,2,1)==0.0d0).and.(box(ii,3,1)==0.0d0).and.(box(ii,3,2)==0.0d0)) THEN
         volume(ii)=box(ii,1,1)*box(ii,2,2)*box(ii,3,3)
         cell(ii,1,1)=box(ii,1,1)
         cell(ii,2,2)=box(ii,2,2)
         cell(ii,3,3)=box(ii,3,3)
         cell(ii,1,2)=90.0d0
         cell(ii,1,3)=90.0d0
         cell(ii,2,3)=90.0d0
         ortho=1
      ELSE
         volume(ii)=box(ii,1,1)*box(ii,2,2)*box(ii,3,3)
         x=box(ii,1,1)
         y=sqrt(box(ii,2,1)**2+box(ii,2,2)**2)
         z=sqrt(box(ii,3,1)**2+box(ii,3,2)**2+box(ii,3,3)**2)
         cell(ii,1,1)=x
         cell(ii,2,2)=y
         cell(ii,3,3)=z
         cell(ii,2,3)=(acos(dot_product(box(ii,2,:),box(ii,1,:))/(x*y)))/fact_pi_div_180 ! gamma
         cell(ii,1,3)=(acos(dot_product(box(ii,3,:),box(ii,1,:))/(x*z)))/fact_pi_div_180 ! beta
         cell(ii,1,2)=(acos(dot_product(box(ii,3,:),box(ii,2,:))/(x*y)))/fact_pi_div_180 ! alpha
      END IF
  
    END DO
  
  END SUBROUTINE BOX2CELL
  
  SUBROUTINE WRAP (coors,box,ortho,natoms,nframes)
  
    INTEGER,INTENT(IN)::ortho,natoms,nframes
    double precision,DIMENSION(nframes,3,3),INTENT(IN)::box
    double precision,dimension(nframes,natoms,3),intent(INOUT)::coors
  
    DOUBLE PRECISION::Lx,Ly,Lz,x,y,z
  
    INTEGER::ii,jj,nn
  
    DO jj=1,nframes
  
      Lx=box(jj,1,1)
      Ly=box(jj,2,2)
      Lz=box(jj,3,3)
  
      IF (ortho==1) THEN
  
         DO ii=1,natoms
            x=coors(jj,ii,1)
            y=coors(jj,ii,2)
            z=coors(jj,ii,3)
            IF (x<0.0d0) THEN
               nn=CEILING(abs(x)/Lx)
               x=x+nn*Lx
            ELSE IF (x>=Lx) THEN
               nn=INT(x/Lx)
               x=x-nn*Lx
            END IF
            IF (y<0.0d0) THEN
               nn=CEILING(abs(y)/Ly)
               y=y+nn*Ly
            ELSE IF (y>=Ly) THEN
               nn=INT(y/Ly)
               y=y-nn*Ly
            END IF
            IF (z<0.0d0) THEN
               nn=CEILING(abs(z)/Lz)
               z=z+nn*Lz
            ELSE IF (z>=Lz) THEN
               nn=INT(z/Lz)
               z=z-nn*Lz
            END IF
            coors(jj,ii,:)=(/x,y,z/)
         END DO
         
      ELSE
  
         print*,'WRAP function not implemented for not orthorhombic unit cells.'
  
      END IF
 
    END DO

  END SUBROUTINE WRAP

END MODULE MODULE_BOX
