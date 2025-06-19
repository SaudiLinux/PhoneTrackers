#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phone Number Lookup Tool - Enhanced Version
Developer: Saudi Linux
Email: SaudiLinux7@gmail.com

DISCLAIMER: This tool is for educational purposes only.
It only searches publicly available information through legitimate APIs.
Do not use for illegal activities or privacy violations.
"""

import requests
import json
import re
import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote
from config import (
    DEVELOPER_INFO, APP_SETTINGS, COUNTRY_CODES, USER_AGENTS,
    VALIDATION_RULES, ERROR_MESSAGES, SUCCESS_MESSAGES, DISCLAIMERS,
    get_config, get_country_info, is_educational_mode, get_user_agent
)

class PhoneLookupTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': get_user_agent()
        })
        self.setup_logging()
        self.results_dir = get_config('output')['output_directory']
        self.ensure_results_directory()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_config = get_config('logging')
        logging.basicConfig(
            level=getattr(logging, APP_SETTINGS['log_level']),
            format=log_config['log_format'],
            handlers=[
                logging.FileHandler(log_config['log_file'], encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def ensure_results_directory(self):
        """Create results directory if it doesn't exist"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            
    def validate_phone_number(self, phone: str) -> tuple[bool, str]:
        """Enhanced phone number validation"""
        if not phone:
            return False, ERROR_MESSAGES['invalid_phone']
            
        # Remove all non-digit characters except +
        clean_phone = re.sub(r'[^+\d]', '', phone)
        
        # Check length
        digit_count = len(re.sub(r'[^\d]', '', clean_phone))
        if digit_count < VALIDATION_RULES['min_phone_length'] or digit_count > VALIDATION_RULES['max_phone_length']:
            return False, f"{ERROR_MESSAGES['invalid_phone']} (Length: {digit_count})"
            
        # Check for valid characters
        allowed_chars = set(VALIDATION_RULES['allowed_characters'])
        if not all(c in allowed_chars for c in phone):
            return False, f"{ERROR_MESSAGES['invalid_phone']} (Invalid characters)"
            
        return True, SUCCESS_MESSAGES['validation_passed']
    
    def format_phone_number(self, phone: str) -> str:
        """Enhanced phone number formatting"""
        # Remove all non-digit characters except +
        clean_phone = re.sub(r'[^+\d]', '', phone)
        
        # If already has country code
        if clean_phone.startswith('+'):
            return clean_phone
            
        # Saudi Arabia specific formatting
        if clean_phone.startswith('966'):
            return f"+{clean_phone}"
        elif clean_phone.startswith('05'):
            return f"+966{clean_phone[1:]}"
        elif clean_phone.startswith('5') and len(clean_phone) == 9:
            return f"+966{clean_phone}"
        elif clean_phone.startswith('0') and len(clean_phone) == 10:
            # Assume Saudi if starts with 0 and 10 digits
            return f"+966{clean_phone[1:]}"
        else:
            # Try to detect country code
            for code in COUNTRY_CODES.keys():
                code_digits = code[1:]  # Remove +
                if clean_phone.startswith(code_digits):
                    return f"+{clean_phone}"
            
            # Default: assume it needs +966 if no country code detected
            return f"+966{clean_phone}"
    
    def detect_country_and_carrier(self, phone: str) -> Dict:
        """Detect country and carrier information"""
        formatted_phone = self.format_phone_number(phone)
        
        # Find matching country code
        country_info = None
        detected_code = None
        
        for code, info in COUNTRY_CODES.items():
            if formatted_phone.startswith(code):
                country_info = info
                detected_code = code
                break
        
        if not country_info:
            return {
                'country_code': 'Unknown',
                'country': 'Unknown',
                'country_ar': 'غير معروف',
                'carrier': 'Unknown',
                'line_type': 'Unknown',
                'is_mobile': False
            }
        
        # Extract number after country code
        number_part = formatted_phone[len(detected_code):]
        
        # Check if it's mobile based on prefixes
        is_mobile = False
        detected_carrier = 'Unknown'
        
        if country_info['mobile_prefixes']:
            for prefix in country_info['mobile_prefixes']:
                if number_part.startswith(prefix):
                    is_mobile = True
                    break
        
        # Saudi Arabia specific carrier detection
        if detected_code == '+966' and is_mobile:
            if number_part.startswith('50') or number_part.startswith('53') or number_part.startswith('56'):
                detected_carrier = 'STC'
            elif number_part.startswith('51') or number_part.startswith('54') or number_part.startswith('57'):
                detected_carrier = 'Mobily'
            elif number_part.startswith('52') or number_part.startswith('55') or number_part.startswith('58'):
                detected_carrier = 'Zain'
            elif number_part.startswith('59'):
                detected_carrier = 'Virgin Mobile'
        
        return {
            'country_code': detected_code,
            'country': country_info['country'],
            'country_ar': country_info['country_ar'],
            'carrier': detected_carrier,
            'line_type': 'Mobile' if is_mobile else 'Landline',
            'is_mobile': is_mobile,
            'available_carriers': country_info['carriers']
        }
    
    def educational_lookup(self, phone: str) -> Dict:
        """Educational lookup simulation"""
        formatted_phone = self.format_phone_number(phone)
        country_carrier_info = self.detect_country_and_carrier(formatted_phone)
        
        # Simulate lookup delay
        time.sleep(1)
        
        result = {
            'phone_number': formatted_phone,
            'lookup_timestamp': datetime.now().isoformat(),
            'country_info': country_carrier_info,
            'owner_info': {
                'name': 'Not Available (Educational Mode)',
                'address': 'Not Available (Educational Mode)',
                'location': country_carrier_info.get('country', 'Unknown'),
                'note': 'Real data lookup requires proper authorization and legal compliance'
            },
            'associated_accounts': {
                'emails': [],
                'social_media': [],
                'note': 'Educational mode - No real account data available'
            },
            'technical_info': {
                'number_type': country_carrier_info.get('line_type', 'Unknown'),
                'carrier': country_carrier_info.get('carrier', 'Unknown'),
                'country_code': country_carrier_info.get('country_code', 'Unknown'),
                'is_valid': True,
                'is_mobile': country_carrier_info.get('is_mobile', False)
            },
            'disclaimer': DISCLAIMERS['educational_use'],
            'privacy_note': DISCLAIMERS['respect_privacy'],
            'legal_note': DISCLAIMERS['legal_compliance']
        }
        
        return result
    
    def perform_lookup(self, phone: str) -> Dict:
        """Main lookup function"""
        self.logger.info(f"Starting lookup for phone: {phone}")
        
        # Validate phone number
        is_valid, validation_message = self.validate_phone_number(phone)
        if not is_valid:
            self.logger.error(f"Validation failed: {validation_message}")
            return {'error': validation_message}
        
        formatted_phone = self.format_phone_number(phone)
        
        try:
            if is_educational_mode():
                result = self.educational_lookup(formatted_phone)
                self.logger.info("Educational lookup completed")
                return result
            else:
                # Real API lookup would go here
                self.logger.warning("Real API mode not implemented - using educational mode")
                return self.educational_lookup(formatted_phone)
                
        except Exception as e:
            self.logger.error(f"Lookup error: {str(e)}")
            return {'error': f"{ERROR_MESSAGES['api_error']}: {str(e)}"}
    
    def save_results(self, results: Dict, phone: str) -> str:
        """Save results to file"""
        if 'error' in results:
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        clean_phone = re.sub(r'[^\d]', '', phone)
        filename = f"lookup_{clean_phone}_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Results saved to {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save results: {str(e)}")
            return None
    
    def display_results(self, results: Dict):
        """Display formatted results"""
        print("\n" + "="*60)
        print(f"📱 {APP_SETTINGS['app_name']}")
        print(f"👨‍💻 Developer: {DEVELOPER_INFO['name']}")
        print(f"📧 Email: {DEVELOPER_INFO['email']}")
        print("="*60)
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return
        
        # Phone number info
        print(f"📞 Phone Number: {results.get('phone_number', 'N/A')}")
        print(f"🕒 Lookup Time: {results.get('lookup_timestamp', 'N/A')}")
        
        # Country and carrier info
        country_info = results.get('country_info', {})
        print("\n🌍 Country & Carrier Information:")
        print("-" * 40)
        print(f"Country: {country_info.get('country', 'Unknown')} ({country_info.get('country_ar', 'غير معروف')})")
        print(f"Country Code: {country_info.get('country_code', 'Unknown')}")
        print(f"Carrier: {country_info.get('carrier', 'Unknown')}")
        print(f"Line Type: {country_info.get('line_type', 'Unknown')}")
        print(f"Is Mobile: {'Yes' if country_info.get('is_mobile') else 'No'}")
        
        # Owner info
        owner_info = results.get('owner_info', {})
        print("\n👤 Owner Information:")
        print("-" * 25)
        print(f"Name: {owner_info.get('name', 'N/A')}")
        print(f"Location: {owner_info.get('location', 'N/A')}")
        print(f"Address: {owner_info.get('address', 'N/A')}")
        
        # Associated accounts
        accounts = results.get('associated_accounts', {})
        print("\n📧 Associated Accounts:")
        print("-" * 25)
        emails = accounts.get('emails', [])
        social_media = accounts.get('social_media', [])
        print(f"Emails: {', '.join(emails) if emails else 'None found'}")
        print(f"Social Media: {', '.join(social_media) if social_media else 'None found'}")
        
        # Technical info
        tech_info = results.get('technical_info', {})
        print("\n🔧 Technical Information:")
        print("-" * 30)
        print(f"Number Type: {tech_info.get('number_type', 'Unknown')}")
        print(f"Carrier: {tech_info.get('carrier', 'Unknown')}")
        print(f"Valid: {'Yes' if tech_info.get('is_valid') else 'No'}")
        
        # Disclaimers
        print("\n⚠️  Important Notes:")
        print("-" * 20)
        print(f"• {results.get('disclaimer', '')}")
        print(f"• {results.get('privacy_note', '')}")
        print(f"• {results.get('legal_note', '')}")
        
        print("\n" + "="*60)

