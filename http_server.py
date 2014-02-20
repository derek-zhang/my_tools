#!/usr/bin/python

import BaseHTTPServer
import gzip
import SocketServer
import time
import sys
import getopt

class ChunkingHTTPServer(SocketServer.ThreadingMixIn,
                        BaseHTTPServer.HTTPServer):
    daemon_threads = True

def chunk_generator():
    for i in xrange(10):
        time.sleep(.1)
        yield "this is chunk: %s\r\n" % i

class ContentLengthRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = 'HTTP/1.1/'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        myfile = file('index', 'rb')
        mybuf = myfile.read()
        self.send_header('Content-Length', len(mybuf) )
        self.end_headers()

        self.wfile.write(mybuf)

class ConnectionCloseRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = 'HTTP/1.1/'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        myfile = file('index', 'rb')
        mybuf = myfile.read()
        self.end_headers()

        self.wfile.write(mybuf)
        self.close_connection = 1

class ChunkingRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Transfer-Encoding', 'chunked')
        self.send_header('Content-Type', 'text/plain')


        myfile = file('index', 'rb')
        mybuf = myfile.read()
        self.end_headers()
        tosend = '%X\r\n' % (len(mybuf))
        self.wfile.write(tosend)
        
        
        self.wfile.write(mybuf)
        self.wfile.write('\r\n')


        #for chunk in chunk_generator():
        #   if not chunk:
        #       continue

        #   tosend = '%X\r\n%s\r\n' % (len(chunk), chunk)
        #   self.wfile.write(tosend)

        self.wfile.write('0\r\n\r\n')

def usage():
    print "h --- help"
    print "l --- use Content-Length"
    print "c --- no Content-Length, use close connection"
    print "k --- no Content-Length, use chunked Encoding"

if __name__ == '__main__':
    print sys.argv[0]
    if sys.argv[1] == '-h':
        usage()
        sys.exit(2)
    elif sys.argv[1] == '-l':
        server = ChunkingHTTPServer(
            ('127.0.0.1', 80), ContentLengthRequestHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()
    elif sys.argv[1] == '-c':
        server = ChunkingHTTPServer(
            ('127.0.0.1', 80), ConnectionCloseRequestHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()
    elif sys.argv[1] == '-k':
        server = ChunkingHTTPServer(
            ('127.0.0.1', 80), ChunkingRequestHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()
    else:
        usage()
        sys.exit(2)

