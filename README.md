**Globant's Data Engineering Coding Challenge**
-----------------------------------------------------------
**Local Rest API + Database + Cloud Infrastracture**
-----------------------------------------------------------
Creation of a local REST API that can:
1. Receive historical data from CSV files
2. Upload these files to the new DB
3. Be able to insert batch transactions (1 up to 1000 rows) with one request

**Section: SQL**
------------------------------------------------------------------------
Based on the data provied for the databases, The stakeholders ask for some specific metrics they need. 

Create the following queries with the following information:

**First Query:** FirstNumber of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.

**Second Query:** List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).

**Section: Cloud, Testing & Containers**
-----------------------------------------------------------------
1. Host Arquitecture in any public cloud
2. Add Automated test to the API
3. Containerize your application


**CSV files structures**
-------------------------------------------------------------------------
hired_emplotees.csv schema
| id           | name                   | datetime               | department_id   | job_id       |
| -------------| ---------------------- | ---------------------- | --------------- | ------------ |
| INTEGER      | STRING                 | STRING (ISO format)    | INTEGER         | INTEGER      |

Example hired_emplotees.csv
| id  | name               | datetime              | department_id | job_id |
| --- | ------------------ | --------------------- | ------------- | ------ |
| 1   | John Doe           | 2021-01-01T00:00:00Z  | 1             | 1      |
| 2   | Jane Smith         | 2021-02-15T09:30:00Z  | 2             | 3      |
| 3   | Michael Johnson    | 2021-03-27T16:45:00Z  | 3             | 2      |


departments.csv schema
| id           | department   |
| -------------| ------------ |
| INTEGER      | STRING       |

example departments.csv
| id  | department     |
| --- | -------------- |
| 1   | Supply Chain   |
| 2   | Maintenance    |
| 3   | Staff          |

jobs.csv schema
| id           | job          |
| -------------| -------------|
| INTEGER      | STRING       |

example jobs.csv 
| id  | job           |
| --- | ------------- |
| 1   | Recruiter     |
| 2   | Manager       |
| 3   | Analyst       |

How to reproduce the infrastructure?
---------------------------------------------------------------------------
Start by pulling the repository
Then, create a virtual environment using python 3.8 and install the requirements following the next steps (you need to have installed Python 3.8):

You need to have installed sqlite3 3.41.2 latest stable
```
sudo apt install sqlite3
```
(Optional)
For ease visualization tool you can install SQLite Browser
```
sudo apt install sqlitebrowser
```
Since this project has used GCP as public cloud provider, install Cloud SDK into your local machine. You can log into your GCP project from Cloud SDK
```
curl https://sdk.cloud.google.com | bash
```

After all the packages necesarry installed, go to the root repository

How to insert raw data to my database from CSV files?
-----------------------------------------------------------
**Before adding raw data into your database, be aware of running at least one time your main.py file, since it has classes to create your database schema using SQLAlchemy Library, otherwise it wont work**

To import data from CSV files into your pre-defined tables in SQLite using DB Browser for SQLite, you can follow these steps:

Open DB Browser for SQLite and open your database file.

Click on the "Execute SQL" tab to execute SQL queries.

Create temporary tables to match your pre-defined table structure. For example, you can create temporary tables for hired_employees, departments, and jobs as follows:


```
CREATE TABLE temp_hired_employees (
  id INTEGER,
  name TEXT,
  hire_datetime TEXT,
  department_id INTEGER,
  job_id INTEGER
);

CREATE TABLE temp_departments (
  id INTEGER,
  department TEXT
);

CREATE TABLE temp_jobs (
  id INTEGER,
  job TEXT
);
```

Import the CSV data into the temporary tables using the "Import" feature in DB Browser for SQLite:

Go to the "File" menu and select "Import" > "Table from CSV file."
Choose the CSV file containing the data for each table and select the corresponding temporary table.
Map the CSV columns to the table columns appropriately.
Click "OK" to import the data into the temporary tables.

You can create raw data here --> https://extendsclass.com/csv-generator.html

Insert the data from the temporary tables into your pre-defined tables:

Execute the following SQL queries:

```
INSERT INTO hired_employees (id, name, hire_datetime, department_id, job_id)
SELECT id, name, hire_datetime, department_id, job_id
FROM temp_hired_employees;

INSERT INTO departments (id, department)
SELECT id, department
FROM temp_departments;

INSERT INTO jobs (id, job)
SELECT id, job
FROM temp_jobs;
```
Finally drop the temp tables created
```
DROP TABLE temp_hired_employees;
DROP TABLE temp_departments;
DROP TABLE temp_jobs;

```

How to run the infrastructure?
-------------------------------------------------
Option 1:
--------------------------
After creating the virtual environment, install the requerirements
```
pip3 install -r requirements.txt
```
Then run:
```
python main.py
```
Option 2:
----------------------------------
Build and run the docker container:
```
docker build . -t my-flask-app 
```
```
docker run -p 5000:5000 my-flask-app
```

How to deploy and how is deployed?
--------------------------------------
Currenlty the model is deploted in a cluster DockerHub cluster.

There are currenlty 3 endpoints

* "/" Its the home of the website, where the user is going to be capable of upload data or select the specific query
* "/upload" A new interface when the user can upload data, if the data is not matched with the schema it will be notified
* "/query" It is the result of the query selected (either query1 or query2) Data must be present in the database otherwise it will be empty

Next Steps
-----------------------------------
To have the database running in GCP you must do the following:
1. You should dump the sqlite database, since theres no sqlite cloud instance in GCP. After dumping your database you cloud create a Cloud SQL instance and insert the dumping file to your SQL instance created.

2. Upload your docker image into Google Container Registry
Change <PROJECT-ID> with the problem that you have created in GCP
´´´
docker tag my-flask-app gcr.io/<PROJECT-ID>/my-flask-app
´´´
3. Deplot the flask application into  Google App Engine using Google Cloud SDK (gcloud)
In the root directory of your Flask application, create an app.yaml file with the following content:
```
runtime: python3.8
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  # Add any necessary environment variables for your Flask application
  FLASK_APP: "main
  DB_CONNECTION: "sqlite:///unix_socket/<path_to_instance>/<database_name>.db?charset=utf8"
```

And last run this command:
```
gcloud app deploy
```

Well done!, You have a full API Rest aplication + database running on GCP with AppEngine :D!
