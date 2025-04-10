
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
dates = pd.date_range(start="2024-10-01", periods=6, freq="M")
revenue = [85345, 82100, 87700, 79900, 88200, 86964]
expenses = [59800, 60050, 61800, 58900, 61000, 59426]
net_profit = [r - e for r, e in zip(revenue, expenses)]

df = pd.DataFrame({
    "Date": dates,
    "Revenue": revenue,
    "Expenses": expenses,
    "Net Profit": net_profit
})

st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#004e3d;'>🟢 GENTYX Dashboard</h1>", unsafe_allow_html=True)

# Layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("Revenue Over Time")
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Revenue"], marker='o', color="#004e3d", linewidth=2)
    ax.set_facecolor("white")
    ax.set_xticklabels(df["Date"].dt.strftime('%b'), rotation=0)
    ax.set_ylabel("Amount ($)")
    ax.tick_params(colors="#555555")
    sns.despine()
    st.pyplot(fig)

with col2:
    st.subheader("Financial Health")
    st.markdown("<h2 style='color:#004e3d;'>82</h2>", unsafe_allow_html=True)

with col3:
    st.subheader("Net Profit")
    st.markdown("<h3 style='color:#004e3d;'>$27,538</h3>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("🧮 Scenario Simulator")

col4, col5 = st.columns(2)
sim_revenue = col4.slider("Simulated Revenue", 50000, 100000, 90000, 1000)
sim_expenses = col5.slider("Simulated Expenses", 30000, 90000, 62000, 1000)
sim_profit = sim_revenue - sim_expenses

sim_fig, sim_ax = plt.subplots()
sim_ax.bar(["Sim Revenue", "Sim Expenses", "Sim Profit"],
           [sim_revenue, sim_expenses, sim_profit],
           color=["#00795f", "#f4a261", "#2a9d8f"])
sim_ax.set_facecolor("white")
sns.despine()
st.pyplot(sim_fig)

st.markdown("---")
st.subheader("🧠 Actionable Insights")
st.markdown("- 🔹 15% increase in **operating expenses** last month.")
st.markdown("- 🔸 **Outstanding invoices** rose to $24,000 receivable.")
st.markdown("- 🟡 **Payroll expenses** increased by 25%.")
