#  coding: utf-8
import socketserver
import os
# Copyright 2022 Aden Adar
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.result = self.data.split(b"\r\n")
        for i in self.result:
            print(i.decode("utf-8"), end="\n")
        print()

        # Read request type
        request_type = self.result[0].split(b" ")[0].decode("utf-8")
        request_path = self.result[0].split(b" ")[1].decode("utf-8")
        location = os.path.join(os.path.abspath(os.path.abspath("./www") + request_path))
        print("Request type: " + request_type)
        print("Request path: " + request_path)
        print("Location: " + location)
        is_subpath = location.startswith(os.path.abspath("./www"))

        # Checks for valid HTTP method
        if request_type != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\n\n"
            self.request.sendall(response.encode())
            return

        if os.path.isdir(location):
            if request_path[-1] != "/":
                response = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + self.server.server_address[0] + ":" + str(self.server.server_address[1]) + request_path + "/\n\n"
                self.request.sendall(response.encode())
                return

            if "index.html" in os.listdir(location):
                location = os.path.join(location, "index.html")

        if os.path.isfile(location) and is_subpath:
            fin = open(location)
            content = fin.read()
            fin.close()
        else:
            response = "HTTP/1.1 404 Not Found\n\n"
            self.request.sendall(response.encode())
            return

        if location.split('.')[-1] == "html":
            content_type = "text/html"
        else:
            content_type = "text/css"
        response = 'HTTP/1.1 200 OK\r\n' + "Content-Type: " + content_type + "\n\n" + content
        self.request.sendall(response.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


# REFERENCE
# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
