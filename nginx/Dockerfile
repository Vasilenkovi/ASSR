FROM nginx:1.19.0-alpine
ENV hostname 51.250.114.60
COPY ./default.conf /etc/nginx/conf.d/
ADD ./static/ /static/
VOLUME /static/
