import pytest
import pandas as pd
import csv

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def csv_data():
    path_to_file = "src/data/data.csv"
    with open(path_to_file, newline="") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def validate_schema():
    def _validate(actual_schema, expected_schema):
        assert actual_schema == expected_schema, \
            f"Schema mismatch! Expected {expected_schema}, got {actual_schema}"
    return _validate

# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(items):
    for item in items:
        if not item.keywords:
            item.add_marker(pytest.mark.unmarked)