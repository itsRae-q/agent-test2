import numpy as np
import pandas as pd

# 模拟生成100只股票的数据
np.random.seed(42)
n_stocks = 100

# 生成股票代码
stock_codes = [f'股票{i+1:03d}' for i in range(n_stocks)]

# 生成自由现金流（单位：亿元）
free_cashflow = np.random.uniform(1, 100, n_stocks)

# 生成企业价值（单位：亿元）
enterprise_value = np.random.uniform(50, 500, n_stocks)

# 计算自由现金流率
fcf_rate = free_cashflow / enterprise_value

# 按自由现金流率从高到低排序
sorted_indices = np.argsort(fcf_rate)[::-1]
stock_codes_sorted = [stock_codes[i] for i in sorted_indices]
free_cashflow_sorted = free_cashflow[sorted_indices]
enterprise_value_sorted = enterprise_value[sorted_indices]
fcf_rate_sorted = fcf_rate[sorted_indices]

# 根据自由现金流计算初始权重
total_fcf = np.sum(free_cashflow_sorted)
initial_weights = free_cashflow_sorted / total_fcf

# 应用10%权重上限
max_weight = 0.10
adjusted_weights = np.minimum(initial_weights, max_weight)

# 重新归一化权重（确保权重和为1）
adjusted_weights = adjusted_weights / np.sum(adjusted_weights)

# 创建结果DataFrame
result_df = pd.DataFrame({
    '股票代码': stock_codes_sorted,
    '自由现金流(亿元)': free_cashflow_sorted,
    '企业价值(亿元)': enterprise_value_sorted,
    '自由现金流率': fcf_rate_sorted,
    '权重': adjusted_weights
})

# 保存到CSV文件
result_df.to_csv('股票权重数据.csv', index=False, encoding='utf-8-sig')

print(f"已生成{len(result_df)}只股票的权重数据")
print(f"权重总和: {adjusted_weights.sum():.6f}")
print(f"最大权重: {adjusted_weights.max():.6f}")
print(f"前10只股票权重:")
print(result_df.head(10)[['股票代码', '权重']])
