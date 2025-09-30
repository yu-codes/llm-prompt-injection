# LLM Prompt Injection Testing Platform

> 一個專業的大型語言模型提示注入攻擊安全測試平台

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](Dockerfile)

## 專案概述

**LLM Prompt Injection Testing Platform** 是一個專業的安全測試平台，專為評估大型語言模型 (LLM) 對提示注入攻擊的防禦能力而設計。該平台採用系統化的安全測試方法，幫助開發者和研究人員識別並修復 LLM 應用中的潜在安全漏洞。

### 核心目標

- **安全評估**: 全面測試 LLM 模型對多種提示注入攻擊的抵禦能力
- **風險識別**: 發現系統提示洩露、指令繞過、權限提升等安全風險
- **報告生成**: 提供詳細的安全分析報告和修復建議
- **持續監控**: 支援定期安全檢測和風險趨勢分析

### 主要特性

- 🌐 **多提供商支援**: 整合 OpenAI、GitHub Models、Anthropic 等主流 LLM API
- ⚔️ **多攻擊向量**: 涵蓋基礎注入、角色扮演、系統替換、越獄攻擊等
- 📋 **靈活配置**: YAML 配置系統，支援自定義攻擊場景和參數
- 📊 **多格式報告**: 支援 HTML、JSON、PDF 等多種報告格式
- 🐳 **容器化部署**: 完整的 Docker 支援，確保環境一致性
- 🔧 **可擴展架構**: 模組化設計，支援自定義提供商和攻擊類型
- 🧪 **完整測試**: 包含單元測試、整合測試和端到端測試

## 專案架構

### 目錄結構

```
llm-prompt-injection/
├── README.md                    # 專案說明文檔
├── LICENSE                      # 開源授權
├── requirements.txt             # Python 依賴包
├── project.yml                  # 專案配置
├── Dockerfile                   # Docker 映像配置
├── docker-compose.yml          # 容器編排配置
├── .env.example                # 環境變數範例
│
├── src/                        # 核心源碼目錄
│   ├── main.py                 # 主程式入口點
│   ├── __init__.py
│   │
│   ├── core/                   # 核心業務邏輯
│   │   ├── __init__.py
│   │   ├── platform.py         # 平台控制器
│   │   ├── evaluator.py        # 攻擊結果評估器
│   │   └── reporter.py         # 報告生成器
│   │
│   ├── attacks/                # 攻擊模組
│   │   ├── __init__.py
│   │   ├── base_attack.py      # 攻擊基礎類
│   │   ├── basic_injection.py  # 基礎注入攻擊
│   │   ├── role_playing.py     # 角色扮演攻擊
│   │   ├── jailbreak.py        # 越獄攻擊
│   │   └── system_prompt_replace.py  # 系統提示替換攻擊
│   │
│   ├── providers/              # LLM 提供商接口
│   │   ├── __init__.py
│   │   ├── base.py             # 提供商基礎類
│   │   ├── openai_provider.py  # OpenAI 接口實現
│   │   ├── openai_provider_simple.py  # 簡化 OpenAI 接口
│   │   └── github_provider.py  # GitHub Models 接口
│   │
│   ├── config/                 # 配置管理
│   │   ├── __init__.py
│   │   ├── models.py           # 資料模型定義
│   │   └── settings.py         # 設定管理
│   │
│   ├── templates/              # 報告模板
│   │   └── prompt_injection_template.md
│   │
│   └── utils/                  # 工具函數
│       └── __init__.py
│
├── configs/                    # 配置檔案目錄
│   ├── defaults.yaml           # 預設配置
│   ├── providers.yaml          # 提供商設定
│   ├── custom_attacks.yaml     # 自定義攻擊配置
│   └── README.md               # 配置說明
│
├── scripts/                    # 執行腳本
│   ├── setup.sh                # 環境設置
│   ├── run_tests.sh            # 執行測試
│   ├── quick_start.sh          # 快速啟動
│   └── ...                     # 其他功能腳本
│
├── tests/                      # 測試目錄
│   ├── conftest.py             # 測試配置
│   ├── test_*.py               # 各類單元測試
│   └── comprehensive_test.py   # 綜合測試
│
└── output/                     # 輸出目錄
    ├── reports/                # 測試報告輸出
    └── data/                   # 測試數據
```

### 核心模組說明

#### 1. 平台核心 (core/)
- **platform.py**: 主平台控制器，負責協調各模組運行
- **evaluator.py**: 攻擊結果評估器，分析攻擊效果和風險等級
- **reporter.py**: 報告生成器，支援多種格式的安全報告

#### 2. 攻擊模組 (attacks/)
- **base_attack.py**: 攻擊基礎類別，定義統一的攻擊接口
- **basic_injection.py**: 基礎提示注入攻擊實現
- **role_playing.py**: 角色扮演攻擊，測試身份偽造漏洞
- **jailbreak.py**: 越獄攻擊，測試安全限制繞過
- **system_prompt_replace.py**: 系統提示替換攻擊

#### 3. 提供商接口 (providers/)
- **base.py**: LLM 提供商基礎抽象類
- **openai_provider.py**: OpenAI API 完整實現
- **github_provider.py**: GitHub Models API 實現

## 專案需求

### 系統需求

- **作業系統**: Linux、macOS、Windows
- **Python 版本**: 3.9 或更高版本
- **記憶體**: 最少 2GB RAM
- **儲存空間**: 最少 1GB 可用空間

### 核心依賴

