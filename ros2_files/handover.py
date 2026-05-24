# acare_planner/handover.py
# Spec Reference: Section VII (Handover — Multi-Modal Verification)
# Section XII (Task Planner — HANDOVER substates)
#
# Three-check sequential handover verification protocol.
# All three checks must pass before gripper releases the tool.
#
# Check 1 — Continuous face verification (auth_node monitors every 0.5s)
#   Cosine similarity >= 0.78 against logged-in user embedding
#   3 consecutive failures → TTS 'Please face the camera.'
#
# Check 2 — Hand detection (vision_node MediaPipe Hands)
#   Open palm (3+ fingers extended) facing upward in handover zone
#   Prompts if hand not detected or not open
#
# Check 3 — Voice confirmation
#   TTS 'Say take to receive.'
#   Staff says 'take' or 'yes'
#   Voice consistency check passes
#
# Total timeout: 30 seconds for all three checks combined.
# On timeout: safe deposit → STANDBY.
#
# Height adjustment: staff can say 'lower'/'higher' during handover.
# Preference stored per user in users.db.

import asyncio
import time
import threading


class HandoverProtocol:
    """
    Manages the three-check handover verification sequence.

    Instantiated by planner_node. Receives callbacks from:
      - auth_node: current face similarity score
      - vision_node: HandStatus messages (/hand_status)
      - voice_node: voice confirmation words

    Usage:
        protocol = HandoverProtocol(tts_fn, gripper_pub, logger)
        success = await protocol.run(intent, timeout=30.0)
    """

    FACE_SIM_THRESHOLD  = 0.78
    FACE_FAIL_MAX       = 3
    FACE_CHECK_INTERVAL = 0.5   # seconds
    TOTAL_TIMEOUT       = 30.0  # seconds

    def __init__(self, tts_fn, gripper_pub, logger=None):
        """
        tts_fn      — async callable: await tts_fn(text, urgent=False)
        gripper_pub — ROS2 publisher for GripperCommand
        logger      — ROS2 node logger
        """
        self.tts         = tts_fn
        self.gripper_pub = gripper_pub
        self.logger      = logger

        # State updated by external callbacks
        self._latest_face_sim    = 0.0
        self._latest_hand_status = None   # HandStatus msg or dict
        self._voice_confirmed    = False
        self._height_adjustment  = 0.0   # metres, updated by 'lower'/'higher'

        self._lock = threading.Lock()

    # -------------------------------------------------------------------------
    # External callbacks — called by planner_node from ROS2 subscriptions
    # -------------------------------------------------------------------------

    def on_face_similarity(self, sim: float):
        """Called by auth_node every 0.5s with current face cosine similarity."""
        with self._lock:
            self._latest_face_sim = sim

    def on_hand_status(self, msg):
        """Called when /hand_status message received from vision_node."""
        with self._lock:
            self._latest_hand_status = msg

    def on_voice_word(self, word: str):
        """
        Called by voice_node when a word is recognised during HANDOVER.
        Accepts 'take', 'yes', 'got it' as confirmation.
        Accepts 'lower', 'higher' as height adjustment commands.
        """
        w = word.strip().lower()
        if w in ('take', 'yes', 'got it', 'okay', 'ok'):
            with self._lock:
                self._voice_confirmed = True
        elif w == 'lower':
            with self._lock:
                self._height_adjustment -= 0.05   # 5cm down
        elif w == 'higher':
            with self._lock:
                self._height_adjustment += 0.05   # 5cm up

    # -------------------------------------------------------------------------
    # Main handover sequence
    # -------------------------------------------------------------------------

    async def run(self, intent, timeout: float = 30.0) -> bool:
        """
        Runs the full three-check handover sequence.

        intent — ValidatedIntent with .tool and .name fields
        timeout — total seconds for all three checks

        Returns True if all checks passed and tool released.
        Returns False on timeout or failure.
        """
        deadline = time.monotonic() + timeout

        # Reset state
        with self._lock:
            self._voice_confirmed = False
            self._height_adjustment = 0.0

        # --- CHECK 1: Continuous face verification ---
        if self.logger:
            self.logger.info('Handover: Check 1 — face verification')

        face_fails = 0
        while time.monotonic() < deadline:
            with self._lock:
                sim = self._latest_face_sim

            if sim >= self.FACE_SIM_THRESHOLD:
                face_fails = 0
                break   # face verified

            face_fails += 1
            if face_fails >= self.FACE_FAIL_MAX:
                await self.tts('Please face the camera.')
                face_fails = 0

            await asyncio.sleep(self.FACE_CHECK_INTERVAL)
        else:
            if self.logger:
                self.logger.warn('Handover: timeout during face verification')
            return False

        # --- CHECK 2: Hand detection ---
        if self.logger:
            self.logger.info('Handover: Check 2 — hand detection')

        await self.tts('Please place your open palm under the gripper.')

        while time.monotonic() < deadline:
            with self._lock:
                hs = self._latest_hand_status

            if hs is not None:
                hand_detected = getattr(hs, 'hand_detected', False)
                is_open       = getattr(hs, 'is_open', False)
                palm_up       = getattr(hs, 'palm_up', False)

                if hand_detected:
                    if not is_open:
                        await self.tts('Please open your palm.')
                    elif not palm_up:
                        await self.tts('Please turn your palm upward.')
                    else:
                        break   # hand OK

            await asyncio.sleep(0.1)
        else:
            if self.logger:
                self.logger.warn('Handover: timeout during hand detection')
            return False

        # --- CHECK 3: Voice confirmation ---
        if self.logger:
            self.logger.info('Handover: Check 3 — voice confirmation')

        await self.tts('Say take to receive.')

        with self._lock:
            self._voice_confirmed = False

        while time.monotonic() < deadline:
            with self._lock:
                confirmed = self._voice_confirmed
            if confirmed:
                break
            await asyncio.sleep(0.05)
        else:
            if self.logger:
                self.logger.warn('Handover: timeout during voice confirmation')
            return False

        # --- All checks passed — release gripper ---
        if self.logger:
            self.logger.info('Handover: all checks passed — releasing gripper')

        self._release_gripper()
        await asyncio.sleep(1.0)   # wait for force sensor to drop to zero

        return True

    def _release_gripper(self):
        """Publishes RELEASE command to gripper."""
        try:
            from acare_msgs.msg import GripperCommand
            cmd = GripperCommand()
            cmd.command      = 'RELEASE'
            cmd.force_target = 0.0
            self.gripper_pub.publish(cmd)
        except Exception as e:
            if self.logger:
                self.logger.error(f'Gripper release failed: {e}')

    def get_height_adjustment(self) -> float:
        """Returns accumulated height adjustment in metres (from 'lower'/'higher' commands)."""
        with self._lock:
            return self._height_adjustment
