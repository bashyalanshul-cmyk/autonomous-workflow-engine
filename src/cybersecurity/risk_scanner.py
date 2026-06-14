import pandas as pd
import json
from datetime import datetime
import re


class CybersecurityRiskScanner:
    def __init__(self):
        self.sensitive_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            "ssn": r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b',
            "credit_card": r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\b',
            "ip_address": r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            "password": r'\bpassword\b|\bpasswd\b',
            "api_key": r'\bapi[_-]?key\b|\bsecret[_-]?key\b'
        }
        
    def scan_data(self, df, dataset_name):
        risk_report = {
            "dataset_name": dataset_name,
            "scan_timestamp": datetime.now().isoformat(),
            "risk_level": "Low",
            "risk_score": 0,
            "findings": [],
            "recommendations": []
        }
        
        text_content = str(df.columns.tolist()) + " " + str(df.head(50).values.flatten().tolist())
        text_content = text_content.lower()
        
        for data_type, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                risk_report["findings"].append({
                    "data_type": data_type,
                    "matches_found": len(matches),
                    "severity": "High" if data_type in ["ssn", "credit_card", "api_key"] else "Medium"
                })
                
        high_risk = sum(1 for f in risk_report["findings"] if f["severity"] == "High")
        medium_risk = sum(1 for f in risk_report["findings"] if f["severity"] == "Medium")
        
        risk_score = high_risk * 30 + medium_risk * 15
        risk_report["risk_score"] = min(100, risk_score)
        
        if risk_score > 70:
            risk_report["risk_level"] = "Critical"
        elif risk_score > 40:
            risk_report["risk_level"] = "High"
        elif risk_score > 20:
            risk_report["risk_level"] = "Medium"
            
        if risk_report["findings"]:
            risk_report["recommendations"].append("Anonymize or encrypt sensitive personal data")
            risk_report["recommendations"].append("Implement access controls for sensitive information")
            risk_report["recommendations"].append("Remove API keys and credentials from datasets")
            
        risk_report["recommendations"].append("Regular security audits of data pipelines")
        risk_report["recommendations"].append("Implement data masking for production environments")
        
        return risk_report
        
    def save_risk_report(self, report, output_path):
        with open(output_path / "cybersecurity_risk_report.json", 'w') as f:
            json.dump(report, f, indent=2)
