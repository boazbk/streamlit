import streamlit as st
import pandas as pd
import numpy as np
import urllib.request
import urllib 
import json
import matplotlib.pyplot as plt

st.title('State to national needle')


'''
Data from [538 interactive forecast](https://projects.fivethirtyeight.com/trump-biden-election-map/) (see [this file](https://projects.fivethirtyeight.com/trump-biden-election-map/simmed-maps.json))
'''


@st.cache
def get_data():
    with urllib.request.urlopen("https://projects.fivethirtyeight.com/trump-biden-election-map/simmed-maps.json") as f:
        simulations = json.load(f)
    df = pd.DataFrame(simulations['maps'], columns=[ "Winner", "Trump", "Biden"] + simulations['states'])
    return df


try:
    df  = get_data()

except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )


states = ["NC","FL","GA"] 

fullnames = { "NC": "North Carolina" , "FL": "Florida", "GA": "Georgia" }

bounds = { s+mod: -10 if mod==" (min)" else +10 for s in states for mod in [" (min)"," (max)"] }

sliders = { s: st.slider(fullnames[s], -10.0,+10.0, (-10.0,+10.0),0.5)  for s in states }


temp = df.copy()
for s in states:
    temp = temp[(-temp[s]> sliders[s][0]) & (-temp[s]< sliders[s][1])]

'''
### Prediction
'''

st.markdown(f"Based on above parameters, Biden's chance to win is __{100*(1-temp.Winner.mean()):.0f}%__")


fig, ax = plt.subplots(figsize = (12,6))

# the histogram of the data
n, bins, patches = ax.hist(temp.Biden, bins=[100, 150, 200,  250, 270, 300, 350,400,450,500, 538], density=True)
ax.set_xticks(bins)
# add a 'best fit' line
ax.set_xlabel('Biden electoral votes', fontsize= 24)
ax.set_ylabel('Probability')
cond = ", ".join([s +f"$\in [{sliders[s][0]},{sliders[s][1]}]$" for s in states])

plt.suptitle("Histogram of Biden electoral votes", color="red", fontsize=24)
plt.title(rf'Assuming {cond}')
plt.axvline(x=270, color="red")

# Tweak spacing to prevent clipping of ylabel
plt.show()
st.pyplot(fig)


    

