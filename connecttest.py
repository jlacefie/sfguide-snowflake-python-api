import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Replace these variables with your Snowflake credentials and file path to your private key
USER = 'jlacefie999'
ACCOUNT = 'gob73116.us-east-1'
# PASSWORD = 'SnowFlake1!'
# PRIVATE_KEY_PATH = '/Users/jonathanlacefield/Desktop/Personal/sfl/snowflake_demo_key'
PRIVATE_KEY = b'''-----BEGIN PRIVATE KEY-----
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
NnmHzBC5gxpv/OvoRLhVy/DjcIY4
-----END PRIVATE KEY-----
'''

'''
# Load the private key
with open(PRIVATE_KEY_PATH, "rb") as key_file:
    p_key= serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
'''


print(f"private key {PRIVATE_KEY}")

p_key= serialization.load_pem_private_key(
    PRIVATE_KEY,
    password=None,
    backend=default_backend()
    )
 
print(f"p_key {p_key}")

# Convert the private key to the format expected by Snowflake
pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

print(f"pkb {pkb}")

print('starting to connect to snowflake')

conn = snowflake.connector.connect(
        user=USER,
        account=ACCOUNT,
        private_key=pkb
    )

'''
try:
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT
    )
    print("Successfully connected to Snowflake!")
    # Optionally, execute a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_TIMESTAMP")
    one_row = cursor.fetchone()
    print(f"Current Timestamp: {one_row[0]}")
finally:
    cursor.close()
    conn.close()
'''

print('connected to snowflake')