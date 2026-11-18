"""Validate actual repository cleanup without relaxing website or history gates."""
import json
import sys
from repository_cleanup_release import validate

if __name__ == '__main__':
    report, _ = validate()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(bool(report['errors']))
