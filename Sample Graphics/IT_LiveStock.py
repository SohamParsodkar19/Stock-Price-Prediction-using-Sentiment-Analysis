#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import datetime
import yfinance as yf


# In[24]:


s = datetime.datetime(2024,1,1)
e = datetime.datetime(2024,9,14)


# In[25]:


hcl = yf.download('HCLTECH.NS',start = s,end= e)
hcl['Symbol'] = 'HCL'


# In[26]:


hcl


# In[27]:


techm = yf.download('TECHM.NS',start = s,end= e)
techm['Symbol'] = 'TECHMAHINDRA'


# In[28]:


persis = yf.download('PERSISTENT.NS',start = s,end= e)
persis['Symbol'] = 'PERSISTENT'


# In[29]:


oracel = yf.download('OFSS.NS',start = s,end= e)
oracel['Symbol'] = 'OFSS'


# In[30]:


litm = yf.download('LTIM.NS',start = s,end= e)
litm['Symbol'] = 'LTIM'


# In[31]:


it = pd.concat([hcl,techm,persis,oracel,litm], axis=0)


# In[32]:


it


# In[33]:


it['Category'] = 'IT'


# In[34]:


it


# In[35]:


it = it.reset_index()


# In[36]:


it


# In[37]:


it.to_csv("anushka_ITStock.csv")


# In[ ]:





# In[ ]:





# In[ ]:




