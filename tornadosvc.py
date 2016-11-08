# uncomment the next import line to get print to show up or see early
# exceptions if there are errors then run
#   python -m win32traceutil
# to see the output
#import win32traceutil
import win32serviceutil

PORT_TO_BIND = 8888

SERVICE_NAME = "TornadoWebService"
SERVICE_DISPLAY_NAME = "Tornado Service"
SERVICE_DESCRIPTION = """Service to run our django spatial database"""

class PyWebService(win32serviceutil.ServiceFramework):
    """Python Web Service."""

    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_deps_ = None        # sequence of service names on which this depends
    # Only exists on Windows 2000 or later, ignored on Windows NT
    _svc_description_ = SERVICE_DESCRIPTION

    def SvcDoRun(self):
        import os
        import sys

        import tornado.wsgi
        from django.core.wsgi import get_wsgi_application
        from tornado.options import options, define, parse_command_line

        define('port', type=int, default=PORT_TO_BIND)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'ymac_sdb.settings'
        sys.path.append(r"C:\inetpub\wwwroot\ymac_sdb\YMAC_DB\\")

        parse_command_line()

        wsgi_app = get_wsgi_application()
        container = tornado.wsgi.WSGIContainer(wsgi_app)

        tornado_app = tornado.web.Application(
            [
                ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
            ])

        self.server = tornado.httpserver.HTTPServer(tornado_app)
        self.server.listen(options.port)
        server = self.server
        tornado.ioloop.IOLoop.instance().start()


    def SvcStop(self):
        import tornado.wsgi
        server = self.server
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PyWebService)