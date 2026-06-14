import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.switch_backend('Agg')  # Non-interactive backend


class DataVisualizer:
    def __init__(self):
        pass
    
    def generate_all_visualizations(self, df, dataset_name, output_path):
        """Generate all visualizations for a dataset"""
        charts_dir = output_path / "charts"
        charts_dir.mkdir(exist_ok=True)
        
        charts = []
        
        # Revenue & Expenses Over Time (if date column exists)
        if 'date' in df.columns:
            chart_path = self._plot_revenue_expenses_over_time(df, dataset_name, charts_dir)
            if chart_path:
                charts.append(chart_path)
        
        # Revenue by Department (if department exists)
        if 'department' in df.columns and 'revenue' in df.columns:
            chart_path = self._plot_revenue_by_department(df, dataset_name, charts_dir)
            if chart_path:
                charts.append(chart_path)
        
        # Expenses vs Revenue Scatter Plot
        if 'revenue' in df.columns and 'expenses' in df.columns:
            chart_path = self._plot_revenue_vs_expenses(df, dataset_name, charts_dir)
            if chart_path:
                charts.append(chart_path)
        
        # Carbon Emissions Distribution
        if 'carbon_emissions_kg' in df.columns:
            chart_path = self._plot_carbon_distribution(df, dataset_name, charts_dir)
            if chart_path:
                charts.append(chart_path)
        
        # Employee Satisfaction Distribution
        if 'employee_satisfaction' in df.columns:
            chart_path = self._plot_satisfaction_distribution(df, dataset_name, charts_dir)
            if chart_path:
                charts.append(chart_path)
        
        # Correlation Heatmap (numeric columns)
        chart_path = self._plot_correlation_heatmap(df, dataset_name, charts_dir)
        if chart_path:
            charts.append(chart_path)
        
        return charts
    
    def _plot_revenue_expenses_over_time(self, df, dataset_name, output_dir):
        try:
            df_plot = df.copy()
            df_plot['date'] = pd.to_datetime(df_plot['date'])
            df_plot = df_plot.sort_values('date')
            
            plt.figure(figsize=(12, 6))
            plt.plot(df_plot['date'], df_plot['revenue'], label='Revenue', marker='o', linewidth=2)
            plt.plot(df_plot['date'], df_plot['expenses'], label='Expenses', marker='s', linewidth=2)
            plt.title(f'Revenue & Expenses Over Time - {dataset_name}', fontsize=14, pad=20)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Amount ($)', fontsize=12)
            plt.legend(fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_path = output_dir / f"{dataset_name}_revenue_expenses_trend.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        except Exception as e:
            print(f"Warning: Could not create revenue/expenses plot: {e}")
            plt.close()
            return None
    
    def _plot_revenue_by_department(self, df, dataset_name, output_dir):
        try:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='department', y='revenue', data=df, hue='department', palette='viridis', legend=False)
            plt.title(f'Revenue Distribution by Department - {dataset_name}', fontsize=14, pad=20)
            plt.xlabel('Department', fontsize=12)
            plt.ylabel('Revenue ($)', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_path = output_dir / f"{dataset_name}_revenue_by_department.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        except Exception as e:
            print(f"Warning: Could not create department revenue plot: {e}")
            plt.close()
            return None
    
    def _plot_revenue_vs_expenses(self, df, dataset_name, output_dir):
        try:
            plt.figure(figsize=(10, 8))
            scatter = plt.scatter(df['revenue'], df['expenses'], c=df.get('employee_satisfaction', [0]*len(df)), 
                                cmap='coolwarm', s=100, alpha=0.7)
            plt.colorbar(scatter, label='Employee Satisfaction' if 'employee_satisfaction' in df.columns else '')
            plt.title(f'Revenue vs Expenses - {dataset_name}', fontsize=14, pad=20)
            plt.xlabel('Revenue ($)', fontsize=12)
            plt.ylabel('Expenses ($)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            output_path = output_dir / f"{dataset_name}_revenue_vs_expenses.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        except Exception as e:
            print(f"Warning: Could not create scatter plot: {e}")
            plt.close()
            return None
    
    def _plot_carbon_distribution(self, df, dataset_name, output_dir):
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(df['carbon_emissions_kg'], bins=20, kde=True, color='forestgreen', edgecolor='black')
            plt.title(f'Carbon Emissions Distribution - {dataset_name}', fontsize=14, pad=20)
            plt.xlabel('Carbon Emissions (kg)', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.tight_layout()
            
            output_path = output_dir / f"{dataset_name}_carbon_distribution.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        except Exception as e:
            print(f"Warning: Could not create carbon plot: {e}")
            plt.close()
            return None
    
    def _plot_satisfaction_distribution(self, df, dataset_name, output_dir):
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(df['employee_satisfaction'], bins=15, kde=True, color='royalblue', edgecolor='black')
            plt.title(f'Employee Satisfaction Distribution - {dataset_name}', fontsize=14, pad=20)
            plt.xlabel('Satisfaction Score (1-5)', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.tight_layout()
            
            output_path = output_dir / f"{dataset_name}_satisfaction_distribution.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return output_path
        except Exception as e:
            print(f"Warning: Could not create satisfaction plot: {e}")
            plt.close()
            return None
    
    def _plot_correlation_heatmap(self, df, dataset_name, output_dir):
        try:
            numeric_df = df.select_dtypes(include=['number'])
            if len(numeric_df.columns) > 1:
                plt.figure(figsize=(10, 8))
                corr_matrix = numeric_df.corr()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                           square=True, linewidths=1, cbar_kws={"shrink": 0.8})
                plt.title(f'Correlation Heatmap - {dataset_name}', fontsize=14, pad=20)
                plt.tight_layout()
                
                output_path = output_dir / f"{dataset_name}_correlation_heatmap.png"
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                return output_path
        except Exception as e:
            print(f"Warning: Could not create correlation heatmap: {e}")
            plt.close()
            return None

