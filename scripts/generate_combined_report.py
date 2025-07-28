#!/usr/bin/env python3
"""
Combined Report Generator for Hybrid API Automation Framework
Generates a comprehensive HTML report combining results from all testing frameworks
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path


class CombinedReportGenerator:
    """Generates combined reports from multiple testing frameworks."""
    
    def __init__(self):
        self.reports_dir = Path("reports")
        self.output_file = self.reports_dir / "combined-report.html"
        self.framework_results = {}
        
    def collect_results(self):
        """Collect results from all testing frameworks."""
        print("Collecting test results from all frameworks...")
        
        # Collect REST Assured results
        self._collect_rest_assured_results()
        
        # Collect Python results
        self._collect_python_results()
        
        # Collect Postman results
        self._collect_postman_results()
        
        # Collect Karate results
        self._collect_karate_results()
        
    def _collect_rest_assured_results(self):
        """Collect REST Assured test results."""
        surefire_dir = Path("target/surefire-reports")
        if surefire_dir.exists():
            test_files = list(surefire_dir.glob("TEST-*.xml"))
            if test_files:
                self.framework_results["rest_assured"] = {
                    "framework": "REST Assured (Java)",
                    "status": "completed",
                    "test_files": len(test_files),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.framework_results["rest_assured"] = {
                    "framework": "REST Assured (Java)",
                    "status": "no_results",
                    "message": "No test results found"
                }
        else:
            self.framework_results["rest_assured"] = {
                "framework": "REST Assured (Java)",
                "status": "not_run",
                "message": "Test directory not found"
            }
    
    def _collect_python_results(self):
        """Collect Python test results."""
        pytest_report = self.reports_dir / "pytest-report.html"
        if pytest_report.exists():
            self.framework_results["python"] = {
                "framework": "Pytest (Python)",
                "status": "completed",
                "report_file": str(pytest_report),
                "timestamp": datetime.now().isoformat()
            }
        else:
            self.framework_results["python"] = {
                "framework": "Pytest (Python)",
                "status": "not_run",
                "message": "No pytest report found"
            }
    
    def _collect_postman_results(self):
        """Collect Postman test results."""
        newman_report = self.reports_dir / "newman-report.html"
        if newman_report.exists():
            self.framework_results["postman"] = {
                "framework": "Newman (Postman)",
                "status": "completed",
                "report_file": str(newman_report),
                "timestamp": datetime.now().isoformat()
            }
        else:
            self.framework_results["postman"] = {
                "framework": "Newman (Postman)",
                "status": "not_run",
                "message": "No Newman report found"
            }
    
    def _collect_karate_results(self):
        """Collect Karate test results."""
        karate_dir = Path("target/karate-reports")
        if karate_dir.exists():
            karate_files = list(karate_dir.glob("*.html"))
            if karate_files:
                self.framework_results["karate"] = {
                    "framework": "Karate Framework",
                    "status": "completed",
                    "report_files": len(karate_files),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.framework_results["karate"] = {
                    "framework": "Karate Framework",
                    "status": "no_results",
                    "message": "No Karate reports found"
                }
        else:
            self.framework_results["karate"] = {
                "framework": "Karate Framework",
                "status": "not_run",
                "message": "Karate reports directory not found"
            }
    
    def generate_html_report(self):
        """Generate the combined HTML report."""
        print(f"Generating combined report: {self.output_file}")
        
        html_content = self._generate_html_content()
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(exist_ok=True)
        
        # Write HTML file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Combined report generated successfully: {self.output_file}")
    
    def _generate_html_content(self):
        """Generate the HTML content for the combined report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Count completed frameworks
        completed_count = sum(1 for result in self.framework_results.values() 
                            if result.get("status") == "completed")
        total_count = len(self.framework_results)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hybrid API Automation Framework - Combined Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .summary {{
            padding: 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .summary-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .framework-results {{
            padding: 20px;
        }}
        .framework-card {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .framework-header {{
            padding: 15px 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .framework-name {{
            font-weight: bold;
            color: #333;
        }}
        .status-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .status-completed {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status-not_run {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .status-no_results {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .framework-body {{
            padding: 20px;
        }}
        .framework-details {{
            color: #666;
            line-height: 1.6;
        }}
        .report-link {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background-color: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}
        .report-link:hover {{
            background-color: #5a6fd8;
        }}
        .footer {{
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Hybrid API Automation Framework</h1>
            <p>Combined Test Execution Report</p>
            <p>Generated on: {timestamp}</p>
        </div>
        
        <div class="summary">
            <h2>Execution Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Frameworks</h3>
                    <div class="number">{total_count}</div>
                    <p>Total Frameworks</p>
                </div>
                <div class="summary-card">
                    <h3>Completed</h3>
                    <div class="number">{completed_count}</div>
                    <p>Successful Executions</p>
                </div>
                <div class="summary-card">
                    <h3>Success Rate</h3>
                    <div class="number">{int((completed_count/total_count)*100) if total_count > 0 else 0}%</div>
                    <p>Overall Success</p>
                </div>
            </div>
        </div>
        
        <div class="framework-results">
            <h2>Framework Results</h2>
"""
        
        # Add framework results
        for framework_key, result in self.framework_results.items():
            status_class = f"status-{result['status']}"
            status_text = result['status'].replace('_', ' ').title()
            
            html += f"""
            <div class="framework-card">
                <div class="framework-header">
                    <div class="framework-name">{result['framework']}</div>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                <div class="framework-body">
                    <div class="framework-details">
"""
            
            if result['status'] == 'completed':
                html += f"<p><strong>Status:</strong> Successfully completed</p>"
                html += f"<p><strong>Timestamp:</strong> {result['timestamp']}</p>"
                
                if 'report_file' in result:
                    html += f'<a href="{result["report_file"]}" class="report-link" target="_blank">View Detailed Report</a>'
                elif 'test_files' in result:
                    html += f"<p><strong>Test Files:</strong> {result['test_files']}</p>"
                elif 'report_files' in result:
                    html += f"<p><strong>Report Files:</strong> {result['report_files']}</p>"
            else:
                html += f"<p><strong>Status:</strong> {result.get('message', 'Not executed')}</p>"
            
            html += """
                    </div>
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <p>Hybrid API Automation Framework - Comprehensive Testing Solution</p>
            <p>Supporting REST Assured, Pytest, Postman, and Karate frameworks</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html


def main():
    """Main function to generate combined report."""
    print("=" * 60)
    print("Hybrid API Automation Framework - Combined Report Generator")
    print("=" * 60)
    
    generator = CombinedReportGenerator()
    
    try:
        # Collect results from all frameworks
        generator.collect_results()
        
        # Generate combined HTML report
        generator.generate_html_report()
        
        print("\n" + "=" * 60)
        print("✅ Combined report generation completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error generating combined report: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 