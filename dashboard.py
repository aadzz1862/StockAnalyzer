# dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
import io
from main import app, StockAnalyzerState

# Set Streamlit Page Config
st.set_page_config(
    page_title="📈 Market Sentiment Analyzer",
    layout="wide"
)

st.title("📈 Market Sentiment Dashboard")

# Sidebar Tickers
tickers = st.sidebar.multiselect(
    "Select Tickers to Analyze",
    options=["AAPL", "MSFT", "GOOGL", "META", "AMZN", "NVDA", "TSLA", "AI"],
    default=["AAPL", "MSFT", "GOOGL"]
)

# Button to run the pipeline
if st.button("Run Analysis"):
    # Initial state
    initial_state: StockAnalyzerState = {
        "tickers": tickers,
        "articles": [],
        "trends": {},
        "report": "",
        "llama_summary": ""
    }

    with st.spinner("Analyzing market sentiment..."):
        output = app.invoke(initial_state)

    # Display Markdown Report
    st.subheader("📄 Markdown Report")
    st.markdown(output["report"])

    # Display Llama Summary
    st.subheader("🧠 Llama 3 Summary")
    st.write(output["llama_summary"])

    # 🚀 Download Buttons
    st.subheader("⬇️ Download Reports")

    # Download Markdown Report (.md)
    markdown_bytes = output["report"].encode('utf-8')
    st.download_button(
        label="Download Markdown Report 📄",
        data=markdown_bytes,
        file_name="market_report.md",
        mime="text/markdown"
    )

    # Download Llama 3 Summary (.txt)
    llama_bytes = output["llama_summary"].encode('utf-8')
    st.download_button(
        label="Download Llama Summary 🧠",
        data=llama_bytes,
        file_name="llama_summary.txt",
        mime="text/plain"
    )

    # 🚀 Sentiment Chart
    st.subheader("📊 Sentiment Overview")

    trends = output.get("trends", {})

    if trends:
        # Create a DataFrame from trends
        df = pd.DataFrame([
            {
                "Ticker": ticker,
                "Positive": data["positive"],
                "Negative": data["negative"],
                "Neutral": data["neutral"],
                "Avg Sentiment Score": data["avg_sentiment_score"]
            }
            for ticker, data in trends.items()
        ])

        st.dataframe(df)

        # Bar chart: Average Sentiment Score per Ticker
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Ticker', sort='-y'),
            y=alt.Y('Avg Sentiment Score'),
            color=alt.condition(
                alt.datum["Avg Sentiment Score"] > 0,
                alt.value("green"),
                alt.value("red")
            )
        ).properties(
            title="Average Sentiment Score per Ticker"
        )

        st.altair_chart(chart, use_container_width=True)

        # Stacked bar chart: Positive, Negative, Neutral counts
        df_melted = df.melt(id_vars=['Ticker'], value_vars=['Positive', 'Negative', 'Neutral'],
                            var_name='Sentiment', value_name='Count')

        stacked_chart = alt.Chart(df_melted).mark_bar().encode(
            x='Ticker:N',
            y='Count:Q',
            color='Sentiment:N'
        ).properties(
            title="Sentiment Breakdown per Ticker"
        )

        st.altair_chart(stacked_chart, use_container_width=True)

else:
    st.info("⬅️ Select tickers and click 'Run Analysis' to begin.")

