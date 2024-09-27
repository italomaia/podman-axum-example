# -- ALL TARGETS GO BELOW

# fails if ENV is empty or not defined
# ex: guard-hello -> checks whether HELLO env var is set and non-empty 
guard-var-%:
	@if [ -z ${${*}} ]; then \
		echo 'Required environment variable `${*}` is not set or empty.';\
		exit 1;\
	fi

# used by axum services
build-img-axum-dev:
	@invoke img-build -i rust-axum-dev

# used by axum services
build-img-axum-prd: guard-var-name guard-var-repo guard-var-tag
	@invoke img-build -i rust-axum-prd -n ${name}:${tag} -r ${repo} -t ${tag}

srv-up: guard-var-crate
	@invoke up -c services/${crate}

srv-down: guard-var-crate
	@invoke down -c services/${crate}

srv-stop: guard-var-crate
	@invoke stop -c services/${crate}

srv-logs-%: guard-var-crate
	@invoke logs -c services/${crate} -s ${*}

srv-wlogs-%: guard-var-crate
	@invoke logs -c services/${crate} -s ${*} -o "--follow"

web-example-up:
	@make srv-up crate=web-example

web-example-down:
	@make srv-down crate=web-example

web-example-stop:
	@make srv-stop crate=web-example

web-example-logs:
	@make srv-logs-web-server crate=web-example

web-example-wlogs:
	@make srv-wlogs-web-server crate=web-example