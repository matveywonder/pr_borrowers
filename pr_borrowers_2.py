#!/usr/bin/env python
# coding: utf-8


# In[1]:


import pandas as pd

try:
    data = pd.read_csv('/datasets/data.csv')
except:
    data = pd.read_csv('https://code.s3.yandex.net/datasets/data.csv')


# In[2]:


data.head(20)


# In[3]:


data.info()


# ## Предобработка данных

# ### Удаление пропусков

# In[4]:


#null_data = data[data['days_employed'].isnull()]
#null_data 
#Для задания 2.7.5  3.5 
data.isna().sum()


# In[5]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['total_income'].isna()), 'total_income'] =     data.loc[(data['income_type'] == t), 'total_income'].median()


# ### Обработка аномальных значений

# In[6]:


data['days_employed'] = data['days_employed'].abs()


# In[7]:


data.groupby('income_type')['days_employed'].agg('median')


# У двух типов (безработные и пенсионеры) получатся аномально большие значения. Исправить такие значения сложно, поэтому оставим их как есть.


# In[8]:


data['children'].unique()


# In[9]:


data = data[(data['children'] != -1) & (data['children'] != 20)]




# In[10]:


data['children'].unique()


# ### Удаление пропусков (продолжение)


# In[11]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['days_employed'].isna()), 'days_employed'] =     data.loc[(data['income_type'] == t), 'days_employed'].median()


# In[12]:


data.isna().sum()


# ### Изменение типов данных


# In[13]:


data['total_income'] = data['total_income'].astype(int)


# ### Обработка дубликатов


# In[14]:


data['education'] = data['education'].str.lower()


# In[15]:


data.duplicated().sum()


# In[16]:


data = data.drop_duplicates()


# ### Категоризация данных


# In[17]:


def categorize_income(income):
    try:
        if 0 <= income <= 30000:
            return 'E'
        elif 30001 <= income <= 50000:
            return 'D'
        elif 50001 <= income <= 200000:
            return 'C'
        elif 200001 <= income <= 1000000:
            return 'B'
        elif income >= 1000001:
            return 'A'
    except:
        pass


# In[18]:


data['total_income_category'] = data['total_income'].apply(categorize_income)


# In[19]:


data['purpose'].unique()


# In[20]:


def categorize_purpose(row):
    try:
        if 'автом' in row:
            return 'операции с автомобилем'
        elif 'жил' in row or 'недвиж' in row:
            return 'операции с недвижимостью'
        elif 'свад' in row:
            return 'проведение свадьбы'
        elif 'образов' in row:
            return 'получение образования'
    except:
        return 'нет категории'


# In[23]:


data['purpose_category'] = data['purpose'].apply(categorize_purpose)


# ### Шаг 3. Исследование данных

# #### 3.1 Есть ли зависимость между количеством детей и возвратом кредита в срок?

# In[33]:


children_debt = data.pivot_table(index='children', values='debt', aggfunc=['mean', 'count', 'sum'])
children_debt.columns = ['ratio', 'person', 'debt']
children_debt


# **Вывод:** Люди, имеющие от 1 до 4 детей, с большей вероятностью не смогут вернуть кредит в срок. У кого нет детей возвращают кредиты в срок чуть чаще. Клиенты с пятью детьми возвращают кредит вовремя, но их довольно мало для объективной оценки.


# #### 3.2 Есть ли зависимость между семейным положением и возвратом кредита в срок?

# In[34]:


children_debt = data.pivot_table(index='family_status', values='debt', aggfunc=['mean', 'count', 'sum'])
children_debt.columns = ['ratio', 'person', 'debt']
children_debt


# **Вывод:** Чаще всего возвращают кредит вовремя люди, которые раньше состояли в браке. Чуть хуже ситуация у семей, состоящих в браке. Клиенты не состоящие в браке, либо состоящие в незарегистрированном имеют больше всего просрочек по кредиту. Практически 10% не состоящих в браке имели просрочки.


# #### 3.3 Есть ли зависимость между уровнем дохода и возвратом кредита в срок?

# In[35]:


children_debt = data.pivot_table(index='total_income_category', values='debt', aggfunc=['mean', 'count', 'sum'])
children_debt.columns = ['ratio', 'person', 'debt']
children_debt


# **Вывод:** На основе полученных данных видно, что возможно сравнить только 2 группы (В и С), так как в остальных категориях недостаточное колличество клиентов. Из выше сказанного следует, что люди с доходом от 200 тысяч рублей до 1 млн. выплачивают кредиты вовремя чаще, чем клиенты с доходом от 50 тысяч до 200 тысяч рублей.

 
# #### 3.4 Как разные цели кредита влияют на его возврат в срок?

# In[36]:


children_debt = data.pivot_table(index='purpose_category', values='debt', aggfunc=['mean', 'count', 'sum'])
children_debt.columns = ['ratio', 'person', 'debt']
children_debt


# **Вывод:** Больше всего возвратов в срок, выдданных на операции с недвижимостью. Кредиты на образование и авто имееют худший результат. 


# ### Шаг 4: общий вывод.

# Гипотиза о том, что зависимость между количеством детей и возвратом кредита в срок подтверждена. Клиенты без детей возвращают кредит в срок раньше. Клиенты с пятью детьми возвращают кредит вовремя, но их количества не хватает для объективной оценки.
# 
# Люди не состоящие вбраке имеют больше всего просрочек по кредиту. Практически 10% не состоящих в браке имели просрочки, Чуть хуже ситуация у семей, состоящих в браке. Чаще всего возвращают кредит вовремя люди, которые раньше состояли в браке.(вдовец / вдова / в разводе). Стоит уделять больше внимания одиноким людям при выдаче кредита.
# 
# Гипотиза о зависимости между уровнем дохода и возвратом кредита в срок, не может быть доказана. Деление клиентов на группы по уровню дахода, не позволяет выявить зависимость. Однако, люди с доходом от 200 тысяч рублей до 1 млн. выплачивают кредиты вовремя чаще, чем клиенты с доходом от 50 тысяч до 200 тысяч рублей. Стоит обратить внимание на то как сформированны группы.
# 
# Кредиты на операции с недвижимостью и проведение свадьбы имеют большую вероятность, быть выплаченными вовремя, чем кредиты на получение образования и операции с автомобилем.
# 
