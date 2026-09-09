FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

ARG API_URL=http://backend:5000
ENV API_URL=${API_URL}

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
