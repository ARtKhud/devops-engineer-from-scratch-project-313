FROM node:25-alpine3.22

WORKDIR /app

# # Принимаем аргумент
# ARG API_URL=http://localhost/api
# # Устанавливаем как ENV переменную
# ENV API_URL=${API_URL}

RUN npm install @hexlet/project-devops-deploy-crud-frontend

CMD [ "npx", "start-hexlet-devops-deploy-crud-frontend"]