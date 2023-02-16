from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 5000

routes = {
    "static": {
        "/": open("index.html").read(),
        "/about": "Copyright Reserved by Blade",
        "/greeting": "Hello my friend"
    },
    "api": {        
    }
}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in routes["static"]:
            self.http_header(200, "text/html")
            self.wfile.write(bytes(routes["static"][self.path], "utf-8"))
        elif self.path.startswith("/api"): #http://localhost:5000/api/getallusers
            self.http_header(200, "application/json")
            self.wfile.write(bytes("{\"result\": \"OK\"}", "utf-8"))
        else:
            self.http_header(404, "text/html")
            self.wfile.write(bytes("Page not found!", "utf-8"))
        return
    
    def do_POST(self):
        print("Hit by a post request")
        return
    
    def http_header(self, statuscode, contenttype):
        self.send_response(statuscode)
        self.send_header("Content-type", contenttype)
        self.end_headers()
    
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt: #CTRL + C
        pass

    webServer.server_close()
    print("Server has stopped.")
