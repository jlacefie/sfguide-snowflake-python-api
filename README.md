
# A Simple API Powered by Snowflake
Forked from https://quickstarts.snowflake.com/guide/build_a_custom_api_in_python_on_aws/index.html?index=..%2F..index#0

Technologies used: [Snowflake](https://snowflake.com/), [Python](https://www.python.org/), [Flask](https://palletsprojects.com/p/flask/), [AWS API Gateway](https://aws.amazon.com/api-gateway/), [AWS Lambda](https://aws.amazon.com/lambda/), [Serverless Framework](https://www.serverless.com/)

Requirements: 
* Snowflake.com and Serverless.com account
* node.js, python 3, virtualenv installed
* Citibike data loaded into Snowflake
* Snowflake user authorized to access citibike data with key pair authentication

This project demonstrates how to build and deploy a custom API powered by Snowflake. It uses a simple Python Flask API service running on AWS Lambda using Serverless Framework. Connectivity to Snowflake is made via key pair authentication.

## Configuration

Copy the serverless-template.yml to serverless.yml and modify the parameters according to your Snowflake configuration. Put your private key
to your Snowflake user in AWS SSM is us-west-2 region under the parameter <ACCOUNT>.DATA_APPS_DEMO.

Your SnowFlake Account is of the format <Locator>.<Region> where Locator is found on your SnowFlake proile (bottom right of the web console) and Region is the region where your Snowflake Wharehouse is running

Use the guided exercise found here to setup this project https://quickstarts.snowflake.com/guide/build_a_custom_api_in_python_on_aws


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

## Demo Sample Queries

### customer lookup by customer phone
curl "http://localhost:5000/customer/details_by_phone?phone=23-145-909-1370" | jq '.result.rows[] | {NAME: .NAME, ACCOUNT_BALANCE: .ACCOUNT_BALANCE, NATION: .NATION}'

### order lookup by customer phone
curl "http://localhost:5000/order/orders_by_cust_phone?phone=23-145-909-1370" | jq  '.result.rows[] | {ORDER: .OKEY, ORDERSTATUS: .ORDERSTATUS, TOTAL: .TOTALPRICE}'

### order details by order key
curl "http://localhost:5000/order/details_by_orderkey?okey=5953734" | jq '.result.rows[] | {ORDER: .OKEY, LINENUMBER: .LINENUMBER, PARTNAME: .PARTNAME, QUANTITY: .QUANTITY}'