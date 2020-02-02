# этап production (production-stage)
FROM nginx:1.17.8-alpine as production-stage
COPY nginx/conf.d/nginx.conf /etc/nginx/nginx.conf
COPY frontend/dist /dist/

RUN mkdir /etc/nginx/sites-enabled/ \
    && ln -s /etc/nginx/nginx.conf /etc/nginx/sites-enabled/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