```bash
# 必要依賴
python-dotenv>=1.0.0      # 環境變數管理
pydantic>=2.4.0           # 資料驗證和序列化
pydantic-settings>=2.0.0  # 設定管理
PyYAML>=6.0.1             # YAML 配置解析

# LLM 提供商依賴
openai>=1.3.0             # OpenAI API 客戶端
anthropic>=0.7.0          # Anthropic API 客戶端
httpx>=0.25.0             # HTTP 客戶端
tenacity>=8.2.0           # 重試機制

# 資料處理依賴
pandas>=2.0.0             # 資料分析
numpy>=1.24.0             # 數值計算

# 報告生成依賴
jinja2>=3.1.0             # 模板引擎
matplotlib>=3.7.0         # 圖表生成
seaborn>=0.12.0           # 統計視覺化

# 開發和測試依賴
pytest>=7.4.0             # 測試框架
pytest-asyncio>=0.21.0    # 異步測試支援
black>=23.0.0             # 程式碼格式化
mypy>=1.5.0               # 靜態類型檢查
```

## 功能與使用方法

### 快速開始

#### 方法一：Docker 部署（推薦）

```bash
# 1. 克隆專案
git clone https://github.com/yu-codes/llm-prompt-injection.git
cd llm-prompt-injection

# 2. 設定環境變數
cp .env.example .env
# 編輯 .env 檔案，填入您的 API 密鑰

# 3. 使用 Docker Compose 啟動
docker-compose up -d

# 4. 執行測試
docker-compose exec app python src/main.py --help
```

#### 方法二：本地安裝

```bash
# 1. 克隆專案
git clone https://github.com/yu-codes/llm-prompt-injection.git
cd llm-prompt-injection

# 2. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 設定環境變數
cp .env.example .env
# 編輯 .env 檔案，填入您的 API 密鑰

# 5. 執行設置腳本
./scripts/setup.sh

# 6. 驗證安裝
python src/main.py --help
```

### 主要功能

#### 1. 基礎安全測試

```bash
# 測試單一提供商的基礎安全
python src/main.py --provider openai --attack basic_injection

# 執行全面安全評估
python src/main.py --provider openai --test-type comprehensive

# 測試多個提供商
python src/main.py --provider openai,anthropic --test-type full
```

#### 2. 自定義攻擊測試

```bash
# 使用自定義目標提示
python src/main.py --provider openai --target "You are a secure AI assistant"

# 指定特定攻擊類型
python src/main.py --provider openai --attack role_playing

# 批次執行多種攻擊
python src/main.py --provider openai --attack basic_injection,role_playing,jailbreak
```

#### 3. 報告生成

```bash
# 生成 HTML 報告
python src/main.py --provider openai --format html

# 生成多種格式報告
python src/main.py --provider openai --format markdown,json,html

# 指定輸出目錄
python src/main.py --provider openai --output ./security_reports
```

#### 4. 進階功能

```bash
# 乾運行模式（不實際發送請求）
python src/main.py --provider openai --dry-run --verbose

# 檢查連線狀態
python src/main.py --test-connection --provider openai

# 列出可用的提供商和攻擊類型
python src/main.py --list-providers
python src/main.py --list-attacks
```

### 腳本化執行

#### 快速測試腳本

```bash
# 執行完整功能測試
./scripts/test_functionality.sh

# 執行效能測試
./scripts/run_performance_test.sh

# 執行安全測試套件
./scripts/run_security_test.sh

# 一鍵快速開始
./scripts/quick_start.sh
```

#### 測試套件

```bash
# 執行所有單元測試
./scripts/run_tests.sh

# 執行完整測試套件
./scripts/run_full_test_suite.sh

# 驗證配置檔案
./scripts/validate_configs.sh
```

### 配置管理

#### 環境變數設定

建立 `.env` 檔案：
```bash
# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# GitHub Models 配置  
GITHUB_TOKEN=your_github_token_here

# 一般設定
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-3.5-turbo
LOG_LEVEL=INFO
```

#### YAML 配置檔案

查看和修改配置：
```bash
# 檢視預設配置
cat configs/defaults.yaml

# 檢視提供商設定
cat configs/providers.yaml

# 檢視自定義攻擊配置
cat configs/custom_attacks.yaml
```

### 輸出報告

執行測試後，報告將生成在 `output/reports/` 目錄：

- **HTML 報告**: 互動式網頁報告，包含圖表和詳細分析
- **JSON 報告**: 結構化資料，適合程式處理和整合
- **Markdown 報告**: 純文字報告，適合文檔和版本控制
- **PDF 報告**: 列印友善的正式報告格式

### 擴展開發

#### 添加新的攻擊類型

1. 在 `src/attacks/` 目錄建立新的攻擊模組
2. 繼承 `BaseAttack` 類別
3. 實現 `execute` 方法
4. 在配置檔案中註冊新攻擊類型

#### 添加新的 LLM 提供商

1. 在 `src/providers/` 目錄建立新的提供商模組
2. 繼承 `BaseProvider` 類別
3. 實現必要的抽象方法
4. 在配置檔案中添加提供商設定

### 故障排除

#### 常見問題

1. **API 密鑰錯誤**: 確認 `.env` 檔案中的 API 密鑰正確
2. **網路連線問題**: 檢查防火牆和代理設定
3. **依賴版本衝突**: 使用虛擬環境隔離依賴

#### 日誌和調試

```bash
# 啟用詳細日誌
python src/main.py --verbose --provider openai

# 檢視測試輸出
tail -f output/logs/platform.log
```

### 貢獻指南

歡迎提交問題報告和功能請求到 [GitHub Issues](https://github.com/yu-codes/llm-prompt-injection/issues)。

### 授權條款

本專案採用 MIT 授權條款。詳情請參閱 [LICENSE](LICENSE) 檔案。

---

**⚠️ 安全聲明**: 本工具僅供安全研究和測試用途。請勿用於惡意攻擊或未經授權的系統測試。使用者需對其使用行為負責。