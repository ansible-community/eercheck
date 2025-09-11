#!/usr/bin/env python3

import unittest
import os
import subprocess
import json
import sys

with open("/runner/vars.json", "r") as fobj:
    data = json.load(fobj)


def system(cmd):
    """
    Invoke a shell command.

    :returns: A tuple of output, err message, and return code
    """
    ret = subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    out, err = ret.communicate()
    return out, err, ret.returncode


class eertest(unittest.TestCase):
    def test_bash(self):
        """Tests the bash version as the same of upstream"""
        out, err, eid = system("bash --version")
        out = out.decode("utf-8")
        self.assertIn("-redhat-linux-gnu", out, out)

    def test_version(self):
        """Tests the fedora version as the same of upstream"""
        out, err, eid = system("cat /etc/os-release")
        out = out.decode("utf-8")
        self.assertIn(f"VERSION_ID={data['fedora-version']}", out)

    def test_ansible_version(self):
        """Tests the bash version as the same of upstream"""
        out, err, eid = system("ansible --version")
        out = out.decode("utf-8")
        self.assertIn(f"ansible [core {data['ansible-core-version']}", out)

    def test_collection_version(self):
        """Tests the coleections version as the same of upstream"""
        out, err, eid = system("ansible-galaxy collection list --format json")
        out = out.decode("utf-8")
        out_dict = json.loads(out)
        if os.environ.get("IMAGENAME") == "base":
            self.assertIn(data['ansible.posix'], out_dict["/usr/share/ansible/collections/ansible_collections"]["ansible.posix"]["version"])
            self.assertIn(data['ansible.utils'], out_dict["/usr/share/ansible/collections/ansible_collections"]["ansible.utils"]["version"])
            self.assertIn(data['ansible.windows'], out_dict["/usr/share/ansible/collections/ansible_collections"]["ansible.windows"]["version"])
        else:
            self.assertEqual(1, len(out_dict.keys()))
            self.assertTrue("/usr/local/lib/python3.13/site-packages/ansible/_internal/ansible_collections" in out_dict )


if __name__ == "__main__":
    status_code = unittest.main()
    sys.exit(status_code)

# get all test variables reading the test input file
# write the collection test apt both for base and minimal
# the idea is to have an input file where we can get all the values of variables from
