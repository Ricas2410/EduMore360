"""
Ultra-minimal WSGI application for Railway deployment.
This is a standalone application that only serves the health check endpoint.
It doesn't depend on Django or any other part of the application.
"""

def application(environ, start_response):
    """
    A minimal WSGI application that only serves the health check endpoint.
    """
    path = environ.get('PATH_INFO', '')
    
    if path == '/health/' or path == '/health':
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'OK']
    
    # For any other path, return a 404
    status = '404 Not Found'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b'Not Found']

# If this file is run directly, start a simple server
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = 8000
    httpd = make_server('', port, application)
    print(f"Serving on port {port}...")
    httpd.serve_forever()
