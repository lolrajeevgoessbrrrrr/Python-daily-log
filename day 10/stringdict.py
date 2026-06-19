import json

# Python dict → JSON string
data = {"name": "Rajeev", "age": 19}
json_string = json.dumps(data)
print(json_string)
print(type(json_string))  # it's a string now, not a dict!

# JSON string → Python dict
back_to_dict = json.loads(json_string)
print(back_to_dict["name"])