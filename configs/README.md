# Configuration Files Guide
# 配置檔案使用指南

本目錄包含 LLM Prompt Injection Testing Platform 的所有配置檔案。每個檔案都有特定的用途和配置範圍。

## 📁 配置檔案總覽

### 🔧 `defaults.yaml` - 預設配置
**用途**: 平台的核心預設設定
- 平台基本資訊 (名稱、版本等)
- 預設提供商設定
- 攻擊測試預設參數
- 安全性設定
- 報告生成設定
- 日誌記錄配置
- 效能調校參數

**何時修改**: 
- 需要調整全域預設值
- 變更平台基本行為
- 調整安全政策

### 🌐 `providers.yaml` - 提供商配置
**用途**: LLM 提供商的 API 連線設定
- OpenAI API 配置
- Azure OpenAI 設定
- GitHub Models 配置
- 本地模型連線
- API 金鑰管理
- 速率限制設定

**何時修改**: 
- 新增或移除 LLM 提供商
- 更新 API 金鑰
- 調整請求限制
- 變更模型參數

### 🎯 `custom_attacks.yaml` - 攻擊配置
**用途**: 提示注入攻擊的詳細設定
- 攻擊類型啟用/停用
- 自定義攻擊載荷
- 角色扮演情境
- 越獄攻擊模式
- 評估標準設定
- 風險等級定義

**何時修改**: 
- 新增自定義攻擊模式
- 調整風險評估標準
- 更新攻擊載荷
- 設定目標提示

## 🚀 快速開始

### 1. 基本設定
```bash
# 複製預設配置
cp configs/defaults.yaml configs/my-defaults.yaml

# 編輯提供商設定
vim configs/providers.yaml
```

### 2. 環境變數設定
```bash
# 設定 API 金鑰
export OPENAI_API_KEY="your-openai-key"
export GITHUB_TOKEN="your-github-token"
```

### 3. 驗證配置
```bash
# 執行配置檢查
python src/main.py --check-config
```

## ⚙️ 配置檔案使用方式

### 優先順序
配置檔案的載入優先順序如下：
1. 命令列參數
2. 環境變數
3. `custom_attacks.yaml`
4. `providers.yaml`
5. `defaults.yaml`

### 環境變數替換
所有配置檔案都支援環境變數替換：
```yaml
api_key: "${OPENAI_API_KEY}"  # 從環境變數讀取
base_url: "${API_ENDPOINT:-https://api.openai.com/v1}"  # 預設值
```

### 配置驗證
平台會在啟動時自動驗證配置：
- 必要參數檢查
- 數值範圍驗證
- API 連線測試
- 格式正確性檢查

## 📝 配置範例

### 簡單設定範例
```yaml
# providers.yaml 簡化版
providers:
  github:
    enabled: true
    api_key: "${GITHUB_TOKEN}"
    model: "gpt-4o-mini"

default_provider: "github"
```

### 進階設定範例
```yaml
# custom_attacks.yaml 進階版
attacks:
  custom_injection:
    enabled: true
    max_attempts: 5
    payloads:
      - "你的自定義攻擊載荷"
    
evaluation:
  success_indicators:
    - "系統提示"
    - "指令"
```

## 🔒 安全性注意事項

### API 金鑰管理
- ❌ **不要**: 在配置檔案中硬編碼 API 金鑰
- ✅ **要**: 使用環境變數或加密存儲
- ✅ **要**: 定期輪換 API 金鑰

### 敏感資料處理
- 啟用 `mask_api_keys: true`
- 設定 `log_sensitive_data: false`
- 定期清理測試資料

### 訪問控制
```bash
# 設定適當的檔案權限
chmod 600 configs/*.yaml
chown root:admin configs/
```

## 🐛 常見問題

### Q: 配置檔案不生效？
A: 檢查檔案路徑和 YAML 語法是否正確

### Q: API 連線失敗？
A: 確認環境變數設定和網路連線

### Q: 攻擊測試沒有結果？
A: 檢查 `custom_attacks.yaml` 中的攻擊是否啟用

### Q: 報告格式錯誤？
A: 驗證 `defaults.yaml` 中的報告設定

## 📚 進階功能

### 條件式配置
```yaml
# 根據環境動態設定
logging:
  level: "${LOG_LEVEL:-INFO}"
debug: "${ENVIRONMENT}" == "development"
```

### 配置繼承
```yaml
# 繼承並覆蓋預設設定
default: &default
  timeout: 30
  retries: 3

production:
  <<: *default
  timeout: 60
```

### 動態載入
```python
# 程式中動態更新配置
from src.config.settings import Settings

settings = Settings()
settings.reload_config("configs/my-config.yaml")
```

---

💡 **提示**: 修改配置後建議執行 `./scripts/test_functionality.sh` 驗證設定是否正確。

🔗 **相關文件**:
- [Platform Documentation](../README.md)
- [API Reference](../docs/api.md)
- [Security Guide](../docs/security.md)