# The system process log data from Online Recruitment Application

## Objective 
This idea of this project is building a system to process log data from Online Recruitment Application . The log data from applications such as website or mobile apps will be sent to Kafka in the middle step before being inserted into the Datalake in Cassandra . From raw data in Cassandra , the system build a ETL pipeline to process data then store processed data in MySQL . Now this data can be visualized in visualization tools like Grafana , Power BI , Tableau to bring insights about the labor market 

Tech stack : Python , Kafka , PySpark , Cassandra , MySQL

## Data Structure  
### Datalake : 
Contains the log data about the events that just happened in applications . The log data created when user interacts with the applications then applications will send this data to Kafka and in Kafka the system will insert data in Datalake (Cassandra)

#### Schema : 
```
root
 |-- create_time: string (nullable = false)
 |-- bid: integer (nullable = true)
 |-- bn: string (nullable = true)
 |-- campaign_id: integer (nullable = true)
 |-- cd: integer (nullable = true)
 |-- custom_track: string (nullable = true)
 |-- de: string (nullable = true)
 |-- dl: string (nullable = true)
 |-- dt: string (nullable = true)
 |-- ed: string (nullable = true)
 |-- ev: integer (nullable = true)
 |-- group_id: integer (nullable = true)
 |-- id: string (nullable = true)
 |-- job_id: integer (nullable = true)
 |-- md: string (nullable = true)
 |-- publisher_id: integer (nullable = true)
 |-- rl: string (nullable = true)
 |-- sr: string (nullable = true)
 |-- ts: string (nullable = true)
 |-- tz: integer (nullable = true)
 |-- ua: string (nullable = true)
 |-- uid: string (nullable = true)
 |-- utm_campaign: string (nullable = true)
 |-- utm_content: string (nullable = true)
 |-- utm_medium: string (nullable = true)
 |-- utm_source: string (nullable = true)
 |-- utm_term: string (nullable = true)
 |-- v: integer (nullable = true)
 |-- vp: string (nullable = true)
```
### Data Warehouse : 
Contains the events data . For example : In each hour in each day , there are how many people click in the job (the job belongs to which campaign ,group , company) .

#### Schema : 
```
root
 |-- job_id: integer (nullable = true)
 |-- campaign_id: integer (nullable = true)
 |-- publisher_id: integer (nullable = true)
 |-- group_id: integer (nullable = true)
 |-- hours: integer (nullable = true)
 |-- dates: string (nullable = true)
 |-- click_nums: long (nullable = true)
 |-- bid_set: double (nullable = true)
 |-- spend_hours: long (nullable = true)
 |-- conversion_nums: long (nullable = true)
 |-- unqualified_nums: long (nullable = true)
 |-- qualified_nums: long (nullable = true)
 |-- company_id: integer (nullable = true)
 |-- latest_updated_time: string (nullable = false)
 |-- sources: string (nullable = false)
```
## Process data
Calculate the number of user clicks , conversions , the number of user qualified , unqualified for all jobs in platform 
Step :
1. Filter the action in 4 `customer_tracks` `['click','conversion','unqualified','qualified']`
2. Fill null data
3. Calculate the value for further analyze step 
4. Store processed in MySQL

## Setup 
Cassandra : [Cassandra Setup](./Cassandra/README.md)

Spark : [Spark Setup](./ETL/Dockerfile)

Kafka : [Kafka Setup](./kafka/README.md)

MySQL : [MySQL Setup](./MySQL/README.md)
