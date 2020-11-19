#
# Nginx dockerfile
#
FROM nginx:1.15.8

# deleting old main config file
RUN rm /etc/nginx/nginx.conf

# copying new main nginx
COPY nginx.conf /etc/nginx/

# deleting config file
RUN rm /etc/nginx/conf.d/default.conf

