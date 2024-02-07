from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime
import time
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        utc_time = datetime.datetime.utcnow()
        toronto_time = utc_time - datetime.timedelta(hours=5)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        message = json.dumps({
            'Current Toronto Time': toronto_time.strftime('%Y-%m-%d %H:%M:%S')
        })
        self.wfile.write(message.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8008):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd server...')

if __name__ == '__main__':
    run()