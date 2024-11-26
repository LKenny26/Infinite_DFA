from collections import deque

def check_states(states):
    states = states.replace(" ", "")
    state_array = states.split(',')
    if "" in state_array:
        state_array.remove("")
    if states == "":
        print("Error there is no state(s)")
        exit(1)
    return state_array

def check_lang(lang):
    lang = lang.replace(" ", "")
    if lang == "":
        print("Error there is no language")
        exit(1)
    lang_array = lang.split(",")
    if "" in lang_array:
        lang_array.remove("")
    return lang_array

def check_transitions(transitions, states, lang):
    transitions = transitions.replace(" ", "")
    transitions_array = transitions.split("),")
    if "" in transitions_array:
        transitions_array.remove("")
    new_array = [ [""]*(len(lang)+1) for i in (range(len(states)+1))]
    for i in range(len(states)):
        new_array[i+1][0] = states[i]
    for j in range(len(lang)):
        new_array[0][j+1] = lang[j]

    for string in transitions_array:
        string = string.replace("(", "")
        string = string.replace(")","")
        transistion = string.split(",")
        x = 0
        y = 0
        for n in range(len(states)):
            if transistion[0] == new_array[n+1][0]:
                x = n+1
                break
        for m in range(len(lang)):
            if transistion[2] == new_array[0][m+1]:
                y = m+1
                break
        
        new_array[x][y] = transistion[1]
    
    for i in range(len(states)):
        for j in range(len(lang)):
            if i == 0 and j == 0:
                pass
            else:
                if new_array[i][j] == "":
                    print("Error there is a missing transition, this is not a proper DFA")
                    exit(1)
    return new_array

def check_start(start, states):
    start = start.replace(" ", "")
    if start in states:
        return start
    else:
        print("Error the start state is not in the states given or was never provided")
        exit(1)

def check_accept(accept, states):
    accept = accept.replace(" ", "")
    accept_states = accept.split(",")
    if accept_states == [""]:
        return accept_states
    for state in accept_states:
        if state in states:
            pass
        else:
            print("Error the accept state is not apart of states")
            exit(1)
    return accept_states

def check_loops(states_D, language, transition_D, start, accept_D):
    # Get number of states
    num_states = len(states_D)
    states_N, transition_N, accept_N = build_DFA_N(num_states, language)
    states_I, transition_I, start_I, accept_I = build_DFA_I(states_D, states_N, transition_D, transition_N, accept_D, accept_N, language)
    is_empty_DFA_I = E_DFA(states_I, language, transition_I, start_I, accept_I)
    return not is_empty_DFA_I

def build_DFA_N(num_states_D, lang_D):
    #DFA that accepts N length strings with N being num states in DFA D
    transition_N = [ [""]*(len(lang_D)+1) for i in (range(num_states_D+2))]
    states_N = []
    for n in range(num_states_D):
        transition_N[n+1][0] = f"q{n}"
        states_N.append(f"q{n}")
        i = 1
        for char in lang_D:
            transition_N[n+1][i] = f"q{n+1}"
            transition_N[0][i] = char
            i+=1

    for x in range(len(lang_D)+1):
        transition_N[num_states_D+1][x] = f"q{num_states_D}"

    states_N.append(f"q{num_states_D}")
    accept_N = [f"q{num_states_D}"]
    return(states_N, transition_N, accept_N)

def build_DFA_I(states_D, states_N, transition_D, transition_N, accept_D, accept_N, lang):
    states_I = []
    for i in range(len(states_D)):
        for j in range(len(states_N)):
            states_I.append(states_D[i] + ":" + states_N[j])
    transition_I = ""
    new_D_state = ""
    new_N_state = ""
    for state in states_I:
        for char in lang:
                state_one, state_two = state.split(":")
                for x in range(len(lang)+1):
                    if transition_D[0][x] == char:
                        for y in range(len(states_D)+1):
                            if state_one == transition_D[y][0]:
                                new_D_state = transition_D[y][x]
                    if transition_N[0][x] == char:
                        for y in range(len(states_N)+1):
                            if state_two == transition_N[y][0]:
                                new_N_state = transition_N[y][x]
                transition_I = transition_I + f"({state},{new_D_state}:{new_N_state},{char}),"
    transition_I = check_transitions(transition_I, states_I, lang)

    accept_I = []
    if accept_D == [""] or accept_N == [""]:
        accept_I.append("")
    else:
        for state_D in accept_D:
            for state_N in accept_N:
                accept_I.append(state_D + ":" + state_N)

    return states_I, transition_I, "q0:q0", accept_I

def E_DFA(states, language, transition, start, accept):
    if accept == [""]:
        return True

    visited = []
    queue = deque([start])

    while queue:
        current_state = queue.popleft()

        if current_state in accept:
            # there is an accept state that has been visited/"marked"
            return False

        if current_state not in visited:
            visited.append(current_state)
            for i in range(len(language)):
                for x in range(1, len(transition)):
                    if transition[x][0] == current_state:
                        next_state = transition[x][i+1]
                        if next_state not in visited:
                            queue.append(next_state)

    return True


if __name__ == "__main__":
    # Get all the inputs
    states = input("Please provide the states (Ex: q0,q1,q2...qi): ")
    language = input("PLease provide the language (Ex: a,b,c...): ")
    transitions = input("Please provide the transitions (Ex: (q0,q1,a),(q0,q2,b)...): ")
    start = input("Please provide the start state (Ex: q0): ")
    accept = input("Please provide the accepting states(Ex: q2,q4): ")

    # Convert it to correct format and check that it is legal
    state_array = check_states(states)
    language_array = check_lang(language)
    transitions_array = check_transitions(transitions, state_array, language_array)
    start_state = check_start(start, states)
    accept_states = check_accept(accept, states)

    #see if there are any loops in the DFA:
    loops = check_loops(state_array, language_array, transitions_array, start_state, accept_states)

    if loops == True:
        print("This DFA has an infinite language.")
    else:
        print("This DFA does not have an infinite language")