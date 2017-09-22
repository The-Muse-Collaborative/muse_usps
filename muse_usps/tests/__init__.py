""" Unitests that test the muse_usps address validation function. """
import copy
import os
import urllib.error

import lxml.etree
import muse_usps
import nose.tools


# Extract API secrets from the environment.
API_URL = os.environ['MUSE_USPS_API_URL']
USER_ID = os.environ['MUSE_USPS_USER_ID']

# An address used in many tests below. It's the White House!
TEST_ADDRESS = {'address_line_1': '1600 Pennsylvania Ave NW',
                'address_line_2': '',
                'city': 'Washington',
                'state': 'DC',
                'zip_code': '20500'}


@nose.tools.raises(ValueError)
def test_malformed_api_url():
    """ A malformed URL results in a ValueError. """
    muse_usps.validate('bogus', USER_ID, TEST_ADDRESS)


@nose.tools.raises(urllib.error.URLError)
def test_api_url_bad_domain():
    """ A URL for a non-existent domain gives a URLError. """
    muse_usps.validate('http://pqxcbnmpq.com', USER_ID, TEST_ADDRESS)


@nose.tools.raises(urllib.error.HTTPError)
def test_non_existent_api_url_page():
    """ A URL for a real domain, but a bad page is an HTTPError. """
    muse_usps.validate('http://cnn.com/foobar', USER_ID, TEST_ADDRESS)


@nose.tools.raises(lxml.etree.XMLSyntaxError)
def test_non_xml_response():
    """ A URL for a real address that isn't the API and returns HTML will give
    an XML parsing error. """
    muse_usps.validate('https://yahoo.com', USER_ID, TEST_ADDRESS)


@nose.tools.raises(RuntimeError)
def test_empty_user_id():
    """ An empty user ID gives a RuntimeError. """
    muse_usps.validate(API_URL, '', TEST_ADDRESS)


@nose.tools.raises(RuntimeError)
def test_bad_user_id():
    """ An bad user ID gives a RuntimeError. """
    muse_usps.validate(API_URL, 'baduserid', TEST_ADDRESS)


@nose.tools.raises(KeyError)
def test_missing_required_key():
    """ A required input key totally missing will result in a KeyError. """
    address = copy.deepcopy(TEST_ADDRESS)
    del address['address_line_1']
    muse_usps.validate(API_URL, USER_ID, address)


@nose.tools.raises(RuntimeError)
def test_empty_required_key():
    """ A required input key being blank will result in a RuntimeError. """
    address = copy.deepcopy(TEST_ADDRESS)
    address['address_line_1'] = ''
    muse_usps.validate(API_URL, USER_ID, address)


@nose.tools.raises(RuntimeError)
def test_invalid_address():
    """ A well-formed but invalid input will result in a RuntimeError. """
    address = {'address_line_1': '1234 FOOBAR ST',
               'address_line_2': 'APT BAZ',
               'city': 'Washington',
               'state': 'DC',
               'zip_code': '20500'}
    muse_usps.validate(API_URL, USER_ID, address)


def test_missing_address_line_2():
    """ An address that has a blank line 2, but the USPS thinks should have a
    line 2 will receive extra output fields. """
    expected = {'address_line_1': '1600 PENNSYLVANIA AVE NW',
                'address_line_2': '',
                'city': 'WASHINGTON',
                'state': 'DC',
                'zip_code': '20500-0003',
                'usps_extra': {
                    'ReturnText': 'Default address: The address you entered ' +
                                  'was found but more information is needed ' +
                                  '(such as an apartment, suite, or box ' +
                                  'number) to match to a specific address.'}}
    actual = muse_usps.validate(API_URL, USER_ID, TEST_ADDRESS)
    assert actual == expected
