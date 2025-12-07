import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from blockchain_connect import log_alert_to_blockchain, get_alert_count, get_alert

# ===========================================
#   Load Trained Model & Metadata
# ===========================================
model = joblib.load("cyber_ai_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")
metrics = joblib.load("metrics.pkl")

# ===========================================
#   Streamlit Page Configuration
# ===========================================
st.set_page_config(page_title="Cybersecurity AI + Blockchain Dashboard", layout="wide")
st.title("Cybersecurity AI + Blockchain Dashboard")
st.markdown("AI-driven cyberattack detection with immutable blockchain alert logging")

# ===========================================
#   Tabs Layout
# ===========================================
tab1, tab2, tab3 = st.tabs(["Prediction", "Model Insights", "Blockchain Logs"])

# ===========================================
# TAB 1: Prediction + Blockchain Logging
# ===========================================
with tab1:
    st.subheader("Make a New Prediction")

    with st.form("input_form"):
        session_id = st.text_input("Session ID", "SID_00001")
        packet_size = st.number_input("Network Packet Size", min_value=100, max_value=2000, value=500)
        protocol = st.selectbox("Protocol Type", ["TCP", "UDP"])
        login_attempts = st.number_input("Login Attempts", min_value=0, max_value=10, value=2)
        session_duration = st.number_input("Session Duration (seconds)", min_value=0.0, value=500.0)
        encryption = st.selectbox("Encryption Used", ["DES", "AES"])
        ip_reputation = st.number_input("IP Reputation Score", min_value=0.0, max_value=1.0, value=0.5)
        failed_logins = st.number_input("Failed Logins", min_value=0, max_value=10, value=1)
        browser = st.selectbox("Browser Type", ["Chrome", "Firefox", "Edge", "Unknown"])
        unusual_time = st.selectbox("Unusual Time Access", [0, 1])
        submit_btn = st.form_submit_button("🔍 Analyze Session")

    if submit_btn:
        sample = pd.DataFrame([{
            "network_packet_size": packet_size,
            "protocol_type": protocol,
            "login_attempts": login_attempts,
            "session_duration": session_duration,
            "encryption_used": encryption,
            "ip_reputation_score": ip_reputation,
            "failed_logins": failed_logins,
            "browser_type": browser,
            "unusual_time_access": unusual_time
        }])

        for col in ["protocol_type", "encryption_used", "browser_type"]:
            sample[col] = label_encoders[col].transform(sample[col])

        sample_scaled = scaler.transform(sample)

        prediction = model.predict(sample_scaled)[0]
        prob = model.predict_proba(sample_scaled)[0][1]

        st.write("---")
        if prediction == 1:
            st.error(f"**Attack Detected!** Confidence: {prob:.2f}")
        else:
            st.success(f"**Normal Traffic** | Attack Probability: {prob:.2f}")

        with st.spinner("⛓ Logging result to blockchain..."):
            tx = log_alert_to_blockchain(session_id, bool(prediction))
        if tx:
            st.info(f"Logged on Blockchain | TxHash: `{tx}`")

# ===========================================
# TAB 2: Model Insights
# ===========================================
with tab2:
    st.subheader("Model Performance & Insights")
    st.metric("Model Accuracy", f"{metrics['accuracy']*100:.2f}%")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Confusion Matrix")
        cm = np.array(metrics["confusion_matrix"])
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        st.pyplot(fig)

    with col2:
        st.write("### Feature Importance")
        feature_importances = pd.DataFrame({
            "Feature": metrics["features"],
            "Importance": metrics["feature_importances"]
        }).sort_values(by="Importance", ascending=False)

        fig2, ax2 = plt.subplots()
        sns.barplot(x="Importance", y="Feature", data=feature_importances, ax=ax2, palette="viridis")
        st.pyplot(fig2)

# ===========================================
# TAB 3: Blockchain Logs
# ===========================================
with tab3:
    st.subheader("Blockchain Log Summary")

    if st.button("View Recent Alerts"):
        count = get_alert_count()
        st.write(f"Total Alerts on Blockchain: {count}")

        if count == 0:
            st.info("No alerts recorded yet.")
        else:
            for i in range(max(0, count - 5), count):  # last 5
                sid, detected, ts = get_alert(i)
                st.write(f"Session: `{sid}` | Attack: `{detected}` | Time: `{ts}`")
