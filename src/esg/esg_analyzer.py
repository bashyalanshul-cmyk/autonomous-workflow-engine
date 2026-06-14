import pandas as pd
import json
from datetime import datetime
import re


class ESGAnalyzer:
    def __init__(self):
        self.esg_keywords = {
            "environmental": ["carbon", "emission", "energy", "sustainability", "green", "waste", "water", "climate", "renewable", "pollution"],
            "social": ["employee", "labor", "health", "safety", "community", "diversity", "inclusion", "human rights", "philanthropy"],
            "governance": ["board", "audit", "compliance", "ethics", "transparency", "risk", "policy", "regulation", "accountability"]
        }
        
    def analyze_esg(self, df, dataset_name):
        esg_score = {
            "dataset_name": dataset_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "environmental_score": 0,
            "social_score": 0,
            "governance_score": 0,
            "overall_esg_score": 0,
            "esg_indicators_found": [],
            "recommendations": []
        }
        
        text_content = str(df.columns.tolist()) + " " + str(df.head(20).values.flatten().tolist())
        text_content = text_content.lower()
        
        for category, keywords in self.esg_keywords.items():
            found_keywords = []
            for keyword in keywords:
                if keyword in text_content:
                    found_keywords.append(keyword)
                    
            score = min(100, len(found_keywords) * 20)
            esg_score[f"{category}_score"] = score
            
            if found_keywords:
                esg_score["esg_indicators_found"].append({
                    "category": category,
                    "keywords": found_keywords
                })
                
        esg_score["overall_esg_score"] = (
            esg_score["environmental_score"] * 0.35 +
            esg_score["social_score"] * 0.35 +
            esg_score["governance_score"] * 0.30
        )
        
        if esg_score["overall_esg_score"] < 30:
            esg_score["recommendations"].append("Implement ESG data tracking for environmental impact")
            esg_score["recommendations"].append("Develop social responsibility metrics")
        elif esg_score["overall_esg_score"] < 70:
            esg_score["recommendations"].append("Enhance ESG reporting transparency")
            esg_score["recommendations"].append("Set measurable ESG targets")
        else:
            esg_score["recommendations"].append("Maintain strong ESG performance")
            esg_score["recommendations"].append("Consider ESG certification")
            
        return esg_score
        
    def save_esg_analysis(self, analysis, output_path):
        with open(output_path / "esg_analysis.json", 'w') as f:
            json.dump(analysis, f, indent=2)
