TOOL_REGISTRY = {
    "scalpel": {
        "yolo_class": "scalpel",
        "aliases": ["blade", "surgical blade", "the scalpel"],
    },
    "scissors": {
        "yolo_class": "scissors",
        "aliases": ["medical scissors", "surgical scissors", "the scissors"],
    },
    "forceps": {
        "yolo_class": "forceps",
        "aliases": ["surgical forceps", "tweezers", "clamps", "the forceps"],
    },
    "bandage": {
        "yolo_class": "bandage",
        "aliases": ["bandage cloth", "wrap", "dressing"],
    },
    "gauze": {
        "yolo_class": "gauze",
        "aliases": ["gauze pad", "gauze swab"],
    },
    "thermometer": {
        "yolo_class": "thermometer",
        "aliases": ["temp probe", "temperature tool"],
    },
    "oximeter": {
        "yolo_class": "oximeter",
        "aliases": ["oxymeter", "pulse ox", "spo2", "pulse oximeter"],
    },
    "plaster": {
        "yolo_class": "plaster",
        "aliases": ["bandaid", "band aid", "band-aid", "adhesive strip"],
    },
}

_ALIAS_TO_CANONICAL = {}
for canonical, entry in TOOL_REGISTRY.items():
    _ALIAS_TO_CANONICAL[canonical] = canonical
    for alias in entry["aliases"]:
        _ALIAS_TO_CANONICAL[alias.lower()] = canonical


def get_yolo_class(tool_name: str) -> str | None:
    entry = TOOL_REGISTRY.get(tool_name.lower())
    return entry["yolo_class"] if entry else None


def resolve_alias(name: str) -> str | None:
    return _ALIAS_TO_CANONICAL.get(name.lower())


def get_all_canonical_names() -> list[str]:
    return list(TOOL_REGISTRY.keys())


def is_valid_tool(name: str) -> bool:
    return name.lower() in _ALIAS_TO_CANONICAL
