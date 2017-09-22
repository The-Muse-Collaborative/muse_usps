# muse\_usps
[![Build Status](https://travis-ci.org/jonesinator/muse_usps.svg)](https://travis-ci.org/jonesinator/muse_usps)
![License](https://img.shields.io/github/license/jonesinator/muse_usps.svg)
[![Coverage Status](https://coveralls.io/repos/jonesinator/muse_usps/badge.svg?branch=master&service=github)](https://coveralls.io/github/jonesinator/muse_usps?branch=master)

Simple python module providing a `usps.validate` function which validates
addresses over the USPS web API.

## Documentation
[Documentation](https://jonesinator.github.io/muse_usps) is generated from the
souce code using `Sphinx` and served by GitHub pages.

## Installation
Simply clone the repository and run `python setup.py install`.

The tip version can be installed using `pip` with
`pip install -e git+git://github.com/jonesinator/muse_usps.git@master#egg=muse_usps`.
A specific version can be installed by replacing `master` with a tag name or
the the hash of the changeset that should be installed.

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

All of the fields shown are mandatory, but they are allowed to be empty strings.
For instance, the zip code can be an empty string, and the USPS API will fill
it in automatically.

## Development
Clone the repository, and install the pre-commit hooks that run the unit tests,
check for at least 95% code coverage, and lint the code.

Getting a development environment:
```
git clone git@github.com:jonesinator/muse_usps.git
cd muse_usps
make hooks
```

In order to run the unit tests, the USPS API URL and user ID must be available
in the environment variables `MUSE_USPS_API_URL` and `MUSE_USPS_USER_ID`
respectively. These variables should exported in a file named `test_env.sh` so
that they are always available by running `make test` and the pre-commit hooks.
The `test_env.sh` file can be created by copy-pasting the following command and
replacing the values.

```bash
cat << EOF >> test_env.sh
export MUSE_USPS_API_URL="API URL HERE"
export MUSE_USPS_API_URL="USER ID HERE"
EOF
```

For the Travis-CI tests these environment variables are configured in the
Travis-CI repository settings and are not in `travis.yml`. Additionally, the
Travis-CI settings.

The `Makefile` provides several useful targets. Use `make help` for a list.
