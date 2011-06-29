#!/usr/bin/env python
import sys
from netflowindexer import Searcher
from bottle import Bottle, run, request, response
from bottle import template
import re

CONFIG_FILE = "/spare/tmp/netflow/nfdump.ini"

import bottle
bottle.debug(True)
app = Bottle()

@app.route("/search")
def search():
    response.content_type = "text/plain"
    ip   = request.GET.get('ip','').strip()
    databases = request.GET.getall('databases')
    if not ip:
        yield 'missing ip parameter'
        return
    ips = re.split("[, ]+", ip)

    dump = request.GET.get('dump', False)

    s = Searcher(CONFIG_FILE)
    if not databases:
        databases = s.list_databases()

    for d in databases:
        for line in s.search(d, ips, dump):
                yield str(line) + "\n"

TEMPLATE = """
<html>
<body>
<h1>Netflow-Indexer Search</h1>
<form action="search">
<fieldset>
<legend>Search Netflow</legend>
<label for="ip">One or more addresses</label>
<input type="text" name="ip" id="ip" size="80" /> <br />

<label for="dump">Dump?</label>
<input type="checkbox" name="dump" id="dump" /> <br />

<label for="databases">Databases?</label> <br/>
<select name="databases" multiple="multiple">
%for d in databases:
    <option value="{{d}}" selected="selected">{{d}}</option>
%end for
</select> <br />
<input type="submit" value="Search"/>
</form>
</body>
</html>
"""


@app.get("")
@app.get("/")
@app.get("/form")
def form():
    s = Searcher(CONFIG_FILE)
    databases = s.list_databases()
    return template(TEMPLATE, databases=databases)

def main():
    run(app, server='cgi')

if __name__ == "__main__":
    main()
