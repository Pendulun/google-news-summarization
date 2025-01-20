test:
	coverage run -m unittest discover tests
	coverage html -i

test_dataset:
	python3 -m unittest tests.test_dataset
	
test_samples:
	python3 -m unittest tests.test_input

test_join:
	python3 -m unittest tests.test_concat

test_solve:
	python3 -m unittest tests.test_solve