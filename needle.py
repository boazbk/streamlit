import streamlit as st
import pandas as pd
import urllib.request
import urllib 
import json
import matplotlib.pyplot as plt

st.title('State to national needle')


'''
Data from [538 interactive forecast](https://projects.fivethirtyeight.com/trump-biden-election-map/) (see [this file](https://projects.fivethirtyeight.com/trump-biden-election-map/simmed-maps.json))

Choose below the range of possible margins for Biden in North Carolina, Florida, and Georgia, and see how it changes the predicted chance of victory.*
'''

st.text("Disclaimer: This may not 100% correspond to 538's simulator because:\n(1) we assume the margin is always between -10 and +10, \n(2) their data may be more updated, and\n(3) I may have bugs")

@st.cache
def get_data():
    with urllib.request.urlopen("https://projects.fivethirtyeight.com/trump-biden-election-map/simmed-maps.json") as f:
        simulations = json.load(f)
    return pd.DataFrame(simulations['maps'], columns=[ "Winner", "Trump", "Biden"] + simulations['states'])


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

'''
Choose the range of margins in each state - positive means Biden wins the state, negative means he loses:
'''

sliders = {s: st.slider(f"{fullnames[s]} (current 538 predicted margin: {-df[s].median():.1f}% ± {df[s].std():.1f}%)", -
                        10.0, +10.0, (-10.0, +10.0), 0.5, format="%.1f") for s in states}


temp = df.copy()
for s in states:
    temp = temp[(-temp[s]>= sliders[s][0]) & (-temp[s]< sliders[s][1])]

'''
### Prediction
'''

st.markdown(f"Based on above parameters, Biden's chance to win is __{100*(1-temp.Winner.mean()):.0f}%__")

st.markdown(f"Number of simulations is __{len(temp):,}__ out of __{len(df):,}__ (a smaller number of simulations means that the prediction above is less meaningful)")

fig, ax = plt.subplots(figsize = (12,6))

# the histogram of the data
n, bins, patches = ax.hist(temp.Biden, bins=[100, 150, 200,  250, 270, 300, 350,400,450,500, 538], density=True)
ax.set_xticks(bins)
# add a 'best fit' line
ax.set_xlabel('Biden electoral votes', fontsize= 24)
ax.set_ylabel('Probability')
cond = ", ".join([s +f"$\in [{sliders[s][0]},{sliders[s][1]})$" for s in states])

plt.suptitle("Histogram of Biden electoral votes", color="red", fontsize=24)
plt.title(rf'Assuming {cond}')
plt.axvline(x=270, color="red")

# Tweak spacing to prevent clipping of ylabel
plt.show()
st.pyplot(fig)


    

