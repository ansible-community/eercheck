from podman import PodmanClient
import os

uri = "unix:///run/user/1000/podman/podman.sock"
dir_name = os.path.dirname(os.path.realpath(__file__))

volume = [
    {
        "type": "bind",
        "source": f"{dir_name}/alltests.py",
        "target": "/runner/alltests.py",
        "relabel": "Z",
    },
    {
        "type": "bind",
        "source": f"{dir_name}/vars.json",
        "target": "/runner/vars.json",
        "relabel": "Z",
    },
]

with PodmanClient(base_url=uri) as client:
    # find if any container exists  then delete
    containers = client.containers.list(all=True, filters={"name": "testrun"})
    if len(containers) == 1:
        print("Found running conatainer, stopping and removing it.")
        c = containers[0]
        c.stop(ignore=True, timeout=1)
        c.remove()

    image = client.images.get("2cf8285eaa56")
    container = client.containers.run(
        image,
        "/usr/bin/bash",
        name="testrun",
        detach=True,
        tty=True,
        mounts=volume,
        remove=True,
        environment={"IMAGENAME": "base"},
    )
    code, output = container.exec_run("/usr/bin/python3 /runner/alltests.py")

    print(output.decode("utf-8", errors="ignore"))
