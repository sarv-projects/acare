"""Check raw depth values from HP60C"""
import sys, os, time
sys.path.insert(0, os.path.expanduser('~/acare_ws/install/lib/python3.12/site-packages'))
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np

class DepthCheck(Node):
    def __init__(self):
        super().__init__('depth_check')
        self._done = False
        self.create_subscription(Image, '/ascamera_hp60c/camera_publisher/depth0/image_raw', self._cb, 1)

    def _cb(self, msg):
        if self._done:
            return
        self._done = True
        print(f'Encoding: {msg.encoding}  Size: {msg.width}x{msg.height}  step={msg.step}')
        arr = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width)
        centre = arr[msg.height//2, msg.width//2]
        nonzero = arr[arr > 0]
        print(f'Centre pixel depth: {centre} mm')
        print(f'Non-zero pixels: {len(nonzero)} / {arr.size}')
        if len(nonzero) > 0:
            print(f'Depth range: {nonzero.min()}mm - {nonzero.max()}mm')
            print(f'Median depth: {np.median(nonzero):.0f}mm')
        else:
            print('ALL DEPTH VALUES ARE ZERO - depth stream may not be active')

rclpy.init()
node = DepthCheck()
t0 = time.time()
while not node._done and (time.time()-t0) < 10:
    rclpy.spin_once(node, timeout_sec=0.5)
if not node._done:
    print('No depth frame received')
node.destroy_node()
rclpy.shutdown()
