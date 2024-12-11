FROM nginx:1.19.0-alpine
ENV hostname 51.250.112.4
COPY ./nginx/nginx.conf /etc/nginx/conf.d/
ADD ./AssrWeb/static/ /static/
VOLUME /static