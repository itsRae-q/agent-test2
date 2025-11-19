"""
国证自由现金流指数编制方案实现
CNI Free Cash Flow Index (CNIFCF) - 指数代码: 980092

基于技术规格文档实现的指数编排代码
基日：2012年12月31日，基点：1000点
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class CNIFreeCashFlowIndex:
    """国证自由现金流指数编制类"""
    
    def __init__(self):
        self.index_name = "国证自由现金流指数"
        self.index_code = "980092"
        self.base_date = "2012-12-31"
        self.base_point = 1000
        self.max_weight = 0.10  # 单只股票最大权重10%
        self.sample_size = 100  # 样本数量
        
    def generate_mock_stock_data(self, n_stocks=500):
        """
        生成模拟的股票数据，包含财务指标
        """
        np.random.seed(42)
        
        # 股票基本信息
        stock_codes = [f"{str(i).zfill(6)}.SH" if i % 2 == 0 else f"{str(i).zfill(6)}.SZ" 
                      for i in range(1, n_stocks + 1)]
        stock_names = [f"股票{i}" for i in range(1, n_stocks + 1)]
        
        # 行业分类（剔除金融和房地产）
        industries = ['制造业', '信息技术', '医药生物', '电子', '化工', '机械设备', 
                     '电气设备', '汽车', '食品饮料', '轻工制造', '建筑材料', '公用事业',
                     '交通运输', '商业贸易', '休闲服务', '农林牧渔', '采掘', '纺织服装',
                     '家用电器', '建筑装饰', '传媒', '通信', '计算机', '国防军工']
        
        # 生成财务数据
        data = []
        for i, (code, name) in enumerate(zip(stock_codes, stock_names)):
            # 基础数据
            market_cap = np.random.lognormal(15, 1.5)  # 市值（亿元）
            price = np.random.uniform(5, 100)  # 股价
            shares = market_cap * 1e8 / price  # 股本
            
            # 成交金额（剔除后20%）
            daily_turnover = np.random.lognormal(16, 1.2)  # 日均成交金额
            
            # 财务指标
            revenue = np.random.lognormal(20, 1)  # 营业收入
            operating_profit = revenue * np.random.uniform(0.05, 0.25)  # 营业利润
            
            # 现金流指标
            operating_cash_flow = operating_profit * np.random.uniform(0.8, 1.5)  # 经营活动现金流
            capex = revenue * np.random.uniform(0.03, 0.15)  # 资本支出
            free_cash_flow = operating_cash_flow - capex  # 自由现金流
            
            # 企业价值 (EV = 市值 + 净债务)
            net_debt = market_cap * np.random.uniform(-0.2, 0.5)
            enterprise_value = market_cap + net_debt
            
            # 自由现金流率
            fcf_yield = free_cash_flow / enterprise_value if enterprise_value > 0 else 0
            
            # ROE稳定性（12个季度）
            roe_stability = np.random.uniform(0.1, 0.9)  # 稳定性评分
            
            # 经营活动现金流占营业利润比例
            ocf_to_profit_ratio = operating_cash_flow / operating_profit if operating_profit > 0 else 0
            
            # 上市时间（模拟）
            listing_months = np.random.randint(7, 120)  # 上市7-120个月
            
            data.append({
                'stock_code': code,
                'stock_name': name,
                'industry': np.random.choice(industries),
                'market_cap': market_cap,
                'price': price,
                'shares': shares,
                'daily_turnover': daily_turnover,
                'revenue': revenue,
                'operating_profit': operating_profit,
                'operating_cash_flow': operating_cash_flow,
                'free_cash_flow': free_cash_flow,
                'enterprise_value': enterprise_value,
                'fcf_yield': fcf_yield,
                'roe_stability': roe_stability,
                'ocf_to_profit_ratio': ocf_to_profit_ratio,
                'listing_months': listing_months,
                'is_st': np.random.choice([True, False], p=[0.05, 0.95]),  # 5% ST股票
                'has_violation': np.random.choice([True, False], p=[0.03, 0.97]),  # 3% 违规
                'has_loss': np.random.choice([True, False], p=[0.1, 0.9]),  # 10% 亏损
                'price_abnormal': np.random.choice([True, False], p=[0.02, 0.98])  # 2% 价格异常
            })
        
        return pd.DataFrame(data)
    
    def apply_screening_criteria(self, df):
        """
        应用选样筛选条件
        """
        print("开始应用筛选条件...")
        original_count = len(df)
        
        # 1. 基础剔除条件
        print(f"原始股票数量: {len(df)}")
        
        # 剔除ST股票
        df = df[~df['is_st']]
        print(f"剔除ST股票后: {len(df)}")
        
        # 剔除上市时间不足的股票（简化处理，假设都是主板）
        df = df[df['listing_months'] >= 6]
        print(f"剔除上市时间不足股票后: {len(df)}")
        
        # 剔除有重大违规的股票
        df = df[~df['has_violation']]
        print(f"剔除违规股票后: {len(df)}")
        
        # 剔除重大亏损股票
        df = df[~df['has_loss']]
        print(f"剔除亏损股票后: {len(df)}")
        
        # 剔除价格异常波动股票
        df = df[~df['price_abnormal']]
        print(f"剔除价格异常股票后: {len(df)}")
        
        # 2. 第一步筛选：剔除成交金额后20%、金融房地产、ROE稳定性后10%
        turnover_threshold = df['daily_turnover'].quantile(0.2)
        df = df[df['daily_turnover'] > turnover_threshold]
        print(f"剔除成交金额后20%后: {len(df)}")
        
        # 剔除金融房地产（在模拟数据中已排除）
        
        # 剔除ROE稳定性后10%
        roe_threshold = df['roe_stability'].quantile(0.1)
        df = df[df['roe_stability'] > roe_threshold]
        print(f"剔除ROE稳定性后10%后: {len(df)}")
        
        # 3. 第二步筛选：现金流相关条件
        # 自由现金流为正
        df = df[df['free_cash_flow'] > 0]
        print(f"筛选自由现金流为正后: {len(df)}")
        
        # 企业价值为正
        df = df[df['enterprise_value'] > 0]
        print(f"筛选企业价值为正后: {len(df)}")
        
        # 经营活动现金流为正（近三年，简化为当期）
        df = df[df['operating_cash_flow'] > 0]
        print(f"筛选经营现金流为正后: {len(df)}")
        
        # 剔除经营活动现金流占营业利润比例后30%
        ocf_ratio_threshold = df['ocf_to_profit_ratio'].quantile(0.3)
        df = df[df['ocf_to_profit_ratio'] > ocf_ratio_threshold]
        print(f"剔除现金流利润比后30%后: {len(df)}")
        
        print(f"筛选完成，从 {original_count} 只股票筛选出 {len(df)} 只股票")
        return df.reset_index(drop=True)
    
    def select_index_components(self, df):
        """
        选择指数成分股：按自由现金流率排序，选取前100只
        """
        print(f"\n开始选择指数成分股...")
        
        # 按自由现金流率从高到低排序
        df_sorted = df.sort_values('fcf_yield', ascending=False).reset_index(drop=True)
        
        # 选取前100只作为指数样本
        index_components = df_sorted.head(self.sample_size).copy()
        
        # 选取接下来5%作为备选样本
        backup_size = max(1, int(self.sample_size * 0.05))
        backup_components = df_sorted.iloc[self.sample_size:self.sample_size + backup_size].copy()
        
        print(f"选出 {len(index_components)} 只成分股")
        print(f"选出 {len(backup_components)} 只备选股")
        
        return index_components, backup_components
    
    def calculate_weights(self, components_df):
        """
        计算权重：基于自由现金流率，单只股票权重不超过10%
        """
        print(f"\n开始计算权重...")
        
        # 基于自由现金流率计算初始权重
        fcf_yields = components_df['fcf_yield'].values
        
        # 确保所有自由现金流率都为正
        fcf_yields = np.maximum(fcf_yields, 0.0001)
        
        # 计算初始权重（与自由现金流率成正比）
        initial_weights = fcf_yields / fcf_yields.sum()
        
        # 应用权重上限约束（10%）
        adjusted_weights = self.apply_weight_constraints(initial_weights)
        
        # 添加权重到DataFrame
        components_df = components_df.copy()
        components_df['initial_weight'] = initial_weights
        components_df['adjusted_weight'] = adjusted_weights
        components_df['weight_adjustment_factor'] = adjusted_weights / initial_weights
        
        print(f"权重计算完成")
        print(f"最大权重: {adjusted_weights.max():.2%}")
        print(f"最小权重: {adjusted_weights.min():.2%}")
        print(f"权重总和: {adjusted_weights.sum():.4f}")
        
        return components_df
    
    def apply_weight_constraints(self, weights):
        """
        应用权重约束：单只股票权重不超过10%
        """
        weights = np.array(weights)
        max_iterations = 100
        
        for iteration in range(max_iterations):
            # 找出超过上限的权重
            excess_mask = weights > self.max_weight
            
            if not excess_mask.any():
                break
                
            # 计算超出部分
            excess_weights = weights[excess_mask] - self.max_weight
            total_excess = excess_weights.sum()
            
            # 将超出权重设为上限
            weights[excess_mask] = self.max_weight
            
            # 将超出部分按比例分配给未达到上限的股票
            remaining_mask = ~excess_mask
            if remaining_mask.any():
                remaining_capacity = self.max_weight - weights[remaining_mask]
                total_capacity = remaining_capacity.sum()
                
                if total_capacity > 0:
                    # 按剩余容量比例分配
                    allocation_ratio = remaining_capacity / total_capacity
                    weights[remaining_mask] += total_excess * allocation_ratio
                else:
                    # 如果所有股票都达到上限，等权重分配超出部分
                    weights[remaining_mask] += total_excess / remaining_mask.sum()
        
        # 确保权重和为1
        weights = weights / weights.sum()
        
        return weights
    
    def calculate_index_value(self, components_df, base_date=None, current_date=None):
        """
        计算指数值：使用派氏加权法
        """
        if base_date is None:
            base_date = self.base_date
        if current_date is None:
            current_date = datetime.now().strftime('%Y-%m-%d')
            
        print(f"\n计算指数值...")
        
        # 计算当前市值加权总值
        current_market_value = (components_df['price'] * components_df['shares'] * components_df['adjusted_weight']).sum()
        
        # 模拟基期市值（简化处理）
        base_market_value = current_market_value / np.random.uniform(1.5, 3.0)  # 假设指数涨幅
        
        # 计算指数值
        index_value = (current_market_value / base_market_value) * self.base_point
        
        print(f"基期市值: {base_market_value:,.0f}")
        print(f"当前市值: {current_market_value:,.0f}")
        print(f"指数值: {index_value:.2f}")
        
        return {
            'index_value': index_value,
            'base_market_value': base_market_value,
            'current_market_value': current_market_value,
            'calculation_date': current_date
        }
    
    def generate_index_report(self, components_df, index_info):
        """
        生成指数报告
        """
        print(f"\n生成指数报告...")
        
        # 基本信息
        report = {
            'index_info': {
                'name': self.index_name,
                'code': self.index_code,
                'base_date': self.base_date,
                'base_point': self.base_point,
                'calculation_date': index_info['calculation_date'],
                'index_value': index_info['index_value']
            },
            'components_summary': {
                'total_components': len(components_df),
                'max_weight': components_df['adjusted_weight'].max(),
                'min_weight': components_df['adjusted_weight'].min(),
                'avg_weight': components_df['adjusted_weight'].mean(),
                'weight_concentration': (components_df['adjusted_weight'] >= 0.05).sum()  # 权重>=5%的股票数
            }
        }
        
        # 成分股详细信息
        components_detail = components_df[['stock_code', 'stock_name', 'industry', 
                                         'market_cap', 'price', 'fcf_yield', 
                                         'adjusted_weight']].copy()
        components_detail = components_detail.sort_values('adjusted_weight', ascending=False)
        components_detail['weight_pct'] = components_detail['adjusted_weight'] * 100
        
        report['components'] = components_detail
        
        # 行业分布
        industry_weights = components_df.groupby('industry')['adjusted_weight'].sum().sort_values(ascending=False)
        report['industry_distribution'] = industry_weights
        
        return report
    
    def run_index_construction(self):
        """
        执行完整的指数编制流程
        """
        print("=" * 80)
        print(f"{self.index_name} ({self.index_code}) 编制流程")
        print("=" * 80)
        
        # 1. 生成模拟数据
        print("\n1. 生成股票池数据...")
        stock_data = self.generate_mock_stock_data(n_stocks=800)
        
        # 2. 应用筛选条件
        print("\n2. 应用筛选条件...")
        filtered_data = self.apply_screening_criteria(stock_data)
        
        # 3. 选择成分股
        print("\n3. 选择指数成分股...")
        components, backup = self.select_index_components(filtered_data)
        
        # 4. 计算权重
        print("\n4. 计算权重...")
        components_with_weights = self.calculate_weights(components)
        
        # 5. 计算指数值
        print("\n5. 计算指数值...")
        index_info = self.calculate_index_value(components_with_weights)
        
        # 6. 生成报告
        print("\n6. 生成指数报告...")
        report = self.generate_index_report(components_with_weights, index_info)
        
        print("\n" + "=" * 80)
        print("指数编制完成！")
        print("=" * 80)
        
        return report, components_with_weights, backup


def main():
    """
    主函数：执行国证自由现金流指数编制
    """
    # 创建指数编制实例
    index_constructor = CNIFreeCashFlowIndex()
    
    # 执行指数编制
    report, components, backup = index_constructor.run_index_construction()
    
    # 显示结果摘要
    print(f"\n📊 指数编制结果摘要:")
    print(f"指数名称: {report['index_info']['name']}")
    print(f"指数代码: {report['index_info']['code']}")
    print(f"当前指数值: {report['index_info']['index_value']:.2f}")
    print(f"成分股数量: {report['components_summary']['total_components']}")
    print(f"最大权重: {report['components_summary']['max_weight']:.2%}")
    print(f"权重>=5%股票数: {report['components_summary']['weight_concentration']}")
    
    print(f"\n🏭 行业分布 (前10):")
    for industry, weight in report['industry_distribution'].head(10).items():
        print(f"  {industry}: {weight:.2%}")
    
    print(f"\n📈 权重前10成分股:")
    top_components = report['components'].head(10)
    for _, stock in top_components.iterrows():
        print(f"  {stock['stock_code']} {stock['stock_name']}: {stock['weight_pct']:.2f}% "
              f"(FCF收益率: {stock['fcf_yield']:.2%})")
    
    return report, components, backup


if __name__ == "__main__":
    report, components, backup = main()