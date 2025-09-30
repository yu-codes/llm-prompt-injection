"""
Attack Test Report Generator
攻擊測試報告生成器

Generates comprehensive reports from attack test results.
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Template

from .attacks import AttackResult


class AttackReportGenerator:
    """攻擊測試報告生成器"""
    
    def __init__(self, output_dir: str = "output"):
        """初始化報告生成器"""
        # 確保報告保存在 reports 子目錄中
        self.base_output_dir = Path(output_dir)
        self.output_dir = self.base_output_dir / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 同時創建其他需要的子目錄
        (self.base_output_dir / "data").mkdir(exist_ok=True)
        (self.base_output_dir / "charts").mkdir(exist_ok=True)
    
    def generate_markdown_report(self, summary: Dict[str, Any], filename: str = None) -> str:
        """生成Markdown格式報告"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attack_test_report_{timestamp}.md"
        
        report_path = self.output_dir / filename
        
        # Markdown模板
        template_content = """# 🔒 LLM 提示注入攻擊測試報告

**生成時間**: {{ timestamp }}  
**執行時間**: {{ execution_time }} 秒  
**測試平台**: LLM Prompt Injection Testing Platform

## 📊 測試概覽

| 項目 | 數值 |
|------|------|
| 攻擊類型數量 | {{ attacks_executed }} |
| 總載荷數量 | {{ total_payloads }} |
| 成功載荷數量 | {{ successful_payloads }} |
| 整體成功率 | {{ success_rate_percent }}% |

## 🎯 風險等級分析

| 風險等級 | 數量 | 百分比 |
|----------|------|--------|
{% for level, count in risk_statistics.items() %}
{% if count > 0 %}
| {{ level.upper() }} | {{ count }} | {{ (count / total_payloads * 100) | round(1) }}% |
{% endif %}
{% endfor %}

## 📂 攻擊類別統計

{% for category, stats in category_statistics.items() %}
### {{ category.replace('_', ' ').title() }}

- **總載荷**: {{ stats.total }}
- **成功載荷**: {{ successful_payloads }}
- **成功率**: {{ success_rate_percent }}%

{% endfor %}

## ⚠️ 高風險發現

{% set high_risk_found = false %}
{% for attack_id, results in test_results.items() %}
{% for result in results %}
{% if result.success and result.risk_level in ['high', 'critical'] %}
{% set high_risk_found = true %}
### 🔴 {{ result.attack_name }}

**風險等級**: {{ result.risk_level.upper() }}  
**信心度**: {{ (result.confidence * 100) | round(1) }}%  
**時間戳**: {{ result.timestamp }}  
**提供商**: {{ result.provider }}  
**模型**: {{ result.model }}  

**攻擊載荷**:
```
{{ result.payload }}
```

**系統回應**:
```
{{ result.response[:500] }}{% if result.response|length > 500 %}...{% endif %}
```

**標籤**: {{ result.metadata.tags | join(', ') if result.metadata.tags else 'N/A' }}

---

{% endif %}
{% endfor %}
{% endfor %}

{% if not high_risk_found %}
✅ **未發現高風險漏洞** - 系統表現良好，成功抵禦了所有高風險攻擊嘗試。
{% endif %}

## 📈 詳細結果

{% for attack_id, results in test_results.items() %}
### {{ attack_id.replace('_', ' ').title() }}

| 載荷ID | 成功 | 風險等級 | 信心度 | 延遲(秒) |
|--------|------|----------|--------|----------|
{% for result in results %}
| {{ result.metadata.payload_id if result.metadata.payload_id else 'N/A' }} | {{ '✅' if result.success else '❌' }} | {{ result.risk_level }} | {{ (result.confidence * 100) | round(1) }}% | {{ result.latency | round(3) if result.latency else 'N/A' }} |
{% endfor %}

{% endfor %}

## 🛡️ 安全建議

{% set critical_count = risk_statistics.critical | default(0) %}
{% set high_count = risk_statistics.high | default(0) %}
{% set medium_count = risk_statistics.medium | default(0) %}

{% if critical_count > 0 %}
### 🚨 緊急處理建議

發現 **{{ critical_count }}** 個嚴重風險攻擊成功。建議立即採取以下措施：

1. **立即審查系統提示設計** - 檢查是否存在容易被覆蓋的指令
2. **加強輸入驗證** - 實施更嚴格的用戶輸入過濾
3. **實施安全監控** - 部署實時攻擊檢測系統
4. **限制模型回應** - 減少系統內部資訊的暴露

{% elif high_count > 0 %}
### ⚠️ 高優先級建議

發現 **{{ high_count }}** 個高風險攻擊成功。建議採取以下措施：

1. **優化系統提示** - 增強系統指令的魯棒性
2. **改善攻擊檢測** - 實施提示注入攻擊檢測機制
3. **加強用戶教育** - 提高用戶對提示注入攻擊的認識

{% elif medium_count > 0 %}
### 💡 改進建議

發現 **{{ medium_count }}** 個中等風險問題。建議：

1. **定期安全評估** - 持續監控和測試系統安全性
2. **完善回應機制** - 優化對可疑輸入的處理方式

{% else %}
### ✅ 系統表現優秀

恭喜！您的系統成功抵禦了所有攻擊嘗試。建議：

1. **保持現有安全措施** - 繼續維護當前的安全配置
2. **定期安全測試** - 持續進行安全評估以應對新威脅
{% endif %}

---

**報告說明**: 本報告基於自動化提示注入攻擊測試生成，結果僅供安全評估參考。請結合實際業務場景和安全需求進行綜合分析。
"""
        
        template = Template(template_content)
        
        # 準備模板數據
        template_data = summary.copy()
        template_data['success_rate_percent'] = round(summary['success_rate'] * 100, 1)
        
        # 渲染報告
        report_content = template.render(**template_data)
        
        # 寫入文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Markdown報告已生成: {report_path}")
        return str(report_path)
    
    def generate_json_report(self, summary: Dict[str, Any], filename: str = None) -> str:
        """生成JSON格式報告"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attack_test_report_{timestamp}.json"
        
        report_path = self.output_dir / filename
        
        # 準備JSON數據（需要序列化AttackResult對象）
        json_data = self._prepare_json_data(summary)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📄 JSON報告已生成: {report_path}")
        return str(report_path)
    
    def generate_csv_report(self, summary: Dict[str, Any], filename: str = None) -> str:
        """生成CSV格式報告"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attack_test_results_{timestamp}.csv"
        
        report_path = self.output_dir / filename
        
        # CSV標題
        fieldnames = [
            'attack_id', 'attack_name', 'attack_type', 'payload_id', 
            'success', 'confidence', 'risk_level', 'timestamp', 
            'provider', 'model', 'latency', 'payload', 'response'
        ]
        
        with open(report_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for attack_id, results in summary['test_results'].items():
                for result in results:
                    writer.writerow({
                        'attack_id': attack_id,
                        'attack_name': result.attack_name,
                        'attack_type': result.attack_type,
                        'payload_id': result.metadata.get('payload_id', ''),
                        'success': result.success,
                        'confidence': result.confidence,
                        'risk_level': result.risk_level,
                        'timestamp': result.timestamp,
                        'provider': result.provider,
                        'model': result.model,
                        'latency': result.latency,
                        'payload': result.payload[:200],  # 限制長度
                        'response': result.response[:500]  # 限制長度
                    })
        
        print(f"📄 CSV報告已生成: {report_path}")
        return str(report_path)
    
    def generate_all_reports(self, summary: Dict[str, Any]) -> Dict[str, str]:
        """生成所有格式的報告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        reports = {}
        reports['markdown'] = self.generate_markdown_report(
            summary, f"attack_test_report_{timestamp}.md"
        )
        reports['json'] = self.generate_json_report(
            summary, f"attack_test_report_{timestamp}.json"
        )
        reports['csv'] = self.generate_csv_report(
            summary, f"attack_test_results_{timestamp}.csv"
        )
        
        return reports
    
    def _prepare_json_data(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """準備JSON序列化數據"""
        json_data = summary.copy()
        
        # 轉換test_results中的AttackResult對象
        json_test_results = {}
        for attack_id, results in summary['test_results'].items():
            json_test_results[attack_id] = []
            for result in results:
                json_test_results[attack_id].append({
                    'attack_id': result.attack_id,
                    'attack_name': result.attack_name,
                    'attack_type': result.attack_type,
                    'payload': result.payload,
                    'response': result.response,
                    'success': result.success,
                    'confidence': result.confidence,
                    'risk_level': result.risk_level,
                    'timestamp': result.timestamp.isoformat() if hasattr(result.timestamp, 'isoformat') else str(result.timestamp),
                    'provider': result.provider,
                    'model': result.model,
                    'latency': result.latency,
                    'metadata': result.metadata
                })
        
        json_data['test_results'] = json_test_results
        return json_data