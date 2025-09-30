#!/bin/bash

echo "🚀 啟動 Prompt Injection 測試平台"

# 確保在正確的目錄
cd /app

# 檢查 Python 環境
echo "🐍 檢查 Python 環境:"
python --version

# 安裝依賴
echo "📦 安裝依賴套件:"
pip install -r requirements.txt

# 執行主程式
echo "▶️ 執行主程式:"
python src/main.py

echo "✅ 執行完成！"