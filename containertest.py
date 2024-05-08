#!/usr/bin/env python

from podman import PodmanClient
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Please provide the image id to test.")
        sys.exit(-1)
    image_id = sys.argv[1]
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

        image = client.images.get(image_id)
        if image.tags[0].find('minimal') != -1:
            type_of_image = 'minimal'
        else:
            type_of_image = 'base'
        print(f"Starting container image {image.tags[0]}.")
        container = client.containers.run(
            image,
            "/usr/bin/bash",
            name="testrun",
            detach=True,
            tty=True,
            mounts=volume,
            remove=True,
            environment={"IMAGENAME": type_of_image},
        )
        code, output = container.exec_run("/usr/bin/python3 /runner/alltests.py")
        print(output.decode("utf-8", errors="ignore"))
        return code



if __name__ == "__main__":
    code = main()
    sys.exit(code)

