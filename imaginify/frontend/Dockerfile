# Stage 1: Build the React application
FROM node:21.3.0 AS base

ARG REACT_APP_BACKEND_URL
ARG REACT_APP_REAL_CALLS

ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}
ENV REACT_APP_REAL_CALLS=${REACT_APP_REAL_CALLS}


# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app's source code
COPY . .

# Development image
FROM base AS dev

# Set environment to development
ENV NODE_ENV=development

# Expose port for development server
EXPOSE 3000

# Start command for development
CMD ["npm", "start"]

# Production image
FROM base AS build

# Set environment to production
ENV NODE_ENV=production

# Build your app
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:alpine AS nginx
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]