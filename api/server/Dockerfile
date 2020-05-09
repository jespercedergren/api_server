FROM nginx:1.11.3

RUN rm /etc/nginx/nginx.conf
COPY api/server/nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY api/server/api.conf /etc/nginx/conf.d/