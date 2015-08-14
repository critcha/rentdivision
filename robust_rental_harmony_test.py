#%%
location_of_this_script = "/Users/andrew/Dropbox/_Python/rentdivision"
import sys
sys.path.append(location_of_this_script)

#%%
from rental_harmony_lib import rental_harmony
import pandas as pd

#%%
total_rent = 5400
total_rent

#%%
values = pd.DataFrame({
#    Room       :    1      2       3       4
    'Alice'     :   [30,    20,     0,      200 ],
    'Bob'       :   [201,   32,     23,     0   ],
    'Caitlin'   :   [31,    204,    29,     0   ],
    'Dave'      :   [32,    26,     212,    0   ]
    }).T
values

#%%
rental_harmony(total_rent,values)

#%%
import random
total_rent = 0
def random_values(n,m=100) :
    letters = [chr(i + ord('A')) for i in range(0,n)]
    return pd.DataFrame({letters[i] : random.sample(range(0, m), n) for i in range(0,n)}).T

#%%
n=5
envy_free = True
trials = 0
while envy_free and trials < 1000:
    if trials % 100 == 0 :
        print (str(trials) + ' trials completed')
    #print(values)
    values = random_values(n,100)
    working = rental_harmony(0,values)[2]
    if not(envy_free):
        print("Found values where result is not envy free:")
        print(values)
    trials += 1
values

#%%
total_rent = 0
values = pd.DataFrame({
#    Room       :    1      2       3
    'Alice'     :   [3,     0,     0],
    'Bob'       :   [0,     9,     21],
    'Caitlin'   :   [0,     9,     24],
    }).T
values

#min_cycle = [1,2,0,1]
rental_harmony(0,values)

#%%
time(rental_harmony(0,random_values(19,100))[2])
