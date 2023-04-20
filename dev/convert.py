import json

raw = open('words.txt')
json = json.dumps(dict([j.strip() for j in i.split("=")] for i in raw.read().split('\n')), ensure_ascii=False, indent=2)

with open("words.json", "w") as outfile:
    outfile.write(json)