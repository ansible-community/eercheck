
`eercheck` is a command line tool to  test Ansible Community Execution Environment before release. It uses [podman-py](https://podman-py.readthedocs.io/en/latest/) to connect and work with the podman container image, and Python [unittest](https://docs.python.org/3/library/unittest.html) for testing the containers. There are two kinds of Ansible Execution Environments :

- Base Ansible Execution Environments

	- Fedora base image
	- ansible core
	- ansible collections : The following set of collections
		ansible.posix
		ansible.utils
		ansible.windows

- Minimal Ansible Execution Environments

	- Fedora base image
	- ansible core


This project is licensed under GPL-3.0-or-later.

## Usage

Activate the virtual environment in the working directory.

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

```

Activate the `podman` socket.

```
systemctl start podman.socket --user
```

Update `vars.json` with correct version numbers.Pick the correct versions of the Ansible Collections from the `.deps` file of the corresponding Ansible community  package release. For example for 9.4.0 the Collection versions can be found in [here](https://github.com/ansible-community/ansible-build-data/blob/main/9/ansible-9.4.0.deps). You can find the appropriate version of Ansible Community Package [here](https://pypi.org/project/ansible/).
The check needs to be carried out each time before the release of the Ansible Community Execution Environment.


Execute the program by giving the correct container image id.

```
./containertest.py image_id
```

