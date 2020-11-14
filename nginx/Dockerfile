#
# Nginx dockerfile
#
FROM nginx:1.15.8

# deleting old main config file
RUN rm /etc/nginx/nginx.conf
# copying new main ngninx
COPY nginx.conf /etc/nginx/

# deleting copy config file
RUN rm /etc/nginx/conf.d/default.conf
# copying new config file
COPY project.conf /etc/nginx/conf.d/

# copying static folders
COPY static ./static
