import json
import pickle

from flask import Flask

# basics
obj = [
    {"x": 1},
    {"y": 2},
    {"z": 3},
]

# Byte serialization
byte_serialized = pickle.dumps(obj)
print(f"byte serialized: {byte_serialized}")

# Byte deserialization
byte_deserialized = pickle.loads(byte_serialized)
print(f"byte deserialized: {byte_deserialized}")

# JSON serialization
json_serialized = json.dumps(obj)
print(f"json serialized: {json_serialized}")

# JSON deserialization
json_deserialized = json.loads(json_serialized)
print(f"json deserialized: {json_deserialized}")

# api
app = Flask(__name__)


@app.route("/")
def root_endpoint():
    return json.dumps(obj)


# be careful when you use a custom encoder!
class ComplexEncoder(json.JSONEncoder):
    # https://docs.python.org/3/library/json.html

    count_instances = 0

    def __new__(cls, *args, **kwargs):
        print("instantiating ComplexEncoder")  # you'll see it multiple times
        ComplexEncoder.count_instances += 1
        return super().__new__(ComplexEncoder)

    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return json.JSONEncoder.default(self, obj)


# nothing bad happens, since we're dumping one single object, but...
serialized2 = json.dumps(2 + 1j, cls=ComplexEncoder)
print(serialized2)
print(f"{ComplexEncoder.count_instances} instance of ComplexEncoder")

# if you call it multiple times, you'll end up with multiple instances of your
# custom encoder!
array = [2 + 1j for i in range(10)]
for o in array:
    serialized3 = json.dumps(o, cls=ComplexEncoder)
    print(serialized3)
print(f"{ComplexEncoder.count_instances} instances of ComplexEncoder")

# this is a better way:
complex_encoder = ComplexEncoder()
for o in array:
    serialized4 = complex_encoder.default(o)
    print(serialized4)
print(f"{ComplexEncoder.count_instances} instances of ComplexEncoder")
