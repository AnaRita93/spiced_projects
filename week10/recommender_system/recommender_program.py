#!/usr/bin/env python
# coding: utf-8
# In[1]:
"""
Simple Movie Recommender: returns a random movie name from a predefined list

"""
import random 

MOVIES =[
    'Titanic',
    'Praxis Dr Hasenbein',
    'John Wick',
    'Kill Bill'
]

def get_recommendation():
    """ returns a random movie name  """
    r = random.randint(0,len(MOVIES)-1) 
    return MOVIES[r]

movie = get_recommendation()
print(movie)
    

# In[ ]:




