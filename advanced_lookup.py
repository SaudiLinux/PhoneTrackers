#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Phone Lookup Tool
Developer: Saudi Linux
Email: SaudiLinux7@gmail.com

⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️
This tool demonstrates advanced phone number analysis techniques.
Do not use for illegal activities or privacy violations.
"""

import os
import sys
import json
import time
import random
import hashlib
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("❌ Error: requests library not found")
    print("📦 Install with: pip install requests")
    sys.exit(1)

try:
    from config import (
        DEVELOPER_INFO, APP_SETTINGS, COUNTRY_CODES, 
        USER_AGENTS, API_CONFIG, VALIDATION_RULES,
        ERROR_MESSAGES, SUCCESS_MESSAGES, DISCLAIMERS
    )
except ImportError:
    print("❌ Error: config.py not found")
    print("💡 Make sure config.py is in the same directory")
    sys.exit(1)

# Optional imports for enhanced functionality
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

try:
    from fake_useragent import UserAgent
    FAKE_USERAGENT_AVAILABLE = True
except ImportError:
    FAKE_USERAGENT_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

@dataclass
class PhoneAnalysisResult:
    """Data class for phone analysis results"""
    phone_number: str
    formatted_number: str
    country_code: str
    country_name: str
    region: str
    carrier: str
    line_type: str
    timezone: List[str]
    is_valid: bool
    is_possible: bool
    analysis_timestamp: str
    confidence_score: float
    additional_info: Dict
    educational_note: str

class AdvancedPhoneLookup:
    """Advanced Phone Lookup Tool with enhanced analysis capabilities"""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.session = self._create_session()
        self.results_dir = "results"
        self.logs_dir = "logs"
        self._ensure_directories()
        self._setup_logging()
        
    def _create_session(self) -> requests.Session:
        """Create a robust HTTP session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers
        session.headers.update({
            'User-Agent': self._get_user_agent(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        return session
    
    def _get_user_agent(self) -> str:
        """Get a random user agent"""
        if FAKE_USERAGENT_AVAILABLE:
            try:
                ua = UserAgent()
                return ua.random
            except:
                pass
        
        return random.choice(USER_AGENTS['browsers'])
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        for directory in [self.results_dir, self.logs_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        import logging
        
        log_file = os.path.join(self.logs_dir, f"advanced_lookup_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _print_banner(self):
        """Print application banner"""
        if RICH_AVAILABLE:
            banner = Panel.fit(
                "[bold blue]📱 Advanced Phone Lookup Tool 📱[/bold blue]\n"
                f"[green]Developer:[/green] {DEVELOPER_INFO['name']}\n"
                f"[green]Email:[/green] {DEVELOPER_INFO['email']}\n\n"
                "[yellow]⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️[/yellow]",
                border_style="blue"
            )
            self.console.print(banner)
        else:
            print("\n" + "="*60)
            print("📱 Advanced Phone Lookup Tool 📱")
            print(f"Developer: {DEVELOPER_INFO['name']}")
            print(f"Email: {DEVELOPER_INFO['email']}")
            print("\n⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️")
            print("="*60 + "\n")
    
    def validate_phone_number(self, phone_number: str) -> Tuple[bool, str, str]:
        """Validate and format phone number"""
        # Remove all non-digit characters except +
        cleaned = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        
        if not cleaned:
            return False, "", "Phone number cannot be empty"
        
        # Basic validation
        if len(cleaned.replace('+', '')) < VALIDATION_RULES['min_length']:
            return False, "", f"Phone number too short (minimum {VALIDATION_RULES['min_length']} digits)"
        
        if len(cleaned.replace('+', '')) > VALIDATION_RULES['max_length']:
            return False, "", f"Phone number too long (maximum {VALIDATION_RULES['max_length']} digits)"
        
        # Add + if not present
        if not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        
        return True, cleaned, "Valid format"
    
    def analyze_with_phonenumbers(self, phone_number: str) -> Dict:
        """Analyze phone number using phonenumbers library"""
        if not PHONENUMBERS_AVAILABLE:
            return {"error": "phonenumbers library not available"}
        
        try:
            # Parse the number
            parsed = phonenumbers.parse(phone_number, None)
            
            # Get information
            country_code = f"+{parsed.country_code}"
            country_name = geocoder.description_for_number(parsed, "en")
            carrier_name = carrier.name_for_number(parsed, "en")
            timezones = timezone.time_zones_for_number(parsed)
            
            # Validation
            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)
            
            # Number type
            number_type = phonenumbers.number_type(parsed)
            type_mapping = {
                phonenumbers.PhoneNumberType.MOBILE: "Mobile",
                phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
                phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
                phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
                phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
                phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
                phonenumbers.PhoneNumberType.VOIP: "VoIP",
                phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
                phonenumbers.PhoneNumberType.PAGER: "Pager",
                phonenumbers.PhoneNumberType.UAN: "UAN",
                phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
                phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
            }
            
            line_type = type_mapping.get(number_type, "Unknown")
            
            # Format number
            formatted_international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            formatted_national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            formatted_e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            return {
                "success": True,
                "country_code": country_code,
                "country_name": country_name or "Unknown",
                "carrier": carrier_name or "Unknown",
                "timezones": list(timezones),
                "line_type": line_type,
                "is_valid": is_valid,
                "is_possible": is_possible,
                "formatted": {
                    "international": formatted_international,
                    "national": formatted_national,
                    "e164": formatted_e164
                },
                "raw_data": {
                    "country_code_num": parsed.country_code,
                    "national_number": parsed.national_number,
                    "extension": parsed.extension
                }
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def educational_lookup_simulation(self, phone_number: str) -> Dict:
        """Simulate educational lookup with realistic data patterns"""
        # Generate deterministic but realistic-looking data based on phone number
        seed = int(hashlib.md5(phone_number.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Simulate processing time
        time.sleep(random.uniform(1, 3))
        
        # Extract country code
        country_code = "+1"  # Default
        for code, info in COUNTRY_CODES.items():
            if phone_number.startswith(code):
                country_code = code
                break
        
        # Generate educational data
        carriers = ["Educational Carrier A", "Educational Carrier B", "Educational Carrier C"]
        regions = ["Educational Region 1", "Educational Region 2", "Educational Region 3"]
        
        return {
            "phone_number": phone_number,
            "country_code": country_code,
            "country_name": COUNTRY_CODES.get(country_code, {}).get('name', 'Unknown'),
            "region": random.choice(regions),
            "carrier": random.choice(carriers),
            "line_type": random.choice(["Mobile", "Fixed Line", "VoIP"]),
            "confidence": random.uniform(0.7, 0.95),
            "educational_note": "This is simulated data for educational purposes only",
            "timestamp": datetime.now().isoformat(),
            "additional_info": {
                "analysis_method": "Educational Simulation",
                "data_sources": ["Educational Database A", "Educational Database B"],
                "privacy_note": "No real personal data was accessed"
            }
        }
    
    def comprehensive_analysis(self, phone_number: str) -> PhoneAnalysisResult:
        """Perform comprehensive phone number analysis"""
        self.logger.info(f"Starting comprehensive analysis for: {phone_number}")
        
        # Validate phone number
        is_valid_format, formatted_number, validation_msg = self.validate_phone_number(phone_number)
        
        if not is_valid_format:
            return PhoneAnalysisResult(
                phone_number=phone_number,
                formatted_number="",
                country_code="",
                country_name="",
                region="",
                carrier="",
                line_type="",
                timezone=[],
                is_valid=False,
                is_possible=False,
                analysis_timestamp=datetime.now().isoformat(),
                confidence_score=0.0,
                additional_info={"error": validation_msg},
                educational_note=DISCLAIMERS['educational_purpose']
            )
        
        # Perform phonenumbers analysis if available
        phonenumbers_result = self.analyze_with_phonenumbers(formatted_number)
        
        # Perform educational simulation
        educational_result = self.educational_lookup_simulation(formatted_number)
        
        # Combine results
        if phonenumbers_result.get("success"):
            result = PhoneAnalysisResult(
                phone_number=phone_number,
                formatted_number=phonenumbers_result["formatted"]["international"],
                country_code=phonenumbers_result["country_code"],
                country_name=phonenumbers_result["country_name"],
                region=educational_result["region"],
                carrier=phonenumbers_result["carrier"],
                line_type=phonenumbers_result["line_type"],
                timezone=phonenumbers_result["timezones"],
                is_valid=phonenumbers_result["is_valid"],
                is_possible=phonenumbers_result["is_possible"],
                analysis_timestamp=datetime.now().isoformat(),
                confidence_score=educational_result["confidence"],
                additional_info={
                    "phonenumbers_data": phonenumbers_result,
                    "educational_data": educational_result
                },
                educational_note=DISCLAIMERS['educational_purpose']
            )
        else:
            result = PhoneAnalysisResult(
                phone_number=phone_number,
                formatted_number=formatted_number,
                country_code=educational_result["country_code"],
                country_name=educational_result["country_name"],
                region=educational_result["region"],
                carrier=educational_result["carrier"],
                line_type=educational_result["line_type"],
                timezone=[],
                is_valid=True,
                is_possible=True,
                analysis_timestamp=datetime.now().isoformat(),
                confidence_score=educational_result["confidence"],
                additional_info={"educational_data": educational_result},
                educational_note=DISCLAIMERS['educational_purpose']
            )
        
        self.logger.info(f"Analysis completed for: {phone_number}")
        return result
    
    def batch_analysis(self, phone_numbers: List[str]) -> List[PhoneAnalysisResult]:
        """Perform batch analysis on multiple phone numbers"""
        results = []
        
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Analyzing phone numbers...", total=len(phone_numbers))
                
                with ThreadPoolExecutor(max_workers=3) as executor:
                    future_to_number = {executor.submit(self.comprehensive_analysis, num): num for num in phone_numbers}
                    
                    for future in as_completed(future_to_number):
                        number = future_to_number[future]
                        try:
                            result = future.result()
                            results.append(result)
                            progress.update(task, advance=1)
                        except Exception as e:
                            self.logger.error(f"Error analyzing {number}: {str(e)}")
                            progress.update(task, advance=1)
        else:
            print(f"\n🔍 Analyzing {len(phone_numbers)} phone numbers...")
            for i, number in enumerate(phone_numbers, 1):
                print(f"Progress: {i}/{len(phone_numbers)} - {number}")
                try:
                    result = self.comprehensive_analysis(number)
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error analyzing {number}: {str(e)}")
        
        return results
    
    def save_results(self, results: List[PhoneAnalysisResult], filename: str = None) -> str:
        """Save analysis results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"advanced_analysis_{timestamp}.json"
        
        filepath = os.path.join(self.results_dir, filename)
        
        # Convert results to dict format
        results_data = {
            "analysis_info": {
                "tool_name": APP_SETTINGS['name'],
                "version": APP_SETTINGS['version'],
                "developer": DEVELOPER_INFO,
                "timestamp": datetime.now().isoformat(),
                "total_numbers": len(results),
                "educational_note": DISCLAIMERS['educational_purpose']
            },
            "results": [asdict(result) for result in results]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {filepath}")
        return filepath
    
    def export_to_csv(self, results: List[PhoneAnalysisResult], filename: str = None) -> str:
        """Export results to CSV format"""
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas library required for CSV export")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"advanced_analysis_{timestamp}.csv"
        
        filepath = os.path.join(self.results_dir, filename)
        
        # Convert to DataFrame
        data = []
        for result in results:
            row = {
                'Phone Number': result.phone_number,
                'Formatted Number': result.formatted_number,
                'Country Code': result.country_code,
                'Country Name': result.country_name,
                'Region': result.region,
                'Carrier': result.carrier,
                'Line Type': result.line_type,
                'Timezone': ', '.join(result.timezone),
                'Is Valid': result.is_valid,
                'Is Possible': result.is_possible,
                'Confidence Score': result.confidence_score,
                'Analysis Timestamp': result.analysis_timestamp,
                'Educational Note': result.educational_note
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        self.logger.info(f"CSV exported to: {filepath}")
        return filepath
    
    def display_results(self, results: List[PhoneAnalysisResult]):
        """Display analysis results"""
        if RICH_AVAILABLE:
            self._display_results_rich(results)
        else:
            self._display_results_simple(results)
    
    def _display_results_rich(self, results: List[PhoneAnalysisResult]):
        """Display results using rich formatting"""
        for i, result in enumerate(results, 1):
            # Create table for each result
            table = Table(title=f"📱 Analysis Result #{i}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Phone Number", result.phone_number)
            table.add_row("Formatted Number", result.formatted_number)
            table.add_row("Country Code", result.country_code)
            table.add_row("Country Name", result.country_name)
            table.add_row("Region", result.region)
            table.add_row("Carrier", result.carrier)
            table.add_row("Line Type", result.line_type)
            table.add_row("Timezone", ", ".join(result.timezone))
            table.add_row("Is Valid", "✅ Yes" if result.is_valid else "❌ No")
            table.add_row("Is Possible", "✅ Yes" if result.is_possible else "❌ No")
            table.add_row("Confidence Score", f"{result.confidence_score:.2%}")
            table.add_row("Analysis Time", result.analysis_timestamp)
            
            self.console.print(table)
            
            # Educational note
            note_panel = Panel(
                result.educational_note,
                title="⚠️ Educational Note",
                border_style="yellow"
            )
            self.console.print(note_panel)
            self.console.print()
    
    def _display_results_simple(self, results: List[PhoneAnalysisResult]):
        """Display results in simple text format"""
        for i, result in enumerate(results, 1):
            print(f"\n📱 Analysis Result #{i}")
            print("=" * 40)
            print(f"Phone Number: {result.phone_number}")
            print(f"Formatted Number: {result.formatted_number}")
            print(f"Country Code: {result.country_code}")
            print(f"Country Name: {result.country_name}")
            print(f"Region: {result.region}")
            print(f"Carrier: {result.carrier}")
            print(f"Line Type: {result.line_type}")
            print(f"Timezone: {', '.join(result.timezone)}")
            print(f"Is Valid: {'✅ Yes' if result.is_valid else '❌ No'}")
            print(f"Is Possible: {'✅ Yes' if result.is_possible else '❌ No'}")
            print(f"Confidence Score: {result.confidence_score:.2%}")
            print(f"Analysis Time: {result.analysis_timestamp}")
            print(f"\n⚠️ Educational Note: {result.educational_note}")
            print()
    
    def interactive_mode(self):
        """Run interactive mode"""
        self._print_banner()
        
        while True:
            try:
                print("\n🔍 Advanced Phone Lookup Options:")
                print("1. 📱 Single Number Analysis")
                print("2. 📋 Batch Analysis")
                print("3. 📁 Load Numbers from File")
                print("4. 📊 Export Last Results to CSV")
                print("5. 📖 View Analysis History")
                print("6. ❌ Exit")
                
                choice = input("\nSelect option (1-6): ").strip()
                
                if choice == '1':
                    self._single_analysis_mode()
                elif choice == '2':
                    self._batch_analysis_mode()
                elif choice == '3':
                    self._file_analysis_mode()
                elif choice == '4':
                    self._export_csv_mode()
                elif choice == '5':
                    self._view_history_mode()
                elif choice == '6':
                    print("\n👋 Thank you for using Advanced Phone Lookup Tool!")
                    print(f"👨‍💻 Developer: {DEVELOPER_INFO['name']}")
                    print(f"📧 Email: {DEVELOPER_INFO['email']}")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                self.logger.error(f"Interactive mode error: {str(e)}")
    
    def _single_analysis_mode(self):
        """Single number analysis mode"""
        phone_number = input("\n📱 Enter phone number (with country code): ").strip()
        
        if not phone_number:
            print("❌ Phone number cannot be empty")
            return
        
        print("\n🔍 Analyzing phone number...")
        result = self.comprehensive_analysis(phone_number)
        
        self.display_results([result])
        
        # Save result
        filepath = self.save_results([result])
        print(f"\n💾 Results saved to: {filepath}")
        
        # Store for potential CSV export
        self.last_results = [result]
    
    def _batch_analysis_mode(self):
        """Batch analysis mode"""
        print("\n📋 Enter phone numbers (one per line, empty line to finish):")
        numbers = []
        
        while True:
            number = input().strip()
            if not number:
                break
            numbers.append(number)
        
        if not numbers:
            print("❌ No phone numbers entered")
            return
        
        print(f"\n🔍 Analyzing {len(numbers)} phone numbers...")
        results = self.batch_analysis(numbers)
        
        self.display_results(results)
        
        # Save results
        filepath = self.save_results(results)
        print(f"\n💾 Results saved to: {filepath}")
        
        # Store for potential CSV export
        self.last_results = results
    
    def _file_analysis_mode(self):
        """File analysis mode"""
        filename = input("\n📁 Enter filename (txt file with one number per line): ").strip()
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                numbers = [line.strip() for line in f if line.strip()]
            
            if not numbers:
                print("❌ No phone numbers found in file")
                return
            
            print(f"\n📋 Found {len(numbers)} phone numbers in file")
            print(f"🔍 Starting batch analysis...")
            
            results = self.batch_analysis(numbers)
            
            self.display_results(results)
            
            # Save results
            filepath = self.save_results(results)
            print(f"\n💾 Results saved to: {filepath}")
            
            # Store for potential CSV export
            self.last_results = results
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
    
    def _export_csv_mode(self):
        """Export to CSV mode"""
        if not hasattr(self, 'last_results') or not self.last_results:
            print("❌ No results to export. Please run an analysis first.")
            return
        
        if not PANDAS_AVAILABLE:
            print("❌ pandas library required for CSV export")
            print("📦 Install with: pip install pandas")
            return
        
        try:
            filepath = self.export_to_csv(self.last_results)
            print(f"\n📊 CSV exported to: {filepath}")
        except Exception as e:
            print(f"❌ Error exporting CSV: {str(e)}")
    
    def _view_history_mode(self):
        """View analysis history"""
        try:
            files = [f for f in os.listdir(self.results_dir) if f.endswith('.json')]
            
            if not files:
                print("\n📁 No analysis history found")
                return
            
            print(f"\n📖 Analysis History ({len(files)} files):")
            print("=" * 40)
            
            for i, filename in enumerate(sorted(files, reverse=True)[:10], 1):
                filepath = os.path.join(self.results_dir, filename)
                mtime = os.path.getmtime(filepath)
                mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"{i:2d}. {filename} ({mtime_str})")
            
            if len(files) > 10:
                print(f"    ... and {len(files) - 10} more files")
                
        except Exception as e:
            print(f"❌ Error viewing history: {str(e)}")

def main():
    """Main function"""
    try:
        tool = AdvancedPhoneLookup()
        
        if len(sys.argv) > 1:
            # Command line mode
            phone_number = sys.argv[1]
            print(f"\n🔍 Analyzing: {phone_number}")
            
            result = tool.comprehensive_analysis(phone_number)
            tool.display_results([result])
            
            filepath = tool.save_results([result])
            print(f"\n💾 Results saved to: {filepath}")
        else:
            # Interactive mode
            tool.interactive_mode()
            
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()