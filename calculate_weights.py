import numpy as np
import pandas as pd

# 生成模拟的样本数据（100只股票）
np.random.seed(42)
n_stocks = 100

# 生成股票代码
stock_codes = [f'股票{i+1:03d}' for i in range(n_stocks)]

# 生成模拟数据：自由现金流和企业价值
free_cash_flow = np.random.uniform(100, 10000, n_stocks)  # 自由现金流（万元）
enterprise_value = np.random.uniform(10000, 100000, n_stocks)  # 企业价值（万元）

# 创建数据框
df = pd.DataFrame({
    '股票代码': stock_codes,
    '自由现金流': free_cash_flow,
    '企业价值': enterprise_value
})

# 计算自由现金流率
df['自由现金流率'] = df['自由现金流'] / df['企业价值']

# 按自由现金流率从高到低排序
df = df.sort_values('自由现金流率', ascending=False).reset_index(drop=True)

# 根据自由现金流计算初始权重（归一化）
initial_weights = df['自由现金流'].values
initial_weights = initial_weights / initial_weights.sum()

# 应用权重调整因子：确保单只样本权重不超过10%
max_weight = 0.10
adjusted_weights = np.minimum(initial_weights, max_weight)

# 重新归一化，使权重和为1
remaining_weight = 1.0 - adjusted_weights.sum()
if remaining_weight > 0:
    # 将剩余权重分配给未达到上限的股票
    excess_mask = initial_weights < max_weight
    if excess_mask.sum() > 0:
        excess_weights = initial_weights[excess_mask]
        excess_weights_normalized = excess_weights / excess_weights.sum()
        adjusted_weights[excess_mask] += excess_weights_normalized * remaining_weight
    else:
        # 如果所有股票都达到上限，按比例分配剩余权重
        adjusted_weights = adjusted_weights / adjusted_weights.sum()

# 确保权重和为1
adjusted_weights = adjusted_weights / adjusted_weights.sum()

# 添加权重到数据框
df['权重'] = adjusted_weights

# 保存到CSV文件
output_file = 'stock_weights.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"权重数据已保存到 {output_file}")
print(f"\n前10只股票权重:")
print(df[['股票代码', '自由现金流', '企业价值', '自由现金流率', '权重']].head(10).to_string(index=False))
print(f"\n权重统计:")
print(f"总权重: {df['权重'].sum():.6f}")
print(f"最大权重: {df['权重'].max():.6f}")
print(f"最小权重: {df['权重'].min():.6f}")
