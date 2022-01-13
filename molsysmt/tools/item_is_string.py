 def item_is_string(item):

     from molsysmt.forms import string_names_recognized
     from .strings import guess_form_from_string

     output = False

     if type(item) is str:
         if ':' in item:
             string_name = item.split(':')[0]
             if string_name in string_names_recognized:
                 output = 'string:'+string_name
         if output==False:
             output = guess_form_from_string(item)
             if output is None:
                 output = False

     return output

