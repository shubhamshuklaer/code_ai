#!/usr/bin/python3
# https://docs.python.org/3/library/http.server.html
# https://gist.github.com/UniIsland/3346170
# https://github.com/shubhamshuklaer/ivs/blob/master/request_handler.py
import os
import sys
import getopt
import json
# The BaseHTTPServer module has been merged into http.server in Python 3.
from http.server import BaseHTTPRequestHandler,HTTPServer
import socketserver
from urllib.parse import urlparse
import mimetypes

# http://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
serv_path=os.path.join(os.popen("spoj get_root").read().strip(),"spoj")
port=8008

# No need to provide flexibility cause port is hardcoded in the
# static/js/custom.js script
# def usage():
#     print("./file_server.py [-p port] [-d dir_to_serv]")
#
# try:
#     opts,args=getopt.getopt(sys.argv[1:],"hp:d:")
# except getopt.GetoptError:
#     usage()
#     exit(2)
#
# for opt,arg in opts:
#     if opt=="-h":
#         usage()
#         exit(0)
#     elif opt=="-p":
#         port=int(arg)
#     elif opt=="-d":
#         serv_path=os.path.expanduser(arg)
#
# if serv_path == None:
#     usage()
#     exit(2)


class request_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global serv_path
        # http://stackoverflow.com/questions/8928730/processing-http-get-input-parameter-on-server-side-in-python
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        # need to remove /
        file_path=os.path.join(serv_path,self.path[1:self.path.find("?")])
        res_code=200
        print(file_path)
        if os.path.isfile(file_path):
            with open(file_path) as f:
                data_to_send=f.read()
        elif os.path.isdir(file_path):
            dir_list_tmp=os.listdir(file_path)
            dir_list=[]

            for i in range(len(dir_list_tmp)):
                # http://stackoverflow.com/questions/2472221/how-to-check-if-a-file-is-a-textfile/2472243#2472243
                # For cpp file the result is ('text/x-c', None)
                # For binary files it was (None,None)
                mime_type=mimetypes.guess_type(os.path.join(file_path,dir_list_tmp[i]))[0]
                if mime_type != None and 'text' in mime_type:
                    dir_list.append("/"+os.path.basename(file_path)+"/"+dir_list_tmp[i])
            data_to_send=dir_list
        else:
            data_to_send=""
            res_code=404

        self.send_response(res_code)
        self.send_header('Content-type','application/json')
        self.end_headers()
        # https://siongui.github.io/2015/02/20/jsonp-anonymous-callback-function/
        self.wfile.write(("("+query_components["callback"]+")("+json.dumps(data_to_send)+")").encode())

    def do_POST(self):
        file_path=os.path.join(serv_path,self.path[1:])
        length = int(self.headers['content-length'])
        body=self.rfile.read(length)
        with open(file_path,"wb") as f:
            f.write(body)

        res_code=200
        self.send_response(res_code)
        self.send_header('Content-type','text')
        self.end_headers()

print(serv_path)
print(port)

# https://brokenbad.com/address-reuse-in-pythons-socketserver/
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", port), request_handler)
httpd.serve_forever()
