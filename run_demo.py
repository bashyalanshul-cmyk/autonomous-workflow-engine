#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n🤖 AUTONOMOUS CORPORATE WORKFLOW ENGINE")
print("=" * 70)

print("\n[1/8] Loading modules...")
from config.config import INPUT_DIR, OUTPUT_DIR
print("   ✓ Config loaded")

from src.core.data_processor import DataProcessor, convert_numpy_types
print("   ✓ Data processor loaded")

from src.ai_insights.genai_analyzer import GenAIAnalyzer
print("   ✓ AI analyzer loaded")

from src.esg.esg_analyzer import ESGAnalyzer
print("   ✓ ESG analyzer loaded")

from src.cybersecurity.risk_scanner import CybersecurityRiskScanner
print("   ✓ Security scanner loaded")

from src.visualizations.visualizer import DataVisualizer
print("   ✓ Visualizer loaded")

from src.workflow.orchestrator import WorkflowOrchestrator
print("   ✓ Orchestrator loaded")

print("\n[2/8] Creating sample data...")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_records = 100

dates = [datetime.now() - timedelta(days=i) for i in range(n_records)]
departments = np.random.choice(['Sales', 'Engineering', 'HR', 'Finance', 'Marketing'], n_records)
revenue = np.random.normal(50000, 15000, n_records)
expenses = revenue * np.random.uniform(0.4, 0.8, n_records)
employees = np.random.randint(5, 50, n_records)
carbon_footprint = np.random.uniform(100, 1000, n_records)
satisfaction_score = np.random.uniform(3.0, 5.0, n_records)

df = pd.DataFrame({
    'date': dates,
    'department': departments,
    'revenue': revenue,
    'expenses': expenses,
    'employee_count': employees,
    'carbon_emissions_kg': carbon_footprint,
    'employee_satisfaction': satisfaction_score
})

os.makedirs(INPUT_DIR, exist_ok=True)
sample_file = INPUT_DIR / "sample_corporate_data.csv"
df.to_csv(sample_file, index=False)
print(f"   ✓ Created {sample_file.name} with {n_records} records")

print("\n[3/8] Initializing processor...")
processor = DataProcessor()
print(f"   ✓ Session ID: {processor.session_id}")

print("\n[4/8] Ingesting data...")
data = processor.ingest_file(sample_file)
print(f"   ✓ Rows: {len(data)}, Columns: {len(data.columns)}")

print("\n[5/8] Generating insights...")
ai_analyzer = GenAIAnalyzer()
insights = ai_analyzer.generate_insights(data, "sample_corporate_data")
print(f"   ✓ Data quality score: {insights['data_quality_score']:.1f}%")

print("\n[6/8] ESG & Security analysis...")
esg_analyzer = ESGAnalyzer()
esg = esg_analyzer.analyze_esg(data, "sample_corporate_data")
print(f"   ✓ ESG score: {esg['overall_esg_score']:.1f}%")

security_scanner = CybersecurityRiskScanner()
security = security_scanner.scan_data(data, "sample_corporate_data")
print(f"   ✓ Security risk: {security['risk_level']}")

print("\n[7/8] Generating visualizations...")
visualizer = DataVisualizer()
output_subdir = f"demo_{processor.session_id}_{processor.timestamp}"
output_path = processor.save_processed_data(output_subdir)
charts = visualizer.generate_all_visualizations(data, "sample_corporate_data", output_path)
print(f"   ✓ Generated {len(charts)} charts!")

print("\n[8/8] Saving all results...")
ai_analyzer.save_insights(convert_numpy_types({"all_insights": [insights]}), output_path)
esg_analyzer.save_esg_analysis(convert_numpy_types({"all_esg": [esg]}), output_path)
security_scanner.save_risk_report(convert_numpy_types({"all_security": [security]}), output_path)
print(f"   ✓ All output saved to: {output_path}")

print("\n" + "=" * 70)
print("✅ DEMO COMPLETE!")
print("\nWhat makes this unique:")
print("  • Combines data processing + GenAI insights + ESG + cybersecurity")
print("  • Automatically creates structured output directory")
print("  • Multi-layered analysis in one autonomous workflow")
print("  • Beautiful visualizations included! 📊")
print("\nOutput directory contents:")
for item in sorted(os.listdir(output_path)):
    print(f"  - {item}")
