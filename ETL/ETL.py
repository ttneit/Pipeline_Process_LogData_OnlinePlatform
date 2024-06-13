import pyspark.sql.functions as sf
from uuid import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from uuid import * 
from uuid import UUID
from pyspark.sql.window import Window as W
import time_uuid 
import datetime




def convert_to_date(input_str : str) : 
    return time_uuid.TimeUUID(bytes=UUID(input_str).bytes).get_datetime().strftime('%Y-%m-%d %H:%M:%S')


def preprocessing(raw_df) : 
    processed_df = raw_df.withColumn('ts',convertUUID_udf('create_time'))
    processed_df = processed_df.fillna({'bid':0})
    processed_df = processed_df.drop("create_time")
    return processed_df


def process_click_data (df ) : 
    temp_df = df.filter(df.custom_track == 'click')
    temp_df = temp_df.fillna({'job_id':0,'publisher_id':0,'group_id':0,'campaign_id':0})
    calculated_df = temp_df.groupby('campaign_id','publisher_id','group_id','job_id'
                                          ,sf.date_format(sf.col("ts"), "yyyy-MM-dd").alias("date"),
                                        sf.hour(sf.col("ts")).alias("hour"),)\
                                        .agg(sf.count("*").alias("click_nums"), sf.avg("bid").alias("bid_set"),sf.sum("bid").alias("spend_hours"))
    return calculated_df

def process_fields_data (df , fields_col) : 
    temp_df = df.filter(df.custom_track == fields_col)
    temp_df = temp_df.fillna({'job_id':0,'publisher_id':0,'group_id':0,'campaign_id':0})
    calculated_df = temp_df.groupby('campaign_id','publisher_id','group_id','job_id'
                                    ,sf.date_format(sf.col("ts"), "yyyy-MM-dd").alias("date"),
                                    sf.hour(sf.col("ts")).alias("hour"),) \
                            .agg(sf.count("*").alias(f"{fields_col}_nums"))
    return calculated_df

def process_cassandra_data (df) : 
    all_fields = ['conversion','unqualified','qualified']
    full_df = process_click_data(df)
    for field in all_fields :
        field_df = process_fields_data(df,field)
        full_df = full_df.join(field_df,on=['campaign_id','publisher_id','group_id','job_id','hour','date'],how="full" )
    return full_df

def get_company_data(url,driver,user,password) : 
    sql = """(select id as job_id , company_id , group_id , campaign_id from job) query"""
    company = spark.read.format('jdbc').options(url=url,driver=driver , dbtable = sql ,user=user ,password = password).load()
    return company

def import_to_mysql(df) : 
    final_output = df.withColumnRenamed('date','dates').withColumnRenamed('hour','hours')
    final_output = final_output.withColumn('latest_updated_time', sf.date_format(sf.current_timestamp(), 'yyyy-MM-dd HH:mm:ss'))
    final_output = final_output.withColumn('sources',sf.lit('Cassandra'))
    final_output.printSchema()
    final_output.write.format('jdbc') \
    .option("driver",driver) \
    .option("url", f"jdbc:mysql://{host}:{port}/{db_name}") \
    .option("dbtable", "events") \
    .mode("append") \
    .option("user", user) \
    .option("password", password) \
    .save()
    return print('Data imported successfully')

def get_latest_cassandra_time() : 
    raw_df = spark.read.format("org.apache.spark.sql.cassandra") \
                .options(table='tracking',keyspace = 'practice_de').load()
    time_df = raw_df.select('create_time')
    time_df = time_df.withColumn('ts',convertUUID_udf('create_time'))

    latest_time_df  = time_df.agg(sf.max(sf.col('ts')).alias('latest_time'))
    return latest_time_df.first().latest_time

def get_latest_mysql_time(url,driver,user,password) : 
    sql = """(select max(latest_updated_time) as latest_time from events) query"""
    try : 
        time = spark.read.format('jdbc').options(url=url,driver=driver , dbtable = sql ,user=user ,password = password).load()
    except : 
        return "1900-01-01 00:00:00"
    if time is None : 
        return "1900-01-01 00:00:00"
    else : 
        return time.first().latest_time


def main(url,driver,user,password,mysql_time) : 
    print('------------------------------------------------------------------------------------')
    print('Retrieving data from Cassandra')
    print('------------------------------------------------------------------------------------')
    raw_df = spark.read.format("org.apache.spark.sql.cassandra") \
            .options(table='tracking',keyspace = 'practice_de').load()
    print('------------------------------------------------------------------------------------')
    print('Extraxting data from Cassandra')
    print('------------------------------------------------------------------------------------')
    df = raw_df.select('create_time','bid','campaign_id','publisher_id','group_id','job_id','ts','custom_track')
    df = df.filter(df.job_id.isNotNull())
    df.printSchema()
    print('------------------------------------------------------------------------------------')
    print('Preprocessing Cassandra data')
    print('------------------------------------------------------------------------------------')
    preprocessed_df = preprocessing(df)
    preprocessed_df = preprocessed_df.filter(sf.col('ts') > mysql_time)
    preprocessed_df.printSchema()

    print('------------------------------------------------------------------------------------')
    print('Processing Cassandra data')
    print('------------------------------------------------------------------------------------')
    processed_df  = process_cassandra_data(preprocessed_df)
    processed_df.printSchema()
    print('------------------------------------------------------------------------------------')
    print('Extracting company data')
    print('------------------------------------------------------------------------------------')
    company_df = get_company_data(url,driver,user,password)
    final_df = processed_df.join(company_df, on=['job_id'],how='left').drop(company_df.group_id).drop(company_df.campaign_id)
    print('------------------------------------------------------------------------------------')
    print('Import Output to MySQL')
    print('------------------------------------------------------------------------------------')
    import_to_mysql(final_df)
    return print('Task Finished')

if __name__ == '__main__' : 
    spark = SparkSession.builder \
        .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.4.0") \
        .config("spark.cassandra.connection.host", "my-cassandra") \
        .config("spark.cassandra.connection.port", "9042") \
        .config("spark.cassandra.auth.username", "cassandra") \
        .config("spark.cassandra.auth.password", "cassandra") \
        .getOrCreate()

    start_time = datetime.datetime.now()
    host = 'my-mysql'
    port = 3306
    db_name = 'dw'
    user = 'root'
    password = '1'
    url = f'jdbc:mysql://{host}:{port}/{db_name}'
    driver = "com.mysql.cj.jdbc.Driver"
    convertUUID_udf = sf.udf(lambda row : convert_to_date(row))
    cassandra_time = get_latest_cassandra_time()
    mysql_time = get_latest_mysql_time(url,driver,user,password)

    print('The latest time from Cassandra :',cassandra_time)
    print('The latest time from MySQL :',mysql_time)
    if mysql_time >= cassandra_time : 
        print('There is no new data')
        spark.stop()
    else : 
        main(url,driver,user,password,mysql_time)

    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    print('Job takes {} seconds to execute'.format(execution_time))
