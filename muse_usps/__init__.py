""" Provides muse_usps.validate function for validating addresses with the USPS
web API. """
import urllib.parse
import urllib.request

import lxml.etree


def validate(api_url, user_id, address):
    """ Validates an address over the USPS API. """

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

    # Issue the request and deal with any errors.
    response = urllib.request.urlopen(url)
    response_xml = lxml.etree.parse(response).getroot()
    if response_xml.tag == 'Error':
        raise RuntimeError(response_xml.find('Description').text)
    response_address_xml = response_xml.find('Address')
    error = response_address_xml.find('Error')
    if error is not None:
        raise RuntimeError(error.find('Description').text)

    # Translate the response into our address format.
    usps_format = {c.tag: c.text for c in response_address_xml.iterchildren()}
    validated = {}
    validated['address_line_1'] = usps_format.pop('Address2', '')
    validated['address_line_2'] = usps_format.pop('Address1', '')
    validated['city'] = usps_format.pop('City', '')
    validated['state'] = usps_format.pop('State', '')
    validated['zip_code'] = '{0}-{1}'.format(usps_format.pop('Zip5', ''),
                                             usps_format.pop('Zip4', ''))
    validated['usps_extra'] = usps_format
    return validated
