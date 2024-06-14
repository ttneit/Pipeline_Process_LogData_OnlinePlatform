# Set up Cassandra in Docker
1. Pull the latest Cassandra Docker Image
```
docker pull cassandra:latest
```
2. Run the Cassandra Docker Container
```
docker run -d    --name my-cassandra   -p 9042:9042    -e CASSANDRA_CLUSTER_NAME=practice_de -e CASSANDRA_USER=cassandra -e CASSANDRA_PASSWORD=cassandra  cassandra
```
3. Connect to Cassandra 
```
cqlsh
```
4. Before copy csv file to Cassandra table , import the csv file to Cassandra container