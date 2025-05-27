"""
Module for locking Conda/Pip environments, seeds, and data URLs.

This module provides functionality to create a manifest file (JSON-LD)
that captures the state of the environment, ensuring reproducibility.
"""
import json
import platform
import subprocess
import os
import sys

def create_manifest(output_path="gapwatch.jsonld"):
    """
    Creates a JSON-LD manifest file capturing environment details.

    The manifest includes:
    - Python version
    - Platform information
    - Pip installed packages (from pip freeze)
    - Conda environment details (if applicable)
    - Placeholders for data URLs and seeds

    Args:
        output_path (str): The path to write the JSON-LD manifest file.
                           Defaults to "gapwatch.jsonld".
    """
    manifest = {
        "@context": "https://w3id.org/ro/crate/1.1/context", # A common context for RO-Crate
        "@graph": []
    }
    
    # Basic environment information
    env_info = {
        "@id": "#environment",
        "@type": "SoftwareEnvironment",
        "python_version": sys.version,
        "platform": platform.platform(),
        "conda_environment": None,
        "pip_packages": None,
        "data_urls": [], # Placeholder
        "seeds": {}      # Placeholder
    }

    # Get Pip freeze output
    try:
        pip_result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        env_info["pip_packages"] = pip_result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running 'pip freeze': {e}")
        env_info["pip_packages"] = f"Error: {e}"
    except FileNotFoundError:
        print("Error: 'pip' command not found.")
        env_info["pip_packages"] = "Error: pip command not found."

    # Get Conda environment details
    conda_env_name = os.environ.get("CONDA_DEFAULT_ENV")
    if conda_env_name:
        try:
            conda_result = subprocess.run(
                ["conda", "env", "export"], # Using full export for more details
                capture_output=True,
                text=True,
                check=True
            )
            # Storing the raw YAML string for now.
            # Could be parsed further if needed.
            env_info["conda_environment"] = {
                "name": conda_env_name,
                "export": conda_result.stdout.strip()
            }
        except subprocess.CalledProcessError as e:
            print(f"Error running 'conda env export': {e}")
            env_info["conda_environment"] = f"Error: {e}"
        except FileNotFoundError:
            print("Error: 'conda' command not found, but CONDA_DEFAULT_ENV is set.")
            env_info["conda_environment"] = "Error: conda command not found."
    else:
        env_info["conda_environment"] = "Not in a Conda environment or CONDA_DEFAULT_ENV not set."

    manifest["@graph"].append(env_info)

    # Write the manifest to the output file
    try:
        with open(output_path, "w") as f:
            json.dump(manifest, f, indent=4)
        print(f"Manifest created successfully at {output_path}")
    except IOError as e:
        print(f"Error writing manifest file to {output_path}: {e}")

if __name__ == "__main__":
    # Example usage:
    # This will create 'gapwatch.jsonld' in the current directory
    # if the script is run directly.
    create_manifest()
    
    # To test with a specific Conda environment active:
    # conda activate your_env_name
    # python gapwatch/replay.py 
    #
    # To test without Conda:
    # (ensure no Conda env is active)
    # python gapwatch/replay.py
    
    # Example of creating it in a different location
    # create_manifest("my_custom_manifest.jsonld")
    
    # Verify content (optional manual step)
    # with open("gapwatch.jsonld", "r") as f:
    #     data = json.load(f)
    #     print(json.dumps(data, indent=4))
