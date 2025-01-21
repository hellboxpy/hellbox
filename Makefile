init:
	pip install pipenv
	pipenv lock
	pipenv install --dev

test:
	# This runs all of the tests. To run an individual test, run py.test with
	# the -k flag, like "py.test -k test_path_is_not_double_encoded"
	pipenv run test
	pipenv run check
