FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Add health check endpoints
RUN echo 'app.get("/health", (req, res) => { res.status(200).send("OK"); });' >> server.js
RUN echo 'app.get("/ready", (req, res) => { res.status(200).send("OK"); });' >> server.js

# Expose port
EXPOSE 3001

# Start the server
CMD ["node", "server.js"]
