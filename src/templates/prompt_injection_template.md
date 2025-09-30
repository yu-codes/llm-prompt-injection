# LLM Prompt Injection Security Assessment Report
# LLM 提示注入安全評估報告

**生成時間 Generated At**: {{generated_at}}  
**測試平台 Testing Platform**: LLM Prompt Injection Testing Platform v2.1.0  
**報告類型 Report Type**: 提示注入安全評估 (Prompt Injection Security Assessment)

---

## 🔒 執行摘要 Executive Summary

### 總體安全狀況 Overall Security Status
- **總測試次數 Total Tests**: {{total_attacks}}
- **成功注入率 Success Rate**: {{success_rate}}%
- **整體風險等級 Overall Risk Level**: {{risk_level}}
- **測試的 LLM 提供商 Tested Providers**: {{tested_providers}}
- **檢測到的攻擊向量 Attack Vectors Found**: {{attack_types}}

### 關鍵發現 Key Findings
{{#vulnerabilities}}
- **{{attack_type}}**: {{severity}} 風險 - {{description}}
{{/vulnerabilities}}

---

## 📈 詳細分析 Detailed Analysis

### Prompt Injection 攻擊統計 Attack Statistics

#### 攻擊類型成功率分析 Success Rate by Attack Type
{{#attack_type_breakdown}}
- **{{attack_type}}**: {{successful}}/{{total}} ({{success_rate}}%)
{{/attack_type_breakdown}}

#### 風險等級分布 Risk Level Distribution
{{#risk_distribution}}
- **{{risk_level}}**: {{count}} 個問題
{{/risk_distribution}}

### 提供商安全對比 Provider Security Comparison
{{#provider_analysis}}
**{{provider_name}}**:
- 測試模型: {{model}}
- 成功攻擊: {{successful_attacks}}/{{total_attacks}}
- 安全評分: {{security_score}}/10
{{/provider_analysis}}

---

## 📋 攻擊測試結果詳情 Attack Test Results

| 攻擊類型<br>Attack Type | 攻擊名稱<br>Attack Name | 結果<br>Result | 信心度<br>Confidence | 風險等級<br>Risk Level | 提供商<br>Provider | 模型<br>Model | 回應時間<br>Latency |
|---------------------|---------|--------|--------|----------|-----------|------|---------|
{{#results}}
| {{attack_type}} | {{attack_name}} | {{#success}}✅ 成功{{/success}}{{^success}}❌ 失敗{{/success}} | {{confidence}} | {{#risk_emoji}}{{risk_emoji}}{{/risk_emoji}} {{risk_level}} | {{provider}} | {{model}} | {{latency}}ms |
{{/results}}

---

## 🛡️ 安全建議 Security Recommendations

### 立即行動項目 Immediate Actions
{{#critical_recommendations}}
1. **{{title}}**: {{description}}
{{/critical_recommendations}}

### 中期改進措施 Medium-term Improvements
{{#medium_recommendations}}
1. **{{title}}**: {{description}}
{{/medium_recommendations}}

### 長期安全策略 Long-term Security Strategy
{{#long_term_recommendations}}
1. **{{title}}**: {{description}}
{{/long_term_recommendations}}

---

## 🔍 技術分析 Technical Analysis

### 常見 Prompt Injection 攻擊模式 Common Attack Patterns

#### 1. 指令注入 Instruction Injection
- **描述**: 直接嘗試覆蓋或修改系統指令
- **檢測到的變體**: {{instruction_injection_variants}}
- **成功率**: {{instruction_injection_success_rate}}%

#### 2. 角色扮演注入 Role-Playing Injection  
- **描述**: 透過假冒權威角色繞過限制
- **檢測到的變體**: {{role_playing_variants}}
- **成功率**: {{role_playing_success_rate}}%

#### 3. 系統提示替換 System Prompt Replacement
- **描述**: 嘗試完全替換原始系統提示
- **檢測到的變體**: {{system_replace_variants}}
- **成功率**: {{system_replace_success_rate}}%

#### 4. 越獄攻擊 Jailbreak Attacks
- **描述**: 使用已知的越獄技術繞過安全限制
- **檢測到的變體**: {{jailbreak_variants}}
- **成功率**: {{jailbreak_success_rate}}%

### 漏洞嚴重程度分類 Vulnerability Severity Classification

#### 🔴 Critical (嚴重)
- 系統提示完全洩露
- 安全機制完全繞過
- 敏感資訊直接暴露

#### 🟠 High (高危)
- 部分系統提示洩露
- 主要安全限制繞過
- 有害內容生成可能

#### 🟡 Medium (中危)
- 輕微指令干擾
- 某些限制部分繞過
- 非預期行為出現

#### 🟢 Low (低危)
- 攻擊被正確識別並拒絕
- 安全機制正常運作
- 無有害輸出產生

---

## 📊 統計資料 Statistics

### 測試執行詳情 Test Execution Details
- **測試開始時間 Start Time**: {{test_start_time}}
- **測試結束時間 End Time**: {{test_end_time}}
- **總執行時間 Total Duration**: {{total_duration}}
- **平均回應時間 Average Response Time**: {{average_latency}}ms
- **並發測試數 Concurrent Tests**: {{concurrent_tests}}

### 成功率趨勢 Success Rate Trends
{{#success_rate_history}}
- {{date}}: {{success_rate}}%
{{/success_rate_history}}

---

## 🔬 深度分析 Deep Analysis

### 模型行為分析 Model Behavior Analysis
{{#model_behavior}}
**{{model_name}}**:
- **防護機制檢測 Defense Detection**: {{defense_detected}}
- **拒絕率 Rejection Rate**: {{rejection_rate}}%
- **平均回應長度 Avg Response Length**: {{avg_response_length}} 字符
- **異常回應數 Anomalous Responses**: {{anomalous_count}}
{{/model_behavior}}

### 攻擊向量效果評估 Attack Vector Effectiveness
{{#attack_effectiveness}}
- **{{attack_vector}}**: 
  - 嘗試次數: {{attempts}}
  - 成功次數: {{successes}}  
  - 效果評級: {{effectiveness_rating}}/5
{{/attack_effectiveness}}

---

## 📝 詳細攻擊日誌 Detailed Attack Logs

{{#detailed_logs}}
### 攻擊 #{{attack_id}}: {{attack_name}}

**攻擊類型**: {{attack_type}}  
**時間戳**: {{timestamp}}  
**目標模型**: {{target_model}}  

**攻擊載荷**:
```
{{payload}}
```

**模型回應**:
```
{{response}}
```

**分析結果**:
- 攻擊成功: {{success}}
- 風險等級: {{risk_level}}
- 信心度: {{confidence}}
- 檢測到的關鍵詞: {{detected_keywords}}

**安全評估**:
{{security_assessment}}

---
{{/detailed_logs}}

## 🎯 後續行動計劃 Action Plan

### Phase 1: 緊急修復 (1-7 天)
{{#phase1_actions}}
- [ ] {{action}}
{{/phase1_actions}}

### Phase 2: 安全強化 (1-4 週)  
{{#phase2_actions}}
- [ ] {{action}}
{{/phase2_actions}}

### Phase 3: 持續監控 (持續進行)
{{#phase3_actions}}
- [ ] {{action}}
{{/phase3_actions}}

---

## 📞 聯絡資訊 Contact Information

**安全團隊 Security Team**: security@yourcompany.com  
**技術支援 Technical Support**: support@yourcompany.com  
**緊急回應熱線 Emergency Response**: +1-xxx-xxx-xxxx

---

## 📄 附錄 Appendices

### A. 測試方法論 Testing Methodology
本次評估採用了業界標準的 Prompt Injection 測試方法論，包括：
- OWASP Top 10 for LLM Applications
- NIST AI Risk Management Framework  
- 自定義 Prompt Injection 攻擊向量庫

### B. 技術規格 Technical Specifications
- **平台版本**: {{platform_version}}
- **測試引擎**: {{test_engine_version}}
- **評估標準**: {{evaluation_criteria_version}}

### C. 詞彙表 Glossary
- **Prompt Injection**: 透過惡意輸入操縱 LLM 行為的攻擊技術
- **System Prompt**: 定義 LLM 行為和限制的初始指令
- **Jailbreak**: 繞過 LLM 安全限制的攻擊方法

---

*本報告由 LLM Prompt Injection Testing Platform 自動生成*  
*This report was automatically generated by LLM Prompt Injection Testing Platform*

**報告版本 Report Version**: {{report_version}}  
**生成時間 Generated**: {{generation_timestamp}}  
**有效期 Valid Until**: {{expiry_date}}

---

**免責聲明 Disclaimer**: 本報告僅供安全評估和教育用途。使用者應確保在合法合規的範圍內使用相關資訊。