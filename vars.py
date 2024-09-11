import json

vars = {"ansible-core-version":"2.17.4", "fedora-version": ",40","ansible.posix": "1.5.4", "ansible.utils": "4.1.0", "ansible.windows": "2.5.0"}

with open("vars.json","w") as fobj:
    data = json.dumps(vars, indent=4)
    fobj.write(data)
