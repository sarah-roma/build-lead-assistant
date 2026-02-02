# Use an official node image as the base image
FROM node:20-alpine


WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm install

COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Command to run the application
CMD ["npm", "run", "dev"]

