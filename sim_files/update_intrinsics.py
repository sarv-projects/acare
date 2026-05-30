import yaml
path = '/home/acare/acare_ws/src/acare_bringup/config/system.yaml'
with open(path) as f:
    cfg = yaml.safe_load(f)
cfg['camera']['fx'] = 572.04
cfg['camera']['fy'] = 571.49
cfg['camera']['cx'] = 329.27
cfg['camera']['cy'] = 242.09
with open(path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False)
print('system.yaml updated with real HP60C intrinsics')
print(f"  fx={cfg['camera']['fx']} fy={cfg['camera']['fy']} cx={cfg['camera']['cx']} cy={cfg['camera']['cy']}")
