#!/usr/bin/env python
# coding: utf-8

# # COVID India - Histogram comparison
# 
# In this notebook, we will compare the COVID cases in India between states as well as between districts within a state. Particularly, we will look at the following scenarios:
# 
# 1. Number of active/ailing cases vs Number of recoveries
# 2. Number of active/ailing cases vs Number of deaths
# 
# The above two scenarios will be seen inter-state as well as inter-district.
# 
# The data used in this study is from <a href="https://api.covid19india.org/">here</a>.

# ### Load the JSON file that contains statewise records

# In[1]:


import requests
import numpy as np

response = requests.get("https://api.covid19india.org/data.json")
data = response.json()
nat_active = int(data['statewise'][0]['active'])
nat_recovered = int(data['statewise'][0]['recovered'])
nat_death = int(data['statewise'][0]['deaths'])

states, active, recovered, deaths = [],[],[],[]
for state in data['statewise'][1:]:
    if(int(state['confirmed']) > 0):
        states.append(state['statecode'])
        active.append(int(state['active']))
        recovered.append(int(state['recovered']))   
        deaths.append(int(state['deaths']))


# ### Plot ailing vs recovered cases (state-wise) 

# In[2]:


from matplotlib import pyplot as plt

# create plot
plt.subplots(figsize=(18,5))
indices = range(len(states))
bar_width = 0.8
opacity = 0.8

plt.bar(indices, active, width=bar_width, color='r', label='ailing')
plt.bar(indices, recovered, width=3*bar_width/4,alpha=opacity,color='b',label='recovered')
plt.xticks(indices, states)
plt.title('Covid Study - India'+'\n'+'https://www.covid19india.org/')
plt.legend()

plt.show()


# ### Plot ailing vs dead cases (state-wise) 

# In[3]:


plt.subplots(figsize=(18,5))
plt.bar(indices, active, width=bar_width, color='y', label='ailing')
plt.bar(indices, deaths, width=3*bar_width/4,alpha=opacity,color='r',label='dead')
plt.xticks(indices, states)
plt.title('Covid Study - India'+'\n'+'https://www.covid19india.org/')
plt.legend()

plt.show()


# ### Plot the share of  each state's total number of cases. 
# ### Also further divide the share of each state into dead, ailing and recovered

# In[4]:


active = np.asarray(active)
recovered = np.asarray(recovered)
deaths = np.asarray(deaths)
total = active+recovered+deaths
stack = (np.dstack((recovered,active,deaths)).flatten())
colour_stack = ['b','#c2c2f0','r']*(len(stack)//3)

plt.subplots(figsize=(18,8))
plt.pie(total, startangle=90,frame=True)
plt.pie(stack, radius=0.75,colors=colour_stack,startangle=90)
centre_circle = plt.Circle((0,0),0.5,color='black', fc='white',linewidth=0)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.legend(states) 
plt.axis('equal')
plt.show()


# ### Ailing vs Recovered graphs for selected states

# In[5]:


response = requests.get("https://api.covid19india.org/state_district_wise.json")
states = ['Telangana','Andhra Pradesh','Karnataka', 'Tamil Nadu']
data = response.json()
for state in states:
    info = data[state]['districtData']
    districts = list(info.keys())
    if 'Unknown' in districts:
        districts.remove('Unknown')
    active, deaths, recovered = [],[],[]
    for key in districts:
        active.append(info[key]['active'])
        recovered.append(info[key]['recovered'])
        deaths.append(info[key]['deceased'])
    print('\nState: ',state,'\n')
    print("{:30} {:6} {:6} {:6}".format('District','Active','Recovered','Deaths'))
    print('-'*60)
    for idx in range(len(districts)):
        print("{:30} {:6d} {:6d} {:6d}".format(districts[idx],active[idx],recovered[idx],deaths[idx]))

    indices = range(len(districts))
    plt.subplots(figsize=(18,5))
    plt.bar(indices, active, width=bar_width, color='r', label='ailing')
    plt.bar(indices, recovered, width=3*bar_width/4,alpha=opacity,color='b',label='recovered')
    plt.xticks(indices, [dis[:4] for dis in districts])
    plt.title('Covid Study - '+state+'\n'+'https://www.covid19india.org/')
    plt.legend()

    plt.show()

