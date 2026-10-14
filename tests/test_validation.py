"""Tests for validation.py.

TODO: Implement this test once validate_isbn is implemented in
src/data_processing/validation.py.
"""
import pytest
import pandas as pd
import pandas.testing as pdt
from data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardise_dates
)

from data_processing.validation import validate_isbn



@pytest.mark.parametrize("isbn", [
    "9780306406157",
    "9780131103627",
    "9781234567897",
])
def test_valid_isbn_returns_cleaned_string(isbn):
    assert validate_isbn(isbn) == isbn


def test_valid_isbn_with_hyphens_returns_cleaned():
    assert validate_isbn("978-0-306-40615-7") == "9780306406157"# --- Missing values ---

def test_none_returns_none():
    assert validate_isbn(None) is None