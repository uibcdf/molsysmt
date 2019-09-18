MODULE MODULE_BOX

USE MODULE_PBC
USE MODULE_COM

CONTAINS

  !! This box is not used by gro, xtc and trr:
  
  !! box(1,1) = v1_x, box(1,2) = v1_y, box(1,3) = v1_z
  !! box(2,1) = v2_x, box(2,2) = v2_y, box(2,3) = v2_z
  !! box(3,1) = v3_x, box(3,2) = v3_y, box(3,3) = v3_z
  
  !! The gromacs box and cell are:
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

  SUBROUTINE LENGTH_EDGES_BOX(box, lengths, nframes)

    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes,3),INTENT(OUT)::lengths
    INTEGER::ii

    lengths = 0.0d0

    DO ii=1,nframes

        lengths(ii,1) = sqrt(box(ii,1,1)**2 + box(ii,1,2)**2 + box(ii,1,3)**2)
        lengths(ii,2) = sqrt(box(ii,2,1)**2 + box(ii,2,2)**2 + box(ii,2,3)**2)
        lengths(ii,3) = sqrt(box(ii,3,1)**2 + box(ii,3,2)**2 + box(ii,3,3)**2)

    END DO

  END SUBROUTINE LENGTH_EDGES_BOX

  SUBROUTINE ANGLES_BOX(box, angles, nframes)

    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes,3),INTENT(OUT)::angles
    DOUBLE PRECISION::x,y,z,a,b,c
    DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
    INTEGER::ii

    angles = 0.0d0

    DO ii=1,nframes

        x=sqrt(box(ii,1,1)**2+box(ii,1,2)**2+box(ii,1,3)**2)
        y=sqrt(box(ii,2,1)**2+box(ii,2,2)**2+box(ii,2,3)**2)
        z=sqrt(box(ii,3,1)**2+box(ii,3,2)**2+box(ii,3,3)**2)
        a=(acos(dot_product(box(ii,2,:),box(ii,3,:))/(y*z)))/fact_pi_div_180 ! alpha: v2 and v3
        b=(acos(dot_product(box(ii,3,:),box(ii,1,:))/(x*z)))/fact_pi_div_180 ! beta: v1 and v3
        c=(acos(dot_product(box(ii,2,:),box(ii,1,:))/(x*y)))/fact_pi_div_180 ! gamma: v1 and v2
        angles(ii,1) = a
        angles(ii,2) = b
        angles(ii,3) = c

    END DO

  END SUBROUTINE ANGLES_BOX


  !SUBROUTINE CELL2BOX (cell,box,volume,ortho,nframes)
  !
  !  IMPLICIT NONE
  !  INTEGER,INTENT(IN)::nframes
  !  INTEGER::ii
  !  DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(INOUT)::cell
  !  DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(OUT)::box
  !  DOUBLE PRECISION,DIMENSION(nframes),INTENT(OUT)::volume
  !  INTEGER,INTENT(OUT)::ortho
  !  DOUBLE PRECISION::alpha,beta,gamm,x,y,z
  !  DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
  !
  !  DO ii=1,nframes
  !
  !    ortho=0
  !    box=0.0d0
  !    alpha=cell(ii,1,2)
  !    beta=cell(ii,1,3)
  !    gamm=cell(ii,2,3)
  !    x=cell(ii,1,1)
  !    y=cell(ii,2,2)
  !    z=cell(ii,3,3)
  !
  !    box(ii,1,1)=x
  !    IF ((alpha==90.0d0).and.(beta==90.0d0).and.(gamm==90.0d0)) THEN
  !       box(ii,2,2)=y
  !       box(ii,3,3)=z
  !       volume(ii)=x*y*z
  !       ortho=1
  !    ELSE IF ((alpha==0.0d0).and.(beta==0.0d0).and.(gamm==0.0d0)) THEN
  !       cell(ii,1,2)=90.0d0
  !       cell(ii,1,3)=90.0d0
  !       cell(ii,2,3)=90.0d0
  !       box(ii,2,2)=y
  !       box(ii,3,3)=z
  !       volume(ii)=x*y*z
  !       ortho=1
  !    ELSE
  !       alpha=alpha/fact_pi_div_180
  !       beta=beta/fact_pi_div_180
  !       gamm=gamm/fact_pi_div_180
  !       box(ii,2,1)=y*cos(gamm)
  !       box(ii,2,2)=y*sin(gamm)  ! sqrt(y**2-box(2,2)**2)
  !       box(ii,3,1)=z*cos(beta)
  !       box(ii,3,2)=z*(cos(alpha)-cos(beta)*cos(gamm))/sin(gamm) 
  !       box(ii,3,3)=sqrt(z*z-box(ii,3,1)**2-box(ii,3,2)**2)
  !       volume(ii)=box(ii,1,1)*box(ii,2,2)*box(ii,3,3)
  !    END IF
  !
  !  END DO
  !END SUBROUTINE CELL2BOX
  
  !! This function is used by gro, xtc and trr
  !SUBROUTINE BOX2CELL (box,cell,volume,ortho,nframes)
  !
  !  IMPLICIT NONE
  !  INTEGER,INTENT(IN)::nframes
  !  INTEGER::ii
  !  DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(OUT)::cell
  !  DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
  !  DOUBLE PRECISION,DIMENSION(nframes),INTENT(OUT)::volume
  !  INTEGER,INTENT(OUT)::ortho
  !  DOUBLE PRECISION::x,y,z
  !  DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
  !
  !  ortho=0
  !  cell=0.0d0
  !  volume=0.0d0
  !
  !  DO ii=1,nframes 
  !
  !    IF ((box(ii,2,1)==0.0d0).and.(box(ii,3,1)==0.0d0).and.(box(ii,3,2)==0.0d0)) THEN
  !       volume(ii)=box(ii,1,1)*box(ii,2,2)*box(ii,3,3)
  !       cell(ii,1,1)=box(ii,1,1)
  !       cell(ii,2,2)=box(ii,2,2)
  !       cell(ii,3,3)=box(ii,3,3)
  !       cell(ii,1,2)=90.0d0
  !       cell(ii,1,3)=90.0d0
  !       cell(ii,2,3)=90.0d0
  !       ortho=1
  !    ELSE
  !       volume(ii)=box(ii,1,1)*box(ii,2,2)*box(ii,3,3)
  !       x=box(ii,1,1)
  !       y=sqrt(box(ii,2,1)**2+box(ii,2,2)**2)
  !       z=sqrt(box(ii,3,1)**2+box(ii,3,2)**2+box(ii,3,3)**2)
  !       cell(ii,1,1)=x
  !       cell(ii,2,2)=y
  !       cell(ii,3,3)=z
  !       cell(ii,2,3)=(acos(dot_product(box(ii,2,:),box(ii,1,:))/(x*y)))/fact_pi_div_180 ! gamma
  !       cell(ii,1,3)=(acos(dot_product(box(ii,3,:),box(ii,1,:))/(x*z)))/fact_pi_div_180 ! beta
  !       cell(ii,1,2)=(acos(dot_product(box(ii,3,:),box(ii,2,:))/(x*y)))/fact_pi_div_180 ! alpha <<<< Creo que esta mal
  !    END IF
  !
  !  END DO
  !
  !END SUBROUTINE BOX2CELL
  
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

  SUBROUTINE UNWRAP (coors, atoms_indices_serialized, atoms_series_starts, bonds_indices_serialized, &
          & bonds_series_starts, frame_indices, box, inv, ortho, n_frames, n_atoms, n_atoms_indices, &
          & n_atoms_series, n_bonds_indices, n_bonds_series, n_frames_indices)

    IMPLICIT NONE

    INTEGER,INTENT(IN):: n_frames, n_atoms, n_atoms_indices, n_atoms_series
    INTEGER,INTENT(IN):: n_bonds_indices, n_bonds_series, n_frames_indices, ortho
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(INOUT)::coors
    INTEGER,DIMENSION(n_atoms_indices),INTENT(IN)::atoms_indices_serialized ! Molecules in this case
    INTEGER,DIMENSION(n_atoms_series+1),INTENT(IN)::atoms_series_starts
    INTEGER,DIMENSION(n_bonds_indices),INTENT(IN)::bonds_indices_serialized
    INTEGER,DIMENSION(n_bonds_series+1),INTENT(IN)::bonds_series_starts
    INTEGER,DIMENSION(n_frames_indices),INTENT(IN)::frame_indices
    DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box,inv

    INTEGER:: ii, jj, kk, ll
    INTEGER:: molecule_start, molecule_end, molecule_natoms
    INTEGER:: n_left, n_storage
    INTEGER:: atom_id1, atom_id2
    LOGICAL,DIMENSION(n_atoms)::aux_filter
    DOUBLE PRECISION,DIMENSION(3)::vect_aux
    INTEGER,DIMENSION(:),ALLOCATABLE::left,storage
    INTEGER::frame_index
    
    aux_filter(:)=.FALSE.

    DO ii=1,n_atoms_series

        molecule_start=atoms_series_starts(ii)+1
        molecule_end=atoms_series_starts(ii+1)
        molecule_natoms=molecule_end-molecule_start+1

        n_left=1
        ALLOCATE(left(n_left),storage(molecule_natoms))
        jj=atoms_indices_serialized(molecule_start)+1
        left(1)=jj
        aux_filter(jj)=.TRUE.

        DO WHILE (n_left>0)
            n_storage=0
            DO jj=1,n_left
                atom_id1 = left(jj)
                DO kk=bonds_series_starts(atom_id1)+1,bonds_series_starts(atom_id1+1)
                    atom_id2=bonds_indices_serialized(kk)+1
                    IF (aux_filter(atom_id2).eqv..FALSE.) THEN
                        DO ll=1,n_frames_indices
                            frame_index=frame_indices(ll)+1
                            vect_aux(:)=coors(frame_index,atom_id2,:)-coors(frame_index,atom_id1,:)
                            CALL PBC(vect_aux,box(frame_index,:,:),inv(frame_index,:,:),ortho)
                            coors(frame_index,atom_id2,:)=coors(frame_index,atom_id1,:)+vect_aux(:)
                        END DO
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

  SUBROUTINE MINIMUM_IMAGE_CONVENTION(coors, reference_coors, atoms_indices_serialized, atoms_series_starts, frame_indices, &
          & box, inv, ortho, n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frames_indices)

    IMPLICIT NONE

    INTEGER,INTENT(IN):: n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frames_indices, ortho

    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms,3),INTENT(INOUT)::coors
    DOUBLE PRECISION,DIMENSION(n_frames,1,3),INTENT(INOUT)::reference_coors
    INTEGER,DIMENSION(n_atoms_indices),INTENT(IN)::atoms_indices_serialized ! Molecules in this case
    INTEGER,DIMENSION(n_atoms_series+1),INTENT(IN)::atoms_series_starts
    INTEGER,DIMENSION(n_frames_indices),INTENT(IN)::frame_indices
    DOUBLE PRECISION,DIMENSION(n_frames,3,3),INTENT(IN)::box,inv

    INTEGER::ii,jj,ll
    INTEGER::atom_index, frame_index
    DOUBLE PRECISION,DIMENSION(n_frames,1,3)::com,vect_aux
    DOUBLE PRECISION,DIMENSION(n_frames,n_atoms_series,3)::centers_molecules

    centers_molecules = GEOMETRICAL_CENTER(coors, atoms_indices_serialized, atoms_series_starts, frame_indices, &
        & n_frames, n_atoms, n_atoms_indices, n_atoms_series, n_frames_indices)

    DO ii=1, n_atoms_series
        com(:,1,:) = centers_molecules(:,ii,:)
        vect_aux = com - reference_coors
        CALL PBC_TENSOR(vect_aux, box, inv, ortho, n_frames, n_atoms)
        DO jj=atoms_series_starts(ii)+1, atoms_series_starts(ii+1)
            atom_index = atoms_indices_serialized(jj)+1
            DO ll=1,n_frames_indices
                frame_index=frame_indices(ll)+1
                coors(frame_index, atom_index, :) = coors(frame_index, atom_index, :) - com(frame_index, 1, :) +&
                & vect_aux(frame_index, 1, :) + reference_coors(frame_index, 1, :)
            END DO
        END DO
    END DO

  END SUBROUTINE MINIMUM_IMAGE_CONVENTION

END MODULE MODULE_BOX

