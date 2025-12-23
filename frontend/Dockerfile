FROM nginx:1.29-alpine

WORKDIR /app

RUN apk add --update nodejs npm
COPY package.json .
COPY . .
RUN npm install
RUN npm run build

COPY ./build/. /usr/share/nginx/html/
COPY ./nginx.conf /etc/nginx/conf.d/default.conf