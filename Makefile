# options: zc.buildout options
# src: source path
# minimum_coverage: minimun test coverage allowed
# pep8_ignores: ignore listed PEP 8 errors and warnings
# max_complexity: maximum McCabe complexity allowed
# css_ignores: skip file names matching find pattern (use ! -name PATTERN)
# js_ignores: skip file names matching find pattern (use ! -name PATTERN)

SHELL = /bin/sh

options = -N -q -t 3

install:
	mkdir -p buildout-cache/downloads
	python bootstrap.py -c travis.cfg
	bin/buildout -c travis.cfg $(options)

tests:
	bin/test

