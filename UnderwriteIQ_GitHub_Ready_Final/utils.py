
import pandas as pd

def calculate_ratios(balance_sheet, income_statement):
    total_assets = balance_sheet.loc['Total Assets']
    total_liabilities = balance_sheet.loc['Total Liabilities']
    current_assets = balance_sheet.loc['Total Current Assets']
    current_liabilities = balance_sheet.loc['Total Current Liabilities']
    inventory = balance_sheet.loc['Inventory']
    accounts_receivable = balance_sheet.loc['Accounts Receivable']
    cogs = income_statement.loc['COGS']
    revenue = income_statement.loc['Revenue']

    current_ratio = current_assets / current_liabilities
    quick_ratio = (current_assets - inventory) / current_liabilities
    inventory_turnover = cogs / inventory
    receivables_turnover = revenue / accounts_receivable
    debt_to_assets = total_liabilities / total_assets
    debt_to_equity = total_liabilities / (total_assets - total_liabilities)

    ratios = {
        'Current Ratio': round(current_ratio, 2),
        'Quick Ratio': round(quick_ratio, 2),
        'Inventory Turnover': round(inventory_turnover, 2),
        'Receivables Turnover': round(receivables_turnover, 2),
        'Debt to Assets': round(debt_to_assets, 2),
        'Debt to Equity': round(debt_to_equity, 2)
    }

    return ratios

def compare_to_benchmarks(ratios, industry_benchmark):
    flags = {}
    for k, v in ratios.items():
        benchmark_value = industry_benchmark.get(k)
        if benchmark_value is None:
            continue
        if k in ['Current Ratio', 'Quick Ratio', 'Inventory Turnover', 'Receivables Turnover']:
            if v >= benchmark_value:
                flags[k] = '✅ In Line or Above'
            elif v >= benchmark_value * 0.9:
                flags[k] = '⚠️ Slightly Below'
            else:
                flags[k] = '❌ Red Flag'
        else:
            if v <= benchmark_value:
                flags[k] = '✅ In Line or Better'
            elif v <= benchmark_value * 1.1:
                flags[k] = '⚠️ Slightly High'
            else:
                flags[k] = '❌ Red Flag'
    return flags
