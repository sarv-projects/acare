from __future__ import annotations

import re
import subprocess
import sys
import time


EXPECTED_NODES = {
    "/voice_node",
    "/dialogue_node",
    "/auth_node",
    "/state_manager",
    "/planner_node",
    "/embedded_interface_node",
    "/vision_node",
    "/safety_node",
    "/log_node",
    "/admin_node",
}

EXPECTED_TOPICS = {
    "/raw_transcript",
    "/auth_request",
    "/intent_result",
    "/auth_result",
    "/validated_intent",
    "/vision_search_request",
    "/vision_result",
    "/vision_status",
    "/arm_command",
    "/gripper_command",
    "/motion_feedback",
    "/hand_status",
    "/tts_request",
    "/safety_alert",
    "/emergency_stop",
}

FORBIDDEN_ENDPOINTS = {
    "/raw_transcript": {"/voice_node": "subscriber"},
    "/auth_request": {"/auth_node": "publisher"},
    "/validated_intent": {"/planner_node": "publisher"},
    "/vision_status": {"/planner_node": "publisher"},
}


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def wait_for_nodes(timeout_s: float = 30.0) -> set[str]:
    deadline = time.monotonic() + timeout_s
    seen: set[str] = set()
    while time.monotonic() < deadline:
        output = run(["ros2", "node", "list"])
        seen = {line.strip() for line in output.splitlines() if line.strip()}
        if EXPECTED_NODES.issubset(seen):
            return seen
        time.sleep(1.0)
    return seen


def get_topics() -> set[str]:
    output = run(["ros2", "topic", "list"])
    return {line.strip() for line in output.splitlines() if line.strip()}


def topic_info(topic: str) -> str:
    return run(["ros2", "topic", "info", "-v", topic])


def parse_endpoints(info_text: str) -> dict[str, set[str]]:
    endpoints = {"publisher": set(), "subscriber": set()}
    current = None
    for raw_line in info_text.splitlines():
        line = raw_line.strip()
        if line.startswith("Publisher count"):
            current = "publisher"
        elif line.startswith("Subscription count"):
            current = "subscriber"
        elif line.startswith("Node name:") and current:
            node = line.split(":", 1)[1].strip()
            endpoints[current].add(node)
    return endpoints


def main() -> int:
    try:
        nodes = wait_for_nodes()
    except Exception as exc:
        print(f"FAILED: ros2 node list did not run: {exc}")
        return 2

    missing_nodes = sorted(EXPECTED_NODES - nodes)
    if missing_nodes:
        print("FAILED: missing nodes")
        for node in missing_nodes:
            print(f"  {node}")
        return 1

    topics = get_topics()
    missing_topics = sorted(EXPECTED_TOPICS - topics)
    if missing_topics:
        print("FAILED: missing topics")
        for topic in missing_topics:
            print(f"  {topic}")
        return 1

    loopback_errors: list[str] = []
    for topic, rules in FORBIDDEN_ENDPOINTS.items():
        info = parse_endpoints(topic_info(topic))
        for node_name, endpoint_type in rules.items():
            if node_name in info.get(endpoint_type, set()):
                loopback_errors.append(
                    f"{node_name} unexpectedly appears as {endpoint_type} on {topic}"
                )

    if loopback_errors:
        print("FAILED: forbidden topic loopbacks")
        for item in loopback_errors:
            print(f"  {item}")
        return 1

    print("ROS graph validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
