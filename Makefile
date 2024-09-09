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
build-img-axum-prd: guard-var-NAME guard-var-REPO guard-var-TAG
	@invoke img-build -i rust-axum-prd -n ${NAME}:${TAG} -r ${REPO} -t ${TAG}

srv-up: guard-var-crate
	@invoke up -c services/${crate}

srv-down: guard-var-crate
	@invoke down -c services/${crate}

srv-stop: guard-var-crate
	@invoke stop -c services/${crate}

web-example-up:
	@make srv-up crate=web-example

web-example-down:
	@make srv-down crate=web-example

web-example-stop:
	@make srv-stop crate=web-example