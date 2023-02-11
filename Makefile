build:
	docker-compose up -d --build

build-dev:
	docker-compose -f docker-compose.dev.yml up -d --build

up:
	docker-compose up -d

down:
	docker-compose down

test:
	docker-compose run --rm api python manage.py test