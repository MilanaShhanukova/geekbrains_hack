FROM node
COPY ./frontend /opt/app
WORKDIR /opt/app
RUN npm ci --legacy-peer-deps
RUN npm i -g nx
CMD ["npm", "run", "start:docker"]