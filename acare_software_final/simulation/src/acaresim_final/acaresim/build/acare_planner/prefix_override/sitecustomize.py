import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/acare_planner'
