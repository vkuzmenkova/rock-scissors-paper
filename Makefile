migrations:
	alembic upgrade head

lint: 
	isort *

start:
	docker-compose up -d

