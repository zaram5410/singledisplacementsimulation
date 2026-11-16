from drafter import *
from bakery import assert_equal
from dataclasses import dataclass
import random
activity = ["Li","K","Ba","Ca","Na","Mg","Al","Mn","Zn","Cr","Fe","Cd","Co","Ni","Sn","Pb","H2","Cu","Ag","Hg","Pt","Au"]

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
                    
 
assert_equal(reaction_works("Li","Al"), True)
assert_equal(reaction_works("Al","Li"), False)
assert_equal(reaction_works("Ni","Na"), False)
assert_equal(reaction_works("Sn","Sn"), False)
assert_equal(reaction_works("Je","Sn"), None)

@dataclass
class Question:
    reactant1 : str
    reactant2: str
    expected_products : str
    will_work : bool

@dataclass
class State:
    reactant1 : str
    reactant2 : str
    status : str
    anion : str
    products : str
    score : int
    questions : list[Question]
    position : int
    
QUESTIONS = [
    Question("Fe(s)","CuSO4(aq)","FeSO4(aq) + Cu(s)",True),
    Question("Cu(s)","HCl(aq)","No reaction",False),
    Question("2Na(s)","2H2O(l)","2NaOH(aq) + H2(g)",True),
    Question("Ag(s)","ZnSO4(aq)","No reaction",False)
    ]

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
    state.position = random.randint(0,3) #right boundary will change
    question = state.questions[state.position]
    return Page(state, [
        Header("Practice mode!"),
        "Instructions: Two reactants will appear below. See if they react or not!",
        "\n",
        "Score:",
        state.score,
        "\n",
        question.reactant1, " + ", question.reactant2,
        Button("Will react","practice_explanation", Argument("chosen",True)),
        Button("Will not react","practice_explanation",Argument("chosen",False)),
        Button("Check Series","activity_list"),
        Button("Go Back","index")
        ])

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
def practice_explanation(state:State, chosen: bool) -> Page:
    question = state.questions[state.position]
    state.position = random.randint(0,3) #right boundary will change
    if chosen == question.will_work:
        state.score = state.score + 1
        message = "That's correct!"
    else:
        message = "Incorrect!"
    return Page(state, [
        Header(message),
        "The expected products are", question.expected_products,
        "\n",
        "Check the activity series!",
        Button("Go Back","practice_page")
        ])


start_server(State("", "", "","","",0, QUESTIONS, 0))

start_server(State("", "", "","","",0, QUESTIONS, 0))
