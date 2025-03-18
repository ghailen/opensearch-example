# opensearch-example
***An Introduction to OpenSearch***

OpenSearch is a community-driven, open-source search and analytics suite. It is a tool that lets you store, search, and analyse large volumes of data quickly and in near real-time. It is typically used for storing items such as data from log files, but it can also handle any type of structured or unstructured data.

***What you will learn in this tutorial***

In this OpenSearch tutorial, we will systematically explore the various aspects of this powerful tool. The following points provide an overview of what you can expect to learn from this guide:

    Learn how to connect to an OpenSearch cluster using the provided API.
    Understand how to perform basic OpenSearch operations such as creating and deleting indices.
    Learn how to add data to an index individually and in bulk.
    Learn how to search data within an index using the OpenSearch API.
    Learn how to access OpenSearch Dashboards and interact with data in the cluster.
    Understand the concept of index patterns and learn how to create one.
    Discover how to create visually appealing dashboards and visualisations using the index pattern.


***Installation:***
we can use docker to setup the opensearch :
https://opensearch.org/versions/opensearch-2-19-1.html
in this repo there is the docker-compose.yml and the .env file (the .env file contains the password to use to access to the opensearch dashboard , it must be in the same folder as docker-compose.yml) 
then point to the folder which contains the two files , and run : docker compose up
![image](https://github.com/user-attachments/assets/10f72bdf-c24f-4222-9f50-6dbba7705a0c)

the dashboard run on the port :
http://localhost:5601/app/home#/
![image](https://github.com/user-attachments/assets/944bba47-32e9-4567-9602-17a15009ba29)

and the node is up on the port 9200:

we must use the -k to avoid ssl problem 
curl -k -u admin:{{mypassword}} https://localhost:9200 :
![image](https://github.com/user-attachments/assets/3b982ed7-5189-4117-bd03-865929ed15ac)
![image](https://github.com/user-attachments/assets/dccc0adb-027b-4be4-bf35-35a37d3d98e9)

***Creating an index***
First, let’s create a new index within our newly created OpenSearch cluster. We’ll call the new index “movie_ratings” and we’ll also define the index mapping to include fields like “title” for the movie title, “genre” for the movie genre, and “rating” for the movie’s rating. Our index will contain two shards and one replica.

This can be done using the following OpenSearch API request:
https://localhost:9200/movie_ratings
```json
curl --location --request PUT 'https://localhost:9200/movie_ratings' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json' \
--data '{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "genre": {
        "type": "text"
      },
      "rating": {
        "type": "float"
      }
    }
  }
}'
```
=> result:
![image](https://github.com/user-attachments/assets/d009803c-94a1-4c00-9fba-886978e56811)

“acknowledged” in the response indicates that the index was successfully created.
***Listing all Indices***
```json
curl --location 'https://localhost:9200/_cat/indices?v=null' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json'
```
![image](https://github.com/user-attachments/assets/eb6d077a-58bf-4150-8251-9b4390db1e3d)

The command’s response presents a table displaying the indices within our cluster – including the new movie_rating index we just created. Below is a brief description of what each column in the table means.

    health: Represents the health status of the index, where “green” indicates that all primary and replica shards are active and assigned, “yellow” indicates that all primary shards are active and assigned but not all replica shards are active, and “red” indicates that some or all primary shards are not active.
    status: Indicates whether the index is open or closed. An open can be read from and written to, while an index that is closed cannot be accessed.
    index: The name of the index.
    uuid: The unique identifier for the index.
    pri: The number of primary shards for the index.
    rep: The number of replica shards for the index.
    docs.count: The number of documents in the index.
    docs.deleted: The number of deleted documents in the index.
    store.size: The size of the index on disk, including both primary and replica shards.
    pri.store.size: The size of the primary shards on the disk.


Whenever you list the indices in a cluster, chances are you’ll see indices that you did not create. These special indices are created automatically and usually begin with a dot, like .kibana_1, in the screenshot above. This particular index (.kibana_1) is used by Kibana, an open-source data visualisation tool commonly used with OpenSearch. Kibana stores its configuration in this index, so unless you have a specific need or understanding of its impact, you should not modify this or any other special index that was created automatically.

***Adding data to our index***
You should now have a newly created empty index called movie_ratings. However, before you can search it for data, you must first add data to it. This data is known as documents, and the process of adding documents to an index so that it is searchable is known as indexing.

To index a single document, use the request below:

The body of the request contains the document data itself. In the example below, the document consists of a single record that includes the movie title, its genre, and its respective IMDb rating. It would appear as follows:
```json
curl --location 'https://localhost:9200/movie_ratings/_doc' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json' \
--data '{
  "title": "The Shawshank Redemption",
  "genre": "Drama",
  "rating": 9.3
}'
```
![image](https://github.com/user-attachments/assets/dbf93c9c-edb5-4dda-8f18-7663be44da1e)

The response returned by OpenSearch confirms that the document was successfully indexed. Below is an explanation of what some of the attributes in the response mean.
_index: the name of the index where the document was indexed.
_id: the unique identifier for the document that we just indexed. OpenSearch automatically assigns a unique ID to each document if you don’t provide one.
_version: the version of the document. It’s useful for concurrency control. In this case, it’s 1, indicating that this is the first version of the document.
result: the outcome of the operation.
