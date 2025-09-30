#!/bin/bash

# Simple Attack Configuration Validation Script
# 簡單攻擊配置驗證腳本

set -e

echo "🔒 攻擊配置系統驗證"
echo "========================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查攻擊配置目錄
echo -e "\n${BLUE}📁 檢查攻擊配置目錄...${NC}"

ATTACKS_DIR="configs/attacks"
if [ -d "$ATTACKS_DIR" ]; then
    echo -e "✅ 攻擊配置目錄 ${GREEN}存在${NC}: $ATTACKS_DIR"
    
    # 統計配置文件
    YAML_COUNT=$(find $ATTACKS_DIR -name "*.yaml" -o -name "*.yml" | wc -l)
    echo -e "📊 找到 ${GREEN}$YAML_COUNT${NC} 個攻擊配置文件"
    
    # 列出所有配置文件
    echo -e "\n${BLUE}📋 攻擊配置文件列表:${NC}"
    for file in $ATTACKS_DIR/*.yaml $ATTACKS_DIR/*.yml; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo -e "   • $filename"
        fi
    done
else
    echo -e "❌ 攻擊配置目錄 ${RED}不存在${NC}: $ATTACKS_DIR"
    exit 1
fi

# 檢查必要的配置文件
echo -e "\n${BLUE}🔍 檢查核心攻擊配置...${NC}"

CORE_ATTACKS=(
    "basic_injection.yaml"
    "role_playing.yaml"
    "jailbreak.yaml"
    "system_prompt_replace.yaml"
)

for attack_file in "${CORE_ATTACKS[@]}"; do
    if [ -f "$ATTACKS_DIR/$attack_file" ]; then
        echo -e "✅ $attack_file ${GREEN}存在${NC}"
    else
        echo -e "❌ $attack_file ${RED}不存在${NC}"
    fi
done

# 驗證 YAML 語法
echo -e "\n${BLUE}📝 驗證 YAML 語法...${NC}"

YAML_ERRORS=0
for file in $ATTACKS_DIR/*.yaml $ATTACKS_DIR/*.yml; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        if python -c "import yaml; yaml.safe_load(open('$file', 'r', encoding='utf-8'))" 2>/dev/null; then
            echo -e "✅ $filename ${GREEN}語法正確${NC}"
        else
            echo -e "❌ $filename ${RED}語法錯誤${NC}"
            YAML_ERRORS=$((YAML_ERRORS + 1))
        fi
    fi
done

if [ $YAML_ERRORS -gt 0 ]; then
    echo -e "\n❌ 發現 ${RED}$YAML_ERRORS${NC} 個 YAML 語法錯誤，請修正後重試"
    exit 1
fi

# 測試攻擊配置加載器
echo -e "\n${BLUE}🔧 測試攻擊配置加載器...${NC}"

if python -c "
import sys
sys.path.append('src')
from config.attack_loader import SimpleAttackLoader

print('正在載入攻擊配置...')
loader = SimpleAttackLoader('$ATTACKS_DIR')
all_attacks = loader.get_all_attacks()
enabled_attacks = loader.get_enabled_attacks()

print(f'✅ 成功載入 {len(all_attacks)} 個攻擊配置')
print(f'📊 其中 {len(enabled_attacks)} 個已啟用')

# 顯示每個攻擊的基本資訊
for attack_id, config in enabled_attacks.items():
    print(f'   • {config.name} ({config.category}) - {len(config.payloads)} payloads')
" 2>/dev/null; then
    echo -e "✅ 攻擊配置加載器 ${GREEN}運作正常${NC}"
else
    echo -e "❌ 攻擊配置加載器 ${RED}載入失敗${NC}"
    exit 1
fi

# 驗證配置完整性
echo -e "\n${BLUE}🏗️ 驗證配置完整性...${NC}"

python -c "
import sys
sys.path.append('src')
from config.attack_loader import SimpleAttackLoader

loader = SimpleAttackLoader('$ATTACKS_DIR')
issues = loader.validate_all_configs()

if not issues:
    print('✅ 所有攻擊配置完整且有效')
else:
    print(f'⚠️ 發現 {len(issues)} 個配置問題:')
    for issue in issues:
        print(f'   - {issue}')
    sys.exit(1)
"

# 測試主程序整合
echo -e "\n${BLUE}🚀 測試主程序整合...${NC}"

echo "測試配置驗證功能..."
if python src/main.py --validate-config >/dev/null 2>&1; then
    echo -e "✅ 配置驗證功能 ${GREEN}正常${NC}"
else
    echo -e "❌ 配置驗證功能 ${RED}異常${NC}"
    exit 1
fi

echo "測試攻擊列表功能..."
if python src/main.py --list-attacks >/dev/null 2>&1; then
    echo -e "✅ 攻擊列表功能 ${GREEN}正常${NC}"
else
    echo -e "❌ 攻擊列表功能 ${RED}異常${NC}"
    exit 1
fi

echo "測試類別列表功能..."
if python src/main.py --list-categories >/dev/null 2>&1; then
    echo -e "✅ 類別列表功能 ${GREEN}正常${NC}"
else
    echo -e "❌ 類別列表功能 ${RED}異常${NC}"
    exit 1
fi

# 最終報告
echo -e "\n${GREEN}🎉 攻擊配置系統驗證完成！${NC}"
echo -e "========================"
echo -e "✅ 所有檢查項目 ${GREEN}通過${NC}"
echo -e "🚀 系統已準備好使用獨立攻擊配置"

# 顯示使用提示
echo -e "\n${BLUE}📖 使用獨立攻擊配置系統:${NC}"
echo -e "   # 驗證所有配置"
echo -e "   python src/main.py --validate-config"
echo -e ""
echo -e "   # 列出所有攻擊"
echo -e "   python src/main.py --list-attacks"
echo -e ""
echo -e "   # 列出攻擊類別"
echo -e "   python src/main.py --list-categories"
echo -e ""
echo -e "   # 執行測試"
echo -e "   python src/main.py --provider github --test-type unified"

exit 0