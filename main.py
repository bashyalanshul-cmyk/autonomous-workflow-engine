#!/usr/bin/env python3
import sys
from pathlib import Path
from src.workflow.orchestrator import WorkflowOrchestrator


def main():
    print("\n🤖 Autonomous Corporate Workflow Engine")
    print("=" * 50)
    
    orchestrator = WorkflowOrchestrator()
    
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
    else:
        input_dir = Path("input_data")
        input_files = list(input_dir.glob("*.csv")) + list(input_dir.glob("*.xlsx")) + list(input_dir.glob("*.json"))
        
        if not input_files:
            print("\n📊 Creating sample data for demonstration...")
            create_sample_data()
            input_files = list(input_dir.glob("*.csv"))
            
    if input_files:
        orchestrator.run_complete_workflow(input_files)
    else:
        print("\n❌ No input files found!")
        print("   - Place CSV, Excel, or JSON files in input_data/")
        print("   - Or run: python main.py path/to/file1.csv path/to/file2.xlsx")


def create_sample_data():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    from config.config import INPUT_DIR
    
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
    
    df.to_csv(INPUT_DIR / "sample_corporate_data.csv", index=False)
    print(f"   ✓ Created sample data at {INPUT_DIR / 'sample_corporate_data.csv'}")


if __name__ == "__main__":
    main()
