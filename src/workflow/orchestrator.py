import os
import json
from datetime import datetime
from pathlib import Path
from config.config import OUTPUT_DIR
from src.core.data_processor import DataProcessor, convert_numpy_types
from src.ai_insights.genai_analyzer import GenAIAnalyzer
from src.esg.esg_analyzer import ESGAnalyzer
from src.cybersecurity.risk_scanner import CybersecurityRiskScanner
from src.visualizations.visualizer import DataVisualizer


class WorkflowOrchestrator:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.genai_analyzer = GenAIAnalyzer(demo_mode=True)
        self.esg_analyzer = ESGAnalyzer()
        self.cybersecurity_scanner = CybersecurityRiskScanner()
        self.visualizer = DataVisualizer()
        
    def run_complete_workflow(self, input_files):
        workflow_id = self.data_processor.session_id
        timestamp = self.data_processor.timestamp
        output_subdir = f"workflow_{workflow_id}_{timestamp}"
        
        print(f"🚀 Starting Autonomous Workflow Engine - Session: {workflow_id}")
        print("=" * 70)
        
        all_insights = []
        all_esg = []
        all_security = []
        all_charts = []
        
        for file_path in input_files:
            print(f"\n📄 Processing: {Path(file_path).name}")
            
            try:
                df = self.data_processor.ingest_file(file_path)
                print(f"   ✓ Data ingested successfully: {len(df)} rows, {len(df.columns)} columns")
                
                dataset_name = Path(file_path).stem
                
                insights = self.genai_analyzer.generate_insights(df, dataset_name)
                all_insights.append(insights)
                print(f"   ✓ AI Insights generated - Quality Score: {insights['data_quality_score']:.1f}%")
                
                esg = self.esg_analyzer.analyze_esg(df, dataset_name)
                all_esg.append(esg)
                print(f"   ✓ ESG Analysis complete - Score: {esg['overall_esg_score']:.1f}%")
                
                security = self.cybersecurity_scanner.scan_data(df, dataset_name)
                all_security.append(security)
                print(f"   ✓ Security Scan complete - Risk: {security['risk_level']}")
                
            except Exception as e:
                print(f"   ✗ Error processing {Path(file_path).name}: {str(e)}")
                
        output_path = self.data_processor.save_processed_data(output_subdir)
        
        # Save all results
        self.genai_analyzer.save_insights(convert_numpy_types({"all_insights": all_insights}), output_path)
        self.esg_analyzer.save_esg_analysis(convert_numpy_types({"all_esg": all_esg}), output_path)
        self.cybersecurity_scanner.save_risk_report(convert_numpy_types({"all_security": all_security}), output_path)
        
        # Generate visualizations
        print(f"\n📊 Generating visualizations...")
        for file_path in input_files:
            try:
                df = self.data_processor.processed_data[Path(file_path).stem]
                dataset_name = Path(file_path).stem
                charts = self.visualizer.generate_all_visualizations(df, dataset_name, output_path)
                all_charts.extend(charts)
                if charts:
                    print(f"   ✓ Generated {len(charts)} charts for {dataset_name}")
            except Exception as e:
                print(f"   ✗ Could not generate charts for {Path(file_path).name}: {str(e)}")
        
        self._create_executive_summary(output_path, all_insights, all_esg, all_security, all_charts)
        
        print("\n" + "=" * 70)
        print(f"✅ Workflow complete! Output saved to: {output_path}")
        
        return output_path
        
    def _create_executive_summary(self, output_path, insights, esg, security, charts=None):
        summary = {
            "executive_summary": {
                "generated_at": datetime.now().isoformat(),
                "total_datasets": len(insights),
                "average_data_quality": sum(i['data_quality_score'] for i in insights) / len(insights) if insights else 0,
                "average_esg_score": sum(e['overall_esg_score'] for e in esg) / len(esg) if esg else 0,
                "overall_risk_level": max(s['risk_level'] for s in security) if security else "Low",
                "charts_generated": len(charts) if charts else 0,
                "key_highlights": [
                    "End-to-end autonomous data processing complete",
                    "AI-powered insights generated for all datasets",
                    "ESG performance evaluated",
                    "Cybersecurity risk assessment conducted",
                    "Visualizations automatically created"
                ],
                "action_items": []
            }
        }
        
        with open(output_path / "EXECUTIVE_SUMMARY.json", 'w') as f:
            json.dump(summary, f, indent=2)
            
        with open(output_path / "README.md", 'w') as f:
            f.write(f"# Autonomous Workflow Engine Output\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Directory Structure\n\n")
            f.write("- `*_cleaned.csv` - Processed and cleaned datasets\n")
            f.write("- `*_analysis.json` - Data quality and statistical analysis\n")
            f.write("- `ai_insights.json` - AI-generated business insights\n")
            f.write("- `esg_analysis.json` - ESG performance metrics\n")
            f.write("- `cybersecurity_risk_report.json` - Security risk assessment\n")
            f.write("- `EXECUTIVE_SUMMARY.json` - High-level overview\n")
            f.write("- `session_metadata.json` - Processing session details\n")
            f.write("- `charts/` - Directory with visualization PNG files\n")
