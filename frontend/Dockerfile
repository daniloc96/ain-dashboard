# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Build args
ARG NEXT_PUBLIC_JIRA_LINKS
ENV NEXT_PUBLIC_JIRA_LINKS=$NEXT_PUBLIC_JIRA_LINKS

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy built assets from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
