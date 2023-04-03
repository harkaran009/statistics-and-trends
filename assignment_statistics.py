#!/usr/bin/env python
# coding: utf-8

# # first step is to import and load all the required modules 

# In[91]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import seaborn as sns
# pd.set_option('max_columns', 300)


# # below i have created a function to load csv files in accordance to World bank format

# In[92]:


def read_csv(filename):
    try:
        df1 = pd.read_csv(filename)

        df1 = df1.drop(columns = [ 'Indicator Name','Country Code','Indicator Code',
           '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
           '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
           '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
           '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
           '1996', '1997', '1998', '1999'], axis = 1)
        df1 = df1.fillna(0)
        df1 = df1.loc[df1['Country Name'].isin(['India',
                                                'United Kingdom',
                                                'Bangladesh',
                                                'Ecuador',
                                                'China',
                                                'Sweden',
                                                'France',
                                                'United States',
                                                'Nigeria',
                                                'Brazil',
                                                'South Africa',
                                                'World'])]
        
       
        
        df1 = df1.reset_index(drop=True)

        df2 = df1.transpose()
        df2.columns = df2.iloc[0]
        df2 = df2.iloc[1:]
        
        df2 = df2.reset_index()
        df2 = df2.rename(columns={'index': 'Year'})
    

        return df1, df2
    
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
    


# # here i have loaded the csv file and then data to be split into 2 dataframes 

# In[93]:


df1_pop_growth, df2_pop_growth = read_csv('API_SP.POP.GROW_DS2_en_csv_v2_5352531.csv')


# In[94]:


df1_electricity_acc, df2_electricity_acc = read_csv('API_EG.ELC.ACCS.ZS_DS2_en_csv_v2_4902219.csv')


# In[95]:


df1_co2_em, df2_co2_em = read_csv('API_EN.ATM.CO2E.KT_DS2_en_csv_v2_5335725.csv')


# In[96]:


df1_gdp, df2_gdp = read_csv('API_NY.GDP.PCAP.CD_DS2_en_csv_v2_5357510.csv')


# # Here i have loaded the first data set where years are columns and countries are rows

# In[97]:


df1_pop_growth


# # Here i have loaded the second data set where years are rows and countries are columns for population DATA

# In[98]:


df2_pop_growth


# In[99]:


df1_gdp


# # function to plot histograms 

# In[100]:


def plot_histogram(data, xlabel=None, ylabel=None, title=None, bins=None):

    fig, ax = plt.subplots()
    
    if bins:
        ax.hist(data, bins=bins)
    else:
        ax.hist(data)

    if xlabel:
        ax.set_xlabel(xlabel)

    if ylabel:
        ax.set_ylabel(ylabel)

    if title:
        ax.set_title(title)
    
    plt.show()


# # below i have created function for creating bar plot

# In[101]:


def plot_multibar(df, x_col, y_cols, x_label=False, y_label=False, title=False, rotate=False, savefig_image=False):

    fig, ax = plt.subplots()

    n = len(y_cols)
    width = 0.8 / n
    x = np.arange(len(df[x_col]))

    for i in range(n):
        offset = (i - (n-1)/2) * width
        ax.bar(x + offset, df[y_cols[i]], width=width, label=y_cols[i])
        
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(df[x_col], rotation=rotate)
    
    ax.legend(bbox_to_anchor=(1.00, 1.0), loc='upper left')
    ax.grid(axis = 'y') 
    plt.tight_layout()
    plt.savefig(savefig_image, dpi = 300)
    plt.show()
    
    


# # i have below used the bar plot function to plot population rise and CO2 emision 

# In[102]:


plot_multibar(df1_pop_growth,x_col='Country Name',
              y_cols=['2010','2011','2012','2013','2014','2015','2016', '2017', '2018', '2019', '2020'],
              x_label='countries',
              y_label='population rise annual percentage %',
              title = 'population rise from 2010 to 2020',
              rotate = 90,
              savefig_image = 'population.png')



# In[103]:


plot_multibar(df1_gdp,x_col='Country Name',
              y_cols=['2010','2011','2012','2013','2014','2015','2016', '2017', '2018', '2019', '2020'],
              x_label='countries',
              y_label='GPD in (million $)',
              title = 'GDP of different countries',
              rotate = 90,
              savefig_image = 'gdp.png')


# In[104]:


plot_multibar(df1_co2_em,x_col='Country Name',
              y_cols=['2010','2011','2012','2013','2014','2015','2016', '2017', '2018', '2019', '2020'],
              x_label='countries',
              y_label='CO2 emssion in kilo tons',
              title = 'CO2 emssions',
              rotate = 90,
              savefig_image = 'co2.png')


# In[105]:


dfco2 = df1_co2_em.set_index('Country Name')
dfco2 = dfco2.round(1)

dfgdp = df1_gdp.set_index('Country Name')

a = dfgdp.corrwith(dfco2, axis = 1)

plt.figure(figsize=(16,9))
 
sns.heatmap(dfco2, cmap="crest", annot = False, linewidth = 2)
plt.title("Heatmap representing rise in CO2 emissions", fontsize = 25)
plt.xlabel("CO2 emissions (metric tons per capita) Per Year", fontsize = 20)
plt.ylabel("Countries", fontsize = 20)
plt.savefig('heatmap_co2_country.png', dpi=300)
plt.show()

ax = plt.figure()
plt.barh(a.index,a)
plt.ylabel('Countries')
plt.title('correlation representation between GDP in regards to rise in CO2')
plt.grid(axis='y')
plt.savefig('correlation_bar.png', dpi = 300)
plt.show()



# In[ ]:





# In[106]:



plt.figure(figsize=(16,9))
df1_pop_growth = df1_pop_growth.set_index('Country Name')
sns.heatmap(df1_pop_growth, cmap="crest", annot = True, linewidth = 2)
plt.title("Heatmap representing rise Population %", fontsize = 25)
plt.xlabel("Year", fontsize = 20)
plt.ylabel("Country Name", fontsize = 20)
plt.savefig('rise_pop_heatmap.png', dpi=300)
plt.show()


# In[107]:


plt.figure(figsize=(20,10))
 
sns.heatmap(dfco2.corr(), cmap="crest", annot = True, linewidth = 2)
plt.title("Heatmap representing correlation in CO2 emissions", fontsize = 25)
plt.xlabel("year", fontsize = 20)
plt.ylabel("year", fontsize = 20)
plt.savefig('heatmap_corr_co2.png', dpi=300)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




