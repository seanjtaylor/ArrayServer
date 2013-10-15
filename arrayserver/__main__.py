
import os
from tornado.options import define, options
from tornado.web import Application
from tornado.ioloop import IOLoop

from arrayserver.server import ArrayHandler, arrays

define('debug', default=True, help='Run in debug mode')
define('host', default='localhost', help='HTTP host')
define('port', default=6000, type=int, help='HTTP port')
options.parse_command_line()
config = {'debug': options.debug}
app = Application([
    ('/([a-zA-Z-0-9_]+)', ArrayHandler)
    ], **config)

try:
    app.listen(options.port)
    IOLoop.instance().start()
finally:
    # cleanup
    for name, array in arrays.iteritems():
        os.unlink(array['filename'])

