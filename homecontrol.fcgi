#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from homecontrol import app
if __name__ == '__main__':
    WSGIServer(app,bindAddress='/tmp/homecontrol-fcgi.sock').run()
