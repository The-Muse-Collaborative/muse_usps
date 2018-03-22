# muse\_usps
![License](https://img.shields.io/github/license/The-Muse-Collaborative/muse_usps.svg)
[![Build Status](https://travis-ci.org/The-Muse-Collaborative/muse_usps.svg)](https://travis-ci.org/The-Muse-Collaborative/muse_usps)
[![Coverage Status](https://coveralls.io/repos/The-Muse-Collaborative/muse_usps/badge.svg?branch=master&service=github)](https://coveralls.io/github/The-Muse-Collaborative/muse_usps?branch=master)

Simple python module providing a `muse_usps.validate` function which validates
addresses over the USPS web API.

## Documentation
[Documentation](https://The-Muse-Collaborative.github.io/muse_usps) is automatically
generated from the source code using Sphinx by Travis-CI and served by GitHub
pages.

## Installation
Simply clone the repository and run `python setup.py install`.

The tip version can be installed using `pip` with
`pip install -e git+git://github.com/jonesinator/muse_usps.git@master#egg=muse_usps`.
A specific version can be installed by replacing `master` with a tag name or
the the hash of the changeset that should be installed.

This package is not currently uploaded to PyPI, but we may do so in the future.

## Usage

Using the address validator is very simple.

```python
import muse_usps

validated = muse_usps.validate('API URL HERE',
                               'API USER ID HERE',
                               {'address_line_1': '1600 Pennsylvania Ave NW',
                                'address_line_2': '',
                                'city': 'Washington',
                                'state': 'DC',
                                'zip_code': '20500'})
```

All of the fields and keys shown are mandatory, but they are allowed to be
empty strings.  For instance, the zip code can be an empty string, and the USPS
API will fill it in automatically.

## Development
Clone the repository, install the needed python packages and pre-commit hooks,
then run the pre-commit hooks to make sure everything is sane before beginning
development. In order to run the unit tests, the USPS API URL and user ID must
be available in the environment variables `MUSE_USPS_API_URL` and
`MUSE_USPS_USER_ID` respectively.  These variables should exported in a file
named `test_env.sh` so that they are always available by running `make test`
and the pre-commit hooks.  The environment can be set up by copy-pasting the
following code and inserting the correct values for the API secrets.

```bash
git clone git@github.com:jonesinator/muse_usps.git
cd muse_usps
pip install -r requirements.txt
make hooks
cat << EOF >> test_env.sh
export MUSE_USPS_API_URL="API URL HERE"
export MUSE_USPS_USER_ID="USER ID HERE"
EOF
make pre-commit
```

The `Makefile` provides several useful targets. Use `make help` for a list.

Git tags are used to mark version numbers. The version numbers are extracted
from the latest git tag by the Python package and the Sphinx documentation.

## Travis-CI Configuration

For the Travis-CI tests the environment variables `MUSE_USPS_API_URL` and
`MUSE_USPS_USER_ID` are configured in the Travis-CI repository settings.
Additionally, the Travis-CI repository settings specify a
`COVERALLS_REPO_TOKEN` environment variable for uploading code coverage results
to coveralls.io.

To enable Travis-CI to automatically publish to GitHub Pages a deploy key was
added to this repository. The private key was encrypted
([instructions](https://docs.travis-ci.com/user/encrypting-files/)) and added
to the repository as `travis_github_deploy_key.enc`. The encryption keys were
added to the repository settings in Travis-CI as `encrypted_bfd322024369_key`
and `encrypted_bfd322024369_iv`.
