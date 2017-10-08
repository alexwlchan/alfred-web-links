ROOT = $(shell git rev-parse --show-toplevel)
BUILD_IMAGE = alexwlchan/build_alfred_workflow

requirements.txt: requirements.in
	docker run --volume $(ROOT):/src --rm --tty micktwomey/pip-tools

.docker/build: requirements.txt build_alfred_workflow.py
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

shortcuts.alfredworkflow: .docker/build
	docker run --volume $(ROOT):/data --rm $(BUILD_IMAGE)
