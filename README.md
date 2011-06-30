NetflowIndexer-web
==================

Simple web interface for Netflow-indexer

Usage
-----

    netflow-indexer-web /path/to/netflow-indexer-config-file.ini

CGI usage
---------

    from netflowindexer_web import app, set_config_file, run

    set_config_file("/path/to/netflow-indexer-config-file.ini")
    run(app, server='cgi')


WSGI usage
----------
This should work too:

    from netflowindexer_web import app, set_config_file
    set_config_file("/path/to/netflow-indexer-config-file.ini")
    application = app
