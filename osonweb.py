import logging
import os
import socket


class TinyWeb:
    def __init__(self, templates_folder: str = "templates"):
        self.logger = logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.routes = {}
        self.templates_folder = templates_folder
    
    def route(self, path, method: str = "GET", content_type: str = "text/html"):
        """Decorator to register a route."""
        def wrapper(func):
            self.routes[path] = {'response': func, 'method': method, 'content_type': content_type}
            return func
        return wrapper

    def render_html_file(self, filename: str):
        path = f"{self.templates_folder}/{filename}"
        if not os.path.exists(path):
            return f"<h1>{path} did not exist</h1>"
        
        if not path.endswith(".html"):
            return f"<h1>{path} must be html file</h1>"
        
        with open(path, "r") as html:
            return html.read()

    def run(self, host: str = "127.0.0.1", port: int = 8080):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((host, port))
        
        server.listen(1)
        logging.info(f"Server started at http://{host}:{port}")

        while True:
            client, addr = server.accept()
            request = client.recv(1024).decode("utf-8")
            data = request.split("\r\n")[0].split(" ")
            print(request)
            try:
                if data == ['']:
                    method, path = None, None
                else:
                    method, path = data[0], data[1]

                if self.routes == {}:
                    logging.error("at least one route need to be created")
                
                route = self.routes.get(path)
                status_code = None
                if route is None:
                    html = "<h1>404 not found</h1>"
                    content_type = "text/html"
                    status_code = "404"
                else:
                    status_code = "200"
                    html = route['response']()
                    content_type = route['content_type']
                
                response = (
                    f"HTTP/1.1 {status_code} OK\r\n"
                    f"Content-Type: {content_type}; charset=utf-8\r\n"
                    f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                    "\r\n" + html
                )
                
                client.send(response.encode("utf-8"))
                client.close()
            except Exception as e:
                logging.error("Error: ", exc_info=True)
