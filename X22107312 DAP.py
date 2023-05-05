#!/usr/bin/env python
# coding: utf-8

# NAME: TAIWO MUBARAK OLADAPO
#     
# ID: 22107312
#     
# DOMAIN: CRIME
#     
# https://catalog.data.gov/dataset/index-crimes-by-county-and-agency-beginning-1990/resource/6e32ad5e-770f-49f7-b3fc-48c40f69ab5e

# In[1]:


# import necessary libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import urllib
import json
import luigi
import psycopg2

import pymongo
from pymongo import MongoClient, InsertOne

#Ignore the warnings
import warnings
warnings.filterwarnings("ignore")


# In[2]:


# Load the URL

url = "https://data.ny.gov/api/views/ca8h-8gjq/rows.json"


# In[3]:


# Extract the json data

response = urllib.request.urlopen(url)
data = json.loads(response.read())
response.close()


# In[4]:


# Extract the column names from the metadata
df_columns = pd.DataFrame(data["meta"]["view"]["columns"])
columns = df_columns['fieldName'].tolist()


# In[5]:


# Create a DataFrame from the data with the extracted column names
df_data = pd.DataFrame(data["data"], columns=columns)


# In[6]:


# Drop unnecessary columns
df_data.drop([':sid',':id',':position',':created_at',':created_meta',':updated_at',':updated_meta',':meta'], axis = 1 , inplace = True)
columns = df_data.columns
columns


# In[7]:


# Description of fields

df_columns.drop(index = [0,1,2,3,4,5,6,7], axis = 0, inplace = True)
df_columns[['fieldName', 'description']]


# # Storing data in MongoDB

# In[8]:


client = pymongo.MongoClient("mongodb://localhost:27017")
client


# In[9]:


# Create database and collection
db_name = 'Crimes_database'
collection_name = 'Crimes_collection'
if db_name in client.list_database_names():
    print(f"databaes {db_name} is exist.")
else: 
    db = client[db_name]
    if collection_name in client.db.list_collection_names():
        print(f"Collection {collection_name} is exist.")
    else :
        collection = db[collection_name]


# In[10]:


# Convert dataset to dictionary
dict_data = df_data.to_dict(orient="records")
# insert data into mongo db
db = client[db_name]
db[collection_name].insert_many(dict_data)


# In[11]:


uri = "mongodb+srv://dap:dap@cluster0.dcyzoyt.mongodb.net/test"


# In[12]:


client = pymongo.MongoClient(uri)


# In[13]:


db = client["CrimeDataset"]


# In[14]:


print(db)


# In[15]:


db.NewYorkCrime.insert_many(dict_data)


# # ETL Process Using Luigi Python Libraries

# In[16]:


# create a class to run luigi task and run the pipeline 
class LoadFromMongodb(luigi.Task):
    """
    A Luigi task to write a json file into mongodb
    """
    client = luigi.Parameter()
    database = luigi.Parameter()
    collection = luigi.Parameter()
    path = luigi.Parameter()

    def output(self):
        """
        Returns the target output for this task. 

        """
        return luigi.LocalTarget(self.path)

    def run(self):
        """
        Contains the logic of the Task, 
        """
        # setting mongodb client
        client = pymongo.MongoClient(self.client)
        db = client[self.database]
        collection = db[self.collection]
        
        # load data from mongo db and save into dataframe
        loaded_data = collection.find()
        df = pd.DataFrame(loaded_data)
        df.drop(['_id'], axis = 1, inplace = True)
        with self.output().open("w") as f:
            f.write(df.to_csv(index = False))


# In[17]:


luigi.build([LoadFromMongodb(client="mongodb://localhost:27017", database="Crimes_database", collection = "Crimes_collection",
                             path = "Crime_database.csv")], workers=1, local_scheduler=True)


# In[18]:


df= pd.read_csv("Crime_database.csv")


# In[19]:


df.head()


# # Handling missing values

# In[20]:


df.shape


# In[21]:


df.info()


# In[22]:


df.isna().sum().sort_values(ascending = False)/df.shape[0]*100


# In[23]:


df = df.dropna(subset=['Index Total' , 'Violent Total', 'Murder', 'Rape', 'Robbery', 'Aggravated Assault',
                      'Property Total', 'Burglary', 'Larceny', 'Motor Vehicle Theft'], axis = 0)
df.shape


# In[24]:


df['Months Reported'] = df['Months Reported'].fillna(0)


# In[25]:


df.to_csv('New_data.csv', index=False) # index=False to exclude index column


# In[26]:


df.isna().sum()


# In[27]:


df.head()


# # Storing Structured datasets in PostgreSQL

# In[28]:


conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="Oladapotaiwo#1998",
                        port="5432")
conn.autocommit = True
cursor = conn.cursor()
# create database
query = '''CREATE database Crime_database'''
try: 
    cursor.execute(query)
    conn.close()
except Exception as e:
    conn.close()
    print(str(e))


# In[29]:


# create table
conn = psycopg2.connect(database="crime_database",
                        host="localhost",
                        user="postgres",
                        password="Oladapotaiwo#1998",
                        port="5432")
cursor = conn.cursor()

    
query ='''CREATE TABLE crime_data(county VARCHAR(255), agency VARCHAR(255), year INTEGER, months_reported FLOAT,
       index_total FLOAT, violent_total FLOAT, murder FLOAT, rape FLOAT, robbery FLOAT,
       aggravated_assault FLOAT, property_total FLOAT, burglary FLOAT, larceny FLOAT, motor_vehicle_theft FLOAT,
       region VARCHAR(255))'''
try:
    cursor.execute(query)
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print(str(e))


# In[30]:


# Insert data into table

conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)

cursor = conn.cursor()

