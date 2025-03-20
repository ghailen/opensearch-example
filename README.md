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

***Adding data in bulk***
a random example for test:
```json
curl --location 'https://localhost:9200/_bulk' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json' \
--data '
{ "index": { "_index": "test_index", "_id": "1" } }
{ "name": "Alice", "age": 25, "city": "Paris" }
{ "index": { "_index": "test_index", "_id": "2" } }
{ "name": "Bob", "age": 30, "city": "Lyon" }
{ "update": { "_index": "test_index", "_id": "1" } }
{ "doc": { "age": 26 } }
{ "delete": { "_index": "test_index", "_id": "2" } }
'
```
![image](https://github.com/user-attachments/assets/df02b6b1-7fbc-46a0-84b4-b7c5ff479886)
![image](https://github.com/user-attachments/assets/fbb64a27-0f2a-4a9b-844f-0347d8dab6a7)
![image](https://github.com/user-attachments/assets/09e8b337-81ef-43a8-9744-f68bd0af33d2)


let’s now add a couple more documents to our collection of movies. However, this time we’ll use the _bulk API endpoint to add them simultaneously.
```json
curl --location 'https://localhost:9200/_bulk' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json' \
--data '
{ "index": { "_index": "movie_ratings", "_id": "1" } }
{ "title" : "Inception", "genre" : "Action", "rating" : 8.8 }
{ "index" : { "_index" : "movie_ratings" } }
{ "title" : "Pulp Fiction", "genre" : "Crime", "rating" : 8.9 }
'
```
![image](https://github.com/user-attachments/assets/cf29fe3b-c4ba-4c8d-affc-880357c4429b)

The two new documents mean our index now has three documents in total. While an index with a mere three documents is manageable, OpenSearch is designed to handle much larger indices – with hundreds of thousands of documents.

Using the methods from earlier to index such large datasets is time-consuming and inefficient. So, another approach is needed here; Ingestion.

Ingestion refers to the process of gathering and indexing data from various sources, such as log files, databases, etc, into OpenSearch. However, the data in these files are usually in a format that cannot be used directly by OpenSearch through an API client, as demonstrated in the previous example. The data often needs to be parsed and formatted correctly so that it can be properly indexed. This may involve extracting fields from log messages, converting timestamps to a standard format, or other data transformation tasks. Once the data is properly formatted, it can then be indexed, which involves adding it to the OpenSearch database in a way that allows it to be searched. In some cases, additional data can be added during the ingestion process to provide more context or to make the data more useful. For example, if you’re indexing web server logs, you might add geographic information based on the IP addresses in the logs.

To see this in action, we will ingest a list of computer games into our OpenSearch cluster.

The dataset to be ingested is from a CSV file that contains the records of about a thousand computer games. You can find and download the same dataset from Kaggle – https://www.kaggle.com/datasets/iamsouravbanerjee/computer-games-dataset

![image-23-1536x1255](https://github.com/user-attachments/assets/09b1a917-a795-4990-8ac2-94e92c46b1c8)
The file is a typical CSV file where the first row is a header that contains six fields: Name, Developer, Producer, Genre, Operating System, and Date Released.
 dowload the zip which contains csv from this curl :
curl -L -o C:/Workspace/projects/opensearch/computer-games-dataset.zip  https://www.kaggle.com/api/v1/datasets/download/iamsouravbanerjee/computer-games-dataset
![image](https://github.com/user-attachments/assets/ec82a521-c4fc-4a17-b244-301652a14283)

Before we can use this data in OpenSearch, we first need to convert the CSV data to JSON format. There are various ways to do that, but for the purpose of this guide, we’ll be using a free online conversion tool which can be found at the link below:
https://www.convertcsv.com/csv-to-json.htm
![image](https://github.com/user-attachments/assets/941e4efd-06cc-412c-b11e-acec13e79509)

After converting the data from the CSV file into JSON format, we can proceed to index it into our OpenSearch cluster. Thanks to the open-source nature of OpenSearch, clients are available for a wide range of platforms and programming languages. You can find these clients at the following link: https://opensearch.org/docs/2.7/clients/index/

For simplicity, we’ll use a basic Python script that reads the data directly from our saved JSON file. A copy of the script can be found below:
The Python script above reads JSON data directly from the file which we converted from a CSV file earlier. However, there is no reason why the same Python script can’t be modified to include a function to do the CSV to JSON conversion. Below is a modified version which does just that.
![image](https://github.com/user-attachments/assets/4438a45b-7adf-450d-9b58-6c5d13a4d833)
=>
dont forget to add verify=false , to ignore ssl verification in dev/test environement, in the production environment it is better to add ssl certifacte.
![image](https://github.com/user-attachments/assets/611c9a74-9466-4ffd-b2b2-e32add7fb5db)


let's run the script:
first install the request module :
![image](https://github.com/user-attachments/assets/3c6165f0-ddb4-49da-9391-91f231e28395)

python publish_json_to_opensearch.py  to run the script

Running either script adds the data from the file into our OpenSearch cluster in a new index called games_index which was specified in the script.
the script is executed successfully:
![image](https://github.com/user-attachments/assets/5be56b14-1769-4b53-97b7-b3971aa16a5d)

Using the request from earlier to list our indices, we can see the newly created index in the OpenSearch cluster. The docs.count column indicates that the new index has a total of 1095 documents within it, ready to be searched.
=>
![image](https://github.com/user-attachments/assets/961e9ace-80d7-494a-97dd-824ff084b861)

***Searching the Index***
OpenSearch offers a flexible search language known as the query domain-specific language (DSL), which allows us to effectively search through our data using a JSON interface. This makes it ideal for querying data via the OpenSearch API.

With query DSL, you need to specify a query in the query parameter of the search. One of the simplest searches in OpenSearch uses the match_all query, which matches all documents in an index. This is useful for listing all the documents contained in our index. Let’s give that a try.
```json
curl --location --request GET 'https://localhost:9200/movie_ratings/_search' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json' \
--data '{
  "query": {
    "match_all": {}
  }
}'
```
![image](https://github.com/user-attachments/assets/89443b67-e998-4adc-bb94-2aa0673f0b8c)

=> response :
```json
{
    "took": 7,
    "timed_out": false,
    "_shards": {
        "total": 2,
        "successful": 2,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 3,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_index": "movie_ratings",
                "_id": "1",
                "_score": 1.0,
                "_source": {
                    "title": "Inception",
                    "genre": "Action",
                    "rating": 8.8
                }
            },
            {
                "_index": "movie_ratings",
                "_id": "PaOgqZUBTet7jWEcp6W_",
                "_score": 1.0,
                "_source": {
                    "title": "Pulp Fiction",
                    "genre": "Crime",
                    "rating": 8.9
                }
            },
            {
                "_index": "movie_ratings",
                "_id": "NaOHqZUBTet7jWEcj6V8",
                "_score": 1.0,
                "_source": {
                    "title": "The Shawshank Redemption",
                    "genre": "Drama",
                    "rating": 9.3
                }
            }
        ]
    }
}
```

=> we see all data of the index.

The response returned lists of all the documents found in our index. In addition to details that we created like title, genre, and rating, each document entry also includes additional attributes such as the index name (_index) and a unique document ID (_id) which is specific to that document.

To perform an actual search of the index, we can use the same search request from earlier, only this time, we modify the request’s body slightly to indicate what we’re looking for, like this:

now let s work with the other index games_index
![image](https://github.com/user-attachments/assets/0c7515ca-b00a-4148-9f66-f41ee2b46333)

In the example above, we searched for the term “rock”, which resulted in a list of matching documents referred to as “hits.” These hits represent documents within the index that contain the search term within any field. For example, the first hit has the word rock in the Name field, while the second hit has the word rock in the Producer and Developer fields.
```json
{
    "took": 23,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 5,
            "relation": "eq"
        },
        "max_score": 5.9073567,
        "hits": [
            {
                "_index": "games_index",
                "_id": "h6PBqZUBTet7jWEcgqdK",
                "_score": 5.9073567,
                "_source": {
                    "Name": "Lego Rock Raiders",
                    "Developer": "Data Design Interactive",
                    "Producer": "Lego Media",
                    "Genre": "Real-time strategy, action",
                    "Operating System": "Microsoft Windows",
                    "Date Released": "November 15, 1999"
                }
            },
            {
                "_index": "games_index",
                "_id": "4aPBqZUBTet7jWEcJqUp",
                "_score": 5.7722692,
                "_source": {
                    "Name": "Banished",
                    "Developer": "Shining Rock Software",
                    "Producer": "Shining Rock Software",
                    "Genre": "City building, strategy",
                    "Operating System": "Microsoft Windows",
                    "Date Released": "February 18, 2014"
                }
            },
            {
                "_index": "games_index",
                "_id": "T6PBqZUBTet7jWEcq6iR",
                "_score": 5.223794,
                "_source": {
                    "Name": "Rock 'n' Roll Adventures",
                    "Developer": "Data Design Interactive",
                    "Producer": "Data Design Interactive",
                    "Genre": "Platform",
                    "Operating System": "Microsoft Windows",
                    "Date Released": "September 17, 2007"
                }
            },
            {
                "_index": "games_index",
                "_id": "KqPBqZUBTet7jWEcbadb",
                "_score": 4.2420635,
                "_source": {
                    "Name": "Guitar Hero III: Legends of Rock",
                    "Developer": "Neversoft",
                    "Producer": "Aspyr Media",
                    "Genre": "Music, Rhythm",
                    "Operating System": "Microsoft Windows, Mac OS X",
                    "Date Released": "November 13, 2007"
                }
            },
            {
                "_index": "games_index",
                "_id": "XqPBqZUBTet7jWEcQKa3",
                "_score": 2.9998503,
                "_source": {
                    "Name": "Counter-Strike: Condition Zero",
                    "Developer": "Valve, Gearbox Software, Ritual Entertainment, Turtle Rock Studios",
                    "Producer": "Valve",
                    "Genre": "First-person shooter",
                    "Operating System": "Microsoft Windows, Linux, macOS",
                    "Date Released": "March 23, 2004"
                }
            }
        ]
    }
}
```
But what if we want to do a more specific search, such as limiting the hits to only the “Name” field? We can achieve that by modifying the search request to specify the fields we want to restrict the search to. Here’s an example of how that would look:
![image](https://github.com/user-attachments/assets/d859635c-c47d-421b-a083-e2b68ff3e603)
The modified request now only returns hits that contain the word rock within the “Name” field. Hits containing the term “rock” in fields other than the “Name” field are excluded from the results.

Had our goal been to search within the “Producer” field, then our request would have looked like this instead:
![image](https://github.com/user-attachments/assets/daebebfe-e880-490a-aa09-9a145e99d7b8)

It is also possible to use the bool query within the request body to restrict our search to multiple fields within the same search. This is super useful for making very specific searches. For example, if we want to find RPG games that can be played on macOS from our index, we could make a request like this to restrict our search to only documents that match both criteria.
![image](https://github.com/user-attachments/assets/99c203d0-d40a-4be1-b963-d0a21bdfaaa1)

Querying data is a significant part of OpenSearch, making it a very broad topic that, unfortunately, is beyond the scope of this guide. If you’re interested in learning more about how to effectively query data using the OpenSearch API, I highly recommend referring to the OpenSearch documentation on the topic: https://opensearch.org/docs/2.7/query-dsl/

***Delete an index***

Removing an index is quite straightforward. We simply initiate a DELETE request to the specific endpoint corresponding to the index we wish to delete.
![image](https://github.com/user-attachments/assets/15755035-b7cc-4313-a17a-77271d7c41d5)

The response confirms that the delete operation was successful.

***The OpenSearch Dashboard***
Earlier in this guide, we discussed the steps involved in creating an OpenSearch index and the process of ingesting data into it. We also provided a brief overview of querying this data using the OpenSearch API.

But you may be asking yourself: How useful is all this data in our OpenSearch cluster if it can only be accessed through an API, with results given back in JSON format?

This is where OpenSearch Dashboards come in.

OpenSearch Dashboards is a powerful tool that complements the OpenSearch API by providing a user-friendly interface for visualising and analysing the data stored in an OpenSearch cluster.

***Index patterns***

An index pattern is a way to designate the indices we want OpenSearch Dashboards to examine when running a search or query. This simplifies our work because instead of specifying the exact index or list of indices each time we want to explore data or create a visualisation, we can just specify the index pattern.

To create an index pattern, open the left-side navigation pane, and click “Stack Management”, followed by “Index patterns”. Then click the “Create index pattern” button.

http://localhost:5601/app/management/opensearch-dashboards/indexPatterns
![image](https://github.com/user-attachments/assets/0f0fb465-5984-4e9d-a9a8-2e053c4211c8)

The next step involves establishing a pattern that allows us to specify the indices we wish to include in our index pattern. One option is to use an asterisk (*) as a wildcard character, enabling us to select all available indices. However, in our case, we only want to select a single index. So, we simply enter the complete name of the index and then click “next” to finalise the creation of the index pattern.

![image](https://github.com/user-attachments/assets/d5db4587-c208-43f8-b61d-e09109369429)
![image](https://github.com/user-attachments/assets/d57c4351-f421-4a6e-a50f-68b31d0a189e)


![image](https://github.com/user-attachments/assets/f3f9d637-bf2a-4389-bee5-626ca3680c93)

The last page on the creation screen lists all the fields within the newly created index pattern. You’ll notice some entries ending in .keyword. This is the result of the default dynamic mapping settings in OpenSearch. For text fields, this generally means that two versions of the field are created within our index pattern:

<fieldname>: This is the analysed version of the field. It’s broken down into individual terms (which are roughly equivalent to words), and each of these terms can be searched independently. This is useful for full text search.

<fieldname>.keyword: This is the not-analysed version of the field. It is a single term exactly as it was provided, useful for sorting, aggregations, and exact value searches. It also allows for efficient “term” queries, which match the exact value of the field.

Let’s say we have a field named “colour” with the value “Dark Blue”. In the analysed “colour” field, this would be broken down into two terms, “Dark” and “Blue”. If you searched for just “Blue”, this document would be a match. However, in the <fieldname>.keyword field, the value is a single term, “Dark Blue”. If you searched for just “Blue” in this field, it wouldn’t be a match.

This strategy of using <fieldname> and <fieldname>.keyword allows us to perform both full-text searches and exact value operations on the same textual data.

***Interacting with the data***
With the index pattern created, we can now interact with our data in the cluster. To do this, head back to the OpenSearch Dashboards home page and click “Visualize and analyze”. Then click “Discover”.

The Discover page on OpenSearch Dashboards provides a UI to explore and interact with the data stored in your OpenSearch cluster. It offers a search and visualisation interface where you can execute queries and view the results in real-time. Give it a try by entering a search term in the search box!

![image](https://github.com/user-attachments/assets/c5b50b78-c01b-4e97-b232-d115da5d0017)

In OpenSearch Dashboards, you can perform basic searches to find data within the cluster. However, it also offers an enhanced filtering capability called Dashboards Query Language (DQL). DQL is a user-friendly, text-based query language specifically designed for filtering and retrieving data within OpenSearch Dashboards. By utilising DQL, you can easily construct more advanced queries to precisely narrow down and filter your data, enabling you to retrieve the specific information you need. More information about DQL can be found in the official documentation linked below: https://opensearch.org/docs/latest/dashboards/discover/dql/

***Dashboards and visualisations***
With our data now organised into an index pattern, we can use the index pattern to create visually appealing dashboards and visualisations that effectively convey the information within it. To do so, we simply need to access the side panel and select the “Dashboards” option. From there, click on the button to create a new dashboard.
http://localhost:5601/app/dashboards#/create?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),panels:!(),query:(language:kuery,query:''),timeRestore:!f,title:'',viewMode:edit)
![image](https://github.com/user-attachments/assets/2d02bffc-11b2-4f0d-a149-db89733a0305)
The choice of visualisation here depends on the specific information you aim to communicate. For this demo, we will opt for simplicity and use a pie chart to display the distribution of different categories within our dataset. However, I highly recommend exploring other visualisations at your own pace to discover what works best for your data and your needs.
![image](https://github.com/user-attachments/assets/d0f91591-7bba-4db5-b895-97200a837e37)

By default, and without any configuration, the pie chart displays a count of all the data inside our index. At this stage, the visualisation is not very useful.

To make the data more meaningful, we must tell OpenSearch what we want it to visualise. For example, to have the pie chart display a breakdown of the top 50 game producers from our dataset, we need to tell open search that this is what we want to see. We do this by adding a new bucket and selecting “Split slices”.

![image-46-1536x526](https://github.com/user-attachments/assets/d2a52d35-ef2e-46ba-85d2-34299a282e1e)

Next, under Aggregation, we select Terms. This instructs OpenSearch to craft our pie chart so that each distinct category (or ‘Term’) represents a segment within the pie chart. 

Since our goal is to compile a list of producers, this will be our Term, so we must select that as the corresponding field from the available options in the field dropdown box. Additionally, to ensure that the pie chart displays only the top 50 producers, we must set the size to 50.

![image](https://github.com/user-attachments/assets/483d7e0a-1337-4328-b93b-e68f56b14363)

Clicking update will result in a pie chart like the one below. We can customise it further by clicking the options tab and selecting things such as labels and the type of pie chart to display.

![image](https://github.com/user-attachments/assets/4b49a6e4-57ea-4a4e-9268-cd0b8d3add4d)

Once saved, the visualisation object is now ready to be added to a dashboard. Do this by heading to the dashboard page and clicking the text that says “Add an existing object to this dashboard”.

====================================================================================================

***EXAMPLE WITH WEBLOGIC LOG***
download first filebeat for windows:
https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html
![image](https://github.com/user-attachments/assets/d5d9af81-4658-4434-8e43-c1236445f853)

First of all we need to search for the compatible version of filebeat with opensearch:
we need a oss version to be compatible so we need to follow this doc:
https://opensearch.org/docs/latest/tools/#agents-and-ingestion-tools
run this api:
```json
curl --location --request PUT 'https://localhost:9200/_cluster/settings' \
--header 'Authorization: Basic YWRtaW46R0hBSUxFTkVtYXJrMTE5OTQqKg==' \
--header 'Content-Type: application/json' \
--data '{
  "persistent": {
    "compatibility": {
      "override_main_response_version": true
    }
  }
}'
```
the version of opensearch here is :
![image](https://github.com/user-attachments/assets/a80b408d-721b-4ce9-a863-7bce8dcf6fa5)

download the version 7.12.1 of filebeat:
from there : https://www.elastic.co/downloads/past-releases/filebeat-oss-7-12-1
install the msi version ,
go to the path:
C:\Program Files\Elastic\Beats\7.12.1\filebeat>
and run this command:
filebeat.exe -e -c C:\Workspace\projects\opensearch\filebeat.yml

this is the filebeat yml file conf: 

 ```json 
      filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - C:/Workspace/projects/opensearch/weblogic-logs.log

output.elasticsearch:
  hosts: ["https://localhost:9200"]
  username: "admin"
  password: "mypassword" 
  ssl.verification_mode: none
  index: "weblogic-logs"

setup.template.name: "weblogic-logs"
setup.template.pattern: "weblogic-logs*"
setup.ilm.enabled: false

setup.kibana:
  host: "https://localhost:5601"
  
logging.level: debug
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat.log
  keepfiles: 7
```
  
![image](https://github.com/user-attachments/assets/68e18782-0c47-4547-9359-7e47e77a56cd)

the index weblogic-log will create automatically by filebeat:
example of some log of filebeat:
```json 
2025-03-19T16:16:57.474+0100    INFO    template/load.go:109    template with name 'weblogic-logs' loaded.
2025-03-19T16:16:57.474+0100    INFO    [index-management]      idxmgmt/std.go:298      Loaded index template.
2025-03-19T16:16:57.474+0100    DEBUG   [esclientleg]   eslegclient/connection.go:364   GET https://localhost:9200/  <nil>
2025-03-19T16:16:57.477+0100    INFO    [publisher_pipeline_output]     pipeline/output.go:151  Connection to backoff(elasticsearch(https://localhost:9200)) established
2025-03-19T16:16:57.923+0100    DEBUG   [elasticsearch] elasticsearch/client.go:230     PublishEvents: 9 events have been published to elasticsearch in 445.2693ms.
2025-03-19T16:16:57.923+0100    DEBUG   [publisher]     memqueue/ackloop.go:160 ackloop: receive ack [0: 0, 9]
2025-03-19T16:16:57.923+0100    DEBUG   [publisher]     memqueue/eventloop.go:535       broker ACK events: count=9, start-seq=1, end-seq=9

2025-03-19T16:16:57.924+0100    DEBUG   [acker] beater/acker.go:59      stateful ack    {"count": 9}
2025-03-19T16:16:57.924+0100    DEBUG   [publisher]     memqueue/ackloop.go:128 ackloop: return ack to broker loop:9
2025-03-19T16:16:57.924+0100    DEBUG   [registrar]     registrar/registrar.go:264      Processing 9 events
2025-03-19T16:16:57.924+0100    DEBUG   [registrar]     registrar/registrar.go:231      Registrar state updates processed. Count: 9
2025-03-19T16:16:57.924+0100    DEBUG   [publisher]     memqueue/ackloop.go:131 ackloop:  done send ack
2025-03-19T16:16:57.924+0100    DEBUG   [registrar]     registrar/registrar.go:201      Registry file updated. 1 active states.
2025-03-19T16:16:59.022+0100    DEBUG   [harvester]     log/log.go:107  End of file reached: C:\Workspace\projects\opensearch\weblogic-logs.log; Backoff now.
2025-03-19T16:17:03.029+0100    DEBUG   [harvester]     log/log.go:107  End of file reached: C:\Workspace\projects\opensearch\weblogic-logs.log; Backoff now.
```

herre we can see that a new index is created :
![image](https://github.com/user-attachments/assets/384cb3d2-6966-43a9-9b29-66da76a71867)

lets create a new index to see the log in the dashboard:
![image](https://github.com/user-attachments/assets/d5785acf-0c55-4e9d-a30c-97cbcb387596)

![image](https://github.com/user-attachments/assets/24776c48-df43-4a6b-aa31-61309681d1fe)

let s check the log in the opensearch dabshboard index pattern:
![image](https://github.com/user-attachments/assets/dcbf36a5-c49c-4201-bf39-9cd4794db3d9)
we can add filter message , to filter by messages:

===========================
let s suppose that we have multiple weblogic log files:
![image](https://github.com/user-attachments/assets/1068356a-d5af-4d66-b408-bf6f48fc695c)
with this format weblogic-logs-{yyyy.mm.dd}
we want to create for each file an index, the new yaml file will be like that :

```json
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - C:\\Workspace\\projects\\opensearch\\weblogic-logs-*.log
    fields_under_root: true

processors:
  - dissect:
      field: "log.file.path"  # Use the correct field name for the file path
      tokenizer: "C:\\Workspace\\projects\\opensearch\\weblogic-logs-%{log_date}.log"
      target_prefix: "dissect"
  - rename:
      fields:
        - from: "dissect.log_date"
          to: "logfile"

output.elasticsearch:
  hosts: ["https://localhost:9200"]
  username: "admin"
  password: "mypassword"
  ssl.verification_mode: none
  index: "weblogic-logs-%{[logfile]}"  # Use the extracted `logfile` value

setup.template.name: "weblogic-logs"
setup.template.pattern: "weblogic-logs-*"
setup.ilm.enabled: false

setup.kibana:
  host: "https://localhost:5601"

logging.level: debug
logging.to_files: true
logging.files:
  path: C:/Workspace/projects/opensearch/log/filebeat
  name: filebeat.log
  keepfiles: 7
```

![image](https://github.com/user-attachments/assets/b35b8437-a832-4fc7-86fc-5efba6debe3b)


NOTE : IN CASE IF WE WANT TO CREATE AND INDEX WILL CURRENT DATE we can use something like index : weblogic-logs-%{+yyyy.MM,dd}  => this will create an index we today date with the format mentionned.

the 3 index are added :
![image](https://github.com/user-attachments/assets/24711f01-957b-4ab0-8900-c05c86d36392)

let s create a new index pattern to use it in dashboard:
![image](https://github.com/user-attachments/assets/1fd19be5-362a-41b5-b4b7-27f8db2de634)

![image](https://github.com/user-attachments/assets/9b7cb76b-0fd1-40e7-aacd-dbe283f6f694)

the new index pattern name  weblogic-logs-*
![image](https://github.com/user-attachments/assets/e368ab6b-0f2f-439f-bc91-176a757b3aa9)


in the index pattern filter we can add as filter the logfile and message :
![image](https://github.com/user-attachments/assets/78d086e1-3708-43fd-8016-db1490005838)
=> we can see all the message of log of all files.

