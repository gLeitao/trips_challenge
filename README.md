# Trips Challenge Project

This is the Trips Challenge project, a solution to a coding challenge provided by Jobsity.



## Prerequisites

In order to run this project, you will need to have the following installed and configured on your machine:


### Terraform
Terraform is an infrastructure as code tool used to create the AWS architecture. To install it, please follow the instructions from the official website:
 - https://www.terraform.io/downloads.html

### AWS CLI

The AWS CLI is a command-line tool that allows you to interact with AWS services. To install it, please follow the instructions from the official website:
insta
### Environment Variables

You will need to set your  `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as environment variables. If you don't have them, you can create them by following the instructions from the AWS documentation:
- https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys

### Python

You will need Python 3.7 or higher installed on your machine. You can download it from the official website:
- https://www.python.org/downloads/

### Python Libraries

You will also need to install the following Python libraries:

```
pip install \
    boto3==1.26.81 \
    botocore==1.29.81 \
    jmespath==1.0.1 \
    python-dateutil==2.8.2 \
    s3transfer==0.6.0 \
    six==1.16.0 \
    urllib3==1.26.14
```

## Running the AWS Infrastructure

To run the AWS infrastructure, go to the infra folder and run the following commands:

`This step is only necessary if you want to set up the entire infrastructure. Otherwise, you can skip to the item  **Running ETL.** ` 

```terraform
terraform init
terraform apply
```
This will create an the required infra to run this project.

## Running the ETL
To run the ETL process, go to the scripts/upload folder and execute the following command:
```
python upload_local_file_s3.py --path /path/file.csv
```
`Remeber to replace /path/file.csv with the path to your CSV file.` 

This process will upload the CSV to S3 and invoke the Step Function, the workflow orchestrator responsible for triggering the ETLs that process the data.

![plot](img/stepfunction.png)

## ETL Step by Step

### Modeling Strategy

The data modeling approach for this project is based on the fact and dimension model, with a focus on the star schema design. This approach was chosen to maximize performance when querying data and building dashboards in the future.

In the star schema, one central fact table is connected to a set of dimension tables, each of which contains descriptive information about the data in the fact table. This approach simplifies complex queries and enables faster data retrieval.

By implementing this modeling strategy, was aimed to ensure that the data is structured in a way that facilitates efficient querying and analysis, and enables us to gain valuable insights from the data.


### Move Raw

The Move Raw process reads the CSV file that has been ingested into the data lake and is stored in the landing layer. It then infers the schema of the attributes in the file and converts the data to the Parquet format. Finally, it saves the transformed data in the raw layer of the data lake.

By converting the data to Parquet format, we can take advantage of its columnar storage format, which provides significant performance improvements over traditional row-based formats like CSV. Additionally, by storing the transformed data in the raw layer, we preserve the original data as it was received, enabling us to easily reprocess it if needed

### Dimregions Job

The Dimregions Job is responsible for creating and maintaining a Delta table called dimregions, which stores the distinct regions that the data may present. 

The job reads the Parquet data from the raw layer of the data lake and applies an incremental update process to the dimregions table. If a new region is identified in the data, it is inserted into the table, while existing records are discarded.

By creating a Delta table for the distinct regions in the data, we can easily and efficiently query and analyze the data. Additionally, by using an incremental update process, we can keep the dimregions table up to date with any new regions that may be added to the data in the future.

#### Schema
| Column Name | Description |
| ------ | ------ |
| cdregion | Unique code for each region record|
| region | Descriptive name of the region |

### DimDataSource Job

Similar to the DimRegions job, this job reads records from the raw layer and stores them in a Delta table called DimDataSource. This table is responsible for storing the distinct data sources that the data can present, meaning it is an incremental update process where, when there is a new data source, an insert is made, and when it is an existing one, the record is discarded. The job ensures that there is only one record for each data source in the table.

#### Schema
| Column Name | Description |
| ------ | ------ |
| cddatasource | Unique code for each datasource record|
| datasource | Descriptive name of the datasource |

### Facttrips Job

This process reads data from the raw layer and inserts it into the delta table "facttrips", which stores consolidated information about trips, grouped by region, data source, and datetime (considering only the hour of the day). Thus, it generates a quantity of trips performed at the same hour of the day, with the same data source, for the same region.

Although fact tables are not commonly incremental updates but rather appends, in this specific scenario, I chose to develop it as an incremental update since it will have loads during the day. This way, it is easier to ensure the integrity and performance of the load. However, it is essential to note that there is a caveat in this approach. The structure assumes that the CSV file submitted for the load does not contain duplicate information and that it is not submitted more than once. If this occurs, it will duplicate data in the fact table. Since there was no information on how the data would be obtained, I chose not to handle it in the fact table. In this scenario, it would be more appropriate to treat this information when obtaining it.

#### Schema
| Column Name | Description |
| ------ | ------ |
| cddatasource | Unique code for each datasource record|
| datasource | Descriptive name of the datasource |
| datetime | Date of the trip (considering only the hour of the day) |
| count_trips | Number of the trips made at the same hour of the day, with the same data source, for the same region |

It is worth noting that the final view of the fact table does not include the coordinates fields, as they do not add any value to the final result, and can even impair performance when extracting data. However, if the data science team or any other team needs to use this information, they can access it in the raw layer.
## Authors
- Geovani Leitão - gLeitao

## License

This project is licensed under the MIT License - see the LICENSE file for details.