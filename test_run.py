#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
from config.config import INPUT_DIR, OUTPUT_DIR
from src.core.data_processor import DataProcessor
from src.ai_insights.genai_analyzer import GenAIAnalyzer
from src.esg.esg_analyzer import ESGAnalyzer
from src.cybersecurity.risk_scanner import CybersecurityRiskScanner
from src.workflow.orchestrator import WorkflowOrchestrator
print("✓ All imports successful!")

print("\nCreating sample data...")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_records = 1000

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
print(f"✓ Created sample data at {sample_file}")

print("\nRunning workflow...")
orchestrator = WorkflowOrchestrator()
output_path = orchestrator.run_complete_workflow([sample_file])

print("\n✅ Test complete! Check output directory:", output_path)
