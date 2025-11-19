"""
简单的风险平价模型策略
风险平价的核心思想：让每个资产对投资组合的风险贡献相等
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize


OUTPUT_DIR = Path(__file__).resolve().parent


def generate_mock_data(n_assets=4, n_days=252):
    """
    生成模拟的股票收益率数据
    """
    np.random.seed(42)
    
    # 生成随机收益率数据（日收益率）
    returns = np.random.randn(n_days, n_assets) * 0.02  # 标准差约2%
    
    # 添加一些相关性
    correlation_matrix = np.array([
        [1.0, 0.3, 0.2, 0.1],
        [0.3, 1.0, 0.25, 0.15],
        [0.2, 0.25, 1.0, 0.2],
        [0.1, 0.15, 0.2, 1.0]
    ])
    
    # 应用相关性
    L = np.linalg.cholesky(correlation_matrix)
    returns = returns @ L.T
    
    # 创建DataFrame
    asset_names = [f'资产{i+1}' for i in range(n_assets)]
    dates = pd.date_range(start='2023-01-01', periods=n_days, freq='D')
    df = pd.DataFrame(returns, index=dates, columns=asset_names)
    
    return df


def calculate_covariance_matrix(returns):
    """
    计算协方差矩阵
    """
    return returns.cov().values * 252  # 年化协方差矩阵


def risk_parity_objective(weights, cov_matrix):
    """
    风险平价的目标函数：最小化各资产风险贡献的方差
    """
    weights = np.array(weights)
    portfolio_vol = np.sqrt(weights.T @ cov_matrix @ weights)
    
    # 计算每个资产的风险贡献
    marginal_contrib = cov_matrix @ weights
    risk_contrib = weights * marginal_contrib / portfolio_vol
    
    # 目标：让所有风险贡献尽可能相等
    # 最小化风险贡献的方差
    target_risk = portfolio_vol / len(weights)  # 每个资产应该贡献的风险
    return np.sum((risk_contrib - target_risk) ** 2)


def optimize_risk_parity(cov_matrix):
    """
    优化风险平价权重
    """
    n_assets = cov_matrix.shape[0]
    
    # 初始权重：等权重
    initial_weights = np.ones(n_assets) / n_assets
    
    # 约束条件：权重和为1，权重非负
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
    ]
    
    bounds = [(0, 1) for _ in range(n_assets)]
    
    # 优化
    result = minimize(
        risk_parity_objective,
        initial_weights,
        args=(cov_matrix,),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'maxiter': 1000}
    )
    
    return result.x


def calculate_risk_contributions(weights, cov_matrix):
    """
    计算每个资产的风险贡献
    """
    weights = np.array(weights)
    portfolio_vol = np.sqrt(weights.T @ cov_matrix @ weights)
    
    # 边际风险贡献
    marginal_contrib = cov_matrix @ weights
    
    # 风险贡献
    risk_contrib = weights * marginal_contrib / portfolio_vol
    
    # 风险贡献百分比
    risk_contrib_pct = risk_contrib / portfolio_vol * 100
    
    return risk_contrib, risk_contrib_pct


def save_results(returns, optimal_weights, risk_contrib_pct, portfolio_vol):
    """
    将回测结果保存到文件
    """
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"risk_parity_{timestamp}"

    returns_file = OUTPUT_DIR / f"{base_name}_returns.csv"
    weights_file = OUTPUT_DIR / f"{base_name}_weights.csv"
    summary_file = OUTPUT_DIR / f"{base_name}_summary.json"

    # 保存收益率数据
    returns.to_csv(returns_file, index=True, encoding="utf-8")

    # 保存权重与风险贡献
    summary_df = pd.DataFrame({
        '资产': returns.columns,
        '权重': optimal_weights,
        '风险贡献占比(%)': risk_contrib_pct
    })
    summary_df.to_csv(weights_file, index=False, encoding="utf-8")

    metadata = {
        'timestamp': timestamp,
        'portfolio_volatility': float(portfolio_vol),
        'returns_file': str(returns_file.name),
        'weights_file': str(weights_file.name)
    }
    summary_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        'returns_file': str(returns_file),
        'weights_file': str(weights_file),
        'summary_file': str(summary_file)
    }


def main():
    """
    主函数：执行风险平价策略
    """
    print("=" * 60)
    print("风险平价模型策略")
    print("=" * 60)
    
    # 1. 生成模拟数据
    print("\n1. 生成模拟数据...")
    returns = generate_mock_data(n_assets=4, n_days=252)
    print(f"   生成了 {len(returns)} 天的收益率数据")
    print(f"   资产数量: {len(returns.columns)}")
    print(f"\n   收益率统计:")
    print(returns.describe())
    
    # 2. 计算协方差矩阵
    print("\n2. 计算协方差矩阵...")
    cov_matrix = calculate_covariance_matrix(returns)
    print(f"   协方差矩阵形状: {cov_matrix.shape}")
    print(f"\n   协方差矩阵:")
    print(pd.DataFrame(cov_matrix, 
                       index=returns.columns, 
                       columns=returns.columns))
    
    # 3. 优化风险平价权重
    print("\n3. 优化风险平价权重...")
    optimal_weights = optimize_risk_parity(cov_matrix)
    
    print(f"\n   最优权重:")
    for i, asset in enumerate(returns.columns):
        print(f"   {asset}: {optimal_weights[i]:.2%}")
    
    # 4. 计算风险贡献
    print("\n4. 计算风险贡献...")
    risk_contrib, risk_contrib_pct = calculate_risk_contributions(
        optimal_weights, cov_matrix
    )
    
    portfolio_vol = np.sqrt(optimal_weights.T @ cov_matrix @ optimal_weights)
    print(f"\n   投资组合年化波动率: {portfolio_vol:.2%}")
    print(f"\n   各资产风险贡献:")
    for i, asset in enumerate(returns.columns):
        print(f"   {asset}: {risk_contrib_pct[i]:.2f}%")
    
    # 5. 对比等权重策略
    print("\n5. 对比等权重策略...")
    equal_weights = np.ones(len(returns.columns)) / len(returns.columns)
    equal_vol = np.sqrt(equal_weights.T @ cov_matrix @ equal_weights)
    equal_risk_contrib, equal_risk_contrib_pct = calculate_risk_contributions(
        equal_weights, cov_matrix
    )
    
    print(f"\n   等权重策略:")
    print(f"   投资组合年化波动率: {equal_vol:.2%}")
    print(f"   各资产风险贡献:")
    for i, asset in enumerate(returns.columns):
        print(f"   {asset}: {equal_risk_contrib_pct[i]:.2f}%")
    
    # 6. 保存结果
    print("\n6. 保存结果到文件...")
    file_paths = save_results(returns, optimal_weights, risk_contrib_pct, portfolio_vol)
    print(f"   收益率数据: {file_paths['returns_file']}")
    print(f"   权重与风险贡献: {file_paths['weights_file']}")
    print(f"   元数据: {file_paths['summary_file']}")

    print("\n" + "=" * 60)
    print("策略执行完成！")
    print("=" * 60)
    
    # 返回结果
    results = {
        'weights': optimal_weights,
        'portfolio_volatility': portfolio_vol,
        'risk_contributions': risk_contrib_pct,
        'assets': returns.columns.tolist(),
        'files': file_paths
    }
    
    return results


if __name__ == "__main__":
    results = main()
