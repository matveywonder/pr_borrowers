#!/usr/bin/env python
# coding: utf-8

# # Исследование надежности заемщиков


# In[1]:


import pandas as pd # импортируем библиотеку pandas


# In[2]:


data = pd.read_csv('/datasets/data.csv') # прочитаем csv-файл


# In[3]:


data.head(20) 


# In[4]:


data.info() 


# ## Предобработка данных

# ### Удаление пропусков


# In[5]:


data.isna().sum() 


# In[6]:


for i in data['income_type'].unique():
    data.loc[(data['income_type'] == i) & (data['total_income'].isna()), 'total_income'] =     data.loc[(data['income_type'] == i), 'total_income'].median()


# ### Обработка аномальных значений


# In[7]:


data['days_employed'] = data['days_employed'].abs()
print(data)


# In[8]:


data.groupby('income_type')['days_employed'].median()


# У двух типов (безработные и пенсионеры) получатся аномально большие значения. Исправить такие значения сложно, поэтому оставим их как есть.


# In[9]:


data['children'].unique() 


# In[10]:


data = data[(data['children'] != -1) & (data['children'] != 20)]


# In[11]:


data['children'].unique() # ваш код здесь


# ### Удаление пропусков (продолжение)


# In[12]:


for i in data['income_type'].unique():
    data.loc[(data['income_type'] == i) & (data['days_employed'].isna()), 'days_employed'] =     data.loc[(data['income_type'] == i), 'days_employed'].median() 


# In[13]:


data.isna().sum() 


# ### Изменение типов данных


# In[14]:


data['total_income'] = data['total_income'].astype('int') 


# ### Обработка дубликатов


# In[15]:


data['education'] = data['education'].str.lower()


# In[16]:


data['education'].duplicated().count() # посчитаем дубликаты


# In[17]:


data = data.drop_duplicates() # удалим дубликаты


# ### Категоризация данных


# In[18]:


def categorize_income(income):
    
    if income <= 30000:
        return 'E'
    if income >= 30001 and income <= 50000:
        return 'D'
    if income >= 50001 and income <= 200000:
        return 'C'
    if income >= 200001 and income <= 1000000:
        return 'B'
    return 'A'


# In[19]:


data['total_income_category'] = data['total_income'].apply(categorize_income)


# In[20]:


data['purpose'].unique() 


# In[21]:


def categorize_purpose(purpose):
    
    if 'автом' in purpose:
        return 'операции с автомобилем'
    elif 'жил' in purpose or 'недвиж' in purpose:
        return 'операции с недвижимостью'
    elif 'свадьб' in purpose:
        return 'проведение свадьбы'
    elif 'образов':
        return 'получение образования'


# In[22]:


data['purpose_category'] = data['purpose'].apply(categorize_purpose)


# In[ ]:




