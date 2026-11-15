"""Exact user-authorized metadata replacements, retained for preservation gates."""
import json
from pathlib import Path
OVERRIDES=json.loads((Path(__file__).resolve().parents[1]/'docs/audit-followup-2026-11-15/metadata.json').read_text())
def approved(path,field,original):
 entry=OVERRIDES.get(path,{}).get(field)
 return entry['new'] if entry else original
