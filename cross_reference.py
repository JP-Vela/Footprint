import json

data = dict()

#Open json file and turn into dictionary
with open("cross_output\\output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

keys_to_delete = []

# Loop through urls in json file and delete empty ones
for url in data.keys():
    if data[url]["bio"] == "" and data[url]["name"] == "" and data[url]["name guess"] == "":
        keys_to_delete.append(url)

for key in keys_to_delete:
    del data[key]


# Save cleaned file
with open("cross_output\\output.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(data, indent=4))



# Calculate similarity scores