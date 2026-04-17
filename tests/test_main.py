import json
import os
import sys
from unittest.mock import patch
import pytest
from src.main import main

@pytest.fixture
def sample_json_input(tmp_path):
    data = [
        {"id": "1", "name": "Sala", "area": 15.0, "height": 2.8}
    ]
    file_path = tmp_path / "input.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path

@pytest.fixture
def bad_json_input(tmp_path):
    data = [
        {"id": "1", "name": "Sala"} # Missing area and height
    ]
    file_path = tmp_path / "bad.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path

def test_main_mock_data(capsys):
    with patch.object(sys, "argv", ["main.py"]):
        main()
        
    captured = capsys.readouterr()
    assert "--- AUDIT REPORT ---" in captured.out
    assert "total_rooms\": 4" in captured.out

def test_main_with_input_file(sample_json_input, capsys):
    with patch.object(sys, "argv", ["main.py", "--input", str(sample_json_input)]):
        main()
        
    captured = capsys.readouterr()
    assert "total_rooms\": 1" in captured.out
    assert "compliant_rooms\": 1" in captured.out

def test_main_with_input_and_output_file(sample_json_input, tmp_path):
    output_file = tmp_path / "output.json"
    
    with patch.object(sys, "argv", ["main.py", "--input", str(sample_json_input), "--output", str(output_file)]):
        main()
        
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        result = json.load(f)
        
    assert result["total_rooms"] == 1
    assert result["compliant_rooms"] == 1

def test_main_validation_error(bad_json_input):
    with patch.object(sys, "argv", ["main.py", "--input", str(bad_json_input)]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    assert excinfo.value.code == 1

def test_main_file_not_found():
    with patch.object(sys, "argv", ["main.py", "--input", "non_existent_file.json"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    assert excinfo.value.code == 1
    
def test_main_output_file_error(sample_json_input):
    with patch.object(sys, "argv", ["main.py", "--input", str(sample_json_input), "--output", "/non_existent_dir/output.json"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    assert excinfo.value.code == 1
