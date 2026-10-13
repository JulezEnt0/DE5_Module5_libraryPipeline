"""Data ingestion functions.

TODO: Complete these functions for the library project.
"""
"""Data ingestion functions for the library project."""

import json
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv(filepath, **kwargs):
    """Load CSV file with error handling.

    Args:
        filepath: Path to CSV file
        **kwargs: Additional arguments for pd.read_csv()

    Returns:
        pd.DataFrame: Loaded data

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    filepath = Path(filepath)

    if not filepath.is_file():
        logger.error("CSV file not found: %s", filepath)
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    try:
        logger.info("Loading CSV from %s", filepath)
        df = pd.read_csv(filepath, **kwargs)
        logger.info(
            "Successfully loaded %s rows and %s columns from %s",
            len(df),
            len(df.columns),
            filepath,
        )
        return df
    except Exception:
        logger.exception("Error loading CSV from %s", filepath)
        raise


def load_json(filepath, **kwargs):
    """Load JSON file and flatten structure.

    Args:
        filepath: Path to JSON file
        **kwargs: Additional arguments for pd.json_normalize()

    Returns:
        pd.DataFrame: Flattened data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If the file isn't valid JSON
    """
    filepath = Path(filepath)

    if not filepath.is_file():
        logger.error("JSON file not found: %s", filepath)
        raise FileNotFoundError(f"JSON file not found: {filepath}")

    try:
        logger.info("Loading JSON from %s", filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.json_normalize(data, **kwargs)
        logger.info(
            "Successfully loaded %s rows and %s columns from %s",
            len(df),
            len(df.columns),
            filepath,
        )
        return df
    except Exception:
        logger.exception("Error loading JSON from %s", filepath)
        raise

    # Check file exists
    if not filepath.exists():
        logger.error(f"Excel File not found: {filepath}")
        raise FileNotFoundError(f"Excel File not found: {filepath}")

    try:
        logger.info(f"Loading Excel from {filepath} (sheet_name={sheet_name})")
        df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)

        if isinstance(df, dict):
            total_rows = sum(len(v) for v in df.values())
            line = f"Successfully loaded {len(df)} sheets, total {total_rows} rows from {filepath}"
            logger.info(line)
        else:
            logger.info(f"Successfully loaded {len(df)} rows from {filepath}")

        return df

    except ValueError as e:
        logger.error(f"Value error loading Excel {filepath}: {e}")
        raise
    except ImportError as e:
        logger.error(f"Missing Excel engine for {filepath}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading Excel {filepath}: {e}")
        raise
