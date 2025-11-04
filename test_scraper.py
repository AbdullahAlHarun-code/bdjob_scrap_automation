"""
Simple test script to verify bdgovtjob scraper dependencies
"""

print("=" * 60)
print("Testing imports for bdgovtjob scraper...")
print("=" * 60)

missing = []

try:
    print("1. Importing selenium...", end=" ")
    from selenium import webdriver
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    missing.append("selenium")

try:
    print("2. Importing pandas...", end=" ")
    import pandas as pd
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    missing.append("pandas")

try:
    print("3. Importing webdriver_manager...", end=" ")
    from webdriver_manager.chrome import ChromeDriverManager
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    missing.append("webdriver-manager")

try:
    print("4. Importing beautifulsoup4...", end=" ")
    from bs4 import BeautifulSoup
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    missing.append("beautifulsoup4")

print("\n" + "=" * 60)

if not missing:
    print("✅ ALL DEPENDENCIES INSTALLED!")
    print("\nYou can now run the scraper:")
    print("  python bdgovtjob.py")
else:
    print("❌ MISSING PACKAGES:")
    for pkg in missing:
        print(f"   - {pkg}")
    print("\n💡 TO FIX: Open CMD (not PowerShell) and run:")
    print(f"   python -m pip install {' '.join(missing)}")
    print("\nOR install all at once:")
    print("   python -m pip install selenium pandas webdriver-manager beautifulsoup4")

print("=" * 60)

