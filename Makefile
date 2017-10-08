ROOT = $(shell git rev-parse --show-toplevel)
BUILD_IMAGE = alexwlchan/build_alfred_workflow
LINT_IMAGE = alexwlchan/flake8


.docker/build: requirements.txt build_alfred_workflow.py
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

.docker/flake8: flake8.Dockerfile
	docker build --tag $(LINT_IMAGE) --file flake8.Dockerfile .
	mkdir -p .docker
	touch .docker/flake8


requirements.txt: requirements.in
	docker run --volume $(ROOT):/src --rm --tty micktwomey/pip-tools

web-links.alfredworkflow: .docker/build data
	docker run --volume $(ROOT)/data:/data --rm $(BUILD_IMAGE)

lint: .docker/flake8
	docker run --volume $(ROOT):/src --rm --tty $(LINT_IMAGE)


.PHONY: lint
