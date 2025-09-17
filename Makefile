up: 
	docker-compose up -d --build

down: 
	docker-compose down

re-up: down up

exec:
	docker-compose exec jupyter bash