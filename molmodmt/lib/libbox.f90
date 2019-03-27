MODULE MODULE_BOX

USE MODULE_PBC

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

  SUBROUTINE UNWRAP(coors,molecules,molecules_start,bonds,bonds_start, &
      box,ortho,inv,n_frames,n_atoms,n_molecules,n_molecules_start,n_bonds,n_bonds_start)

    IMPLICIT NONE

    INTEGER,INTENT(IN):: n_frames, n_atoms, ortho
    INTEGER,INTENT(IN):: n_molecules, n_molecules_start, n_bonds, n_bonds_start

    INTEGER,DIMENSION(n_molecules),INTENT(IN)::molecules
    INTEGER,DIMENSION(n_molecules_start),INTENT(IN)::molecules_start
    INTEGER,DIMENSION(n_bonds),INTENT(IN)::bonds
    INTEGER,DIMENSION(n_bonds_start),INTENT(IN)::bonds_start
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(INOUT)::coors
    DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box,inv

    INTEGER:: ii,jj,kk
    INTEGER:: molecule_start, molecule_end, molecule_natoms
    INTEGER:: n_left,n_storage
    INTEGER:: atom_id1,atom_id2
    LOGICAL,DIMENSION(n_atoms)::aux_filter
    DOUBLE PRECISION,DIMENSION(n_frames,3)::vect_aux
    INTEGER,DIMENSION(:),ALLOCATABLE::left,storage
    
    aux_filter(:)=.FALSE.

    DO ii=1,n_molecules_start-1

        molecule_start=molecules_start(ii)+1
        molecule_end=molecules_start(ii+1)
        molecule_natoms=molecule_end-molecule_start+1

        n_left=1
        ALLOCATE(left(n_left),storage(molecule_natoms))
        left(1)=molecules(molecule_start)+1

        DO WHILE (n_left>0)
            n_storage=0
            DO jj=1,n_left
                atom_id1 = left(jj)
                DO kk=bonds_start(atom_id1)+1,bonds_start(atom_id1+1)
                    atom_id2=bonds(kk)+1
                    IF (aux_filter(atom_id2).eqv..FALSE.) THEN
                        vect_aux(:,:)=coors(:,atom_id2,:)-coors(:,atom_id1,:)
                        CALL PBCARRAY(vect_aux,box,inv,ortho,n_frames)
                        coors(:,atom_id2,:)=coors(:,atom_id1,:)+vect_aux(:,:)
                        aux_filter(atom_id2)=.TRUE.
                        n_storage=n_storage+1
                        storage(n_storage)=atom_id2
                    END IF
                END DO
            END DO
            n_left=n_storage
            IF (n_left>0) THEN
                DEALLOCATE(left)
                ALLOCATE(left(n_left))
                left(:)=storage(1:n_left)
            END IF
        END DO

        DEALLOCATE(left,storage)

    END DO

  END SUBROUTINE UNWRAP

END MODULE MODULE_BOX

