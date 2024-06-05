import sys
import json
from podman import PodmanClient
import podman
import unittest
import re
import os

uri = "unix:///run/user/1000/podman/podman.sock"
volume = [{"type": "bind", "source": "/home/adas/code/redhat/eercheck/alltests.py" ,"target": "/runner/alltests.py", "relabel": "Z"}, {"type": "bind", "source": "/home/adas/code/redhat/eercheck/vars.json" ,"target": "/runner/vars.json", "relabel": "Z"}]

with PodmanClient(base_url=uri) as client:
    image = client.images.get(sys.argv[1])
print(image)
