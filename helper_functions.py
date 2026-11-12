from bakery import assert_equal
import random

activity = ["Li","K","Ba","Ca","Na","Mg","Al","Mn","Zn","Cr","Fe","Cd","Co","Ni","Sn","Pb","H2","Cu","Ag","Hg","Pt","Au"]
soluable = ["NO3","ClO4","Cl","I","Na","NH4","K"] #doesn't work
insoluable = ["CO3","PO4","OH","S"] #doesn't work

def get_reactant_number(reactant: str) -> int:
    if reactant not in activity:
        return -1
    else: 
        for index, element in enumerate(activity):
            if reactant == element:
                return index
        
        
assert_equal(get_reactant_number("Na"),4)
assert_equal(get_reactant_number("Al"),6)
assert_equal(get_reactant_number("Zn"),8)

def reaction_works(reactant1: str, reactant2: str) -> int:
    reactant1_number = get_reactant_number(reactant1)
    reactant2_number = get_reactant_number(reactant2) #the one with ions
    if reactant1_number == -1 or reactant2_number == -1:
        return -1
    if reactant1_number < reactant2_number:
        return 1
    else:
        return 0
"""  
def solution_reaction_works(reactant1: str, reactant2: str) -> int:
    
    if reactant1 not in soluable and reactant2 not in soluable:
        if reactant1 not in insoluable and reactant2 not in insoluable:
            return -1
    else:
        for element in soluable:
            if element in reactant1:
                if element in reactant2:
                    return 1
                else:
    
    pass
 """                   
                    
        
    
assert_equal(reaction_works("Li","Al"), True)
assert_equal(reaction_works("Al","Li"), False)
assert_equal(reaction_works("Ni","Na"), False)
assert_equal(reaction_works("Sn","Sn"), False)
assert_equal(reaction_works("Je","Sn"), None)
