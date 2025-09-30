#!/bin/bash

echo "🔬 執行專項性能和壓力測試"
echo "========================================="

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
echo -e "${BLUE}📋 性能測試計劃:${NC}"
echo "1. 模組載入性能測試"
echo "2. 攻擊載荷生成性能測試"  
echo "3. 記憶體使用測試"
echo "4. 並發處理測試"
echo "5. 大量數據處理測試"
echo ""

# 創建臨時性能測試腳本
cat > /tmp/performance_test.py << 'EOF'
#!/usr/bin/env python3
"""性能測試腳本"""

import time
import sys
import asyncio
import psutil
import os
from pathlib import Path

# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class PerformanceTest:
    def __init__(self):
        self.results = {}
    
    def measure_time(self, func_name):
        """裝飾器：測量執行時間"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                self.results[func_name] = duration
                print(f"⏱️  {func_name}: {duration:.3f}秒")
                return result
            return wrapper
        return decorator
    
    @measure_time("模組載入測試")
    def test_module_loading(self):
        """測試模組載入性能"""
        try:
            # 測試核心模組載入
            from src.core.platform import PromptInjectionPlatform
            from src.core.reporter import ReportGenerator
            from src.core.evaluator import AttackEvaluator
            
            # 測試提供商模組載入
            from src.providers.github_provider import GitHubProvider
            from src.providers.openai_provider import OpenAIProvider
            
            # 測試攻擊模組載入
            from src.attacks.basic_injection import BasicInjectionAttack
            from src.attacks.role_playing import RolePlayingAttack
            
            return True
        except Exception as e:
            print(f"❌ 模組載入錯誤: {e}")
            return False
    
    @measure_time("平台初始化測試")  
    def test_platform_initialization(self):
        """測試平台初始化性能"""
        try:
            from src.core.platform import PromptInjectionPlatform
            platform = PromptInjectionPlatform()
            return True
        except Exception as e:
            print(f"❌ 平台初始化錯誤: {e}")
            return False
    
    @measure_time("攻擊載荷生成測試")
    def test_payload_generation(self):
        """測試攻擊載荷生成性能"""
        try:
            from src.attacks.basic_injection import BasicInjectionAttack
            from src.attacks.role_playing import RolePlayingAttack
            
            # 測試基本注入攻擊載荷生成
            basic_attack = BasicInjectionAttack()
            basic_payloads = basic_attack.get_payloads()
            
            # 測試角色扮演攻擊載荷生成
            role_attack = RolePlayingAttack()
            role_payloads = role_attack.get_payloads()
            
            total_payloads = len(basic_payloads) + len(role_payloads)
            print(f"      生成總載荷數: {total_payloads}")
            
            return True
        except Exception as e:
            print(f"❌ 載荷生成錯誤: {e}")
            return False
    
    def test_memory_usage(self):
        """測試記憶體使用情況"""
        print("💾 記憶體使用測試:")
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"      初始記憶體使用: {initial_memory:.2f} MB")
        
        # 執行一些操作來測試記憶體使用
        try:
            from src.core.platform import PromptInjectionPlatform
            from src.attacks.basic_injection import BasicInjectionAttack
            from src.core.reporter import ReportGenerator
            
            # 創建多個物件
            platforms = [PromptInjectionPlatform() for _ in range(10)]
            attacks = [BasicInjectionAttack() for _ in range(20)]
            reporters = [ReportGenerator() for _ in range(5)]
            
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
            print(f"      峰值記憶體使用: {peak_memory:.2f} MB")
            print(f"      記憶體增長: {peak_memory - initial_memory:.2f} MB")
            
            # 清理
            del platforms, attacks, reporters
            
            return True
        except Exception as e:
            print(f"❌ 記憶體測試錯誤: {e}")
            return False
    
    async def test_concurrent_processing(self):
        """測試並發處理性能"""
        print("🔄 並發處理測試:")
        
        try:
            from src.attacks.basic_injection import BasicInjectionAttack
            
            # 創建多個攻擊實例
            attacks = [BasicInjectionAttack() for _ in range(10)]
            
            # 並發執行載荷生成
            start_time = time.time()
            
            async def generate_payloads(attack):
                return attack.get_payloads()
            
            tasks = [generate_payloads(attack) for attack in attacks]
            results = await asyncio.gather(*tasks)
            
            end_time = time.time()
            duration = end_time - start_time
            
            total_payloads = sum(len(result) for result in results)
            print(f"      並發執行時間: {duration:.3f}秒")
            print(f"      總生成載荷數: {total_payloads}")
            print(f"      平均每秒生成: {total_payloads/duration:.1f} 個載荷")
            
            return True
        except Exception as e:
            print(f"❌ 並發測試錯誤: {e}")
            return False
    
    def test_large_data_processing(self):
        """測試大量數據處理"""
        print("📊 大量數據處理測試:")
        
        try:
            from src.core.reporter import ReportGenerator
            
            # 創建大量模擬數據
            large_dataset = []
            for i in range(1000):
                mock_result = type('MockResult', (), {
                    'attack_id': f'attack_{i}',
                    'attack_name': f'Test Attack {i}',
                    'attack_type': 'basic_injection',
                    'payload': f'Test payload {i}' * 10,  # 較長的載荷
                    'response': f'Test response {i}' * 20,  # 較長的回應
                    'success': i % 3 == 0,
                    'confidence': 0.5 + (i % 50) / 100,
                    'risk_level': ['low', 'medium', 'high'][i % 3],
                    'timestamp': time.time(),
                    'provider': 'test_provider',
                    'model': 'test_model',
                    'latency': 100 + (i % 500),
                    'metadata': {'test': True}
                })()
                large_dataset.append(mock_result)
            
            # 測試處理時間
            start_time = time.time()
            
            # 模擬評估處理
            processed_count = 0
            for result in large_dataset:
                # 模擬一些處理操作
                if hasattr(result, 'attack_type') and result.attack_type:
                    processed_count += 1
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"      處理數據量: {len(large_dataset)} 筆")
            print(f"      處理時間: {duration:.3f}秒") 
            print(f"      處理速度: {len(large_dataset)/duration:.1f} 筆/秒")
            print(f"      成功處理: {processed_count} 筆")
            
            return True
        except Exception as e:
            print(f"❌ 大數據處理錯誤: {e}")
            return False
    
    async def run_all_tests(self):
        """執行所有性能測試"""
        print("開始執行性能測試...")
        print("=" * 40)
        
        success_count = 0
        total_count = 0
        
        # 1. 模組載入性能測試
        total_count += 1
        if self.test_module_loading():
            success_count += 1
        
        # 2. 平台初始化測試
        total_count += 1  
        if self.test_platform_initialization():
            success_count += 1
        
        # 3. 攻擊載荷生成測試
        total_count += 1
        if self.test_payload_generation():
            success_count += 1
        
        # 4. 記憶體使用測試
        total_count += 1
        if self.test_memory_usage():
            success_count += 1
        
        # 5. 並發處理測試
        total_count += 1
        if await self.test_concurrent_processing():
            success_count += 1
        
        # 6. 大量數據處理測試
        total_count += 1
        if self.test_large_data_processing():
            success_count += 1
        
        print("\n" + "=" * 40)
        print("📊 性能測試結果摘要:")
        print(f"總測試數: {total_count}")
        print(f"通過: {success_count}")
        print(f"失敗: {total_count - success_count}")
        print(f"成功率: {(success_count/total_count*100):.1f}%")
        
        # 輸出詳細性能數據
        print("\n⏱️  詳細性能數據:")
        for test_name, duration in self.results.items():
            if duration < 1.0:
                status = "🚀 優秀"
            elif duration < 3.0:
                status = "✅ 良好"
            elif duration < 5.0:
                status = "⚠️  一般"
            else:
                status = "🐌 需優化"
            
            print(f"  {test_name}: {duration:.3f}秒 {status}")
        
        return success_count == total_count

async def main():
    test_suite = PerformanceTest()
    success = await test_suite.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
EOF

# 執行性能測試
echo -e "${BLUE}開始執行性能測試...${NC}"
echo ""

if python3 /tmp/performance_test.py; then
    echo ""
    echo -e "${GREEN}✅ 性能測試完成${NC}"
    TEST_RESULT=0
else
    echo ""
    echo -e "${RED}❌ 性能測試失敗${NC}"
    TEST_RESULT=1
fi

# 清理臨時檔案
rm -f /tmp/performance_test.py

# 計算總執行時間
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "========================================="
echo -e "${BLUE}📊 性能測試總結${NC}"
echo "========================================="
echo "總執行時間: ${DURATION}秒"

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}🎉 性能測試全部通過！平台性能表現良好。${NC}"
    echo ""
    echo -e "${BLUE}💡 性能優化建議:${NC}"
    echo "1. 定期監控記憶體使用情況"
    echo "2. 考慮實現攻擊載荷緩存機制"
    echo "3. 在高並發場景下使用適當的限流策略"
    echo "4. 定期清理大型測試結果檔案"
else
    echo -e "${RED}⚠️  性能測試發現問題，建議優化相關模組。${NC}"
    echo ""
    echo -e "${YELLOW}🔧 可能的優化方向:${NC}"
    echo "1. 檢查模組載入是否有不必要的依賴"
    echo "2. 優化攻擊載荷生成算法"
    echo "3. 實現記憶體池管理"
    echo "4. 考慮使用異步處理優化性能"
fi

exit $TEST_RESULT