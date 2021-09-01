import os
import json

from .hw import Timer
from .proggen import ProgramGen
from .constants import MASTER_TIMER

root = os.path.abspath(os.path.split(__file__)[0])

with open(root + os.path.sep + "pin_mapping.json", 'r') as f:
    pin_mapping = json.load(f)

with open(root + os.path.sep + "hw_desc.json", "r") as f:
    hw_desc = json.load(f)

master_timer = Timer(hw_desc=hw_desc[MASTER_TIMER],
                     name=MASTER_TIMER)
