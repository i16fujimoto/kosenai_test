#!/bin/bash

# MinIO
echo "MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY" >> .env
echo "MINIO_SECRET_KEY=$MINIO_SECRET_KEY" >> .env

# DB
echo "MONGO_INITDB_ROOT_USERNAME=$MONGO_INITDB_ROOT_USERNAME" >> .env
echo "MONGO_INITDB_ROOT_PASSWORD=$MONGO_INITDB_ROOT_PASSWORD" >> .env
echo "DATABASE_HOST=$DATABASE_HOST" >> .env
echo "DATABASE_NAME=$DATABASE_NAME" >> .env

# Django
echo "SECRET_KEY=$SECRET_KEY" >> .env
echo "ENGINE=$ENGINE" >> .env
echo "PORT=$PORT" >> .env
