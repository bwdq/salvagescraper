import json
y = 0
print('INSERT INTO make VALUES')
f = open("sample-search-response.txt", "r")
response = f.read()
f.close()
js = json.loads(response)
data = js['data']
results = data['results']
facetFields = results['facetFields']
for i in facetFields:
    if i['quickPickCode'] == 'MAKE':
        facetCounts = i['facetCounts']
        for facet in facetCounts:
            query = facet['query']
            field = query.split(":")
            loc = field[1]
            parsed = loc.replace("\"", "")
            #final = "( DEFAULT, '" + parsed + "'),"
            final = "(" + str(y) + ", '" + parsed + "'),"
            y = y + 1
            print(final)
