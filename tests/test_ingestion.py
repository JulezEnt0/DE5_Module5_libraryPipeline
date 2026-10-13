"""Tests for ingestion.py.

TODO: Implement these tests for load_csv, load_json, and load_excel in
src/data_processing/ingestion.py.
"""
import json

import pandas as pd
import pytest

from data_processing.ingestion import load_csv, load_json, load_excel


# --- load_csv ---

def test_load_csv(tmp_path):
    """Loads a CSV into a DataFrame with the right shape and values."""
    file = tmp_path / "books.csv"
    file.write_text("id,title\n1,Dune\n2,Emma\n")

    df = load_csv(file)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["id", "title"]
    assert df["title"].iloc[0] == "Dune"


def test_load_csv_accepts_string_path(tmp_path):
    """The pipeline passes strings, so check that works too."""
    file = tmp_path / "books.csv"
    file.write_text("id,title\n1,Dune\n")

    assert len(load_csv(str(file))) == 1




def test_load_csv_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "nope.csv")


def test_load_csv_empty_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")

    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(file)


# --- load_json ---

def test_load_json(tmp_path):
    """Loads a list of records into a DataFrame."""
    file = tmp_path / "loans.json"
    file.write_text(json.dumps([
        {"id": 1, "title": "Dune"},
        {"id": 2, "title": "Emma"},
    ]))

    df = load_json(file)

    assert df.shape == (2, 2)
    assert list(df.columns) == ["id", "title"]


def test_load_json_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_json(tmp_path / "nope.json")



# --- load_excel ---

def test_load_excel(tmp_path):
    """Loads the first sheet by default."""
    file = tmp_path / "catalogue.xlsx"
    pd.DataFrame({"id": [1, 2], "title": ["Dune", "Emma"]}).to_excel(file, index=False)

    df = load_excel(file)

    assert df.shape == (2, 2)
    assert df["title"].iloc[1] == "Emma"


def test_load_excel_named_sheet(tmp_path):
    file = tmp_path / "catalogue.xlsx"
    with pd.ExcelWriter(file) as writer:
        pd.DataFrame({"a": [1]}).to_excel(writer, sheet_name="First", index=False)
        pd.DataFrame({"b": [1, 2, 3]}).to_excel(writer, sheet_name="Second", index=False)

    df = load_excel(file, sheet_name="Second")

    assert list(df.columns) == ["b"]
    assert len(df) == 3


def test_load_excel_multiple_sheets_returns_dict(tmp_path):
    file = tmp_path / "catalogue.xlsx"
    with pd.ExcelWriter(file) as writer:
        pd.DataFrame({"a": [1]}).to_excel(writer, sheet_name="One", index=False)
        pd.DataFrame({"b": [2]}).to_excel(writer, sheet_name="Two", index=False)

    result = load_excel(file, sheet_name=["One", "Two"])

    assert isinstance(result, dict)
    assert set(result) == {"One", "Two"}


def test_load_excel_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_excel(tmp_path / "nope.xlsx")


def test_load_excel_bad_sheet_name(tmp_path):
    file = tmp_path / "catalogue.xlsx"
    pd.DataFrame({"a": [1]}).to_excel(file, index=False)

    with pytest.raises(ValueError):
        load_excel(file, sheet_name="DoesNotExist")