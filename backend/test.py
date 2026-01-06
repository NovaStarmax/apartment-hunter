from pathlib import Path
import json

with open(Path(__file__).parent / "models" / "final.json") as f:
    data = json.load(f)

name = data['linear_regression']
print(json.dumps(name, indent=4))