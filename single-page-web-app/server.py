from http.server import BaseHTTPRequestHandler, HTTPServer
import json

hostName = "localhost"
serverPort = 5000

def parse_FormData(query):
    splitted = query.split('&')
    ret = {}
    for pair in splitted:
        kvp = pair.split('=')
        ret[kvp[0]]=kvp[1]
    return ret

users = [
    {
    "username": "admin",
    "password": "adminpass"
    },
    {
    "username": "blade",
    "password": "edalb" #encrypted: a=fasdfsafsdfj289fd
    }
]

def authentication(userObj):
    for user in users:
        if user["username"] == userObj["username"] and user["password"] == userObj["password"]:
            return True
    return False

routes = {
    "static": {
        "/": open("index.html").read(),
    },
    "api": {
        "get":{
            "/api/login":{
                "message": "Please login with your username and password.",
                "view": open("login.partial.html").read()
            },
            "/api/logout":{
                "message": ""
            }
        },
        "post":{
            "/api/login":{
                
            }
        }
    }
}

def loginCheck(username, password):
    isSuccess = authentication({"username": username, "password": password})
    statusCode = 200
    if not isSuccess:
        statusCode = 400
    return {
        "status": statusCode,
        "view":""
    }

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in routes["static"]:
            self.http_header(200, "text/html")
            self.wfile.write(bytes(routes["static"][self.path], "utf-8"))
        elif self.path.startswith("/api"):
            # handle the error of restful api calls
            self.http_header(200, "application/json")
            obj = routes["api"]["get"][self.path]
            self.wfile.write(bytes(json.dumps(obj), "utf-8"))
        else:
            self.http_header(404, "text/html")
            self.write(bytes("Page not found!", "utf-8"))
        return
    
    def do_POST(self):
        # check the routes

        self.http_header(200, "text/html")
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        userData = parse_FormData(post_data.decode("UTF-8"))
        if authentication(userData):
            self.wfile.write(bytes("Welcome, " + userData["username"], "UTF-8"))
        else:
            self.wfile.write(bytes("Username and password do not match.", "UTF-8"))
        self.wfile.write(bytes("<a href=\"/login\">login</a>", "UTF-8"))
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
