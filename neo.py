import json

from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "password"))
session = driver.session()

# session.run("CREATE (a:Person {name:'Arthur', title:'King'})")
#
# result = session.run("MATCH (a:Person) WHERE a.name = 'Arthur' RETURN a.name AS name, a.title AS title")
# for record in result:
#     print("%s %s" % (record["title"], record["name"]))

session.run("MATCH (n) DETACH DELETE n")

with open('jira.json') as f:
    l = json.load(f)
    for i in l:
        fields = i['fields']
        node = {
            'key': i['key'],
            'summary': fields['summary'],
            'status': fields['status']['name'],
            'reporter': fields['reporter']['key']
        }

        session.run("CREATE (%s:Ticket {key:{key}, summary:{summary}, status:{status}, reporter:{reporter}})" % i[
            'key'].replace('-', ''), node)

    for i in l:
        fields = i['fields']
        links = fields.get('issuelinks', [])
        for x in links:
            outw = x.get('outwardIssue')
            if outw:
                session.run(
                    "CREATE (%s)-[:%s]->(%s)" % (i[
                                                     'key'].replace('-', ''), 'dependency',
                                                 outw.get('key').replace('-', '')))
                print("%s - [:%s ] -> %s" % (i['key'], x['type']['outward'], outw.get('key')))

session.close()
