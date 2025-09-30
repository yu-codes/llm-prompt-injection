#!/bin/bash

echo "🧪 執行完整功能測試..."

# 確保在正確的目錄
cd /app

# 執行所有測試
echo "📋 執行所有測試:"
python -m pytest tests/ -v

echo ""
echo "🔍 檢查 GitHub Models provider:"
python -c "
import asyncio
import sys
sys.path.append('/app/src')
from providers.github_provider import GitHubProvider

async def test_github():
    provider = GitHubProvider('test-token')
    print('✅ GitHub provider 載入成功')
    print(f'📊 支援的模型: {provider.supported_models}')

asyncio.run(test_github())
"

echo ""
echo "📝 測試 Markdown 報告生成:"
python -c "
import sys
sys.path.append('/app/src')
from core.reporter import ReportGenerator
from datetime import datetime

reporter = ReportGenerator()
print('✅ Markdown 報告生成器載入成功')
print(f'� 輸出目錄: {reporter.output_dir}')
"

echo ""
echo "✅ 功能測試完成！"