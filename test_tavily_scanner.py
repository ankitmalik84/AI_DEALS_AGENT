#!/usr/bin/env python3
"""
Test script for Tavily Scanner Agent
Demonstrates Indian deal discovery capabilities
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.tavily_scanner_agent import TavilyScannerAgent
from config import Config

def test_tavily_scanner():
    """
    Test the Tavily scanner for Indian deals
    """
    print("🇮🇳 Testing Tavily Scanner for Indian Deals")
    print("=" * 50)
    
    # Check if Tavily API key is available
    tavily_key = Config.get_tavily_key()
    if not tavily_key:
        print("❌ No Tavily API key found!")
        print("Please add TAVILY_API_KEY to your .env file")
        print("\nTo get a Tavily API key:")
        print("1. Go to https://tavily.com")
        print("2. Sign up for an account")
        print("3. Get your API key from the dashboard")
        print("4. Add TAVILY_API_KEY=your_key_here to your .env file")
        return False
    
    # Initialize scanner
    try:
        scanner = TavilyScannerAgent()
        if not scanner.tavily:
            print("❌ Tavily scanner not properly initialized")
            return False
            
        print("✅ Tavily Scanner initialized successfully")
        print()
        
        # Test search
        print("🔍 Searching for Indian deals...")
        selection = scanner.scan(memory=[])
        
        if selection and selection.deals:
            print(f"✅ Found {len(selection.deals)} curated Indian deals!")
            print()
            
            for i, deal in enumerate(selection.deals, 1):
                print(f"Deal {i}:")
                print(f"  Product: {deal.product_description[:100]}...")
                print(f"  Price: ₹{deal.price}")
                print(f"  URL: {deal.url}")
                print()
                
            return True
        else:
            print("❌ No deals found. This could be due to:")
            print("- API rate limits")
            print("- No current deals matching criteria")
            print("- Network issues")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Tavily scanner: {str(e)}")
        return False

def compare_scanners():
    """
    Compare RSS vs Tavily scanner results
    """
    print("\n" + "=" * 50)
    print("🆚 Comparing RSS vs Tavily Scanners")
    print("=" * 50)
    
    from agents.scanner_agent import ScannerAgent
    
    # Test RSS Scanner
    print("📡 Testing RSS Scanner (International deals)...")
    try:
        rss_scanner = ScannerAgent()
        rss_selection = rss_scanner.scan(memory=[])
        
        if rss_selection and rss_selection.deals:
            print(f"✅ RSS found {len(rss_selection.deals)} international deals")
            print(f"   Sample: {rss_selection.deals[0].product_description[:80]}...")
        else:
            print("❌ RSS scanner found no deals")
    except Exception as e:
        print(f"❌ RSS scanner error: {str(e)}")
    
    # Test Tavily Scanner
    print("\n🇮🇳 Testing Tavily Scanner (Indian deals)...")
    tavily_result = test_tavily_scanner()
    
    print("\n📊 Summary:")
    print("RSS Scanner:")
    print("  ✅ Covers US/International deals")
    print("  ❌ Limited relevance for Indian market")
    print("  ❌ USD pricing not relevant for Indian consumers")
    
    print("\nTavily Scanner:")
    print("  ✅ Focuses on Indian e-commerce sites")
    print("  ✅ INR pricing relevant for Indian consumers")  
    print("  ✅ Real-time search capabilities")
    print("  ✅ Covers Flipkart, Amazon India, Myntra, etc.")

if __name__ == "__main__":
    print("🤖 AI Deal Agent Framework - Tavily Integration Test")
    print("=" * 60)
    
    # Test individual scanner
    success = test_tavily_scanner()
    
    # Compare both scanners
    compare_scanners()
    
    if success:
        print("\n🎉 Tavily integration test completed successfully!")
        print("\nNext steps:")
        print("1. Add TAVILY_API_KEY to your .env file")
        print("2. Run the main framework with: python deal_agent_framework.py")
        print("3. The system will automatically prefer Indian deals when available")
    else:
        print("\n⚠️  Tavily integration needs setup")
        print("The system will fallback to RSS feeds until Tavily is configured") 