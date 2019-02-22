import numpy as np
import random
from itertools import permutations
import json
import sys

home = [101, 107, 106, 121, 102, 106, 107, 106, 121, 102, 107, 106, 121, 102, 106, 107, 106, 121, 102, 107, 106, 121, 102, 106, 107, 106, 121, 102]
away = [102, 104, 105, 106, 106, 101, 104, 105, 106, 106, 101, 104, 105, 106, 106, 101, 86, 105, 106, 106, 101, 94, 105, 106, 106, 106, 107, 106]

if len(home) != len(away):
    print("Please check your input.")
    sys.exit(1)

dic = {
    -6: 60,
    -5: 51,
    -4: 48,
    -3: 45,
    -2: 42,
    -1: 40,
    0: 38,
    1: 36,
    2: 33,
    3: 30,
    4: 27,
    5: 21,
    6: 15    
}

home = sorted(home)
away = sorted(away)

home_final = []
away_final = []

while True:
    if home[-1] - away[-1] > 6:
        home_final.append(home[-1])
        away_final.append(away[-1])       
        del home[-1]
        del away[-1]
    else:
        break

while True:
    if home[0] - away[0] < -6:
        home_final.append(home[0]) 
        away_final.append(away[-1])
        del home[0]
        del away[-1]
    else:
        break

def get_goal(n):
    n = 6 if n > 6 else n
    n = -6 if n < -6 else n
    return dic[n]

def find_best_small(home_perms, away_perms):

    max_goal = 0
    max_home = []
    max_away = []
    x = 0
    for i in home_perms:
        x += 1
        home_perm = np.array(i)
        away_perm = np.array(away_perms)
        diff = away_perm - home_perm
        goals = [get_goal(x) for x in diff]
        sm = sum(goals)
        if sm > max_goal:    
            max_home = home_perm
            max_goal = sm
    return max_home
	
def find_best_large(home, away):
    x = 0
    sm = 0
    best = []
    for i in range(10000):
        
        random.shuffle(home)
        while True:
            found = False
            for i in range(len(home)):
                for j in range(i + 1, len(home), 1):
                    if away[i] == away[j]:
                        continue
                    sum1 = get_goal(away[i] - home[i]) + get_goal(away[j] - home[j])
                    sum2 = get_goal(away[i] - home[j]) + get_goal(away[j] - home[i])

                    if sum2 > sum1:
                        home[i], home[j] = home[j], home[i]
                        found = True
            if not found:
                break
        diff = np.array(away) - np.array(home)
        t = sum([get_goal(t) for t in diff])
        if sm < t:
            sm = t
            best = np.array(home).copy()
    return best
	
def get_best(home, away):
    if len(home) < 10:
        return find_best_small([c for c in  permutations(home, len(home))], away)
    else:
        return find_best_large(home, away)

home_res = get_best(home, away) 
diff = np.array(away) - home_res
diff = np.append(diff, (np.array(away_final) - np.array(home_final)))
goals = [get_goal(x) for x in diff]

sm = sum(goals)

for i, j in zip(np.append(home_res, np.array(home_final)), np.append(away, np.array(away_final))):
    print(str(i) + "-" + str(j) + "\t +/-: " + ("+" if j > i else "") + str(j - i) + "\t goal: " + str(get_goal(j - i)))
    
print("-" * 60)
print("goal: " + str(sm))
