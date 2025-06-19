#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for Phone Lookup Tool
Developer: Saudi Linux
Email: SaudiLinux7@gmail.com
"""

import os
from typing import Dict, List

# Developer Information
DEVELOPER_INFO = {
    'name': 'Saudi Linux',
    'email': 'SaudiLinux7@gmail.com',
    'version': '1.0.0',
    'description': 'Educational Phone Lookup Tool'
}

# Application Settings
APP_SETTINGS = {
    'app_name': 'Phone Lookup Tool',
    'debug_mode': False,
    'log_level': 'INFO',
    'max_retries': 3,
    'timeout': 30,
    'rate_limit_delay': 1  # seconds between requests
}

# User Agent strings for web requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

# Country codes and their information
COUNTRY_CODES = {
    '+966': {
        'country': 'Saudi Arabia',
        'country_ar': 'المملكة العربية السعودية',
        'carriers': ['STC', 'Mobily', 'Zain', 'Virgin Mobile'],
        'mobile_prefixes': ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
    },
    '+1': {
        'country': 'United States/Canada',
        'country_ar': 'الولايات المتحدة/كندا',
        'carriers': ['Verizon', 'AT&T', 'T-Mobile', 'Sprint'],
        'mobile_prefixes': []
    },
    '+44': {
        'country': 'United Kingdom',
        'country_ar': 'المملكة المتحدة',
        'carriers': ['EE', 'O2', 'Vodafone', 'Three'],
        'mobile_prefixes': ['7']
    },
    '+971': {
        'country': 'United Arab Emirates',
        'country_ar': 'الإمارات العربية المتحدة',
        'carriers': ['Etisalat', 'du'],
        'mobile_prefixes': ['50', '52', '54', '55', '56', '58']
    },
    '+965': {
        'country': 'Kuwait',
        'country_ar': 'الكويت',
        'carriers': ['Zain', 'Ooredoo', 'STC'],
        'mobile_prefixes': ['5', '6', '9']
    },
    '+973': {
        'country': 'Bahrain',
        'country_ar': 'البحرين',
        'carriers': ['Batelco', 'Zain', 'STC'],
        'mobile_prefixes': ['3']
    },
    '+974': {
        'country': 'Qatar',
        'country_ar': 'قطر',
        'carriers': ['Ooredoo', 'Vodafone'],
        'mobile_prefixes': ['3', '5', '6', '7']
    },
    '+968': {
        'country': 'Oman',
        'country_ar': 'عمان',
        'carriers': ['Omantel', 'Ooredoo'],
        'mobile_prefixes': ['9']
    },
    '+962': {
        'country': 'Jordan',
        'country_ar': 'الأردن',
        'carriers': ['Zain', 'Orange', 'Umniah'],
        'mobile_prefixes': ['7']
    },
    '+961': {
        'country': 'Lebanon',
        'country_ar': 'لبنان',
        'carriers': ['Alfa', 'touch'],
        'mobile_prefixes': ['3', '7']
    },
    '+20': {
        'country': 'Egypt',
        'country_ar': 'مصر',
        'carriers': ['Orange', 'Vodafone', 'Etisalat'],
        'mobile_prefixes': ['10', '11', '12', '15']
    }
}

# API Configuration (Educational - No real APIs)
API_CONFIG = {
    'enable_apis': False,  # Set to False for educational mode
    'apis': {
        'carrier_lookup': {
            'url': 'https://api.example.com/carrier',
            'key': 'YOUR_API_KEY_HERE',
            'enabled': False
        },
        'reverse_lookup': {
            'url': 'https://api.example.com/reverse',
            'key': 'YOUR_API_KEY_HERE',
            'enabled': False
        }
    }
}

# Output Settings
OUTPUT_SETTINGS = {
    'save_results': True,
    'output_format': 'json',  # json, csv, txt
    'output_directory': 'results',
    'include_timestamp': True,
    'pretty_print': True
}

# Security Settings
SECURITY_SETTINGS = {
    'educational_mode': True,  # Always keep True for educational use
    'respect_robots_txt': True,
    'rate_limiting': True,
    'max_requests_per_minute': 10,
    'use_proxy': False,
    'proxy_list': []
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_file': 'phone_lookup.log',
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_rotation': True,
    'max_log_size': '10MB',
    'backup_count': 5
}

# GUI Settings (for future GUI version)
GUI_SETTINGS = {
    'theme': 'dark',
    'window_size': '800x600',
    'font_family': 'Arial',
    'font_size': 12,
    'language': 'ar'  # ar for Arabic, en for English
}

# Database Settings (for future database integration)
DATABASE_SETTINGS = {
    'use_database': False,
    'db_type': 'sqlite',
    'db_file': 'phone_lookup.db',
    'cache_results': True,
    'cache_duration': 3600  # seconds
}

# Validation Rules
VALIDATION_RULES = {
    'min_phone_length': 7,
    'max_phone_length': 15,
    'allowed_characters': '+0123456789 ()-',
    'require_country_code': False
}

# Error Messages
ERROR_MESSAGES = {
    'invalid_phone': 'رقم الهاتف غير صحيح - Invalid phone number',
    'api_error': 'خطأ في الاتصال بالخدمة - API connection error',
    'rate_limit': 'تم تجاوز الحد المسموح من الطلبات - Rate limit exceeded',
    'no_results': 'لم يتم العثور على نتائج - No results found',
    'network_error': 'خطأ في الشبكة - Network error'
}

# Success Messages
SUCCESS_MESSAGES = {
    'lookup_complete': 'تم البحث بنجاح - Lookup completed successfully',
    'results_saved': 'تم حفظ النتائج - Results saved successfully',
    'validation_passed': 'تم التحقق من الرقم - Phone number validated'
}

# Educational Disclaimers
DISCLAIMERS = {
    'educational_use': 'هذه الأداة للأغراض التعليمية فقط - This tool is for educational purposes only',
    'respect_privacy': 'احترم خصوصية الآخرين - Respect others privacy',
    'legal_compliance': 'استخدم الأداة وفقاً للقوانين المحلية - Use according to local laws',
    'no_warranty': 'لا توجد ضمانات على دقة المعلومات - No warranty on information accuracy'
}

def get_config(section: str = None) -> Dict:
    """Get configuration section or all config"""
    config_sections = {
        'app': APP_SETTINGS,
        'api': API_CONFIG,
        'output': OUTPUT_SETTINGS,
        'security': SECURITY_SETTINGS,
        'logging': LOGGING_CONFIG,
        'gui': GUI_SETTINGS,
        'database': DATABASE_SETTINGS,
        'validation': VALIDATION_RULES,
        'countries': COUNTRY_CODES,
        'developer': DEVELOPER_INFO
    }
    
    if section:
        return config_sections.get(section, {})
    return config_sections

def get_country_info(country_code: str) -> Dict:
    """Get country information by country code"""
    return COUNTRY_CODES.get(country_code, {
        'country': 'Unknown',
        'country_ar': 'غير معروف',
        'carriers': [],
        'mobile_prefixes': []
    })

def is_educational_mode() -> bool:
    """Check if running in educational mode"""
    return SECURITY_SETTINGS.get('educational_mode', True)

def get_user_agent() -> str:
    """Get a random user agent"""
    import random
    return random.choice(USER_AGENTS)

# Environment variables override
def load_env_config():
    """Load configuration from environment variables"""
    if os.getenv('PHONE_LOOKUP_DEBUG'):
        APP_SETTINGS['debug_mode'] = os.getenv('PHONE_LOOKUP_DEBUG').lower() == 'true'
    
    if os.getenv('PHONE_LOOKUP_API_KEY'):
        API_CONFIG['apis']['carrier_lookup']['key'] = os.getenv('PHONE_LOOKUP_API_KEY')
    
    if os.getenv('PHONE_LOOKUP_OUTPUT_DIR'):
        OUTPUT_SETTINGS['output_directory'] = os.getenv('PHONE_LOOKUP_OUTPUT_DIR')

# Load environment configuration on import
load_env_config()