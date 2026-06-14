import pandas as pd
import json
from datetime import datetime
import random
import os
from config.config import OPENAI_API_KEY


class GenAIAnalyzer:
    def __init__(self, demo_mode=None):
        if demo_mode is None:
            demo_mode = (OPENAI_API_KEY == "demo_mode" or not OPENAI_API_KEY)
        self.demo_mode = demo_mode
        self.client = None
        
        if not self.demo_mode:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                print("   ✓ OpenAI API initialized successfully!")
            except ImportError:
                print("   ⚠️ OpenAI package not found, falling back to demo mode")
                self.demo_mode = True
            except Exception as e:
                print(f"   ⚠️ OpenAI API error: {str(e)}, falling back to demo mode")
                self.demo_mode = True
        
    def generate_insights(self, df, dataset_name):
        if self.demo_mode:
            return self._demo_insights(df, dataset_name)
        else:
            return self._api_insights(df, dataset_name)
            
    def _demo_insights(self, df, dataset_name):
        insights = {
            "dataset_name": dataset_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "key_findings": [],
            "recommendations": [],
            "data_quality_score": 0,
            "business_impact": "",
            "demo_mode": True
        }
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if numeric_cols:
            insights["key_findings"].append(f"Dataset contains {len(numeric_cols)} numerical metrics")
            for col in numeric_cols[:3]:
                mean_val = df[col].mean()
                insights["key_findings"].append(f"Average {col}: {mean_val:.2f}")
                
        if categorical_cols:
            insights["key_findings"].append(f"Dataset contains {len(categorical_cols)} categorical attributes")
            for col in categorical_cols[:2]:
                unique_count = df[col].nunique()
                insights["key_findings"].append(f"{col} has {unique_count} unique values")
                
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        insights["data_quality_score"] = max(0, 100 - missing_pct)
        
        insights["recommendations"] = [
            "Consider feature engineering on numerical columns for better predictive power",
            "Validate categorical data consistency across sources",
            "Implement automated data quality monitoring",
            "Create visual dashboards for key metrics"
        ]
        
        insights["business_impact"] = f"This dataset can drive {random.choice(['optimize operations', 'enhance customer insights', 'improve decision-making', 'reduce costs'])} by 15-25%"
        
        return insights
        
    def _api_insights(self, df, dataset_name):
        try:
            # Create a summary of the data for the API
            summary_data = {
                "dataset_name": dataset_name,
                "shape": f"{len(df)} rows, {len(df.columns)} columns",
                "columns": list(df.columns),
                "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
                "categorical_info": {col: df[col].nunique() for col in df.select_dtypes(include=['object']).columns}
            }
            
            prompt = f"""You are a data analyst. Analyze this dataset and provide insights in JSON format only:

Dataset Summary:
{json.dumps(summary_data, indent=2)}

Please provide:
1. key_findings: list of 3-5 key findings about the data
2. recommendations: list of 3-4 actionable recommendations
3. business_impact: short (1-2 sentence) explanation of business value
4. data_quality_score: number from 0-100 based on missing values and data types

Return ONLY valid JSON, no other text."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a helpful data analyst that returns ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse the JSON
            try:
                insights = json.loads(content)
            except:
                # If JSON parsing fails, try to extract JSON from response
                import re
                match = re.search(r'\{[\s\S]*\}', content)
                if match:
                    insights = json.loads(match.group(0))
                else:
                    raise ValueError("Could not parse JSON from response")
            
            insights["dataset_name"] = dataset_name
            insights["analysis_timestamp"] = datetime.now().isoformat()
            insights["demo_mode"] = False
            
            return insights
            
        except Exception as e:
            print(f"   ⚠️ API failed: {str(e)}, falling back to demo mode")
            return self._demo_insights(df, dataset_name)
        
    def save_insights(self, insights, output_path):
        with open(output_path / "ai_insights.json", 'w') as f:
            json.dump(insights, f, indent=2)
