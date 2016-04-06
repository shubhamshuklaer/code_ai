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

# http://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
serv_path=os.path.join(os.popen("spoj get_root").read().strip(),"spoj")
port=8000

def usage():
    print("./file_server.py [-p port] [-d dir_to_serv]")

try:
    opts,args=getopt.getopt(sys.argv[1:],"hp:d:")
except getopt.GetoptError:
    usage()
    exit(2)

for opt,arg in opts:
    if opt=="-h":
        usage()
        exit(0)
    elif opt=="-p":
        port=int(arg)
    elif opt=="-d":
        serv_path=os.path.expanduser(arg)

if serv_path == None:
    usage()
    exit(2)


class request_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global serv_path
        # need to remove /
        file_path=os.path.join(serv_path,self.path[1:])
        res_code=200
        if os.path.isfile(file_path):
            with open(file_path) as f:
                data_to_send=f.read()
        elif os.path.isdir(file_path):
            dir_list=os.listdir(file_path)
            for i in range(len(dir_list)):
                dir_list[i]="/"+os.path.basename(file_path)+"/"+dir_list[i]
            data_to_send=json.dumps(dir_list)
        else:
            data_to_send=""
            res_code=404

        self.send_response(res_code)
        self.send_header('Content-type','text')
        self.end_headers()
        self.wfile.write(data_to_send.encode())

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
