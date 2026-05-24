# acare_planner/tool_registry.py
# Spec Reference: Section XII (Task Planner — Tool Registry)
#
# Maps canonical tool names and aliases to YOLO model class names.
# Used by planner_node to translate intent parser output → vision search class.
#
# Tool classes match the trained model (6 classes):
#   cream, medical scissors, oxymeter, plaster, surgical forceps, thermometer
#
# Canonical names (used by intent parser and normaliser):
#   cream, scissors, oximeter, plaster, forceps, thermometer

# Registry: canonical_name → {yolo_class, aliases}
TOOL_REGISTRY = {
    'cream': {
        'yolo_class': 'cream',
        'aliases': ['lotion', 'ointment', 'topical', 'cream tube'],
    },
    'scissors': {
        'yolo_class': 'medical scissors',
        'aliases': ['medical scissors', 'surgical scissors', 'the smaller one',
                    'cutting tool', 'the scissors'],
    },
    'oximeter': {
        'yolo_class': 'oxymeter',
        'aliases': ['oxymeter', 'pulse ox', 'spo2', 'sp02',
                    'oxygen monitor', 'pulse oximeter'],
    },
    'plaster': {
        'yolo_class': 'plaster',
        'aliases': ['bandaid', 'band aid', 'band-aid', 'strip',
                    'adhesive strip', 'the plaster'],
    },
    'forceps': {
        'yolo_class': 'surgical forceps',
        'aliases': ['surgical forceps', 'tweezers', 'clamps',
                    'graspers', 'the forceps'],
    },
    'thermometer': {
        'yolo_class': 'thermometer',
        'aliases': ['temp probe', 'temperature tool', 'temperature',
                    'the thermometer'],
    },
}

# Flat alias → canonical name lookup (built from registry)
_ALIAS_TO_CANONICAL = {}
for _canonical, _entry in TOOL_REGISTRY.items():
    _ALIAS_TO_CANONICAL[_canonical] = _canonical
    for _alias in _entry['aliases']:
        _ALIAS_TO_CANONICAL[_alias.lower()] = _canonical


def get_yolo_class(tool_name: str) -> str | None:
    """
    Returns the YOLO model class name for a canonical tool name.
    Returns None if tool not found.

    Example: get_yolo_class('oximeter') → 'oxymeter'
    """
    entry = TOOL_REGISTRY.get(tool_name.lower())
    return entry['yolo_class'] if entry else None


def resolve_alias(name: str) -> str | None:
    """
    Resolves any tool name or alias to its canonical name.
    Returns None if not recognised.

    Example: resolve_alias('pulse ox') → 'oximeter'
    Example: resolve_alias('surgical forceps') → 'forceps'
    """
    return _ALIAS_TO_CANONICAL.get(name.lower())


def get_all_canonical_names() -> list:
    """Returns list of all canonical tool names."""
    return list(TOOL_REGISTRY.keys())


def get_all_yolo_classes() -> list:
    """Returns list of all YOLO model class names."""
    return [entry['yolo_class'] for entry in TOOL_REGISTRY.values()]


def is_valid_tool(name: str) -> bool:
    """Returns True if name is a canonical tool name or known alias."""
    return name.lower() in _ALIAS_TO_CANONICAL


if __name__ == '__main__':
    print('tool_registry.py smoke test:')
    tests = [
        ('oximeter',         'oxymeter'),
        ('forceps',          'surgical forceps'),
        ('scissors',         'medical scissors'),
        ('pulse ox',         'oximeter'),
        ('surgical forceps', 'forceps'),
        ('unknown_tool',     None),
    ]
    all_pass = True
    for name, expected in tests:
        if expected in TOOL_REGISTRY:
            result = get_yolo_class(resolve_alias(name))
        elif expected is None:
            result = resolve_alias(name)
        else:
            result = resolve_alias(name)
        ok = result == expected
        if not ok:
            all_pass = False
        print(f'  [{"PASS" if ok else "FAIL"}] {name!r} → {result!r} (expected {expected!r})')
    print('All tests passed.' if all_pass else 'SOME TESTS FAILED.')
