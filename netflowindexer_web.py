#!/usr/bin/env python
import sys
from netflowindexer import Searcher
from bottle import Bottle, run, request, response, redirect, request
from bottle import template
import re


import bottle
#bottle.debug(True)
app = Bottle()

@app.route("/search")
def search():
    response.content_type = "text/plain"
    ip   = request.GET.get('ip','').strip()
    filter    = request.GET.get('filter','').strip()
    databases = request.GET.getall('databases')
    if not ip:
        yield 'missing ip parameter'
        return
    ips = re.split("[, ]+", ip)

    dump = request.GET.get('dump', False)

    s = Searcher(app.config['nfi_config'])
    if not databases:
        databases = s.list_databases()

    for d in databases:
        for line in s.search(d, ips, dump, filter):
                yield str(line) + "\n"

TEMPLATE = """
<html>
<head>
<style type="text/css">
label {
    font-weight: bold;
}
</style>
</head>
<body>
<h1>Netflow-Indexer Search</h1>
<form action="search">
<fieldset>
<legend>Search Netflow</legend>
<label for="ip">One or more addresses</label> <br>
<input type="text" name="ip" id="ip" size="80" /> <br>

<label for="filter">Optional filter</label> <br>
<input type="text" name="filter" id="filter" size="80" /> <br>

<label for="dump">Dump records?</label> <br>
<input type="checkbox" name="dump" id="dump" /> <br>

<input type="submit" value="Search"/> <br/>
<label for="databases">Limit Databases?</label> <br>
<select id="databases" name="databases" multiple="multiple" size=50>
%for d in databases:
    <option value="{{d}}">{{d.split("/")[-1]}}</option>
%end for
</select> <br>
</form>
<script>
document.getElementById("databases").options[0].selected=false;
</script>
</body>
</html>
"""


@app.get("/")
@app.get("/form")
def form():
    if request.environ['PATH_INFO']=='':
        return redirect(request.environ['REQUEST_URI'] + '/')
    s = Searcher(app.config['nfi_config'])
    databases = s.list_databases()
    return template(TEMPLATE, databases=databases)

def set_config_file(filename):
    app.config['nfi_config'] = filename

def main():
    config = sys.argv[1]
    set_config_file(config)
    run(app, server='auto', port=8000)

if __name__ == "__main__":
    main()
