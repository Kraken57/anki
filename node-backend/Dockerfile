FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --production

COPY . .

# Expose the port Render will assign at runtime
EXPOSE 5000

# Start the app
CMD ["node", "src/index.js"]
