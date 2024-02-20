import json
 
f = open('specs.json')
data = json.load(f)

files = []
for i in data['specs'][0]['markdown_paths']:
    files.append(i)
 
with open('out.md', 'w') as out:
    for f in files:
        with open(f"spec/{f}") as i:
            for l in i:
                out.write(l)

        out.write("\n\n")

out.close()