""" Packaging script for muse_usps."""
import shlex
import subprocess

import setuptools


def run(cmd):
    """ Simple helpter to run a shell command and get the output. """
    return subprocess.check_output(shlex.split(cmd)).decode('utf-8').strip()


setuptools.setup(name='muse_usps',
                 version=run('git describe --abbrev=0'),
                 description='USPS Address Verification',
                 install_requires=['lxml'],
                 packages=['muse_usps'])
