"""License validation and premium feature gating."""
import os
import hashlib
import hmac
from typing import Optional
from datetime import datetime


class LicenseManager:
    """Manage premium license validation and feature access."""
    
    # Secret key for license validation (in production, use env var)
    _SECRET_KEY = "nova_premium_secret_2026"
    
    @staticmethod
    def check_license() -> bool:
        """
        Check if a valid premium license exists.
        
        Looks for NOVA_LICENSE_KEY environment variable.
        
        Returns:
            True if valid license found, False otherwise
        """
        license_key = os.getenv('NOVA_LICENSE_KEY')
        
        if not license_key:
            return False
        
        return LicenseManager._validate_key(license_key)
    
    @staticmethod
    def _validate_key(key: str) -> bool:
        """
        Validate license key format and signature.
        
        Format: {user_id}:{timestamp}:{signature}
        
        Args:
            key: License key string
        
        Returns:
            True if valid, False otherwise
        """
        try:
            parts = key.split(':')
            if len(parts) != 3:
                return False
            
            user_id, timestamp, signature = parts
            
            # Recreate signature
            message = f"{user_id}:{timestamp}"
            expected_sig = hmac.new(
                LicenseManager._SECRET_KEY.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()[:16]
            
            return signature == expected_sig
        except Exception:
            return False
    
    @staticmethod
    def generate_license(user_id: str) -> str:
        """
        Generate a new license key.
        
        Args:
            user_id: Unique user identifier
        
        Returns:
            License key string
        """
        timestamp = str(int(datetime.now().timestamp()))
        message = f"{user_id}:{timestamp}"
        
        signature = hmac.new(
            LicenseManager._SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()[:16]
        
        return f"{user_id}:{timestamp}:{signature}"
    
    @staticmethod
    def get_upgrade_message() -> str:
        """
        Get friendly upgrade message for freemium users.
        
        Returns:
            Upgrade message string
        """
        return (
            "\n[yellow]⭐ Premium Feature[/yellow]\n\n"
            "This feature requires a Nova Premium license.\n\n"
            "Premium includes:\n"
            "  • Advanced SEO checks (broken links, sitemap validation)\n"
            "  • AI-powered fix suggestions\n"
            "  • HTML reports with visualizations\n"
            "  • Priority support\n\n"
            "Get your license at: https://github.com/GalaxyBuilt/nova\n"
            "Or contact: galaxy@txchyon.com\n"
        )
    
    @staticmethod
    def require_premium(feature_name: str = "This feature") -> bool:
        """
        Check premium license and show upgrade message if not found.
        
        Args:
            feature_name: Name of the premium feature
        
        Returns:
            True if premium license valid, False otherwise
        """
        if LicenseManager.check_license():
            return True
        
        from rich.console import Console
        console = Console()
        console.print(LicenseManager.get_upgrade_message())
        return False
