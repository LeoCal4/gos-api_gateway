#
# GoOutSafe API Gateway
# Nginx configuration
#

# Definition of upstreams
upstream api_gateway_upstream {
    {% for upstream in upstreams %}
    server {{ upstream.ip }}:{{ upstream.port }};
    {% endfor %}
}

# Main server context
server {

    listen 80;

    location / {
        proxy_pass http://api_gateway_upstream;

        # Do not change this
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_redirect default;
    }

    # static content serving (directly)
    location /static {
        rewrite ^/static(.*) /$1 break;
        root /static;
    }

    # statistics
    location /nginx_stats {
        stub_status on;
    }
}
