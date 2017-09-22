# muse\_usps
[![Build Status](https://travis-ci.org/jonesinator/muse_usps.svg)](https://travis-ci.org/jonesinator/muse_usps)
![License](https://img.shields.io/github/license/jonesinator/muse_usps.svg)
[![Coverage Status](https://coveralls.io/repos/jonesinator/muse_usps/badge.svg?branch=master&service=github)](https://coveralls.io/github/jonesinator/muse_usps?branch=master)
Simple python module providing `usps.validate` function which validates
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

```
import muse_usps

validated = muse_usps.validate('API URL HERE',
                               'API USER ID HERE',
                               {'address_line_1': '1600 Pennsylvania Ave NW',
                                'address_line_2': '',
                                'city': 'Washington',
                                'state': 'DC',
                                'zip_code': '20500'})
```

## Development
Clone the repository, and install the pre-commit hooks that run the unit tests,
check for at least 95% code coverage, and lint the code.

Getting a development environment:
```
git clone git@github.com:jonesinator/muse_usps.git
cd muse_usps
make hooks
make test
```

The `Makefile` provides several useful targets.
* `lint` -- Runs the linter on all python code.
* `test` -- Runs the unit tests.
