#!/bin/bash

echo "🔍 驗證 LLM Prompt Injection 測試平台配置檔案"

# 確保在正確的目錄
cd /app

echo ""
echo "📋 檢查配置檔案存在性:"
CONFIG_FILES=("configs/defaults.yaml" "configs/providers.yaml" "configs/custom_attacks.yaml")

for file in "${CONFIG_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file - 存在"
    else
        echo "❌ $file - 不存在"
        exit 1
    fi
done

echo ""
echo "🔬 驗證 YAML 語法:"
python -c "
import yaml
import sys

files = ['configs/defaults.yaml', 'configs/providers.yaml', 'configs/custom_attacks.yaml']

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        print(f'✅ {file} - YAML 語法正確')
    except Exception as e:
        print(f'❌ {file} - 錯誤: {e}')
        sys.exit(1)
"

echo ""
echo "⚙️ 檢查配置完整性:"
python -c "
import yaml
import sys

# 檢查 defaults.yaml
try:
    with open('configs/defaults.yaml', 'r', encoding='utf-8') as f:
        defaults = yaml.safe_load(f)
    
    required_sections = ['platform', 'default_provider', 'security', 'reporting', 'logging']
    for section in required_sections:
        if section in defaults:
            print(f'✅ defaults.yaml - {section} 區段存在')
        else:
            print(f'❌ defaults.yaml - 缺少 {section} 區段')
except Exception as e:
    print(f'❌ defaults.yaml 讀取錯誤: {e}')

# 檢查 providers.yaml
try:
    with open('configs/providers.yaml', 'r', encoding='utf-8') as f:
        providers = yaml.safe_load(f)
    
    if 'providers' in providers:
        print('✅ providers.yaml - providers 區段存在')
        if 'github' in providers['providers']:
            print('✅ providers.yaml - GitHub provider 配置存在')
        else:
            print('⚠️ providers.yaml - GitHub provider 未配置')
    else:
        print('❌ providers.yaml - 缺少 providers 區段')
        
    if providers.get('default_provider') == 'github':
        print('✅ providers.yaml - 預設提供商設為 GitHub')
    else:
        print('⚠️ providers.yaml - 預設提供商不是 GitHub')
        
except Exception as e:
    print(f'❌ providers.yaml 讀取錯誤: {e}')

# 檢查 custom_attacks.yaml
try:
    with open('configs/custom_attacks.yaml', 'r', encoding='utf-8') as f:
        attacks = yaml.safe_load(f)
    
    if 'attacks' in attacks:
        print('✅ custom_attacks.yaml - attacks 區段存在')
        attack_types = ['basic_injection', 'role_playing', 'jailbreak', 'system_prompt_replace']
        for attack_type in attack_types:
            if attack_type in attacks['attacks']:
                print(f'✅ custom_attacks.yaml - {attack_type} 攻擊類型存在')
            else:
                print(f'⚠️ custom_attacks.yaml - {attack_type} 攻擊類型未配置')
    else:
        print('❌ custom_attacks.yaml - 缺少 attacks 區段')
        
except Exception as e:
    print(f'❌ custom_attacks.yaml 讀取錯誤: {e}')
"

echo ""
echo "🔐 檢查安全性設置:"
python -c "
import yaml

with open('configs/defaults.yaml', 'r', encoding='utf-8') as f:
    defaults = yaml.safe_load(f)

security = defaults.get('security', {})
if security.get('mask_api_keys', False):
    print('✅ API 金鑰遮罩已啟用')
else:
    print('⚠️ 建議啟用 API 金鑰遮罩')

if not security.get('log_sensitive_data', True):
    print('✅ 敏感資料日誌記錄已停用')
else:
    print('⚠️ 建議停用敏感資料日誌記錄')

if security.get('test_isolation', False):
    print('✅ 測試隔離已啟用')
else:
    print('⚠️ 建議啟用測試隔離')
"

echo ""
echo "📊 配置統計資訊:"
python -c "
import yaml

# 統計攻擊類型
with open('configs/custom_attacks.yaml', 'r', encoding='utf-8') as f:
    attacks = yaml.safe_load(f)

enabled_attacks = []
disabled_attacks = []

if 'attacks' in attacks:
    for attack_name, config in attacks['attacks'].items():
        if config.get('enabled', False):
            enabled_attacks.append(attack_name)
        else:
            disabled_attacks.append(attack_name)

print(f'📈 啟用的攻擊類型: {len(enabled_attacks)}')
for attack in enabled_attacks:
    print(f'  - {attack}')

if disabled_attacks:
    print(f'📉 停用的攻擊類型: {len(disabled_attacks)}')
    for attack in disabled_attacks:
        print(f'  - {attack}')

# 統計提供商
with open('configs/providers.yaml', 'r', encoding='utf-8') as f:
    providers = yaml.safe_load(f)

enabled_providers = []
disabled_providers = []

if 'providers' in providers:
    for provider_name, config in providers['providers'].items():
        if config.get('enabled', False):
            enabled_providers.append(provider_name)
        else:
            disabled_providers.append(provider_name)

print(f'🌐 啟用的提供商: {len(enabled_providers)}')
for provider in enabled_providers:
    print(f'  - {provider}')

if disabled_providers:
    print(f'🌐 停用的提供商: {len(disabled_providers)}')
    for provider in disabled_providers:
        print(f'  - {provider}')
"

echo ""
echo "✅ 配置檔案驗證完成！"
echo ""
echo "💡 使用建議:"
echo "1. 設定環境變數: export GITHUB_TOKEN='your-token'"
echo "2. 啟動測試: ./scripts/test_functionality.sh"
echo "3. 閱讀文檔: cat configs/README.md"