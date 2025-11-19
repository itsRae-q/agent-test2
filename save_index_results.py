"""
保存国证自由现金流指数结果到文档
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from cni_free_cash_flow_index import CNIFreeCashFlowIndex


def save_results_to_files():
    """
    运行指数编制并保存结果到多种格式文档
    """
    print("开始运行指数编制并保存结果...")
    
    # 创建指数编制实例并运行
    index_constructor = CNIFreeCashFlowIndex()
    report, components, backup = index_constructor.run_index_construction()
    
    # 准备保存的数据
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. 保存成分股持仓及权重数据到CSV
    holdings_data = components[['stock_code', 'stock_name', 'industry', 'market_cap', 
                               'price', 'shares', 'fcf_yield', 'adjusted_weight']].copy()
    holdings_data['weight_pct'] = holdings_data['adjusted_weight'] * 100
    holdings_data = holdings_data.sort_values('adjusted_weight', ascending=False)
    
    # 重命名列为中文
    holdings_data.columns = ['股票代码', '股票名称', '所属行业', '市值(亿元)', 
                            '股价', '股本', '自由现金流率', '权重', '权重(%)']
    
    csv_filename = f'国证自由现金流指数_成分股持仓_{current_time}.csv'
    holdings_data.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"✅ 成分股持仓数据已保存到: {csv_filename}")
    
    # 2. 保存行业分布数据
    industry_dist = report['industry_distribution'].reset_index()
    industry_dist.columns = ['行业', '权重']
    industry_dist['权重(%)'] = industry_dist['权重'] * 100
    
    industry_filename = f'国证自由现金流指数_行业分布_{current_time}.csv'
    industry_dist.to_csv(industry_filename, index=False, encoding='utf-8-sig')
    print(f"✅ 行业分布数据已保存到: {industry_filename}")
    
    # 3. 保存完整的指数报告到JSON
    # 处理numpy类型以便JSON序列化
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        return obj
    
    # 转换报告数据
    json_report = {}
    for key, value in report.items():
        if isinstance(value, dict):
            json_report[key] = {k: convert_numpy(v) for k, v in value.items()}
        else:
            json_report[key] = convert_numpy(value)
    
    json_filename = f'国证自由现金流指数_完整报告_{current_time}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, ensure_ascii=False, indent=2)
    print(f"✅ 完整指数报告已保存到: {json_filename}")
    
    # 4. 生成详细的文本报告
    txt_filename = f'国证自由现金流指数_详细报告_{current_time}.txt'
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("国证自由现金流指数 (CNI Free Cash Flow Index) 详细报告\n")
        f.write("=" * 80 + "\n\n")
        
        # 基本信息
        f.write("📋 指数基本信息\n")
        f.write("-" * 40 + "\n")
        f.write(f"指数名称: {report['index_info']['name']}\n")
        f.write(f"指数代码: {report['index_info']['code']}\n")
        f.write(f"基准日期: {report['index_info']['base_date']}\n")
        f.write(f"基准点数: {report['index_info']['base_point']}\n")
        f.write(f"计算日期: {report['index_info']['calculation_date']}\n")
        f.write(f"当前指数值: {report['index_info']['index_value']:.2f}\n\n")
        
        # 成分股概况
        f.write("📊 成分股概况\n")
        f.write("-" * 40 + "\n")
        f.write(f"成分股总数: {report['components_summary']['total_components']}\n")
        f.write(f"最大权重: {report['components_summary']['max_weight']:.2%}\n")
        f.write(f"最小权重: {report['components_summary']['min_weight']:.2%}\n")
        f.write(f"平均权重: {report['components_summary']['avg_weight']:.2%}\n")
        f.write(f"权重≥5%股票数: {report['components_summary']['weight_concentration']}\n\n")
        
        # 行业分布
        f.write("🏭 行业分布\n")
        f.write("-" * 40 + "\n")
        for industry, weight in report['industry_distribution'].items():
            f.write(f"{industry}: {weight:.2%}\n")
        f.write("\n")
        
        # 权重前20成分股
        f.write("📈 权重前20成分股\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'排名':<4} {'股票代码':<12} {'股票名称':<10} {'权重':<8} {'自由现金流率':<12} {'所属行业':<10}\n")
        f.write("-" * 80 + "\n")
        
        top_20 = report['components'].head(20)
        for idx, (_, stock) in enumerate(top_20.iterrows(), 1):
            f.write(f"{idx:<4} {stock['stock_code']:<12} {stock['stock_name']:<10} "
                   f"{stock['weight_pct']:.2f}%{'':<3} {stock['fcf_yield']:.2%}{'':<6} {stock['industry']:<10}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("报告生成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("=" * 80 + "\n")
    
    print(f"✅ 详细文本报告已保存到: {txt_filename}")
    
    # 5. 生成Excel格式的综合报告
    try:
        excel_filename = f'国证自由现金流指数_综合报告_{current_time}.xlsx'
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # 成分股持仓
            holdings_data.to_excel(writer, sheet_name='成分股持仓', index=False)
            
            # 行业分布
            industry_dist.to_excel(writer, sheet_name='行业分布', index=False)
            
            # 指数基本信息
            basic_info = pd.DataFrame([
                ['指数名称', report['index_info']['name']],
                ['指数代码', report['index_info']['code']],
                ['基准日期', report['index_info']['base_date']],
                ['基准点数', report['index_info']['base_point']],
                ['计算日期', report['index_info']['calculation_date']],
                ['当前指数值', f"{report['index_info']['index_value']:.2f}"],
                ['成分股总数', report['components_summary']['total_components']],
                ['最大权重', f"{report['components_summary']['max_weight']:.2%}"],
                ['最小权重', f"{report['components_summary']['min_weight']:.2%}"],
                ['平均权重', f"{report['components_summary']['avg_weight']:.2%}"]
            ], columns=['项目', '数值'])
            basic_info.to_excel(writer, sheet_name='指数基本信息', index=False)
        
        print(f"✅ Excel综合报告已保存到: {excel_filename}")
    except ImportError:
        print("⚠️  未安装openpyxl，跳过Excel文件生成")
    
    # 输出文件清单
    print(f"\n📁 生成的文件清单:")
    print(f"  1. {csv_filename} - 成分股持仓数据")
    print(f"  2. {industry_filename} - 行业分布数据")
    print(f"  3. {json_filename} - 完整JSON报告")
    print(f"  4. {txt_filename} - 详细文本报告")
    if 'excel_filename' in locals():
        print(f"  5. {excel_filename} - Excel综合报告")
    
    return {
        'csv_file': csv_filename,
        'industry_file': industry_filename,
        'json_file': json_filename,
        'txt_file': txt_filename,
        'excel_file': excel_filename if 'excel_filename' in locals() else None
    }


if __name__ == "__main__":
    files = save_results_to_files()
    print(f"\n🎉 所有文件保存完成！")