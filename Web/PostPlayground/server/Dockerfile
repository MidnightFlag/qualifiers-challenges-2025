FROM node:22-alpine

RUN apk --no-cache add \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont

WORKDIR /app
COPY package*.json ./
RUN PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true npm install
COPY . .
EXPOSE 3000

CMD ["node", "app.js"]
