# read model
states = []
with open('model_600k_30k.txt', 'r') as f:
    while True:
        state = f.readline()
        if state == '':
            break
        states.append(state)
        f.readline()
    
    print(len(states))
    states_set = set(states)
    print(len(states_set))