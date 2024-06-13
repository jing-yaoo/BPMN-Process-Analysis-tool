
#dictionary for the dfa
dfa = {'order pizza':{'':0, '1':1},
       1:{'0':2, '1':0},
       2:{'0':1, '1':2}}

print(dfa.get(2).get('0'))

dfa[2] = {'0': 3, '1': 2}

print(dfa.get(2).get('0'))