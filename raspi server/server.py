# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/hello'):
            self.send_response(200)
            self.send_header("Content-type", "picture/png")
            self.end_headers()
            self.wfile.write(bytes("<head><title>hello</title><style>h1 {color:blue;font-size:50px;}</style></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h1>Hello everyone</h1>", "utf-8"))
            self.wfile.write(bytes("</body>", "utf-8"))
            self.wfile.write(bytes("</html>","utf-8"))
        elif self.path.startswith('/example'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<head><title>hello</title><style>h1 {color:blue;font-size:50px;}</style></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h1>This is an example</h1>", "utf-8"))
            self.wfile.write(bytes("</body>", "utf-8"))
            self.wfile.write(bytes("</html>","utf-8"))
        elif self.path.startswith('/favicon.ico'):
            self.send_response(404)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<head><title>not found</title><style>h1 {color:blue;font-size:50px;}</style></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("</body>", "utf-8"))
            self.wfile.write(bytes("</html>","utf-8"))
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")