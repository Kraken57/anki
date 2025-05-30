FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Install dependencies
RUN npm install --production

# Generate Prisma client
RUN npx prisma generate

COPY . .

# Expose the port Render will assign at runtime
EXPOSE 5000

# Start the app
CMD ["node", "src/index.js"]
