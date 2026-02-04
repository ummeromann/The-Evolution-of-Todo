"""Unit tests for utils.py validation and formatting functions."""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import utils


def test_validate_description_valid():
    """Test validating a valid description."""
    result = utils.validate_description("Valid task")
    assert result == "Valid task"

    # Test with leading/trailing whitespace
    result = utils.validate_description("  Trimmed task  ")
    assert result == "Trimmed task"


def test_validate_description_invalid():
    """Test validating invalid descriptions."""
    # Empty string
    assert utils.validate_description("") is None

    # Whitespace only
    assert utils.validate_description("   ") is None
    assert utils.validate_description("\t\n") is None


def test_format_tasks_table_with_tasks():
    """Test formatting task table with tasks."""
    tasks = [
        {"id": 1, "description": "Task 1", "completed": False},
        {"id": 2, "description": "Task 2", "completed": True},
    ]
    result = utils.format_tasks_table(tasks)

    assert "ID" in result
    assert "Description" in result
    assert "Status" in result
    assert "Task 1" in result
    assert "Task 2" in result
    assert "Incomplete" in result
    assert "Complete" in result


def test_format_tasks_table_empty_state():
    """Test formatting task table with no tasks."""
    result = utils.format_tasks_table([])
    assert result == "No tasks yet. Add your first task!"


def test_validate_task_id_valid():
    """Test validating valid task IDs."""
    assert utils.validate_task_id("1") == 1
    assert utils.validate_task_id("42") == 42
    assert utils.validate_task_id("  10  ") == 10  # With whitespace


def test_validate_task_id_invalid():
    """Test validating invalid task IDs."""
    # Non-numeric
    assert utils.validate_task_id("abc") is None
    assert utils.validate_task_id("") is None

    # Negative or zero
    assert utils.validate_task_id("0") is None
    assert utils.validate_task_id("-1") is None

    # Float
    assert utils.validate_task_id("1.5") is None
