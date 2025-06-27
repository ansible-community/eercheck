import json

vars = {"ansible-core-version":"2.18.6", "fedora-version": ",42","ansible.posix": "1.6.2", "ansible.utils": "5.1.2", "ansible.windows": "2.8.0"}

with open("vars.json","w") as fobj:
    data = json.dumps(vars, indent=4)
    fobj.write(data)
