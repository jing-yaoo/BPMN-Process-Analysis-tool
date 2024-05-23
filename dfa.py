
#dictionary for the dfa
dfa = {0:{'0':0, '1':1},
       1:{'0':2, '1':0},
       2:{'0':1, '1':2}}

print(dfa.get(1).get('0'))