#!/usr/bin/env python2
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import sys
import os
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass
class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    args = sys.argv[1:]
    port = 8000
    dir = None
    while args:
        a = args.pop(0)
        if a == '-h':
            usage()
        elif a == "-port":
            port = int(args.pop(0))
        elif not dir:
            dir = os.path.join(a)
            os.chdir(dir)
        else:
            print("argument %s unknown" % a)
            sys.exit(1)
    server = ThreadingSimpleServer(('', port), CORSRequestHandler)
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("Finished")
    # BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)
