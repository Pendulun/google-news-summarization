unit_test:
	coverage run -m unittest discover tests/unit
	coverage html -i

test_dataset:
	python3 -m unittest tests.unit.test_dataset
	
test_samples:
	python3 -m unittest tests.unit.test_input

test_join:
	python3 -m unittest tests.unit.test_concat

test_solve:
	python3 -m unittest tests.unit.test_solve

test_pipeline:
	python3 -m unittest tests.unit.test_pipeline