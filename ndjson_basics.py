import json
import time
from sys import getsizeof

import ndjson
import psycopg2
import requests
from flask import Flask, stream_with_context
from flask_cors import CORS, cross_origin

"""
The main difference of JSON and NDJSON (New Line Delimited JSON) is the
geometry of the data:
    - JSON (objects separated by comma):
        [{"k1": "v1", "k2": "v2"}, {"k1": "v1", "k2": "v2"}, ...]
    - NDJSON (objects separated by new line):
        {"k1": "v1", "k2": "v2"}
        {"k1": "v1", "k2": "v2"}
        ...
"""


json_file = "/Users/jorgeleyjunior/Downloads/4dd8-873d-6013ec8976c3.json"
ndjson_file = "/Users/jorgeleyjunior/Downloads/4dd8-873d-6013ec8976c3.ndjson"

with open(json_file) as f:
    t0 = time.time()
    json_data = json.load(f)
    elapsed = time.time() - t0
    print(f"json read {getsizeof(json_data)}bytes in {elapsed:.2f}s")

with open(ndjson_file) as f:
    t0 = time.time()
    ndjson_data = ndjson.load(f)
    elapsed = time.time() - t0
    print(f"\nndjson read {getsizeof(ndjson_data)}bytes in {elapsed:.2f}s")

# here's the main difference, we can stream ndjson and save memory, since it's
# a line delimited file
with open(ndjson_file) as f:
    t0 = time.time()
    reader = ndjson.reader(f)
    names = set()
    for line in reader:
        names.add(line.get("name"))
        # print(f'\nndjson streamed {getsizeof(line)}bytes in {elapsed:.2f}s')
    elapsed = time.time() - t0
    print(f"processed {names.__len__()} objects in {elapsed:.2f}s")

# and we could also have a streamed JSON response
t0 = time.time()
response = requests.get(
    "https://gist.githubusercontent.com/rfmcnally/0a5a16e09374da7dd478ffbe6b"
    "a52503/raw/095e75121f31a8b7dc88aa89dbd637a944ce264a/ndjson-sample.json",
    stream=True,
)
for json_object in response.iter_lines():
    print(json_object)
# ndjson_data = response.json(cls=ndjson.Decoder)
elapsed = time.time() - t0
print(f"\nndjson response {getsizeof(ndjson_data)}bytes in {elapsed:.2f}s")

# we can also stream our data via API
app = Flask(__name__)


@app.route("/stream-ndjson-file")
@cross_origin()
def stream_ndjson_file():
    @stream_with_context
    def ndjson_line_generator():
        with open(ndjson_file) as f:
            reader = ndjson.reader(f)
            for line in reader:
                time.sleep(1)  # just to see the streaming slowly
                # (remove it in a real app of course)
                yield json.dumps(line)

    return ndjson_line_generator()


# run the api with the command:
#   flask --app ndjson_basics run
# then you can access the streamed data it in the URL:
#   localhost:5000/stream-ndjson-file


conn = psycopg2.connect(
    "host=localhost port=5002 dbname=xchango user=postgres password=25012023"
)


def create_table():
    with conn.cursor() as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS users ("
                "uuid VARCHAR,"
                "first_name VARCHAR,"
                "last_name VARCHAR,"
                "email VARCHAR,"
                "password VARCHAR"
            ") "
        )
        print("table created")
        conn.commit()

def generate_random_data():
    conn.autocommit = False
    import hashlib

    with conn.cursor() as c:
        for i in range(10_000):
            md5 = hashlib.md5(f"{i}".encode()).hexdigest()
            c.execute(
                "INSERT INTO users (uuid, first_name, last_name, email, "
                "password) "
                f"VALUES('{md5}', 'f{i}', 'l{1}', 'e{1}@test.com', 'pass{i}')"
            )
            print('.', end='', flush=True)
        print("data inserted")
    conn.commit()

# create_table()  # comment this after running 1st time to avoid the overload
# generate_random_data()  # comment this after running 1st time to avoid the
                          # overload
@app.route("/stream-ndjson-db")
@cross_origin()
def stream_ndjson_db():
    @stream_with_context
    def ndjson_record_generator():
        with conn.cursor() as cursor:
            """
            itersize: should be a value to balance the network calls X memory.
            i.e.: if we have 100 rows, itersize=2 results in 50 network calls.
            """
            cursor.itersize = 1
            cursor.execute('SELECT * FROM "users" LIMIT 10000')
            for uuid, first_name, last_name, email, password in cursor:
                time.sleep(0.5)
                yield json.dumps(
                    {
                        "uuid": uuid,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": password,
                    }
                ) + "\n"
    return ndjson_record_generator()


"""
Mysql:
    stmt = conn.createStatement(java.sql.ResultSet.TYPE_FORWARD_ONLY,
                  java.sql.ResultSet.CONCUR_READ_ONLY);
    stmt.setFetchSize(Integer.MIN_VALUE);
"""
