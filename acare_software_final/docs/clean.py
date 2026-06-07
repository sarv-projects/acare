import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent / "ACARE_Documentation.md"
content = DOCS.read_text(encoding="utf-8")

pattern = r'\*\*Task Execution Phases \(planner_node\.py\):\*\*\n\nPhase 1 — \*\*Vision Search\*\* \(`_phase_vision_search`\):.*?- Height adjustment via "lower"/"higher" voice commands \(learned per user\)\n'
content = re.sub(pattern, '', content, flags=re.DOTALL)

DOCS.write_text(content, encoding="utf-8")
