from drafter import *
from bakery import assert_equal
from dataclasses import dataclass
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

@dataclass
class State:
    reactant1 : str
    reactant2 : str
    status : str
    anion : str
    products : str
    score : int
    #answer = list[Answer] needs list somewhere
"""
@dataclass
class Answer:
    reactant_1 : str
    reactant_2 : str
    will_work : bool
    why: str
"""

@dataclass
class Practice_mode:
    reactant1 : str
    reactant2: str

@route
def index(state:State) -> Page:
    return Page(state, [
        Header("Reaction Simulator!"),
        "Choose guided simulation or practice mode (for the experts)!",
        "\n",
        Button("Guided Practice","simulation"),
        Button("Practice Mode (Doesn't work)","practice_page")
        ])

@route
def simulation(state:State) -> Page:
    return Page(state, [
        Header("Guided Practice!"),
        "Instructions: Input two reactants into the textboxes below!",
        "Do NOT put charges.",
        "Second reactant should be one with charges.",
        TextBox("first_reactant",state.reactant1),
        "+",
        TextBox("second_reactant",state.reactant2),
        TextBox("attachment",state.anion),
        Button("React!","react"),
        "\n",
        state.status,
        "\n",
        "Expected products:",
        state.products,
        "\n",
        Button("Go Back","index"),
        Button("Check Activity Series","sim_activity_list")
        ])

@route
def react(state:State,first_reactant: str, second_reactant: str, attachment: str) -> Page:
    state.reactant1 = first_reactant
    state.reactant2 = second_reactant
    state.anion = attachment
    works = reaction_works(state.reactant1, state.reactant2)
    if works == -1:
        state.status = "ERROR. Reactant(s) not in activity series. Please be sure reactants are spelled correctly."
    elif works == 1:
        state.status = "Reaction will happen! Explanation here!"
        state.products = state.reactant1 + state.anion + " + " + state.reactant2
    elif works == 0:
        state.status = "Reaction will not happen! Explanation here!"
        state.products = state.reactant1 + " + " + state.reactant2 + state.anion
    return simulation(state)

@route
def practice_page(state:State) -> Page:
    return Page(state, [
        Header("Practice mode!"),
        "Instructions: Two reactants will appear below. See if they react or not!",
        "This is a WIP!",
        "\n",
        "Score:",
        state.score,
        "\n",
        #this space will pull in random compounds from a database. Still trying to figure out how to do this.
        Button("Will react","practice_explanation"),
        Button("Will not react","practice_explanation"),
        Button("Check Series","activity_list"),
        Button("Go Back","index")
        ])

#this doesn't work right now
@route
def practice_random(practice: Practice_mode) -> Page:
    practice.reactant1 = random.choice(activity)
    practice.reactant2 = random.choice(activity)
    return practice_page(practice)

@route
def activity_list(state:State) -> Page:
    return Page(state, [
        "The following oxidation list is as followed:",
        "Li, ","K, ","Ba, ","Ca, ","Na, ","Mg, ","Al, ","Mn, ","Zn, ","Cr, ","Fe, ","Cd, ","Co, ","Ni, ","Sn, ","Pb, ","H2, ","Cu, ","Ag, ","Hg, ","Pt, ","Au",
        "\n",
        Button("Go Back","practice_page")
        ])

@route
def sim_activity_list(state:State) -> Page:
    return Page(state, [
        "The following oxidation list is as followed:",
        "Li, ","K, ","Ba, ","Ca, ","Na, ","Mg, ","Al, ","Mn, ","Zn, ","Cr, ","Fe, ","Cd, ","Co, ","Ni, ","Sn, ","Pb, ","H2, ","Cu, ","Ag, ","Hg, ","Pt, ","Au",
        "\n",
        Button("Go Back","simulation")
        ])

@route
def practice_explanation(state:State) -> Page:
    return Page(state, [
        "This will tell you if you're right or wrong!",
        Button("Go Back","practice_page")
        ])

start_server(State("", "", "","","",0))

    
    
