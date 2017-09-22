""" Packaging script for muse_usps."""
import setuptools
setuptools.setup(name='muse_usps',
                 version='0.0.1',
                 description='USPS Address Verification',
                 install_requires=['lxml'],
                 packages=['muse_usps'])
