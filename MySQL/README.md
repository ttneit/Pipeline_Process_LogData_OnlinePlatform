# Set up MySQL in Docker
1. Pull the latest MySQL Docker Image
```
docker pull mysql:latest
```
2. Run the MySQL Docker Container
```
docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=1 -p 3306:3306 -d mysql:latest

```
3. Connect to MySQL 
```
mysql -u root -p
```

4. Before copy csv file to MySQL table , import the csv file to MySQL container