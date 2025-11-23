#!/usr/bin/env python3
"""
Validate canonical-structure.yaml against validation-rules.json.
Falls back to a lightweight sanity check if jsonschema is not installed.
"""

import sys
import json
import logging
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
STRUCTURE_FILE = PROJECT_ROOT / ".claude" / "structure" / "canonical-structure.yaml"
SCHEMA_FILE = PROJECT_ROOT / ".claude" / "structure" / "validation-rules.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("structure-config-validator")


def load_yaml(path: Path):
    if not path.exists():
        logger.error(f"Missing file: {path}")
        sys.exit(1)
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to parse YAML {path}: {e}")
        sys.exit(1)


def load_json(path: Path):
    if not path.exists():
        logger.error(f"Missing file: {path}")
        sys.exit(1)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse JSON {path}: {e}")
        sys.exit(1)


def validate_with_jsonschema(data, schema):
    try:
        import jsonschema
    except ImportError:
        logger.warning("jsonschema not installed; running lightweight validation instead.")
        return None

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.ValidationError as e:
        logger.error(f"Schema validation failed: {e.message}")
        return False
    except Exception as e:
        logger.error(f"Schema validation error: {e}")
        return False


def lightweight_validation(data):
    """
    Minimal validation to catch obvious issues without jsonschema.
    """
    required_top = ["file_types", "directory_rules", "settings", "metadata"]
    for key in required_top:
        if key not in data:
            logger.error(f"Missing top-level key: {key}")
            return False

    if not isinstance(data.get("file_types"), list) or not data["file_types"]:
        logger.error("file_types must be a non-empty list")
        return False

    for ft in data["file_types"]:
        for field in ("name", "patterns", "canonical_location", "lifecycle_rule"):
            if field not in ft:
                logger.error(f"file_type missing '{field}': {ft}")
                return False

    return True


def main():
    data = load_yaml(STRUCTURE_FILE)
    schema = load_json(SCHEMA_FILE)

    result = validate_with_jsonschema(data, schema)
    if result is None:
        result = lightweight_validation(data)

    if result:
        logger.info("✅ canonical-structure.yaml is valid.")
        sys.exit(0)
    else:
        logger.error("❌ canonical-structure.yaml is invalid.")
        sys.exit(1)


if __name__ == "__main__":
    if sys.version_info < (3, 7):
        logger.error("Python 3.7+ is required.")
        sys.exit(1)
    main()
