import config
import snowflake.connector
from flask import Blueprint, request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from utils import api_response, phone_params_valid, okey_params_valid


def connect():
    p_key = serialization.load_pem_private_key(
            config.SNOWFLAKE_PRIVATE_KEY.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    snowflake.connector.paramstyle='qmark'
    conn = snowflake.connector.connect(
        user=config.SNOWFLAKE_USER,
        account=config.SNOWFLAKE_ACCOUNT,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
        schema=config.SNOWFLAKE_SCHEMA,
        database=config.SNOWFLAKE_DATABASE,
        private_key=pkb,
        session_parameters={
            'QUERY_TAG': 'Snowflake-Python-Connector',
        })
   
    return conn


conn = connect()
connector = Blueprint('connector', __name__)


def exec_and_fetch(sql, params = None):
    cur = conn.cursor().execute(sql, params)
    return cur.fetchall()

def exec_and_fetch(sql, params = None):
    cur = conn.cursor().execute(sql, params)
    return cur.fetchall()

def execute_query_and_return_json(sql):
    cursor = conn.cursor()

    cursor.execute(sql)
        
    # Fetch column headers from cursor.description
    columns = [col[0] for col in cursor.description]
    
    # Fetch all rows from cursor
    rows = cursor.fetchall()
    
    # Construct a list of dictionaries, each representing a row
    results = [dict(zip(columns, row)) for row in rows]
    
    # Construct the final JSON structure
    json_result = {
        "columnNames": columns,
        "rows": results
    }
    
    return json_result

@connector.route("/customer/details_by_phone")
@api_response
def get_customers_by_phone():
    phone = request.args.get('phone')
    if phone and phone_params_valid(phone):
        sql = f"SELECT C.C_NAME AS Name,C.C_ACCTBAL AS Account_Balance,C.C_ADDRESS AS Address,N.N_NAME AS Nation,R.R_NAME AS Region,C_PHONE AS Phone,C_MKTSEGMENT AS Market_Segment FROM CUSTOMER C INNER JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY INNER JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY WHERE C.C_PHONE = '{phone}' ORDER BY C.C_NAME;"
        return execute_query_and_return_json(sql)
    sql = "SELECT COUNT(*) AS CNT FROM CUSTOMER ;"
    #return exec_and_fetch(sql)
    return execute_query_and_return_json(sql)

@connector.route("/order/orders_by_cust_phone")
@api_response
def get_orders_by_cust_phone():
    phone = request.args.get('phone')
    if phone and phone_params_valid(phone):
        sql = f"SELECT O.O_ORDERKEY AS OKey, O.O_CUSTKEY AS CKey, O.O_ORDERSTATUS AS OrderStatus, O.O_TOTALPRICE AS TotalPrice, O.O_CLERK AS Clerk FROM ORDERS O INNER JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY WHERE C.C_PHONE = '{phone}' ORDER BY O_ORDERDATE"
        return execute_query_and_return_json(sql)
    sql = "SELECT COUNT(*) AS CNT FROM ORDERS ;"
    return execute_query_and_return_json(sql)

@connector.route("/order/details_by_orderkey")
@api_response
def get_orders_details_by_okey():
    okey = request.args.get('okey')
    if okey and okey_params_valid(okey):
        sql = f"SELECT O.O_ORDERKEY AS OKey, O.O_CUSTKEY AS CKey, O.O_ORDERSTATUS AS OrderStatus, O.O_TOTALPRICE AS TotalPrive, O.O_CLERK AS Clerk, L.L_LINENUMBER AS LineNumber, L.L_LINESTATUS AS LineStatus, L.L_QUANTITY AS Quantity, L.L_EXTENDEDPRICE AS EPrice, L.L_TAX AS Tax, L.L_SHIPDATE AS ShipDate, L.L_SHIPINSTRUCT AS ShipInstr, L.L_SHIPMODE AS ShipMode, L.L_RETURNFLAG AS ReturnFlag, P.P_NAME AS PartName, P.P_BRAND AS Brand, P.P_MFGR AS Mfgr, P.P_SIZE AS Size, P.P_TYPE AS Type FROM ORDERS O INNER JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY INNER JOIN LINEITEM L ON O.O_ORDERKEY = L.L_ORDERKEY INNER JOIN PART P ON L.L_PARTKEY = P.P_PARTKEY WHERE O.O_ORDERKEY = '{okey}' ORDER BY O.O_ORDERDATE, L.L_LINENUMBER"
        return execute_query_and_return_json(sql)
    sql = "SELECT COUNT(*) FROM ORDERS ;"
    return execute_query_and_return_json(sql)