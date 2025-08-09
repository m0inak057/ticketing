"""
Configuration module for Cashfree API client with proper SSL verification
"""

import urllib3
import warnings
from cashfree_pg.api_client import Cashfree as CashfreeBase
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
        
        # Ensure SSL verification is enabled
        if hasattr(self.api_client, 'configuration'):
            self.api_client.configuration.verify_ssl = True
