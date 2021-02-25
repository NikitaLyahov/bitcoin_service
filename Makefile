run:
	docker-compose up --build

run-daemon:
	docker-compose up --build -d

stop:
	docker-compose down

shell:
	docker-compose run --rm web /bin/sh

mongo-shell:
	docker exec -it bitcoin_service_mongo_1 bash

flake:
	docker-compose run --rm web flake8 .
