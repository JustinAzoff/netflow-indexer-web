#!/usr/bin/env python
import sys
import os
from netflowindexer import Searcher
from bottle import Bottle, run, request, response, redirect, request
from bottle import template
import re


import bottle
#bottle.debug(True)
app = Bottle()

def filter_databases(wanted_databases, all_databases):
    wanted = set(wanted_databases)
    expanded = [d for d in all_databases if os.path.basename(d) in wanted]
    return expanded

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
    all_databases = s.list_databases()
    if not databases:
        search_databases = all_databases
    else:
        search_databases = filter_databases(databases, all_databases)

    for d in search_databases:
        for line in s.search(d, ips, dump, filter):
                yield str(line) + "\n"

def iter_len(it):
    x = 0
    for _ in it:
        x+=1
    return x

@app.route("/stats")
def stats():
    ip = request.GET.get('ip','').strip()
    if not ip:
        return {}
    ips = re.split("[, ]+", ip)

    s = Searcher(app.config['nfi_config'])
    databases = s.list_databases()

    total_databases = len(databases)
    seen_databases = 0
    all_databases = []
    for d in databases:
        hits = iter_len(s.search(d, ips))
        all_databases.append((os.path.basename(d), hits))
        if hits:
            seen_databases += 1

    return {
        'total': total_databases,
        'hits':  seen_databases,
        'databases':    all_databases,
    }


TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title> Netflow Search </title>
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
    <option value="{{d}}">{{d}}</option>
%end
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
    databases = map(os.path.basename, s.list_databases())
    return template(TEMPLATE, databases=databases)

def set_config_file(filename):
    app.config['nfi_config'] = filename

def main():
    config = sys.argv[1]
    set_config_file(config)
    run(app, server='auto', host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
