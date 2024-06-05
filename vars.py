import json

vars = {"ansible-core-version":"2.16.1", "fedora-version": "39","ansible.posix": "1.5.4", "ansible.utils": "2.11.0", "ansible.windows": "2.1.0"}

with open("vars.json","w") as fobj:
    data = json.dumps(vars, indent=4)
    fobj.write(data)
