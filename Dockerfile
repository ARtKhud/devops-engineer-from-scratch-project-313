FROM node:25-alpine as frontend-builder

WORKDIR /frontend

RUN apk update && \
    npm install @hexlet/project-devops-deploy-crud-frontend && \
    cp -r node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /frontend/dist/


FROM python:3.14-alpine

WORKDIR /app
COPY --from=frontend-builder /frontend/dist /var/www/html

RUN apk update \
&& apk add --no-cache curl make nginx \
&& rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock Makefile README.md /app/

RUN make install

COPY . /app/


RUN mv /app/nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /app/bin/start.sh

EXPOSE 80

CMD ["/app/bin/start.sh"]