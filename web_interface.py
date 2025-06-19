#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Interface for Phone Lookup Tool
Developer: Saudi Linux
Email: SaudiLinux7@gmail.com

⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️
This web interface provides a user-friendly way to access phone lookup functionality.
Do not use for illegal activities or privacy violations.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional

try:
    from flask import Flask, render_template_string, request, jsonify, send_file, redirect, url_for
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("❌ Error: Flask not installed")
    print("📦 Install with: pip install flask")
    sys.exit(1)

try:
    from config import DEVELOPER_INFO, APP_SETTINGS, DISCLAIMERS
except ImportError:
    print("❌ Error: config.py not found")
    sys.exit(1)

try:
    from advanced_lookup import AdvancedPhoneLookup
except ImportError:
    print("❌ Error: advanced_lookup.py not found")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'saudi_linux_phone_lookup_2024'

# Initialize lookup tool
lookup_tool = AdvancedPhoneLookup()

# HTML Templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 Phone Lookup Tool - {{ developer_name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .developer-info {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .main-content {
            padding: 40px;
        }
        
        .warning-box {
            background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .form-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .form-section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #34495e;
        }
        
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .input-group input:focus, .input-group textarea:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
        }
        
        .btn {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results {
            margin-top: 30px;
        }
        
        .result-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        
        .result-header {
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .result-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .result-row:last-child {
            border-bottom: none;
        }
        
        .result-label {
            font-weight: bold;
            color: #2c3e50;
        }
        
        .result-value {
            color: #34495e;
        }
        
        .status-valid {
            color: #27ae60;
            font-weight: bold;
        }
        
        .status-invalid {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
        }
        
        .tabs {
            display: flex;
            background: #ecf0f1;
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: none;
            background: transparent;
            font-size: 16px;
        }
        
        .tab.active {
            background: #3498db;
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .main-content {
                padding: 20px;
            }
            
            .result-row {
                flex-direction: column;
            }
            
            .tabs {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 Phone Lookup Tool</h1>
            <p>Advanced Phone Number Analysis & Information Gathering</p>
            <div class="developer-info">
                <strong>👨‍💻 Developer:</strong> {{ developer_name }}<br>
                <strong>📧 Email:</strong> {{ developer_email }}
            </div>
        </div>
        
        <div class="main-content">
            <div class="warning-box">
                ⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️<br>
                This tool is designed for educational and research purposes. Use responsibly and respect privacy laws.
            </div>
            
            <div class="tabs">
                <button class="tab active" onclick="showTab('single')">📱 Single Number</button>
                <button class="tab" onclick="showTab('batch')">📋 Batch Analysis</button>
                <button class="tab" onclick="showTab('history')">📖 History</button>
            </div>
            
            <!-- Single Number Tab -->
            <div id="single" class="tab-content active">
                <div class="form-section">
                    <h2>🔍 Single Phone Number Analysis</h2>
                    <form id="singleForm">
                        <div class="input-group">
                            <label for="phoneNumber">📞 Phone Number (with country code):</label>
                            <input type="text" id="phoneNumber" name="phoneNumber" placeholder="+1234567890" required>
                        </div>
                        <button type="submit" class="btn">🔍 Analyze Number</button>
                    </form>
                </div>
            </div>
            
            <!-- Batch Analysis Tab -->
            <div id="batch" class="tab-content">
                <div class="form-section">
                    <h2>📋 Batch Phone Number Analysis</h2>
                    <form id="batchForm">
                        <div class="input-group">
                            <label for="phoneNumbers">📞 Phone Numbers (one per line):</label>
                            <textarea id="phoneNumbers" name="phoneNumbers" rows="10" placeholder="+1234567890\n+0987654321\n+1122334455" required></textarea>
                        </div>
                        <button type="submit" class="btn">🔍 Analyze Numbers</button>
                    </form>
                </div>
            </div>
            
            <!-- History Tab -->
            <div id="history" class="tab-content">
                <div class="form-section">
                    <h2>📖 Analysis History</h2>
                    <button onclick="loadHistory()" class="btn btn-success">🔄 Refresh History</button>
                    <button onclick="downloadResults()" class="btn btn-warning">📥 Download Last Results</button>
                    <div id="historyContent">
                        <p>Click "Refresh History" to load analysis history.</p>
                    </div>
                </div>
            </div>
            
            <!-- Loading Animation -->
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>🔍 Analyzing phone number(s)... Please wait.</p>
            </div>
            
            <!-- Results Section -->
            <div id="results" class="results"></div>
        </div>
        
        <div class="footer">
            <p>&copy; 2024 {{ developer_name }} | {{ app_name }} v{{ app_version }}</p>
            <p>📧 Contact: {{ developer_email }}</p>
        </div>
    </div>
    
    <script>
        let lastResults = null;
        
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        function displayResults(results) {
            const resultsDiv = document.getElementById('results');
            
            if (!results || results.length === 0) {
                resultsDiv.innerHTML = '<div class="result-card"><p>❌ No results found.</p></div>';
                return;
            }
            
            let html = '<h2>📊 Analysis Results</h2>';
            
            results.forEach((result, index) => {
                html += `
                    <div class="result-card">
                        <div class="result-header">
                            <h3>📱 Result #${index + 1}: ${result.phone_number}</h3>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">📞 Formatted Number:</span>
                            <span class="result-value">${result.formatted_number}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">🌍 Country Code:</span>
                            <span class="result-value">${result.country_code}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">🏳️ Country Name:</span>
                            <span class="result-value">${result.country_name}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">📍 Region:</span>
                            <span class="result-value">${result.region}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">📡 Carrier:</span>
                            <span class="result-value">${result.carrier}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">📱 Line Type:</span>
                            <span class="result-value">${result.line_type}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">🕐 Timezone:</span>
                            <span class="result-value">${result.timezone.join(', ') || 'Unknown'}</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">✅ Is Valid:</span>
                            <span class="result-value ${result.is_valid ? 'status-valid' : 'status-invalid'}">
                                ${result.is_valid ? '✅ Yes' : '❌ No'}
                            </span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">🎯 Confidence Score:</span>
                            <span class="result-value">${(result.confidence_score * 100).toFixed(1)}%</span>
                        </div>
                        
                        <div class="result-row">
                            <span class="result-label">⏰ Analysis Time:</span>
                            <span class="result-value">${new Date(result.analysis_timestamp).toLocaleString()}</span>
                        </div>
                        
                        <div style="margin-top: 15px; padding: 10px; background: #fff3cd; border-radius: 5px; border-left: 4px solid #ffc107;">
                            <strong>⚠️ Educational Note:</strong> ${result.educational_note}
                        </div>
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
            lastResults = results;
        }
        
        function displayError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <div class="result-card">
                    <div style="color: #e74c3c; text-align: center; padding: 20px;">
                        <h3>❌ Error</h3>
                        <p>${message}</p>
                    </div>
                </div>
            `;
        }
        
        // Single number form handler
        document.getElementById('singleForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const phoneNumber = document.getElementById('phoneNumber').value.trim();
            
            if (!phoneNumber) {
                alert('Please enter a phone number');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ phone_number: phoneNumber })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults([data.result]);
                } else {
                    displayError(data.error || 'Analysis failed');
                }
            } catch (error) {
                displayError('Network error: ' + error.message);
            } finally {
                hideLoading();
            }
        });
        
        // Batch analysis form handler
        document.getElementById('batchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const phoneNumbers = document.getElementById('phoneNumbers').value
                .split('\n')
                .map(num => num.trim())
                .filter(num => num.length > 0);
            
            if (phoneNumbers.length === 0) {
                alert('Please enter at least one phone number');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/batch_analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ phone_numbers: phoneNumbers })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data.results);
                } else {
                    displayError(data.error || 'Batch analysis failed');
                }
            } catch (error) {
                displayError('Network error: ' + error.message);
            } finally {
                hideLoading();
            }
        });
        
        async function loadHistory() {
            try {
                const response = await fetch('/history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('historyContent');
                
                if (data.success && data.files.length > 0) {
                    let html = '<h3>📁 Recent Analysis Files:</h3><ul>';
                    data.files.forEach(file => {
                        html += `<li><a href="/download/${file.name}" target="_blank">${file.name}</a> (${file.modified})</li>`;
                    });
                    html += '</ul>';
                    historyDiv.innerHTML = html;
                } else {
                    historyDiv.innerHTML = '<p>📁 No analysis history found.</p>';
                }
            } catch (error) {
                document.getElementById('historyContent').innerHTML = '<p>❌ Error loading history: ' + error.message + '</p>';
            }
        }
        
        function downloadResults() {
            if (!lastResults) {
                alert('No results to download. Please run an analysis first.');
                return;
            }
            
            const dataStr = JSON.stringify(lastResults, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `phone_analysis_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
            link.click();
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE,
                                developer_name=DEVELOPER_INFO['name'],
                                developer_email=DEVELOPER_INFO['email'],
                                app_name=APP_SETTINGS['name'],
                                app_version=APP_SETTINGS['version'])

@app.route('/analyze', methods=['POST'])
def analyze_single():
    """Analyze single phone number"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number', '').strip()
        
        if not phone_number:
            return jsonify({
                'success': False,
                'error': 'Phone number is required'
            })
        
        # Perform analysis
        result = lookup_tool.comprehensive_analysis(phone_number)
        
        # Convert result to dict
        result_dict = {
            'phone_number': result.phone_number,
            'formatted_number': result.formatted_number,
            'country_code': result.country_code,
            'country_name': result.country_name,
            'region': result.region,
            'carrier': result.carrier,
            'line_type': result.line_type,
            'timezone': result.timezone,
            'is_valid': result.is_valid,
            'is_possible': result.is_possible,
            'analysis_timestamp': result.analysis_timestamp,
            'confidence_score': result.confidence_score,
            'educational_note': result.educational_note
        }
        
        # Save result
        lookup_tool.save_results([result])
        
        return jsonify({
            'success': True,
            'result': result_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        })

@app.route('/batch_analyze', methods=['POST'])
def analyze_batch():
    """Analyze multiple phone numbers"""
    try:
        data = request.get_json()
        phone_numbers = data.get('phone_numbers', [])
        
        if not phone_numbers:
            return jsonify({
                'success': False,
                'error': 'Phone numbers are required'
            })
        
        if len(phone_numbers) > 50:  # Limit batch size
            return jsonify({
                'success': False,
                'error': 'Maximum 50 phone numbers allowed per batch'
            })
        
        # Perform batch analysis
        results = lookup_tool.batch_analysis(phone_numbers)
        
        # Convert results to dict format
        results_dict = []
        for result in results:
            result_dict = {
                'phone_number': result.phone_number,
                'formatted_number': result.formatted_number,
                'country_code': result.country_code,
                'country_name': result.country_name,
                'region': result.region,
                'carrier': result.carrier,
                'line_type': result.line_type,
                'timezone': result.timezone,
                'is_valid': result.is_valid,
                'is_possible': result.is_possible,
                'analysis_timestamp': result.analysis_timestamp,
                'confidence_score': result.confidence_score,
                'educational_note': result.educational_note
            }
            results_dict.append(result_dict)
        
        # Save results
        lookup_tool.save_results(results)
        
        return jsonify({
            'success': True,
            'results': results_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Batch analysis failed: {str(e)}'
        })

@app.route('/history')
def get_history():
    """Get analysis history"""
    try:
        results_dir = lookup_tool.results_dir
        
        if not os.path.exists(results_dir):
            return jsonify({
                'success': True,
                'files': []
            })
        
        files = []
        for filename in os.listdir(results_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(results_dir, filename)
                mtime = os.path.getmtime(filepath)
                mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                files.append({
                    'name': filename,
                    'modified': mtime_str,
                    'timestamp': mtime
                })
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': files[:20]  # Return last 20 files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to load history: {str(e)}'
        })

@app.route('/download/<filename>')
def download_file(filename):
    """Download analysis file"""
    try:
        results_dir = lookup_tool.results_dir
        filepath = os.path.join(results_dir, filename)
        
        if not os.path.exists(filepath) or not filename.endswith('.json'):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Download failed: {str(e)}'
        }), 500

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'app_name': APP_SETTINGS['name'],
        'version': APP_SETTINGS['version'],
        'developer': DEVELOPER_INFO,
        'educational_note': DISCLAIMERS['educational_purpose'],
        'endpoints': {
            '/': 'Web interface',
            '/analyze': 'POST - Analyze single phone number',
            '/batch_analyze': 'POST - Analyze multiple phone numbers',
            '/history': 'GET - Get analysis history',
            '/download/<filename>': 'GET - Download analysis file',
            '/api/info': 'GET - API information'
        }
    })

def run_server(host='127.0.0.1', port=5000, debug=False):
    """Run the web server"""
    print(f"\n🌐 Starting Phone Lookup Web Interface...")
    print(f"📱 Developer: {DEVELOPER_INFO['name']}")
    print(f"📧 Email: {DEVELOPER_INFO['email']}")
    print(f"\n🔗 Access the web interface at: http://{host}:{port}")
    print(f"📊 API Info: http://{host}:{port}/api/info")
    print(f"\n⚠️ Educational Purpose Only - Use Responsibly!")
    print(f"\n🛑 Press Ctrl+C to stop the server\n")
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {str(e)}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Phone Lookup Web Interface')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Security warning for public access
    if args.host != '127.0.0.1' and args.host != 'localhost':
        print("\n⚠️ WARNING: You are binding to a public interface!")
        print("🔒 This tool is for educational purposes only.")
        print("🚫 Do not expose this to the public internet without proper security measures.")
        
        confirm = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("👋 Cancelled by user")
            return
    
    run_server(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()