def print_banner():
    """Print application banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📱 Phone Lookup Tool 📱                    ║
║                                                              ║
║  Developer: {DEVELOPER_INFO['name']:<20} Version: {DEVELOPER_INFO['version']:<10} ║
║  Email: {DEVELOPER_INFO['email']:<30}                ║
║                                                              ║
║  ⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️                        ║
║  • Respects privacy and legal boundaries                    ║
║  • Uses only publicly available information                 ║
║  • Does not bypass any security measures                    ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Main application function"""
    print_banner()
    
    lookup_tool = PhoneLookupTool()
    
    print("\n📋 Instructions:")
    print("• Enter a phone number to lookup")
    print("• Supported formats: +966501234567, 0501234567, 966501234567")
    print("• Type 'quit', 'exit', or 'q' to exit")
    print("• Type 'help' for more information\n")
    
    while True:
        try:
            user_input = input("🔍 Enter phone number: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Phone Lookup Tool!")
                print(f"Developed by {DEVELOPER_INFO['name']} - {DEVELOPER_INFO['email']}")
                break
            
            if user_input.lower() == 'help':
                print("\n📖 Help Information:")
                print("• This tool searches for publicly available information only")
                print("• All searches are logged for educational purposes")
                print("• Results are saved in the 'results' directory")
                print("• Respect privacy and use responsibly")
                print("• Contact developer for questions or support\n")
                continue
            
            if not user_input:
                print("❌ Please enter a valid phone number.\n")
                continue
            
            print("\n🔄 Processing lookup...")
            
            # Perform lookup
            results = lookup_tool.perform_lookup(user_input)
            
            # Display results
            lookup_tool.display_results(results)
            
            # Ask to save results
            if 'error' not in results:
                save_choice = input("\n💾 Save results to file? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    saved_file = lookup_tool.save_results(results, user_input)
                    if saved_file:
                        print(f"✅ Results saved to: {saved_file}")
                    else:
                        print("❌ Failed to save results")
            
            print("\n" + "-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Operation cancelled by user")
            print("👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            print("Please try again or contact support.\n")

if __name__ == "__main__":
    main()