with open('New_data.csv', 'r') as f:
    next(f) # skip the header row
    cursor.copy_from(f, 'crime_data', sep=',')
    
conn.commit()

cursor.close()
conn.close()


# # Analysis and Visualization

# In[31]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)

query = """SELECT "year", SUM(index_total) AS total_crimes
           FROM crime_data
           GROUP BY "year"
           ORDER BY "year";"""

df = pd.read_sql(query, conn)

plt.bar(df['year'], df['total_crimes'])
plt.xlabel('year')
plt.ylabel('Number of Crimes')
plt.title('Total Number of Crimes by Year')
plt.show()

conn.close()


# In[32]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)

query = """SELECT "region", SUM(index_total) AS total_crimes
           FROM crime_data
           GROUP BY "region"
           ORDER BY "region";"""

df = pd.read_sql(query, conn)

plt.bar(df['region'], df['total_crimes'])
plt.title('Total Number of Crimes by Region')
plt.xlabel('region')
plt.ylabel('Number of Crimes')
plt.show()

conn.close()


# In[33]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT 'Violent' AS crime_type, SUM("violent_total") AS total
           FROM crime_data
           UNION ALL
           SELECT 'Non-Violent' AS crime_type, SUM("index_total") - SUM("violent_total") AS total
           FROM crime_data"""
cur = conn.cursor()
cur.execute(query)
results = cur.fetchall()
df = pd.DataFrame(results, columns=['crime_type', 'total'])

plt.pie(df['total'], labels=df['crime_type'], autopct='%1.1f%%')
plt.title('Proportion of Violent Crimes to Overall Crimes')
plt.show()

cur.close()
conn.close()


# In[34]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT SUM(murder) AS murder_total, SUM(rape) AS rape_total, 
           SUM(robbery) AS robbery_total, SUM(aggravated_assault) AS assault_total
           FROM crime_data;"""
cursor = conn.cursor()
cursor.execute(query)

data = cursor.fetchall()
df = pd.DataFrame(data, columns=['murder_total', 'rape_total', 'robbery_total', 'assault_total'])
violent_types = ['Murder', 'Rape', 'Robbery', 'Aggravated Assault']
violent_totals = [df['murder_total'].iloc[0], df['rape_total'].iloc[0], 
                  df['robbery_total'].iloc[0], df['assault_total'].iloc[0]]

plt.bar(violent_types, violent_totals)
plt.title('Total Number of Each Type of Violent Crime')
plt.xlabel('Type of Crime')
plt.ylabel('Number of Crimes')
plt.show()

cursor.close()
conn.close()


# In[35]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT SUM(burglary) AS burglary_total, SUM(larceny) AS larceny_total, 
           SUM(motor_vehicle_theft) AS motor_vehicle_theft_total
           FROM crime_data;"""
cursor = conn.cursor()
cursor.execute(query)

data = cursor.fetchall()
df = pd.DataFrame(data, columns=['burglary_total', 'larceny_total', 'motor_vehicle_theft_total'])
non_violent_types = ['burglary', 'larceny', 'motor_vehicle_theft']
non_violent_totals = [df['burglary_total'].iloc[0], df['larceny_total'].iloc[0], 
                  df['motor_vehicle_theft_total']]

plt.bar(non_violent_types, non_violent_totals)
plt.title('Total Number of Each Type of Non-Violent Crime')
plt.xlabel('Type of Crime')
plt.ylabel('Number of Crimes')
plt.show()

cursor.close()
conn.close()


# In[36]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT year, SUM(Violent_total) AS violent_total 
           FROM crime_data 
           GROUP BY year 
           ORDER BY year;"""

df = pd.read_sql(query, conn)
plt.bar(df['year'], df['violent_total'])
plt.title('Total Violent Crimes by Year')
plt.xlabel('Year')
plt.ylabel('Total Violent Crimes')
plt.show()

conn.close()


# In[37]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT County, SUM(Violent_total) AS violent_total 
           FROM crime_data 
           GROUP BY County;"""

df = pd.read_sql(query, conn)
plt.figure(figsize=(11,5))
plt.bar(df['county'], df['violent_total'])
plt.title('Total Violent Crimes by County')
plt.xlabel('County')
plt.ylabel('Total Violent Crimes')
plt.xticks(rotation=90)
plt.show()

conn.close()


# In[38]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT "year", SUM(burglary + larceny + motor_vehicle_theft) AS "Property Total"
           FROM crime_data
           GROUP BY "year"
           ORDER BY "year";"""

df = pd.read_sql(query, conn)
plt.bar(df['year'], df['Property Total'])
plt.title('Total Non-Violent Crimes by Year')
plt.xlabel('Year')
plt.ylabel('Total Non-Violent Crimes')
plt.show()

conn.close()


# In[39]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)
query = """SELECT county, SUM(property_total) AS non_violent_total
           FROM crime_data
           GROUP BY county
           ORDER BY non_violent_total DESC;"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(11,5))
plt.bar(df['county'], df['non_violent_total'])
plt.title('Total Non-Violent Crimes by County')
plt.xlabel('County')
plt.ylabel('Total Non-Violent Crimes')
plt.xticks(rotation=90)
plt.show()

conn.close()


# In[40]:


conn = psycopg2.connect(
    dbname="crime_database",
    host="localhost",
    user="postgres",
    password="Oladapotaiwo#1998",
    port="5432"
)

query = """SELECT county, COUNT(*) as crime_count
           FROM crime_data
           GROUP BY County
           ORDER BY crime_count DESC;"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(11,5))
plt.bar(df['county'], df['crime_count'])
plt.title('Number of Crimes by County')
plt.xlabel('County')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=90)
plt.show()

conn.close()


# In[ ]:




