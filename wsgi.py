"""
Go Out Safe
Web Server Gateway Interface

This file is the entry point for
gooutsafe-api-gateway microservice.
"""
from gooutsafe import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

# application instance, without proxy
un_app = create_app()
# application with proxy fix
app = ProxyFix(app=un_app, x_for=1, x_port=1, x_proto=1, x_host=1)

if __name__ == '__main__':
    un_app.run()
