"""Report generation system for attack results."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64

from ..attacks.base_attack import AttackResult
from .evaluator import EvaluationResult


class ReportGenerator:
    """Generates comprehensive reports from attack results."""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "reports").mkdir(exist_ok=True)
        (self.output_dir / "charts").mkdir(exist_ok=True)
        (self.output_dir / "data").mkdir(exist_ok=True)
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates" / "reports"
        template_dir.mkdir(parents=True, exist_ok=True)
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def generate_comprehensive_report(
        self,
        results: List[AttackResult],
        evaluation: EvaluationResult,
        formats: List[str] = ["html", "json"],
        report_name: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate comprehensive report in multiple formats."""
        
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"prompt_injection_report_{timestamp}"
        
        generated_files = {}
        
        # Generate charts
        charts = self._generate_charts(results, evaluation)
        
        # Prepare report data
        report_data = self._prepare_report_data(results, evaluation, charts)
        
        # Generate requested formats
        if "json" in formats:
            json_file = self._generate_json_report(report_data, report_name)
            generated_files["json"] = json_file
        
        if "html" in formats:
            html_file = self._generate_html_report(report_data, report_name)
            generated_files["html"] = html_file
        
        if "pdf" in formats:
            # PDF generation would require additional dependencies
            # For now, we'll generate HTML and suggest PDF conversion
            generated_files["pdf"] = "PDF generation requires weasyprint - use HTML for now"
        
        return generated_files
    
    def _prepare_report_data(
        self,
        results: List[AttackResult],
        evaluation: EvaluationResult,
        charts: Dict[str, str]
    ) -> Dict[str, Any]:
        """Prepare all data needed for report generation."""
        
        # Convert results to serializable format
        results_data = []
        for result in results:
            results_data.append({
                "attack_id": result.attack_id,
                "attack_name": result.attack_name,
                "attack_type": result.attack_type,
                "payload": result.payload,
                "response": result.response,
                "success": result.success,
                "confidence": result.confidence,
                "risk_level": result.risk_level,
                "timestamp": result.timestamp.isoformat(),
                "provider": result.provider,
                "model": result.model,
                "latency": result.latency,
                "metadata": result.metadata
            })
        
        # Convert evaluation to serializable format
        evaluation_data = {
            "total_attacks": evaluation.total_attacks,
            "successful_attacks": evaluation.successful_attacks,
            "success_rate": evaluation.success_rate,
            "average_confidence": evaluation.average_confidence,
            "risk_distribution": evaluation.risk_distribution,
            "attack_type_breakdown": evaluation.attack_type_breakdown,
            "provider_analysis": evaluation.provider_analysis,
            "timestamp": evaluation.timestamp.isoformat(),
            "metadata": evaluation.metadata
        }
        
        return {
            "summary": {
                "report_title": "LLM Prompt Injection Security Assessment",
                "generated_at": datetime.now().isoformat(),
                "total_attacks": len(results),
                "success_rate": evaluation.success_rate,
                "risk_level": self._calculate_overall_risk(evaluation),
                "tested_providers": list(set(r.provider for r in results)),
                "attack_types": list(set(r.attack_type for r in results))
            },
            "results": results_data,
            "evaluation": evaluation_data,
            "charts": charts,
            "recommendations": self._generate_recommendations(evaluation)
        }
    
    def _generate_charts(
        self,
        results: List[AttackResult],
        evaluation: EvaluationResult
    ) -> Dict[str, str]:
        """Generate charts and return as base64 encoded strings."""
        charts = {}
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Success rate by attack type
        if evaluation.attack_type_breakdown:
            charts["attack_success_rates"] = self._create_attack_success_chart(evaluation.attack_type_breakdown)
        
        # Risk distribution
        if evaluation.risk_distribution:
            charts["risk_distribution"] = self._create_risk_distribution_chart(evaluation.risk_distribution)
        
        # Provider comparison
        if evaluation.provider_analysis:
            charts["provider_comparison"] = self._create_provider_comparison_chart(evaluation.provider_analysis)
        
        # Timeline chart
        charts["attack_timeline"] = self._create_timeline_chart(results)
        
        return charts
    
    def _create_attack_success_chart(self, attack_breakdown: Dict[str, Dict[str, Any]]) -> str:
        """Create attack success rate chart."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        attack_types = list(attack_breakdown.keys())
        success_rates = [data["success_rate"] * 100 for data in attack_breakdown.values()]
        
        bars = ax.bar(attack_types, success_rates)
        ax.set_ylabel('Success Rate (%)')
        ax.set_title('Attack Success Rate by Type')
        ax.set_ylim(0, 100)
        
        # Color bars by success rate
        for bar, rate in zip(bars, success_rates):
            if rate > 70:
                bar.set_color('red')
            elif rate > 40:
                bar.set_color('orange')
            else:
                bar.set_color('green')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _create_risk_distribution_chart(self, risk_distribution: Dict[str, int]) -> str:
        """Create risk distribution pie chart."""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        labels = list(risk_distribution.keys())
        sizes = list(risk_distribution.values())
        colors = {'low': 'green', 'medium': 'yellow', 'high': 'orange', 'critical': 'red'}
        
        pie_colors = [colors.get(label, 'gray') for label in labels]
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=pie_colors, startangle=90)
        ax.set_title('Risk Level Distribution')
        
        return self._fig_to_base64(fig)
    
    def _create_provider_comparison_chart(self, provider_analysis: Dict[str, Dict[str, Any]]) -> str:
        """Create provider vulnerability comparison chart."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        providers = list(provider_analysis.keys())
        success_rates = [data["success_rate"] * 100 for data in provider_analysis.values()]
        vulnerability_scores = [data.get("vulnerability_score", 0) * 100 for data in provider_analysis.values()]
        
        # Success rates
        ax1.bar(providers, success_rates, color='skyblue')
        ax1.set_ylabel('Success Rate (%)')
        ax1.set_title('Success Rate by Provider')
        ax1.set_ylim(0, 100)
        
        # Vulnerability scores
        ax2.bar(providers, vulnerability_scores, color='lightcoral')
        ax2.set_ylabel('Vulnerability Score (%)')
        ax2.set_title('Vulnerability Score by Provider')
        ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _create_timeline_chart(self, results: List[AttackResult]) -> str:
        """Create attack timeline chart."""
        if not results:
            return ""
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data
        timestamps = [r.timestamp for r in results]
        success_indicators = [1 if r.success else 0 for r in results]
        
        # Create scatter plot
        colors = ['red' if success else 'green' for success in success_indicators]
        ax.scatter(timestamps, success_indicators, c=colors, alpha=0.7)
        
        ax.set_ylabel('Attack Outcome (0=Failed, 1=Successful)')
        ax.set_title('Attack Timeline')
        ax.set_ylim(-0.1, 1.1)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string."""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        return image_base64
    
    def _generate_json_report(self, report_data: Dict[str, Any], report_name: str) -> str:
        """Generate JSON format report."""
        file_path = self.output_dir / "reports" / f"{report_name}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return str(file_path)
    
    def _generate_html_report(self, report_data: Dict[str, Any], report_name: str) -> str:
        """Generate HTML format report."""
        template = self.jinja_env.get_template('report_template.html')
        
        html_content = template.render(**report_data)
        
        file_path = self.output_dir / "reports" / f"{report_name}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(file_path)
    
    def _calculate_overall_risk(self, evaluation: EvaluationResult) -> str:
        """Calculate overall risk level."""
        if evaluation.success_rate > 0.7:
            return "Critical"
        elif evaluation.success_rate > 0.4:
            return "High"
        elif evaluation.success_rate > 0.2:
            return "Medium"
        else:
            return "Low"
    
    def _generate_recommendations(self, evaluation: EvaluationResult) -> List[str]:
        """Generate recommendations based on evaluation."""
        recommendations = []
        
        if evaluation.success_rate > 0.5:
            recommendations.append("Implement stronger input validation and sanitization")
            recommendations.append("Review and strengthen system prompts")
            recommendations.append("Add detection mechanisms for prompt injection attempts")
        
        if evaluation.success_rate > 0.3:
            recommendations.append("Regular security testing and monitoring")
            recommendations.append("User education about prompt injection risks")
        
        recommendations.append("Continue monitoring and testing with updated attack patterns")
        
        return recommendations
    
    def _create_default_templates(self):
        """Create default HTML template if it doesn't exist."""
        template_path = Path(self.jinja_env.loader.searchpath[0]) / "report_template.html"
        
        if not template_path.exists():
            template_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ summary.report_title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { border-bottom: 2px solid #333; padding-bottom: 20px; }
        .summary { background: #f5f5f5; padding: 20px; margin: 20px 0; }
        .chart { margin: 20px 0; text-align: center; }
        .results-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .results-table th, .results-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .results-table th { background-color: #f2f2f2; }
        .success { color: red; font-weight: bold; }
        .failure { color: green; }
        .risk-high { background-color: #ffcccc; }
        .risk-medium { background-color: #fff3cd; }
        .risk-low { background-color: #d4edda; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ summary.report_title }}</h1>
        <p>Generated: {{ summary.generated_at }}</p>
    </div>
    
    <div class="summary">
        <h2>Executive Summary</h2>
        <ul>
            <li>Total Attacks: {{ summary.total_attacks }}</li>
            <li>Success Rate: {{ "%.1f"|format(summary.success_rate * 100) }}%</li>
            <li>Overall Risk Level: {{ summary.risk_level }}</li>
            <li>Providers Tested: {{ summary.tested_providers|join(', ') }}</li>
        </ul>
    </div>
    
    {% if charts %}
    <div class="charts">
        <h2>Analysis Charts</h2>
        {% for chart_name, chart_data in charts.items() %}
        {% if chart_data %}
        <div class="chart">
            <h3>{{ chart_name|replace('_', ' ')|title }}</h3>
            <img src="data:image/png;base64,{{ chart_data }}" alt="{{ chart_name }}">
        </div>
        {% endif %}
        {% endfor %}
    </div>
    {% endif %}
    
    <div class="recommendations">
        <h2>Recommendations</h2>
        <ul>
            {% for rec in recommendations %}
            <li>{{ rec }}</li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="detailed-results">
        <h2>Detailed Results</h2>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Attack Type</th>
                    <th>Attack Name</th>
                    <th>Success</th>
                    <th>Confidence</th>
                    <th>Risk Level</th>
                    <th>Provider</th>
                    <th>Model</th>
                </tr>
            </thead>
            <tbody>
                {% for result in results %}
                <tr class="risk-{{ result.risk_level }}">
                    <td>{{ result.attack_type }}</td>
                    <td>{{ result.attack_name }}</td>
                    <td class="{% if result.success %}success{% else %}failure{% endif %}">
                        {{ 'SUCCESS' if result.success else 'FAILED' }}
                    </td>
                    <td>{{ "%.2f"|format(result.confidence) }}</td>
                    <td>{{ result.risk_level|upper }}</td>
                    <td>{{ result.provider }}</td>
                    <td>{{ result.model }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
            '''
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)