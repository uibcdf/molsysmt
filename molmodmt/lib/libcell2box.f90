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

SUBROUTINE BOX2INVBOX (box,invbox)

  IMPLICIT NONE
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(OUT)::invbox

  invbox=0.0d0

  invbox(1,1)=1.0d0/box(1,1)
  invbox(2,2)=1.0d0/box(2,2)
  invbox(3,3)=1.0d0/box(3,3)

  invbox(2,1)=-box(2,1)/(box(1,1)*box(2,2))
  invbox(3,1)=(box(2,1)*box(3,2)-box(3,1)*box(2,2))/(box(1,1)*box(2,2)*box(3,3))
  invbox(3,2)=-box(3,2)/(box(2,2)*box(3,3))

END SUBROUTINE BOX2INVBOX

SUBROUTINE CELL2BOX (cell,box,volume,ortho)

  IMPLICIT NONE
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(INOUT)::cell
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(OUT)::box
  DOUBLE PRECISION,INTENT(OUT)::volume
  INTEGER,INTENT(OUT)::ortho
  DOUBLE PRECISION::alpha,beta,gamma,x,y,z
  DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002

  ortho=0
  box=0.0d0
  alpha=cell(1,2)
  beta=cell(1,3)
  gamma=cell(2,3)
  x=cell(1,1)
  y=cell(2,2)
  z=cell(3,3)

  box(1,1)=x
  IF ((alpha==90.0d0).and.(beta==90.0d0).and.(gamma==90.0d0)) THEN
     box(2,2)=y
     box(3,3)=z
     volume=x*y*z
     ortho=1
  ELSE IF ((alpha==0.0d0).and.(beta==0.0d0).and.(gamma==0.0d0)) THEN
     cell(1,2)=90.0d0
     cell(1,3)=90.0d0
     cell(2,3)=90.0d0
     box(2,2)=y
     box(3,3)=z
     volume=x*y*z
     ortho=1
  ELSE
     alpha=alpha/fact_pi_div_180
     beta=beta/fact_pi_div_180
     gamma=gamma/fact_pi_div_180
     box(2,1)=y*cos(gamma)
     box(2,2)=y*sin(gamma)  ! sqrt(y**2-box(2,2)**2)
     box(3,1)=z*cos(beta)
     box(3,2)=z*(cos(alpha)-cos(beta)*cos(gamma))/sin(gamma) 
     box(3,3)=sqrt(z*z-box(3,1)**2-box(3,2)**2)
     volume=box(1,1)*box(2,2)*box(3,3)
  END IF

END SUBROUTINE CELL2BOX

!! This function is used by gro, xtc and trr
SUBROUTINE BOX2CELL (box,cell,volume,ortho)

  IMPLICIT NONE
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(OUT)::cell
  DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::box
  DOUBLE PRECISION,INTENT(OUT)::volume
  INTEGER,INTENT(OUT)::ortho
  DOUBLE PRECISION::alpha,beta,gamma,x,y,z
  DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002

  ortho=0
  cell=0.0d0
  volume=0.0d0

  IF ((box(2,1)==0.0d0).and.(box(3,1)==0.0d0).and.(box(3,2)==0.0d0)) THEN
     volume=box(1,1)*box(2,2)*box(3,3)
     cell(1,1)=box(1,1)
     cell(2,2)=box(2,2)
     cell(3,3)=box(3,3)
     cell(1,2)=90.0d0
     cell(1,3)=90.0d0
     cell(2,3)=90.0d0
     ortho=1
  ELSE
     volume=box(1,1)*box(2,2)*box(3,3)
     x=box(1,1)
     y=sqrt(box(2,1)**2+box(2,2)**2)
     z=sqrt(box(3,1)**2+box(3,2)**2+box(3,3)**2)
     cell(1,1)=x
     cell(2,2)=y
     cell(3,3)=z
     cell(2,3)=(acos(dot_product(box(2,:),box(1,:))/(x*y)))/fact_pi_div_180 ! gamma
     cell(1,3)=(acos(dot_product(box(3,:),box(1,:))/(x*z)))/fact_pi_div_180 ! beta
     cell(1,2)=(acos(dot_product(box(3,:),box(2,:))/(x*y)))/fact_pi_div_180 ! alpha
  END IF

END SUBROUTINE BOX2CELL

SUBROUTINE WRAP (coors,box,ortho,natom)

  INTEGER,INTENT(IN)::ortho,natom
  double precision,DIMENSION(3,3),INTENT(IN)::box
  double precision,dimension(natom,3),intent(INOUT)::coors

  DOUBLE PRECISION::Lx,Ly,Lz,x,y,z

  INTEGER::ii,jj,nn

  Lx=box(1,1)
  Ly=box(2,2)
  Lz=box(3,3)

  IF (ortho==1) THEN

     DO ii=1,natom
        x=coors(ii,1)
        y=coors(ii,2)
        z=coors(ii,3)
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
        coors(ii,:)=(/x,y,z/)
     END DO
     
  ELSE

     print*,'WRAP function not implemented for not orthorhombic unit cells.'

  END IF

END SUBROUTINE WRAP


