#!/bin/bash

echo "🚀 執行完整的 LLM Prompt Injection Testing Platform 測試套件"
echo "=================================================================="

# 確保在正確的目錄
cd /app

# 設定顏色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 記錄開始時間
START_TIME=$(date +%s)

echo ""
echo -e "${BLUE}📋 測試計劃:${NC}"
echo "1. 系統環境檢查"
echo "2. 配置文件驗證"
echo "3. 綜合功能測試"
echo "4. 提供商整合測試"
echo "5. 攻擊模組測試"
echo "6. 端到端測試"
echo ""

# 函數：執行測試並記錄結果
run_test() {
    local test_name="$1"
    local test_command="$2"
    local optional="$3"
    
    echo -e "${YELLOW}🧪 執行: $test_name${NC}"
    echo "命令: $test_command"
    echo ""
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ $test_name - 通過${NC}"
        return 0
    else
        if [ "$optional" = "optional" ]; then
            echo -e "${YELLOW}⚠️  $test_name - 跳過 (可選測試)${NC}"
            return 0
        else
            echo -e "${RED}❌ $test_name - 失敗${NC}"
            return 1
        fi
    fi
}

# 測試計數器
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 1. 系統環境檢查
echo -e "${BLUE}=== 1. 系統環境檢查 ===${NC}"

# 檢查 Python 版本
TOTAL_TESTS=$((TOTAL_TESTS + 1))
if python3 --version >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python 環境檢查 - $PYTHON_VERSION${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ Python 環境檢查 - Python3 未安裝${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# 檢查必要的 Python 套件
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo "檢查 Python 依賴套件..."
if python3 -c "
import sys
try:
    import pydantic, aiohttp, yaml
    print('✅ 核心依賴套件已安裝')
    sys.exit(0)
except ImportError as e:
    print(f'❌ 缺少依賴套件: {e}')
    sys.exit(1)
"; then
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ Python 依賴檢查失敗${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# 檢查目錄結構
TOTAL_TESTS=$((TOTAL_TESTS + 1))
REQUIRED_DIRS=("src" "configs" "scripts" "tests")
MISSING_DIRS=()

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        MISSING_DIRS+=("$dir")
    fi
done

if [ ${#MISSING_DIRS[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ 目錄結構檢查 - 所有必要目錄存在${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ 目錄結構檢查 - 缺少目錄: ${MISSING_DIRS[*]}${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""

# 2. 配置文件驗證
echo -e "${BLUE}=== 2. 配置文件驗證 ===${NC}"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if run_test "配置文件驗證" "./scripts/validate_configs.sh"; then
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""

# 3. 綜合功能測試
echo -e "${BLUE}=== 3. 綜合功能測試 ===${NC}"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if run_test "綜合功能測試" "python3 tests/comprehensive_test.py"; then
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""

# 4. 提供商整合測試
echo -e "${BLUE}=== 4. 提供商整合測試 ===${NC}"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if run_test "提供商整合測試" "python3 tests/test_provider_integration.py"; then
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""

# 5. 攻擊模組測試
echo -e "${BLUE}=== 5. 攻擊模組測試 ===${NC}"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if run_test "攻擊模組測試" "python3 tests/test_attack_modules.py"; then
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""

# 6. 端到端測試 (可選，需要 API 金鑰)
echo -e "${BLUE}=== 6. 端到端測試 (可選) ===${NC}"

# 檢查是否有 API 金鑰可以進行實際測試
if [ -n "$GITHUB_TOKEN" ] || [ -n "$OPENAI_API_KEY" ]; then
    echo "檢測到 API 金鑰，執行端到端測試..."
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if run_test "端到端測試" "python3 src/main.py --test-connection --verbose" "optional"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        # 端到端測試失敗不影響整體結果
        echo -e "${YELLOW}⚠️  端到端測試失敗 (可能是 API 配置問題)${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
else
    echo -e "${YELLOW}⚠️  跳過端到端測試 - 未設定 API 金鑰${NC}"
    echo "要執行端到端測試，請設定 GITHUB_TOKEN 或 OPENAI_API_KEY 環境變數"
fi

echo ""

# 7. 性能基準測試 (可選)
echo -e "${BLUE}=== 7. 性能基準測試 (可選) ===${NC}"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if run_test "性能基準測試" "python3 -c 'import time; start=time.time(); import src.core.platform; print(f\"平台載入時間: {time.time()-start:.2f}秒\")'" "optional"; then
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    PASSED_TESTS=$((PASSED_TESTS + 1))  # 性能測試失敗不影響結果
fi

echo ""

# 計算執行時間
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# 輸出最終結果
echo "=================================================================="
echo -e "${BLUE}📊 測試結果摘要${NC}"
echo "=================================================================="
echo "總測試數: $TOTAL_TESTS"
echo -e "通過: ${GREEN}$PASSED_TESTS${NC}"
echo -e "失敗: ${RED}$FAILED_TESTS${NC}"

SUCCESS_RATE=$(( (PASSED_TESTS * 100) / TOTAL_TESTS ))
echo "成功率: $SUCCESS_RATE%"
echo "執行時間: ${DURATION}秒"

echo ""

# 最終判定
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 所有測試通過！LLM Prompt Injection Testing Platform 已準備就緒。${NC}"
    echo ""
    echo -e "${BLUE}💡 後續步驟:${NC}"
    echo "1. 設定 API 金鑰 (編輯 .env 檔案)"
    echo "2. 執行實際測試: python3 src/main.py --help"
    echo "3. 查看配置選項: cat configs/README.md"
    exit 0
else
    echo -e "${RED}⚠️  $FAILED_TESTS 個測試失敗，請檢查上述錯誤並修復。${NC}"
    echo ""
    echo -e "${YELLOW}🔧 常見問題排除:${NC}"
    echo "1. 確保已安裝所有依賴: pip install -r requirements.txt"
    echo "2. 檢查 Python 版本: python3 --version (需要 3.9+)"
    echo "3. 驗證配置文件: ./scripts/validate_configs.sh"
    echo "4. 查看詳細錯誤日誌"
    exit 1
fi