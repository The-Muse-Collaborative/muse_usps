""" Packaging script for muse_usps."""
import setuptools
setuptools.setup(name='muse_usps',
                 version='0.0.1',
                 description='USPS Address Verification',
                 install_requires=['lxml'],
                 setup_requires=['nose'],
                 tests_require=['coverage', 'pep8', 'pylint'],
                 packages=['muse_usps'],
                 test_suite='nose.collector')
