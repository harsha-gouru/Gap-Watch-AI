import os
import json
import sys
# Ensure gapwatch modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gapwatch import replay

def test_create_manifest_generates_file(tmp_path):
    """Test that create_manifest generates a file."""
    output_file = tmp_path / "test_manifest.jsonld"
    replay.create_manifest(output_path=str(output_file))
    assert output_file.exists()
    assert output_file.is_file()

def test_create_manifest_content(tmp_path):
    """Test the basic structure and content of the manifest."""
    output_file = tmp_path / "test_manifest.jsonld"
    replay.create_manifest(output_path=str(output_file))
    
    with open(output_file, 'r') as f:
        manifest_data = json.load(f)
    
    # Updated assertions for RO-Crate like structure
    assert "@context" in manifest_data
    assert manifest_data["@context"] == "https://w3id.org/ro/crate/1.1/context"
    assert "@graph" in manifest_data
    
    env_info_found = False
    for item in manifest_data["@graph"]:
        if item.get("@type") == "SoftwareEnvironment":
            assert "python_version" in item
            assert "platform" in item
            assert "pip_packages" in item
            # conda_environment might not be present if conda is not active/installed,
            # but the key should exist.
            assert "conda_environment" in item 
            assert "data_urls" in item # Placeholder
            assert item["data_urls"] == []
            assert "seeds" in item     # Placeholder
            assert item["seeds"] == {}
            env_info_found = True
            break
    assert env_info_found, "SoftwareEnvironment info not found in @graph"
