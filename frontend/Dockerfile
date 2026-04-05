# syntax=docker/dockerfile:1.7
FROM oven/bun:1.2.15

WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile || bun install

COPY . .

EXPOSE 3000

CMD ["bun", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
