FROM stanfoot/vue3-dev:0.1.2

COPY vite.config.js package.json package-lock.json jsconfig.json index.html   ./
COPY public ./public
COPY src ./src
COPY store ./store

# install psql
RUN npm i

EXPOSE 5317

# CMD ["app"]
