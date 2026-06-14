#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path
import json

# Add our project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import INPUT_DIR, OUTPUT_DIR
from src.workflow.orchestrator import WorkflowOrchestrator
from src.core.data_processor import DataProcessor

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload
app.config['UPLOAD_FOLDER'] = INPUT_DIR

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # List previous runs
    runs = []
    if OUTPUT_DIR.exists():
        for run_dir in sorted(OUTPUT_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if run_dir.is_dir():
                summary_file = run_dir / "EXECUTIVE_SUMMARY.json"
                summary = {}
                if summary_file.exists():
                    try:
                        with open(summary_file) as f:
                            summary = json.load(f).get("executive_summary", {})
                    except:
                        pass
                runs.append({
                    "id": run_dir.name,
                    "date": summary.get("generated_at", ""),
                    "datasets": summary.get("total_datasets", 0),
                    "charts": summary.get("charts_generated", 0),
                    "risk_level": summary.get("overall_risk_level", "Unknown")
                })
    return render_template('index.html', runs=runs)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return redirect(url_for('index'))
        
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return redirect(url_for('index'))
    
    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_files.append(file_path)
    
    if saved_files:
        # Run the workflow
        orchestrator = WorkflowOrchestrator()
        output_path = orchestrator.run_complete_workflow(saved_files)
        return redirect(url_for('view_run', run_id=output_path.name))
    
    return redirect(url_for('index'))


@app.route('/run/<run_id>')
def view_run(run_id):
    run_dir = OUTPUT_DIR / run_id
    if not run_dir.exists():
        return "Run not found!", 404
    
    # Load all data
    data = {"run_id": run_id}
    
    # Load executive summary
    summary_file = run_dir / "EXECUTIVE_SUMMARY.json"
    if summary_file.exists():
        try:
            with open(summary_file) as f:
                data["summary"] = json.load(f)
        except:
            data["summary"] = {}
    
    # Load AI insights
    insights_file = run_dir / "ai_insights.json"
    if insights_file.exists():
        try:
            with open(insights_file) as f:
                data["insights"] = json.load(f)
        except:
            data["insights"] = {}
    
    # Load ESG analysis
    esg_file = run_dir / "esg_analysis.json"
    if esg_file.exists():
        try:
            with open(esg_file) as f:
                data["esg"] = json.load(f)
        except:
            data["esg"] = {}
    
    # Load security report
    security_file = run_dir / "cybersecurity_risk_report.json"
    if security_file.exists():
        try:
            with open(security_file) as f:
                data["security"] = json.load(f)
        except:
            data["security"] = {}
    
    # Get charts
    charts_dir = run_dir / "charts"
    data["charts"] = []
    if charts_dir.exists():
        data["charts"] = sorted([f.name for f in charts_dir.glob("*.png")])
    
    # Get cleaned data files
    data["cleaned_files"] = sorted([f.name for f in run_dir.glob("*_cleaned.csv")])
    
    return render_template('view_run.html', data=data)


@app.route('/chart/<run_id>/<filename>')
def serve_chart(run_id, filename):
    return send_from_directory(OUTPUT_DIR / run_id / "charts", filename)


@app.route('/download/<run_id>/<filename>')
def download_file(run_id, filename):
    return send_from_directory(OUTPUT_DIR / run_id, filename, as_attachment=True)


if __name__ == '__main__':
    print("\n⚡ Starting DataPulse AI Dashboard!")
    print("=" * 60)
    print("Open your browser and go to: http://localhost:5001")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)