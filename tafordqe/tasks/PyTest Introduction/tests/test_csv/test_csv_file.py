import pytest
import re

# Validate file is not empty
def test_file_not_empty(csv_data):
    assert len(csv_data) > 0, "CSV file is empty!"


# Validate schema
@pytest.mark.validate_csv
def test_schema(csv_data, validate_schema):
    actual_schema = list(csv_data[0].keys())
    expected_schema = ["id", "name", "age", "email", "is_active"]
    validate_schema(actual_schema, expected_schema)

# Validate age (SKIPPED)
@pytest.mark.validate_csv
@pytest.mark.skip(reason="Skipping age validation as per requirement")
def test_age_valid(csv_data):
    for row in csv_data:
        age = int(row["age"])
        assert 0 <= age <= 100, f"Invalid age {age} for row {row}"


# Validate email format
@pytest.mark.validate_csv
def test_email_format(csv_data):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    for row in csv_data:
        email = row["email"]
        assert re.match(pattern, email), f"Invalid email format: {email}"


# Validate no duplicates (EXPECTED TO FAIL)
@pytest.mark.validate_csv
@pytest.mark.xfail(reason="Dataset contains duplicate rows")
def test_no_duplicates(csv_data):
    seen = set()
    for row in csv_data:
        row_tuple = tuple(row.items())
        assert row_tuple not in seen, f"Duplicate row found: {row}"
        seen.add(row_tuple)


# Parametrized test for is_active
@pytest.mark.parametrize("id_val, expected", [
    ("1", "False"),
    ("2", "True"),
])
def test_is_active_parametrized(csv_data, id_val, expected):
    for row in csv_data:
        if row["id"] == id_val:
            assert row["is_active"] == expected, f"id={id_val} expected {expected}, got {row['is_active']}"


# Same test WITHOUT parametrize (id=2)
def test_is_active_id_2(csv_data):
    for row in csv_data:
        if row["id"] == "2":
            assert row["is_active"] == "True", f"id=2 expected True, got {row['is_active']}"

