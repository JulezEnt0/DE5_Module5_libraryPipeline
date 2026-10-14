"""Tests for cleaning.py.

TODO: Implement these tests once remove_duplicates, handle_missing_values,
and standardise_dates are implemented in src/data_processing/cleaning.py.
"""
import pytest
import pandas as pd
import pandas.testing as pdt
from data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardise_dates
)

from data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardise_dates,
)

# ========================================
# FIXTURES - Reusable test data
# ========================================

@pytest.fixture
def test_remove_duplicates():
    """Test remove_duplicates()."""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 3, 3],
        'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
        'value': [10, 20, 20, 30, 30, 30]
    })
    remove_duplicates

@pytest.fixture
def test_df_with_missing():
    """Sample DataFrame with missing values."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', None, 'Charlie', 'David'],
        'value': [10, 20, None, 40]
    })

@pytest.fixture
def test_df_dates_standerdise():
    """DataFrame with dates in several formats, plus bad and missing values."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "loan_date": 
        [
         "2024-01-15",      # ISO
        "15/01/2024",      # UK style
        "15 Jan 2024",     # text month
        "not a date",      # invalid
         None,              # missing
        ],
    })
# ========================================
# TESTS FOR remove_duplicates()
# ========================================

def test_remove_duplicates_exact(test_remove_duplicates):
    """Test duplicate removal using exact DataFrame comparison."""
    result = remove_duplicates(test_remove_duplicates, subset=['id'])

    expected = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10, 20, 30]
    })

    # Reset index for comparison
    result = result.reset_index(drop=True)

    pdt.assert_frame_equal(result, expected)

def test_remove_duplicates_properties(test_remove_duplicates):
    """Test duplicate removal using property assertions."""
    result = remove_duplicates(test_remove_duplicates, subset=['id'])

    # Test properties instead of exact values
    assert len(result) == 3
    assert result['id'].is_unique
    assert set(result['id']) == {1, 2, 3}

def test_remove_duplicates_no_changes():
    """Test with DataFrame that has no duplicates."""
    df_unique = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C']
    })

    result = remove_duplicates(df_unique, subset=['id'])

    pdt.assert_frame_equal(result, df_unique)

def test_remove_duplicates_empty():
    """Test with empty DataFrame."""
    empty_df = pd.DataFrame({'id': [], 'name': []})
    result = remove_duplicates(empty_df)

    assert len(result) == 0
    pdt.assert_frame_equal(result, empty_df)


# ========================================
# TESTS FOR handle_missing_values()
# ========================================

def test_handle_missing_drop(test_df_with_missing):
    """Test dropping rows with missing values."""
    result = handle_missing_values(test_df_with_missing, strategy='drop')

    # Should only have rows without any NaN
    assert len(result) == 2
    assert result['name'].notna().all()
    assert result['value'].notna().all()

def test_handle_missing_fill(test_df_with_missing):
    """Test filling missing values."""
    result = handle_missing_values(
        test_df_with_missing, 
        strategy='fill', 
        fill_value=0
    )

    # Should have all 4 rows
    assert len(result) == 4
    # No missing values
    assert result['name'].notna().all() or (result['name'] == 0).any()
    assert result['value'].notna().all()

def test_handle_missing_invalid_strategy(test_df_with_missing):
    """Test that invalid strategy raises error."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        handle_missing_values(test_df_with_missing, strategy='invalid')

def test_standardise_dates(test_df_dates_standerdise):
    """Test standardise_dates()."""
    result = standardise_dates(test_df_dates_standerdise, ["loan_date"])
    assert pd.api.types.is_datetime64_any_dtype(result["loan_date"])
    standardise_dates

