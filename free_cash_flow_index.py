"""
国证自由现金流指数权重计算
"""

import numpy as np
import pandas as pd


def generate_mock_stocks(n=15):
    """生成模拟股票数据"""
    np.random.seed(42)
    
    stocks = []
    for i in range(n):
        stock = {
            'code': f'{600000 + i:06d}',
            'name': f'股票{i+1}',
            'free_cash_flow': np.random.uniform(100, 1000),  # 自由现金流（万元）
            'enterprise_value': np.random.uniform(5000, 50000),  # 企业价值（万元）
            'operating_cash_flow': np.random.uniform(200, 2000),  # 经营活动现金流（万元）
            'operating_profit': np.random.uniform(300, 3000),  # 营业利润（万元）
        }
        # 计算自由现金流率
        stock['fcf_rate'] = stock['free_cash_flow'] / stock['enterprise_value']
        # 计算经营活动现金流占营业利润比例
        stock['ocf_ratio'] = stock['operating_cash_flow'] / stock['operating_profit'] if stock['operating_profit'] > 0 else 0
        stocks.append(stock)
    
    return pd.DataFrame(stocks)


def select_samples(df):
    """选样：按照自由现金流率从高到低排序，选取前N只"""
    # 确保所有数值为正
    df = df[
        (df['free_cash_flow'] > 0) & 
        (df['enterprise_value'] > 0) & 
        (df['operating_cash_flow'] > 0)
    ].copy()
    
    # 剔除经营活动现金流占营业利润比例排名后30%的证券
    threshold = df['ocf_ratio'].quantile(0.3)
    df = df[df['ocf_ratio'] >= threshold].copy()
    
    # 按自由现金流率从高到低排序
    df = df.sort_values('fcf_rate', ascending=False)
    
    # 选取前N只（如果数据量小于等于20，就选前10只）
    n_samples = min(10, len(df))
    selected = df.head(n_samples).copy()
    
    return selected


def calculate_weights(df, max_weight=0.10):
    """计算权重：根据自由现金流计算初始权重，单只样本权重不超过10%"""
    # 根据自由现金流计算初始权重
    total_fcf = df['free_cash_flow'].sum()
    initial_weights = df['free_cash_flow'] / total_fcf
    
    # 应用权重上限：使用迭代方法确保所有权重不超过上限
    adjusted_weights = initial_weights.copy()
    
    # 迭代调整直到所有权重都不超过上限
    max_iterations = 100
    for _ in range(max_iterations):
        # 将超过上限的权重设为上限
        adjusted_weights = np.minimum(adjusted_weights, max_weight)
        
        # 计算剩余权重
        remaining_weight = 1.0 - adjusted_weights.sum()
        
        # 如果剩余权重很小，可以停止
        if abs(remaining_weight) < 1e-6:
            break
        
        # 将剩余权重按比例分配给未达到上限的股票
        below_limit_mask = adjusted_weights < max_weight
        if below_limit_mask.sum() > 0:
            below_limit_weights = initial_weights[below_limit_mask]
            below_limit_total = below_limit_weights.sum()
            if below_limit_total > 0:
                adjustment = remaining_weight * (below_limit_weights / below_limit_total)
                adjusted_weights[below_limit_mask] += adjustment
        else:
            # 如果所有股票都达到上限，则按比例分配剩余权重
            adjusted_weights += remaining_weight / len(adjusted_weights)
    
    # 最终归一化确保权重和为1
    adjusted_weights = adjusted_weights / adjusted_weights.sum()
    
    # 再次确保不超过上限
    adjusted_weights = np.minimum(adjusted_weights, max_weight)
    adjusted_weights = adjusted_weights / adjusted_weights.sum()
    
    return adjusted_weights


def main():
    """主函数"""
    print("=" * 60)
    print("国证自由现金流指数权重计算")
    print("=" * 60)
    
    # 1. 生成模拟数据
    print("\n1. 生成模拟股票数据...")
    stocks_df = generate_mock_stocks(n=15)
    print(f"   生成了 {len(stocks_df)} 只股票数据")
    
    # 2. 选样
    print("\n2. 执行选样...")
    selected_df = select_samples(stocks_df)
    print(f"   选中 {len(selected_df)} 只样本股票")
    
    # 3. 计算权重
    print("\n3. 计算权重...")
    weights = calculate_weights(selected_df, max_weight=0.10)
    selected_df['weight'] = weights
    
    # 显示结果
    print("\n   样本股票及权重:")
    print(selected_df[['code', 'name', 'free_cash_flow', 'fcf_rate', 'weight']].to_string(index=False))
    print(f"\n   权重总和: {weights.sum():.6f}")
    print(f"   最大权重: {weights.max():.4%}")
    print(f"   最小权重: {weights.min():.4%}")
    
    # 4. 保存权重数据到文件
    print("\n4. 保存权重数据到文件...")
    output_df = selected_df[['code', 'name', 'weight']].copy()
    output_df['weight'] = output_df['weight'].apply(lambda x: f'{x:.6f}')
    output_df.to_csv('weights.csv', index=False, encoding='utf-8-sig')
    print("   权重数据已保存到 weights.csv")
    
    # 同时保存详细数据
    selected_df.to_csv('stock_details.csv', index=False, encoding='utf-8-sig')
    print("   详细数据已保存到 stock_details.csv")
    
    print("\n" + "=" * 60)
    print("计算完成！")
    print("=" * 60)
    
    return selected_df


if __name__ == "__main__":
    result = main()
