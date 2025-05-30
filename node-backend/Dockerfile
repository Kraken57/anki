FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json first (for caching)
COPY package*.json ./

# Install dependencies (production only)
RUN npm install --production

# Copy prisma folder with schema.prisma (needed for prisma generate)
COPY prisma ./prisma

# Run Prisma generate now that schema.prisma is present
RUN npx prisma generate

# Copy the rest of your source code
COPY . .

# Set the port environment variable
ENV PORT=5000

# Expose the port (matches ENV PORT)
EXPOSE 5000

# Start the Node.js app
CMD ["node", "src/index.js"]
