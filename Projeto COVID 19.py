#!/usr/bin/env python
# coding: utf-8

# In[37]:


import requests as r
import csv
import datetime


# In[38]:


url = 'https://api.covid19api.com/dayone/country/brazil'

resp = r.get(url)


# In[39]:


resp.status_code


# In[40]:


raw_data = resp.json()


# In[41]:


raw_data[0]


# In[42]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'],obs['Deaths'],obs['Recovered'],obs['Active'],obs['Date']])


# In[43]:


final_data.insert(0,['Confirmados','Obitos','recuperados','ativos','data'])

final_data


# In[44]:


CONFIRMADOS = 0
OBITOS = 1 
RECUPERADOS = 2
ATIVOS = 3
DATA = 4


# In[45]:


for i in range(1,len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]


# In[46]:


final_data


# In[47]:


with open('brasil-covid.csv','w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[48]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA],'%Y-%m-%d')


# In[49]:


final_data


# In[51]:


def get_datasets(y, labels):
    if type(y[0])==list:
        datasets = []
        for i in range(len(y)):
            datasets.append({'label':labels[i],'data': y[i]})
        return datasets
    else:
        return[{'label':labels[0],'data':y}]


# In[52]:


def set_title(title=''):
    if title !='':
        display = 'true'
    else:
        display = 'false'
    return {'title':title,'display':display}


# In[53]:


def create_chart(x, y, labels, kind='bar', title=''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
        'type':kind,
        'data':{
            'labels':x,
            'datasets':datasets
        },
        'options':options
    }
    return chart


# In[55]:


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content


# In[57]:


def save_image(path, content):
    with open(path,'wb') as image:
        image.write(content)


# In[59]:


from PIL import Image
from IPython.display import display


# In[63]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[69]:


y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])
    
y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[RECUPERADOS])
    
labels = ['Confirmados','Recuperados']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d-%m-%Y'))

chart = create_chart(x, [y_data_1, y_data_2],labels,title='Gráfico confirmados vs recuperados')
chart_content = get_api_chart(chart)
save_image('Gráfico-Projeto-Covid.png', chart_content)
display_image('Gráfico-Projeto-Covid.png')

