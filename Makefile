migrations:
	alembic upgrade head

lint: 
	isort *
	flake8 --config flake8
	

start:
	docker-compose up
	docker exec -i -t rock-scissors-paper-app-1 bash -c "alembic upgrade head"

