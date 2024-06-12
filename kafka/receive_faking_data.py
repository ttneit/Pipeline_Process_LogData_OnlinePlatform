from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster


cluster = Cluster(['localhost'])
session = cluster.connect(keyspace='practice_de')

consumer = KafkaConsumer(
    'log-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
try:
    for message in consumer:
        record = message.value
        print("Received message:", record)
        query = """
        INSERT INTO tracking (create_time, bid, campaign_id,  publisher_id, group_id, job_id, ts, custom_track) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            session.execute(query, (
                record['create_time'], 
                record['bid'], 
                record['campaign_id'], 
                record['publisher_id'], 
                record['group_id'], 
                record['job_id'], 
                record['ts'], 
                record['custom_track']
            ))
            print("Inserted new data successfully")
        except Exception as e:
            print("Error inserting data:", str(e))
except KeyboardInterrupt:
    print("KeyboardInterrupt: Stopping consumer...")
    consumer.close()