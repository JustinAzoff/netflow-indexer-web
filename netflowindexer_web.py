#!/usr/bin/env python
import sys
from netflowindexer import Searcher
from bottle import Bottle, run, request, response, redirect, request
from bottle import template
import re


import bottle
bottle.debug(True)
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
<!DOCTYPE html>
<html>
<head>
<style type="text/css">
label {
    font-weight: bold;
}
legend {
    font-weight: bold;
}
body {
    background: #2C4762;
}
#content {
    width: 700px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 20px;
    background: #f0f4f8;
    padding: 20px;
}
input {
    border: 2px solid #2C4762;
    padding: 2px;
}
input:focus {
    border: 2px solid green;
}
input[type=submit]:hover {
    background: #2C4762;
    color: #f0f4f8;
}
input {
    margin-bottom: 5px;
}


</style>
<script>
function toggle_filter()
{
 var dump = document.getElementById("dump")
 var filter = document.getElementById("filter")
 var elm = document.getElementById("filter_option")
 elm.style.display = dump.checked? "":"none"
}
</script>
</head>
<body>
<div id="content">
<h1>Netflow-Indexer Search</h1>
<form action="search">
<fieldset>
<legend>Search Netflow</legend>
<label for="ip">One or more addresses separated by space or '+'. Cidr blocks(192.168.1.0/24) are allowed</label> <br>
<input type="search" name="ip" id="ip" size="80" required autofocus> <br>

<label for="dump">Dump full netflow records ?</label> <br>
<input type="checkbox" name="dump" id="dump" onclick="toggle_filter()"> <br>

<div id="filter_option" style="display:none;">
<label for="filter">Optional filter</label> <br>
<input type="search" name="filter" id="filter" size="80" placeholder="Example: 'dst port 22'"> <br>
</div>
<input type="submit" value="Search"> <br>
<label for="databases">Limit Databases to:</label> <br>
<select id="databases" name="databases" multiple="multiple" size=50>
%for d in databases:
    <option value="{{d}}">{{d.split("/")[-1]}}</option>
%end for
</select> <br>
</form>
<script>
document.getElementById("databases").options[0].selected=false;
</script>
</div>
</body>
</html>
"""

def fix_path(request):
    uri = request.environ['REQUEST_URI']
    if '?' in uri:
        new = uri.replace("?", "/?")
    else:
        new = uri + '/'
    return redirect(new)

@app.get("/")
@app.get("/form")
def form():
    if request.environ['PATH_INFO']=='':
        return fix_path(request)
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
