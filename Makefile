.PHONY: build-all
build-all:
	docker-compose -f docker/docker-compose.yml build

.PHONY: start-dev-mode
start-dev-mode:
	touch docker/.bash_history
	docker-compose -f docker/docker-compose.yml run asset_data_system_user

.PHONY: kill-all
kill-all:
	sudo docker kill $(sudo docker ps -q)
