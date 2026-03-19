import streamlit as st
import requests
import json
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI BI Copilot", page_icon="🧠", layout="wide")

st.title("🧠 AI Business Intelligence Copilot")
st.markdown("Ask your data anything and instantly get charts, insights, and decisions.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for file uploads
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_files = st.file_uploader("Upload CSV or PDF", type=["csv", "pdf", "xlsx"], accept_multiple_files=True)
    if st.button("Process Files"):
        if uploaded_files:
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            with st.spinner("Uploading & Indexing..."):
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(f"Uploaded {len(uploaded_files)} files successfully!")
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"Connection Error: Is the API running? {e}")
        else:
            st.warning("Please select a file first.")

# Main Chat Interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "charts" in msg and msg["charts"]:
            for chart_data in msg["charts"]:
                try:
                    # Render plotly JSON
                    fig = go.Figure(data=chart_data.get("data", []), layout=chart_data.get("layout", {}))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to render chart: {e}")

# Chat input
if query := st.chat_input("Ask a question about your data (e.g. 'Show revenue trend')"):
    # Add user msg to state and display
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call backend API
    with st.spinner("Analyzing..."):
        try:
            payload = {
                "query": query,
                "history": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            }
            response = requests.post(f"{API_URL}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                bot_text = data.get("text", "No response text.")
                bot_charts = data.get("charts", [])
                
                if bot_charts:
                    bot_text += f"\n\n*(Generated {len(bot_charts)} charts)*"
                
                # Add to state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": bot_text,
                    "charts": bot_charts
                })
                
                # Display
                with st.chat_message("assistant"):
                    st.markdown(bot_text)
                    if bot_charts:
                        for bot_chart in bot_charts:
                            try:
                                fig = go.Figure(data=bot_chart.get("data", []), layout=bot_chart.get("layout", {}))
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"Chart render error: {e}")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
