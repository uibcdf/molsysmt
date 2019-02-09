MODULE MODULE_MATH

CONTAINS
    
  SUBROUTINE NORMALIZE_VECT (a)
    
    DOUBLE PRECISION,DIMENSION(3),INTENT(INOUT)::a
    DOUBLE PRECISION::norm
    
    norm=sqrt(dot_product(a,a))
    a=a/norm
    
  END SUBROUTINE NORMALIZE_VECT
  
  SUBROUTINE PRODUCT_VECT(a,b,normal)
    
    DOUBLE PRECISION,DIMENSION(3),INTENT(IN)::a,b
    DOUBLE PRECISION,DIMENSION(3),INTENT(OUT)::normal
    
    normal(1)=a(2)*b(3)-a(3)*b(2)
    normal(2)=-a(1)*b(3)+a(3)*b(1)
    normal(3)=a(1)*b(2)-a(2)*b(1)
    
  END SUBROUTINE PRODUCT_VECT


  SUBROUTINE ROTANDTRANS_RMSD(center_orig,U,center_ref,coors,dim_coors,new_coors)

    IMPLICIT NONE

    INTEGER,INTENT(IN)::dim_coors
    DOUBLE PRECISION,DIMENSION(3),INTENT(IN)::center_orig,center_ref
    DOUBLE PRECISION,DIMENSION(3,3),INTENT(IN)::U
    DOUBLE PRECISION,DIMENSION(dim_coors,3),INTENT(IN)::coors

    DOUBLE PRECISION,DIMENSION(dim_coors,3),INTENT(OUT)::new_coors

    INTEGER::ii

    DO ii=1,dim_coors
       new_coors(ii,:)=matmul(transpose(U(:,:)),coors(ii,:)-center_orig)+center_ref
    END DO


  END SUBROUTINE ROTANDTRANS_RMSD

END MODULE MODULE_MATH
