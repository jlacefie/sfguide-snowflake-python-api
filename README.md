
# A Simple API Powered by Snowflake
Forked from https://quickstarts.snowflake.com/guide/build_a_custom_api_in_python_on_aws/index.html?index=..%2F..index#0

Technologies used: [Snowflake](https://snowflake.com/), [Python](https://www.python.org/), [Flask](https://palletsprojects.com/p/flask/), [AWS API Gateway](https://aws.amazon.com/api-gateway/), [AWS Lambda](https://aws.amazon.com/lambda/), [Serverless Framework](https://www.serverless.com/)

Requirements: 
* Snowflake.com and Serverless.com account
* node.js, python 3, virtualenv installed
* Citibike data loaded into Snowflake
* Snowflake user authorized to access citibike data with key pair authentication

This project demonstrates how to build and deploy a custom API powered by Snowflake. It uses a simple Python Flask API service running on AWS Lambda using Serverless Framework. Connectivity to Snowflake is made via key pair authentication.

## API Documentation
API documentation with samples is hosted by Postman [here](https://documenter.getpostman.com/view/36644187/2sA3duGtDu)

## API Sample UI
A Sample UI is provided alongside the forked API example.  The UI is built using Streamlit and can be run locally. 

To use:
1. Download Streamlit 
2. Create a python virtual environment
3. To run the app, use the command `streamlit run streamlit-app.py`.
4. Assuming defaults, access the app at this URL - http://localhost:8501/

## Configuration

Copy the serverless-template.yml to serverless.yml and modify the parameters according to your Snowflake configuration. Put your private key
to your Snowflake user in AWS SSM is us-west-2 region under the parameter <ACCOUNT>.DATA_APPS_DEMO.

Your SnowFlake Account is of the format <Locator>.<Region> where Locator is found on your SnowFlake proile (bottom right of the web console) and Region is the region where your Snowflake Wharehouse is running

Use the guided exercise found here to setup this project https://quickstarts.snowflake.com/guide/build_a_custom_api_in_python_on_aws

This demo uses the SnowFlake sample data tpch tables.  Be sure to create views to expose the shared tables to the user/db/schema created during setup above. Simple CREATE VIEW statements suffice. 

Install serverless and other required node packages and configure serverless (sls) for the project.

```bash
npm install
sls login
```

Create a virtualenv locally and install python packages.

```bash
virtualenv venv --python=python3
source ./venv/bin/activate
pip install -r requirements.txt
```

## Local Development

For local development you will want to use the venv previously created. This will run a local application server and connect to your Snowflake account for data access.

Start the local serverless server.

```bash
sls wsgi serve
```

### Invocation

After successful startup, you can call the created application via HTTP:

```bash
curl http://localhost:5000/
```

Which should result in the following response:

```json
{"result":"Nothing to see here", "time_ms": 0}
```

## Deployment

Build and deploy the application to AWS. For your first time, you will have to run sls without deploy to configure the project.

```bash
sls deploy
```

Also, Serverless requires a LOT of permissions in AWS. This part was challenging if you're trying to achieve Principles of Least Privellege.

I ended up creation a very permissive policy :( 
    
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:*",
                "iam:*",
                "lambda:*",
                "s3:*",
                "logs:*",
                "apigateway:*",
                "dynamodb:*",
                "events:*"
            ],
            "Resource": "*"
        }
    ]
}


### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://xxxxxxx.execute-api.us-west-2.amazonaws.com/dev/
```

Which should result in the following response:

```json
{"result":"Nothing to see here", "time_ms": 0}
```

## Scaling

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 1000. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).


## JSON Parsing
The demo provides 2 types of connection methods for querying Snowflake
1 - Snowflake's Python Connector - connector.py
2 - Snowflakes REST based connector - sqlapi.py

The connector.py example provides formatted jsonn with header values to afford you the opportunity to parse and filter results using jquery. 

The sqlapi.py example returns raw, non header json. 