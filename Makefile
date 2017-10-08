ROOT = $(shell git rev-parse --show-toplevel)

requirements.txt: requirements.in
	docker run --volume $(ROOT):/src --rm --tty micktwomey/pip-tools
