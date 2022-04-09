#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError as _NotImplementedMethodError
from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt import puw as _puw
import numpy as _np
from networkx import Graph as _Graph

_form='biopython.Seq'

## From atom

## From group

def get_group_id_from_group(item, indices='all', check=True):

    raise _NotImplementedMethodError()

def get_group_name_from_group(item, indices='all', check=True):

    raise _NotImplementedMethodError()

def get_group_type_from_group(item, indices='all', check=True):

    raise _NotImplementedMethodError()

## From component

## From molecule

## From chain

## From entity

## From system

def get_n_groups_from_system(item, check=True):

    return len(item)

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

#######################################################################################
########### REMOVE COMMON GET METHODS NOT DEFINED FOR THIS CURRENT FORM ###############
#######################################################################################

