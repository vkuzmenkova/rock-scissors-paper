migrations:
	alembic upgrade head

lint: 
	isort *

start:
	docker-compose up
	docker exec -i -t rock-scissors-paper-app-1 bash -c "alembic upgrade head"

