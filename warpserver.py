from wsgiref.simple_server import make_server
import subprocess
import traceback
import urlparse
import sys


LISTEN_ADDR = 'localhost'
LISTEN_PORT = 8080

WRAPPED_COMMAND = '/bin/cat'


def run_command(environ):
    postdata = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
    postdata = urlparse.parse_qs(postdata)

    proc = subprocess.Popen(WRAPPED_COMMAND, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if 'stdin' in postdata:
        stdout, stderr = proc.communicate(input=postdata['stdin'][0])
    else:
        stdout, stderr = proc.communicate()

    if stderr:
        print stderr

    return ('200 OK', [('Content-type', 'text/plain')], [stdout])


def index_page(environ):
    return ('200 OK', [('Content-type', 'text/html')], ['''
<!DOCTYPE html>
<html charset="utf-8">
    <head>
        <title>Run a thing</title>
    </head>
    <body>
        <h1>Run a thing</h1>
        <form action="/run" method="POST">
            <label for="stdin">stdin:</label>
            <br />
            <textarea name="stdin" cols="80" rows="24"></textarea>
            <br />
            <input type="submit" value="Run!" />
        </form>
    </body>
</html>
'''])


URLMAP = {
    '/run': run_command,
    '/': index_page,
}

def application(environ, start_response):
    fn = URLMAP.get(environ['PATH_INFO'], None)
    if fn is None:
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return ['404 Not Found']
    else:
        try:
            status, headers, response = fn(environ)
            start_response(status, headers)
            return response
        except Exception as e:
            traceback.print_exc()
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return ['500 Internal Server Error']


def main():
    server = make_server(LISTEN_ADDR, LISTEN_PORT, application)
    print 'Server listening on http://%s:%i/' % (LISTEN_ADDR, LISTEN_PORT)
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main())