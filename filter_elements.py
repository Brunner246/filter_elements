#!/usr/bin/env python

"""filter_elements.py: searches elements for specific terms and activates them """

__author__      = "Michael Brunner"
__copyright__   = "Copyright 2021, Cadwork Holz AG"
__maintainer__  = "Michael Brunner"
__email__       = "brunner@cadwork.swiss"
__license__     = "MIT License Agreement"
__version__     = "1.0"
__status__      = "Testing"

#---------------------------------------------------------------

import      utility_controller         as uc
import      element_controller         as ec
import      cadwork                    as cw
import      attribute_controller       as ac
import      re
import      visualization_controller   as vc
import      tkinter
import      tkinter.messagebox


# global variables
FIND_WORD  = uc.get_user_string("""Suchbegriff(e) eingeben (z.B. Beton, Holz, Lattung
                                )""")

#---------------------------------------------------------------

def main():
    
    active_element_ids  = ec.get_active_identifiable_element_ids()
    visible_element_ids = ec.get_visible_identifiable_element_ids()
    
    len_active_element_ids  = len(active_element_ids)
    len_visible_element_ids = len(visible_element_ids)
    
    if len_active_element_ids != 0 and len_active_element_ids != len_visible_element_ids:
        var :bool = uc.get_user_bool("Sollen nur aktive Elemente berücksichtigt werden?", True)
        if var:
            element_ids = active_element_ids
        else:
            element_ids = visible_element_ids
    else:
        element_ids = visible_element_ids
    
    if len(element_ids) == 0:
        warning_msg('Es sind keine Elemente aktiv/sichtbar!')
        exit()
 
    vc.set_inactive(element_ids)
    
    uc.disable_auto_display_refresh()
   
    names = list(map(get_name, element_ids))

    elements = list()
    
    search = re.split(', |;|,|\s', FIND_WORD) 
    search = list(map(str.lower, search))
       
    for n, e in zip(names, element_ids):
        if any(x in n for x in search): 
            elements.append(e)
        else:
            continue
    
    if not elements:
        warning_msg("Namen nicht gefunden!")
            
            
    uc.enable_auto_display_refresh()
    vc.set_active(elements)
    info_msg(f"{len(elements)} Elemente gefunden")
    
    return None
   

#---------------------------------------------------------------

def warning_msg(message):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title= "Achtung",message = message)
    root.destroy()
    
def info_msg(message):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title= "Information",message = message)
    root.destroy()
    
def get_name(element:int) -> str:
    name = ac.get_name(element)
    return name.lower()
        

if __name__ == '__main__':
    main()
    
