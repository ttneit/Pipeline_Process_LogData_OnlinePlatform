from kafka import KafkaProducer
import mysql.connector
import pandas as pd
import numpy as np
import random
import datetime 
import cassandra.util
import json
from sqlalchemy import create_engine


def get_job_data (engine) : 

    query = """SELECT id as job_id , group_id , campaign_id , company_id FROM job"""
    job_df = pd.read_sql(query,engine)
    return job_df


def get_publisher_data(engine) : 

    query = """SELECT distinct(id) as publisher_id  FROM master_publisher"""
    publisher_df = pd.read_sql(query,engine)
    return publisher_df


def faking_data (job_df , publisher_df ) : 
    group_list = set(job_df['group_id'].dropna().tolist())
    campaign_list = set(job_df['campaign_id'].dropna().tolist())
    company_list = set(job_df['company_id'].dropna().tolist())
    publisher_list = set(publisher_df['publisher_id'].dropna().tolist())
    job_list = set(job_df['job_id'].dropna().tolist())

    return {
        'create_time': str(cassandra.util.uuid_from_time(datetime.datetime.now())),
        'bid': np.random.randint(0,5) ,
        'campaign_id':  int(random.choice(list(campaign_list))),
        'company_id':  int(random.choice(list(company_list))),
        'publisher_id': int(random.choice(list(publisher_list))),
        'group_id': int(random.choice(list(group_list))),
        'job_id': int(random.choice(list(job_list))),
        'ts': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'custom_track': random.choice(['click','unqualified','qualified','conversion'])
    }
    

def json_serialize(data) : 
    return json.dumps(data).encode('utf-8')

if __name__ == "__main__"  :
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer = json_serialize)
    host = "localhost"
    user = "root"
    password = "1"
    db_name = "dw"

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"

    engine = create_engine(connection_string)


    for i in range(20) : 
        job_df = get_job_data(engine)
        publisher_df = get_publisher_data(engine)
        message = faking_data(job_df,publisher_df)
        producer.send('log-data', value=message)
        print(message)


    producer.flush()
    producer.close()