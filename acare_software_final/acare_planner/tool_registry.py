# acare_planner/tool_registry.py
# Spec Reference: Section XII (Tool Registry — Alias Handling)
#
# Maps canonical tool names (what users say) to YOLO model class names
# (what the detector outputs). The trained YOLO26 model has 6 classes:
#
#   Model class name     | Canonical name | What users say
#   ---------------------|----------------|---------------------------
#   cream                | cream          | cream, lotion, ointment, topical
#   medical scissors     | scissors       | scissors, cutting tool, snips
#   oxymeter             | oximeter       | oximeter, pulse ox, spo2
#   plaster              | plaster        | plaster, bandaid, adhesive strip
#   surgical forceps     | forceps        | forceps, tweezers, clamps, graspers
#   thermometer          | thermometer    | thermometer, temp probe
#
# The canonical name is what flows through the pipeline (intent → planner → TTS).
# The yolo_class is what vision_node uses to filter YOLO detections.

TOOL_REGISTRY = {
    "cream": {
        "yolo_class": "cream",
        "aliases": ["lotion", "ointment", "topical", "the cream", "tube"],
    },
    "scissors": {
        "yolo_class": "medical scissors",
        "aliases": ["medical scissors", "surgical scissors", "the scissors",
                    "cutting tool", "snips"],
    },
    "forceps": {
        "yolo_class": "surgical forceps",
        "aliases": ["surgical forceps", "tweezers", "clamps", "graspers",
                    "the forceps", "grabber"],
    },
    "thermometer": {
        "yolo_class": "thermometer",
        "aliases": ["temp probe", "temperature tool", "the thermometer"],
    },
    "oximeter": {
        "yolo_class": "oxymeter",
        "aliases": ["oxymeter", "pulse ox", "spo2", "pulse oximeter",
                    "oxygen meter", "the oximeter"],
    },
    "plaster": {
        "yolo_class": "plaster",
        "aliases": ["bandaid", "band aid", "band-aid", "adhesive strip",
                    "the plaster", "strip"],
    },
}

# Build reverse lookup: alias → canonical name
_ALIAS_TO_CANONICAL = {}
for canonical, entry in TOOL_REGISTRY.items():
    _ALIAS_TO_CANONICAL[canonical] = canonical
    for alias in entry["aliases"]:
        _ALIAS_TO_CANONICAL[alias.lower()] = canonical

# Build YOLO class → canonical lookup (for vision_node result mapping)
_YOLO_CLASS_TO_CANONICAL = {}
for canonical, entry in TOOL_REGISTRY.items():
    _YOLO_CLASS_TO_CANONICAL[entry["yolo_class"].lower()] = canonical


def get_yolo_class(tool_name: str) -> str | None:
    """Canonical name → YOLO model class name."""
    entry = TOOL_REGISTRY.get(tool_name.lower())
    return entry["yolo_class"] if entry else None


def yolo_class_to_canonical(yolo_class: str) -> str | None:
    """YOLO model class name → canonical name."""
    return _YOLO_CLASS_TO_CANONICAL.get(yolo_class.lower())


def resolve_alias(name: str) -> str | None:
    """Any alias or canonical name → canonical name."""
    return _ALIAS_TO_CANONICAL.get(name.lower())


def get_all_canonical_names() -> list[str]:
    """Returns all 6 canonical tool names."""
    return list(TOOL_REGISTRY.keys())


def get_all_yolo_classes() -> list[str]:
    """Returns all 6 YOLO model class names."""
    return [entry["yolo_class"] for entry in TOOL_REGISTRY.values()]


def is_valid_tool(name: str) -> bool:
    """Returns True if name is a canonical tool name or a known alias."""
    return name.lower() in _ALIAS_TO_CANONICAL
