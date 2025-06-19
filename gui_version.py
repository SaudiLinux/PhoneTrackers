#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phone Lookup Tool - GUI Version
Developer: Saudi Linux
Email: SaudiLinux7@gmail.com

GUI version using tkinter for better user experience
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
from datetime import datetime
from phone_lookup import PhoneLookupTool
from config import DEVELOPER_INFO, APP_SETTINGS, GUI_SETTINGS

class PhoneLookupGUI:
    def __init__(self, root):
        self.root = root
        self.lookup_tool = PhoneLookupTool()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface"""
        # Configure main window
        self.root.title(f"{APP_SETTINGS['app_name']} - GUI Version")
        self.root.geometry(GUI_SETTINGS['window_size'])
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('TButton', background='#404040', foreground='#ffffff')
        style.configure('TEntry', background='#404040', foreground='#ffffff')
        style.configure('TFrame', background='#2b2b2b')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📱 Phone Lookup Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Developer info
        dev_label = ttk.Label(main_frame, 
                             text=f"Developer: {DEVELOPER_INFO['name']} | {DEVELOPER_INFO['email']}",
                             font=('Arial', 10))
        dev_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Phone number input
        ttk.Label(main_frame, text="Phone Number:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(main_frame, textvariable=self.phone_var, 
                                    font=('Arial', 12), width=30)
        self.phone_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Lookup button
        self.lookup_btn = ttk.Button(main_frame, text="🔍 Lookup", 
                                    command=self.perform_lookup_threaded)
        self.lookup_btn.grid(row=2, column=2, pady=5, padx=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     width=80, height=20,
                                                     font=('Consolas', 10),
                                                     bg='#1e1e1e', fg='#ffffff',
                                                     insertbackground='#ffffff')
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Save button
        self.save_btn = ttk.Button(buttons_frame, text="💾 Save Results", 
                                  command=self.save_results, state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_btn = ttk.Button(buttons_frame, text="🗑️ Clear", 
                                   command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Help button
        self.help_btn = ttk.Button(buttons_frame, text="❓ Help", 
                                  command=self.show_help)
        self.help_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # About button
        self.about_btn = ttk.Button(buttons_frame, text="ℹ️ About", 
                                   command=self.show_about)
        self.about_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Bind Enter key to lookup
        self.phone_entry.bind('<Return>', lambda e: self.perform_lookup_threaded())
        
        # Store last results for saving
        self.last_results = None
        
    def perform_lookup_threaded(self):
        """Perform lookup in a separate thread"""
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showwarning("Warning", "Please enter a phone number")
            return
            
        # Start lookup in thread
        thread = threading.Thread(target=self.perform_lookup, args=(phone,))
        thread.daemon = True
        thread.start()
        
    def perform_lookup(self, phone):
        """Perform the actual lookup"""
        # Update UI in main thread
        self.root.after(0, self.start_lookup_ui)
        
        try:
            # Perform lookup
            results = self.lookup_tool.perform_lookup(phone)
            
            # Update UI with results
            self.root.after(0, self.display_results, results)
            
        except Exception as e:
            error_msg = f"Error during lookup: {str(e)}"
            self.root.after(0, self.display_error, error_msg)
        finally:
            self.root.after(0, self.stop_lookup_ui)
            
    def start_lookup_ui(self):
        """Update UI when lookup starts"""
        self.lookup_btn.configure(state='disabled')
        self.progress.start()
        self.status_var.set("Performing lookup...")
        self.results_text.delete(1.0, tk.END)
        self.save_btn.configure(state='disabled')
        
    def stop_lookup_ui(self):
        """Update UI when lookup stops"""
        self.lookup_btn.configure(state='normal')
        self.progress.stop()
        self.status_var.set("Ready")
        
    def display_results(self, results):
        """Display lookup results"""
        self.last_results = results
        
        if 'error' in results:
            self.display_error(results['error'])
            return
            
        # Format results for display
        formatted_results = self.format_results_for_display(results)
        
        # Display in text area
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, formatted_results)
        
        # Enable save button
        self.save_btn.configure(state='normal')
        
        self.status_var.set("Lookup completed successfully")
        
    def display_error(self, error_msg):
        """Display error message"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"❌ Error: {error_msg}\n\n")
        self.results_text.insert(tk.END, "Please check your input and try again.")
        self.status_var.set("Error occurred")
        
    def format_results_for_display(self, results):
        """Format results for text display"""
        output = []
        output.append("=" * 60)
        output.append(f"📱 {APP_SETTINGS['app_name']} - Results")
        output.append(f"👨‍💻 Developer: {DEVELOPER_INFO['name']}")
        output.append(f"📧 Email: {DEVELOPER_INFO['email']}")
        output.append("=" * 60)
        output.append("")
        
        # Phone number info
        output.append(f"📞 Phone Number: {results.get('phone_number', 'N/A')}")
        output.append(f"🕒 Lookup Time: {results.get('lookup_timestamp', 'N/A')}")
        output.append("")
        
        # Country and carrier info
        country_info = results.get('country_info', {})
        output.append("🌍 Country & Carrier Information:")
        output.append("-" * 40)
        output.append(f"Country: {country_info.get('country', 'Unknown')} ({country_info.get('country_ar', 'غير معروف')})")
        output.append(f"Country Code: {country_info.get('country_code', 'Unknown')}")
        output.append(f"Carrier: {country_info.get('carrier', 'Unknown')}")
        output.append(f"Line Type: {country_info.get('line_type', 'Unknown')}")
        output.append(f"Is Mobile: {'Yes' if country_info.get('is_mobile') else 'No'}")
        output.append("")
        
        # Owner info
        owner_info = results.get('owner_info', {})
        output.append("👤 Owner Information:")
        output.append("-" * 25)
        output.append(f"Name: {owner_info.get('name', 'N/A')}")
        output.append(f"Location: {owner_info.get('location', 'N/A')}")
        output.append(f"Address: {owner_info.get('address', 'N/A')}")
        output.append("")
        
        # Associated accounts
        accounts = results.get('associated_accounts', {})
        output.append("📧 Associated Accounts:")
        output.append("-" * 25)
        emails = accounts.get('emails', [])
        social_media = accounts.get('social_media', [])
        output.append(f"Emails: {', '.join(emails) if emails else 'None found'}")
        output.append(f"Social Media: {', '.join(social_media) if social_media else 'None found'}")
        output.append("")
        
        # Technical info
        tech_info = results.get('technical_info', {})
        output.append("🔧 Technical Information:")
        output.append("-" * 30)
        output.append(f"Number Type: {tech_info.get('number_type', 'Unknown')}")
        output.append(f"Carrier: {tech_info.get('carrier', 'Unknown')}")
        output.append(f"Valid: {'Yes' if tech_info.get('is_valid') else 'No'}")
        output.append("")
        
        # Disclaimers
        output.append("⚠️  Important Notes:")
        output.append("-" * 20)
        output.append(f"• {results.get('disclaimer', '')}")
        output.append(f"• {results.get('privacy_note', '')}")
        output.append(f"• {results.get('legal_note', '')}")
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)
        
    def save_results(self):
        """Save results to file"""
        if not self.last_results:
            messagebox.showwarning("Warning", "No results to save")
            return
            
        # Ask for save location
        phone = self.last_results.get('phone_number', 'unknown')
        clean_phone = ''.join(c for c in phone if c.isdigit())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"lookup_{clean_phone}_{timestamp}.json"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialname=default_filename
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.last_results, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Results saved to:\n{filename}")
                self.status_var.set(f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
                
    def clear_results(self):
        """Clear results area"""
        self.results_text.delete(1.0, tk.END)
        self.last_results = None
        self.save_btn.configure(state='disabled')
        self.status_var.set("Results cleared")
        
    def show_help(self):
        """Show help dialog"""
        help_text = """
📖 Phone Lookup Tool - Help

🔍 How to use:
1. Enter a phone number in the input field
2. Click 'Lookup' or press Enter
3. View the results in the text area
4. Save results if needed

📱 Supported formats:
• +966501234567 (International)
• 0501234567 (Local Saudi)
• 966501234567 (Without +)

⚠️ Important:
• This tool is for educational purposes only
• Respects privacy and legal boundaries
• Uses only publicly available information
• Does not bypass security measures

📧 Support:
Developer: Saudi Linux
Email: SaudiLinux7@gmail.com
"""
        
        messagebox.showinfo("Help", help_text)
        
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
📱 {APP_SETTINGS['app_name']}
Version: {DEVELOPER_INFO['version']}

👨‍💻 Developer: {DEVELOPER_INFO['name']}
📧 Email: {DEVELOPER_INFO['email']}

📝 Description:
{DEVELOPER_INFO['description']}

⚠️ Disclaimer:
This tool is for educational purposes only.
Use responsibly and respect privacy laws.

© 2024 Saudi Linux. All rights reserved.
"""
        
        messagebox.showinfo("About", about_text)

def main():
    """Main function for GUI version"""
    root = tk.Tk()
    app = PhoneLookupGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Set minimum size
    root.minsize(800, 600)
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()