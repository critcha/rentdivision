#This template is meant to be used with iPython,
#ideally in the Spyder IDE where you can run blocks of code 
#delineated by "#%%" with a single kebyoard shortcut.

#%%
#Modify this line to match the folder where you unzipped "rental_harmony.zip":
location_of_this_script = "/Users/andrew/Dropbox/_Python/rentdivision"
import sys
sys.path.append(location_of_this_script)

#%%
from rental_harmony_lib import rental_harmony
import pandas as pd

#%%
#Enter the total rent here:
total_rent = 5400
total_rent

#%%
#Have each housemate choose their least-favorite room, and assign it
#a marginal value of zero dollars.  Then, ask them to imagine living in 
#that room and paying slightly-less-than-average rent.  How much extra 
#would they be willing to pay to move into each other room?  
#Enter those values here:
values = pd.DataFrame({
#    Room       :    1      2       3       4
    'Alice'     :   [30,    20,     0,      200 ],
    'Bob'       :   [201,   32,     23,     0   ],
    'Caitlin'   :   [31,    204,    29,     0   ],
    'Dave'      :   [32,    26,     212,    0   ]
    }).T
values

#%%
#Compute the (room,price) assignment that is maximally-far from 
#creating ency between any two housemates; this assignment
#necessarily also maximizes the total utility of the group,
#measured in marginal dollars:
(solution,envies,envy_free) = rental_harmony(total_rent,values)
solution

#%%
envies

#%%
envy_free