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





