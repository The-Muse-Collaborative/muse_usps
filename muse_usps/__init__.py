""" Provides muse_usps.validate function for validating addresses with the USPS
web API. """
import logging
import urllib.parse
import urllib.request

import lxml.etree


LOGGER = logging.getLogger(__name__)


def validate(api_url, user_id, address):
    """ Validates an address over the USPS API.

    :param api_url: The full http address of the USPS web API.
    :type api_url: string
    :param user_id: The API user ID assigned by USPS.
    :type user_id: string
    :param address: A dictionary containing the address to validate. Must
        contain the keys ``address_line_1``, ``address_line_2``, ``city``,
        ``state``, and ``zip_code`` all with string values. Some values may be
        empty strings and the USPS API will attempt to fill them in if
        possible.
    :type address: dictionary
    :returns: A dictionary containing the same fields as the ``address``
        parameter as validated by the USPS API.  If the USPS API returns extra
        fields, they will be returned in a ``usps_extra`` key on the return
        value containing a dictionary of the returned fields.
    :rtype: dictionary
    """
    LOGGER.debug('USPS validation request: %s', address)

    # Create the XML request.
    def add_child(parent_xml, name, value):
        """ Helper function to add an XML tag with text value. """
        lxml.etree.SubElement(parent_xml, name).text = value
    xml = lxml.etree.Element('AddressValidateRequest', USERID=user_id)
    address_xml = lxml.etree.SubElement(xml, 'Address', ID=str(0))
    add_child(address_xml, 'Address1', address['address_line_2'])
    add_child(address_xml, 'Address2', address['address_line_1'])
    add_child(address_xml, 'City', address['city'])
    add_child(address_xml, 'State', address['state'])
    add_child(address_xml, 'Zip5', address['zip_code'][:5])
    add_child(address_xml, 'Zip4', address['zip_code'][5:].replace('-', ''))
    params = urllib.parse.urlencode([('API', 'Verify'),
                                     ('XML', lxml.etree.tostring(xml))])
    url = '{0}?{1}'.format(api_url, params)

    # Issue the request.
    LOGGER.debug('Issuing request: %s', url)
    try:
        response = urllib.request.urlopen(url)
    except Exception as exc:
        LOGGER.error('Request failed: %s', exc)
        raise
    LOGGER.debug('Received response.')

    # The response is expected to be valid XML.
    try:
        response = lxml.etree.parse(response).getroot()
    except Exception as exc:
        LOGGER.error('Unable to parse response as XML: %s', exc)
        raise

    # For bad requests the USPS API adds an Error tag to the response.
    if response.tag == 'Error':
        error_description = response.find('Description').text
        LOGGER.error('USPS API responded with an error: %s',
                     error_description)
        raise RuntimeError(error_description)

    # For good requests with bad addresses, the USPS API addes an Error tag to
    # the Address tag.
    response = response.find('Address')
    error = response.find('Error')
    if error is not None:
        error_description = error.find('Description').text
        LOGGER.warning('USPS API responded with an address error: %s',
                       error_description)
        raise RuntimeError(error_description)

    # Translate the response into our address format.
    LOGGER.debug('Good response received.')
    usps_format = {c.tag: c.text for c in response.iterchildren()}
    validated = {}
    validated['address_line_1'] = usps_format.pop('Address2', '')
    validated['address_line_2'] = usps_format.pop('Address1', '')
    validated['city'] = usps_format.pop('City', '')
    validated['state'] = usps_format.pop('State', '')
    validated['zip_code'] = usps_format.pop('Zip5', '')
    zip4 = usps_format.pop('Zip4', '')
    if zip4:
        validated['zip_code'] += '-' + zip4
    validated['usps_extra'] = usps_format
    LOGGER.debug('Parsed response: %s', validated)
    return validated
