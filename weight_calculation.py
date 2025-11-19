import numpy as np
import pandas as pd

# 模拟100只样本股票的自由现金流数据
np.random.seed(42)
n_stocks = 100
stock_codes = [f'股票{i+1:03d}' for i in range(n_stocks)]
free_cash_flow = np.random.uniform(100, 10000, n_stocks)  # 模拟自由现金流（万元）

# 根据自由现金流计算初始权重
total_fcf = np.sum(free_cash_flow)
initial_weights = free_cash_flow / total_fcf

# 应用权重上限：单只样本权重不超过10%
max_weight = 0.10
adjusted_weights = np.minimum(initial_weights, max_weight)

# 重新归一化，确保权重和为1
remaining_weight = 1.0 - np.sum(adjusted_weights)
excess_weights = initial_weights - adjusted_weights
excess_weights[excess_weights < 0] = 0

if remaining_weight > 0 and np.sum(excess_weights) > 0:
    # 将剩余权重按比例分配给未达到上限的股票
    excess_normalized = excess_weights / np.sum(excess_weights)
    adjusted_weights += excess_normalized * remaining_weight
else:
    # 如果所有股票都达到上限，按比例缩减
    adjusted_weights = adjusted_weights / np.sum(adjusted_weights)

# 创建权重数据DataFrame
weight_data = pd.DataFrame({
    '股票代码': stock_codes,
    '自由现金流': free_cash_flow,
    '初始权重': initial_weights,
    '调整后权重': adjusted_weights
})

# 保存到CSV文件
weight_data.to_csv('股票权重数据.csv', index=False, encoding='utf-8-sig')
print(f"权重数据已保存到 股票权重数据.csv")
print(f"\n权重统计:")
print(f"总股票数: {len(weight_data)}")
print(f"权重和: {weight_data['调整后权重'].sum():.6f}")
print(f"最大权重: {weight_data['调整后权重'].max():.6%}")
print(f"最小权重: {weight_data['调整后权重'].min():.6%}")
print(f"\n前10只股票权重:")
print(weight_data.head(10)[['股票代码', '自由现金流', '调整后权重']])
