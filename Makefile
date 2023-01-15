.PHONY: start-dev-mode
start-dev-mode:
	touch docker/.bash_history
	docker-compose -f docker/docker-compose.yml run asset_data_system_user

.PHONY: start
start:
	touch docker/.bash_history
	docker-compose -f docker/docker-compose.yml run asset_data_system
