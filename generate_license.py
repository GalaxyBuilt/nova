"""Utility script to generate Nova premium license keys."""
import sys
from nova_premium.license_manager import LicenseManager


def main():
    """Generate a license key for a user."""
    if len(sys.argv) < 2:
        print("Usage: python generate_license.py <user_id>")
        print("\nExample:")
        print("  python generate_license.py user@example.com")
        print("  python generate_license.py github_username")
        sys.exit(1)
    
    user_id = sys.argv[1]
    license_key = LicenseManager.generate_license(user_id)
    
    print(f"\n✓ License key generated for: {user_id}")
    print(f"\nLicense Key:")
    print(f"  {license_key}")
    print(f"\nTo use this license:")
    print(f"  export NOVA_LICENSE_KEY='{license_key}'")
    print(f"  # Or on Windows:")
    print(f"  set NOVA_LICENSE_KEY={license_key}")
    print(f"\nThen run:")
    print(f"  nova scan <project> --premium")
    print()


if __name__ == '__main__':
    main()
