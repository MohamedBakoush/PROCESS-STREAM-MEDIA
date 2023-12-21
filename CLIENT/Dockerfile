FROM node:latest

WORKDIR /client

COPY package*.json ./

RUN npm install

RUN npm run build 

RUN npx prisma generate

COPY . .

EXPOSE 3000
CMD [ "npm", "run", "dev" ]