FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
&& apt-get install -y --no-install-recommends curl make nginx \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock Makefile README.md /app/

RUN make install

COPY . /app/

COPY node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/ /var/www/html

RUN mv /app/nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /app/bin/start.sh

EXPOSE 80

CMD ["/app/bin/start.sh"]