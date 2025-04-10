
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai

openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")  # Replace or set in secrets.toml

# Theme and layout
st.set_page_config(page_title="Gentyx Dashboard", layout="wide")
st.markdown("""
    <style>
    body, html, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f9f9f4;
    }
    h1, h2, h3 {
        color: #004e3d;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

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

# Header
st.markdown("<h1>🟢 GENTYX Financial Dashboard</h1>", unsafe_allow_html=True)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"${df['Revenue'].iloc[-1]:,}")
col2.metric("Expenses", f"${df['Expenses'].iloc[-1]:,}")
col3.metric("Net Profit", f"${df['Net Profit'].iloc[-1]:,}")

# Chart
st.subheader("📈 Revenue Over Time")
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Revenue"], marker='o', color="#004e3d", linewidth=2)
ax.set_facecolor("white")
st.pyplot(fig)

# Scenario Sim
st.subheader("🧮 Scenario Simulator")
sim_rev = st.slider("Simulated Revenue", 50000, 100000, df['Revenue'].iloc[-1], 1000)
sim_exp = st.slider("Simulated Expenses", 30000, 90000, df['Expenses'].iloc[-1], 1000)
sim_profit = sim_rev - sim_exp
delta = sim_profit - df["Net Profit"].iloc[-1]
st.metric("Simulated Net Profit", f"${sim_profit:,}", f"{delta:+,.0f}")

# Chatbot section
st.markdown("---")
st.subheader("🧠 Ask Gen – Your Gentyx AI Copilot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask a financial question...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Gen, a friendly, expert financial assistant for business owners. Be concise and helpful."},
                *st.session_state.chat_history
            ]
        )
        ai_msg = response.choices[0].message["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": ai_msg})
    except Exception as e:
        ai_msg = f"⚠️ Error: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": ai_msg})

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
