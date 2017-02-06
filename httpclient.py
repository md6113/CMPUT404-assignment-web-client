#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

# Read the following page for formatting guidance:
# https://pyformat.info/
# Read-over the second set of CMPUT 404 HTTP slides for guidance on how to structure a GET or POST request:
# https://eclass.srv.ualberta.ca/pluginfile.php/3259366/mod_resource/content/1/05-HTTP-II.pdf
# Reat this python docs page for guidance on how to use the .encode() method:
# https://docs.python.org/2/howto/unicode.html

import sys
import socket
import urllib
from urlparse import urlparse
# you may use urllib to encode data appropriately


def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # Open up a socket connection and return that item
    def connect(self, host, port):
        if not port:
            port = 80
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((host, port))
            return clientSocket
        except Exception:
            print "Error connecting to socket: %s" % Exception
            sys.exit()

    # Get the return code
    def get_code(self, data):
        data = data.split()
        code = int(data[1])
        return code

    # Read everything that gets returned by the request
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # Make the request using the prescribed socket
    def makerequest(self, the_socket, message):
        try:
            the_socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print "Error sending message: " % socket.error
            sys.exit()

        reply = self.recvall(the_socket)
        return reply

    def GET(self, url, args=None):

        # from eclass discussion "Assignment 2" we are allowed to use urlparse
        info = urlparse(url)

        # Create the request
        request = "GET " + info.path + " HTTP/1.1\r\nHost: " + info.hostname + "\r\n"
        request += "Accept: */*\r\nConnection: close\r\n\r\n"

        # Connect to the socket
        the_socket = self.connect(info.hostname, info.port)
        # Send the request to the address
        reply = self.makerequest(the_socket, request)
        # Close the connection to the socket
        the_socket.close()
        # Split the reply into the header and the body
        reply = reply.split('\r\n\r\n')
        # Extract the code from the header
        code = self.get_code(reply[0])
        # Return the code and body
        return HTTPResponse(code, reply[1])

    def POST(self, url, args=None):

        # from eclass discussion "Assignment 2" we are allowed to use urlparse
        info = urlparse(url)

        # From the Restrictions section  we are allowed to use url-encode to format
        if args is None:
            content = ""
        else:
            content = urllib.urlencode(args)

        # Create the request
        request = "POST " + info.path + " HTTP/1.1\r\nHost: " + info.hostname + "\r\n"
        request += "Accept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\n"
        request += "Content-Length: " + str(len(content)) + "\r\n\r\n" + content + "\r\n"

        # Connect to the socket
        the_socket = self.connect(info.hostname, info.port)
        # Send the request to the address
        reply = self.makerequest(the_socket, request)
        # Close the connection to the socket
        the_socket.close()
        # Split the reply into the header and the body
        reply = reply.split('\r\n\r\n')
        # Extract the code from the header
        code = self.get_code(reply[0])
        # Return the code and body
        return HTTPResponse(code, reply[1])

    def command(self, url, command="GET", args=None):
        if command == "POST":
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if len(sys.argv) <= 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 3:
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
