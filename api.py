import bobo

"""
very stupidly simple api

run from command line: bobo -f api.py
"""


@bobo.query('/')
def hello():
    # http://localhost:8080/
    return "hello world"


@bobo.post("/data")
def post_data(data):
    # curl -i -X POST -d "data=xxx" http://localhost:8080/data
    return f"{len(data)} - {data} - {type(data)}"
