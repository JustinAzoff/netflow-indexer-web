#!/usr/bin/env python
import sys
from netflowindexer import config
from netflowindexer.main import get_searcher
import glob
from bottle import Bottle, run, request, response

CONFIG_FILE = "/data/nfdump_xap/nfdump.ini"

#import bottle
#bottle.debug(True)
app = Bottle()

def do_search(indexer_type, database, ips, dump=None,filter=None):
    searcher = get_searcher(indexer_type)
    s = searcher(database)
    return s.search(ips, dump, filter)


@app.route("/search")
def search():
    response.content_type = "text/plain"
    ip   = request.GET.get('ip')
    dump = request.GET.get('dump', False)
    cfgdata = config.read_config(CONFIG_FILE)
    for db in sorted(glob.glob(cfgdata['dbpath'] + "/*.db")):
        for line in do_search(cfgdata['indexer'], db, [ip], dump):
            yield line + "\n"

@app.get("")
@app.get("/")
@app.get("/form")
def form():
    return """
<html>
<body>

<form action="search">
<fieldset>
<legend>Search Netflow</legend>
<label for="ip">Address</dump>
<input type="text" name="ip" id="ip" /> <br />

<label for="dump">Dump?</dump>
<input type="checkbox" name="dump" id="dump" /> <br />

<input type="submit" value="Search"/>
</form>
</body>
</html>
"""

def main():
    run(app, server='cgi')

if __name__ == "__main__":
    main()
