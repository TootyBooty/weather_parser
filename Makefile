up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

reload:
	docker compose -f docker-compose.yml up --build --detach


create_migrations:
	docker exec weather_service_app  alembic revision --autogenerate

roll_migrations:
	docker exec weather_service_app alembic upgrade heads


add_cities:
	sh add_cities.sh
