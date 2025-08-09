"""
Configuration module for Cashfree API client with proper SSL verification
"""

import urllib3
import warnings
from cashfree_pg.api_client import Cashfree as CashfreeBase, ApiClient
from cashfree_pg.configuration import Configuration

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CashfreeSafe(CashfreeBase):
    """
    Enhanced Cashfree client with proper SSL verification
    """
    def __init__(self, *args, **kwargs):
        # Initialize with parent class
        super().__init__(*args, **kwargs)
    
    def _get_api_client_with_ssl(self):
        """Get API client with SSL verification enabled"""
        api_client = ApiClient.get_default()
        
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
        return api_client
    
    def PGCreateOrder(self, x_api_version=None, create_order_request=None, x_request_id=None, x_idempotency_key=None, **kwargs):
        """Override PGCreateOrder to ensure SSL verification"""
        # Temporarily store the original method
        original_get_default = ApiClient.get_default
        
        # Replace with our SSL-enabled version
        ApiClient.get_default = lambda: self._get_api_client_with_ssl()
        
        try:
            # Call the parent method
            return super().PGCreateOrder(
                x_api_version=x_api_version,
                create_order_request=create_order_request,
                x_request_id=x_request_id,
                x_idempotency_key=x_idempotency_key,
                **kwargs
            )
        finally:
            # Restore the original method
            ApiClient.get_default = original_get_default
