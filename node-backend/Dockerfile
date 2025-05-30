# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy source code
COPY . .

# Expose port (Render expects your app to listen on $PORT)
ENV PORT=10000
EXPOSE $PORT

# Start your app (adjust for your start script)
CMD ["node", "src/index.js"]
