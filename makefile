install:
	uv pip install -r requirements.txt
	uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu

unit_test:
	coverage run -m unittest discover src/tests/unit
	coverage html -i

test_dataset:
	python3 -m unittest src.tests.unit.test_dataset
	
test_samples:
	python3 -m unittest src.tests.unit.test_input

test_join:
	python3 -m unittest src.tests.unit.test_concat

test_solve:
	python3 -m unittest src.tests.unit.test_solve

test_pipeline:
	python3 -m unittest src.tests.unit.test_pipeline