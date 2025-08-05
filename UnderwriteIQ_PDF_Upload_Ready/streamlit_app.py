
import streamlit as st
import pandas as pd
import pdfplumber
from utils import calculate_ratios, compare_to_benchmarks

st.set_page_config(page_title="UnderwriteIQ", layout="wide")

def extract_tables_from_pdf(pdf_file):
    balance_sheet = None
    income_statement = None

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                flat_table = [cell for row in table for cell in row if cell]
                if "Total Assets" in flat_table:
                    balance_sheet = pd.DataFrame(table[1:], columns=table[0]).set_index(table[0][0])
                elif "Revenue" in flat_table:
                    income_statement = pd.DataFrame(table[1:], columns=table[0]).set_index(table[0][0])

    return balance_sheet, income_statement

st.markdown("<h1 style='color: white; background-color: #1E3A8A; padding: 20px;'>UnderwriteIQ</h1>", unsafe_allow_html=True)

st.subheader("Upload Financial Statements")

uploaded_file = st.file_uploader("Browse files here...", type=["xlsx", "pdf"])
industry = st.selectbox("Select Industry", ['Retail Imports', 'Logistics & Freight Forwarding', 'Manufacturing', 'Construction Services'])

if uploaded_file is not None and industry:
    if uploaded_file.name.endswith('.pdf'):
        balance_sheet, income_statement = extract_tables_from_pdf(uploaded_file)
    else:
        balance_sheet = pd.read_excel(uploaded_file, sheet_name='Balance Sheet', index_col=0)
        income_statement = pd.read_excel(uploaded_file, sheet_name='Income Statement', index_col=0)

    if balance_sheet is None or income_statement is None:
        st.error("Could not extract tables from the uploaded file. Please ensure the document contains clear tables.")
    else:
        benchmarks_df = pd.read_csv('benchmarks/industry_benchmarks.csv')
        industry_benchmark = benchmarks_df[benchmarks_df['Industry'] == industry].iloc[0].to_dict()

        ratios = calculate_ratios(balance_sheet, income_statement)
        flags = compare_to_benchmarks(ratios, industry_benchmark)

        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("### Ratio Analysis")
            st.markdown("<table style='width:100%'><tr><th>Ratio</th><th>Value</th><th>vs-Benchmark</th></tr>", unsafe_allow_html=True)
            for k, v in ratios.items():
                flag = flags.get(k, 'N/A')
                color = 'green' if '✅' in flag else ('orange' if '⚠️' in flag else 'red' if '❌' in flag else 'black')
                st.markdown(f"<tr><td>{k}</td><td>{v}</td><td style='color:{color};'>{flag}</td></tr>", unsafe_allow_html=True)
            st.markdown("</table>", unsafe_allow_html=True)

        with col2:
            st.markdown("### Underwriting Summary")
            decision = "APPROVE" if all(['❌' not in f for f in flags.values()]) else "REVIEW"
            decision_color = "green" if decision == "APPROVE" else "orange"
            st.markdown(f"<h3 style='color: {decision_color};'>{decision}</h3>", unsafe_allow_html=True)
            st.markdown("""
            Strong liquidity position. Current and quick ratios evaluated against industry benchmarks.
            
            Inventory and receivables turnover efficiency assessed for operational risk.
            
            Solvency stability reviewed through debt-related ratios compared to industry norms.
            """)
            st.button("Download PDF (Coming Soon)")
