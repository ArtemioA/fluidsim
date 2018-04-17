

develop:
	python setup.py develop

clean_so:
	find fluidsim -name "*.so" -delete

clean_pyc:
	find fluidsim -name "*.pyc" -delete
	find fluidsim -name "__pycache__" -type d | xargs rm -rf

clean:
	rm -rf build

cleanall: clean clean_so

black:
	black -l 82 fluidsim

tests:
	fluidsim-test -v

tests_mpi:
	mpirun -np 2 fluidsim-test -v

_tests_coverage:
	mkdir -p .coverage
	coverage run -p -m fluidsim.util.testing -v
	mpirun -np 2 coverage run -p -m fluidsim.util.testing -v

_report_coverage:
	coverage combine
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: _tests_coverage _report_coverage

lint:
	pylint -rn --rcfile=pylintrc --jobs=$(shell nproc) fluidsim

install:
	python setup.py install
