"""
Configuration module for Cashfree API client with proper SSL verification
"""

import urllib3
import warnings
from cashfree_pg.api_client import Cashfree as CashfreeBase, ApiClient
from cashfree_pg.configuration import Configuration
from cashfree_pg.exceptions import ApiTypeError

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CashfreeSafe(CashfreeBase):
    """
    Enhanced Cashfree client with proper SSL verification
    """
    def __init__(self, *args, **kwargs):
        # Initialize with parent class
        super().__init__(*args, **kwargs)
    
    def PGCreateOrder(self, x_api_version=None, create_order_request=None, x_request_id=None, x_idempotency_key=None, **kwargs):
        """Override PGCreateOrder to ensure SSL verification"""
        
        # Create API client directly
        api_client = ApiClient()
        
        # Set up host based on environment
        host = "https://api.cashfree.com/pg"
        if self.XEnvironment == self.SANDBOX:
            host = "https://sandbox.cashfree.com/pg"
        
        configuration = Configuration(host=host)
        configuration.api_key['XClientID'] = self.XClientId
        configuration.api_key['XClientSecret'] = self.XClientSecret
        configuration.api_key['XClientSignature'] = self.XClientSignature
        configuration.api_key['XPartnerMerchantId'] = self.XPartnerMerchantId
        configuration.api_key['XPartnerKey'] = self.XPartnerKey
        
        # Ensure SSL verification is enabled
        configuration.verify_ssl = True
        
        api_client.configuration = configuration
        
        # Replicate the exact logic from the original PGCreateOrder method
        _params = locals()
        
        _all_params = [
            'x_api_version',
            'create_order_request',
            'x_request_id',
            'x_idempotency_key'
        ]
        _all_params.extend([
            'async_req',
            '_return_http_data_only',
            '_preload_content',
            '_request_timeout',
            '_request_auth',
            '_content_type',
            '_headers'
        ])

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method PGCreateOrder" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        if x_request_id:
            _header_params["x-request-id"] = x_request_id

        if x_api_version:
            _header_params["x-api-version"] = x_api_version

        if x_idempotency_key:
            _header_params["x-idempotency-key"] = x_idempotency_key
        _header_params["x-sdk-platform"] = "pythonsdk-4.3.10"

        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['create_order_request'] is not None:
            _body_params = _params['create_order_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['XPartnerAPIKey', 'XClientSecret', 'XPartnerMerchantID', 'XClientID', 'XClientSignatureHeader']  # noqa: E501

        _response_types_map = {
            '200': "OrderEntity",
            '400': "BadRequestError",
            '401': "AuthenticationError",
            '404': "ApiError404",
            '409': "ApiError409",
            '422': "IdempotencyError",
            '429': "RateLimitError",
            '500': "ApiError",
        }

        return api_client.call_api(
            '/orders', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
