"""
Multi-Disease Prediction System
=================================
"""
import json
import pickle


import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="HealthPulse Analytics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Caching helpers
# ----------------------------------------------------------------------
@st.cache_resource
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_metrics():
    with open("models/model_metrics.json") as f:
        return json.load(f)


@st.cache_data
def load_dataset(path):
    return pd.read_csv(path)


diabetes_bundle = load_model("models/diabetes_model.pkl")
heart_bundle = load_model("models/heart_model.pkl")
parkinsons_bundle = load_model("models/parkinsons_model.pkl")
metrics = load_metrics()

diabetes_df = load_dataset("data/diabetes_clean.csv")
heart_df = load_dataset("data/heart_clean.csv")
parkinsons_df = load_dataset("data/parkinsons_clean.csv")

# ----------------------------------------------------------------------
# HealthPulse design system
# ----------------------------------------------------------------------
from pathlib import Path

with open("assets/styles.css", encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
.result-positive {
    background: #FFF4F2;
    border: 1px solid #F4C9C3;
    border-left: 5px solid #C75B50;
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    font-size: 1rem;
    color: #762F2A;
}
.result-negative {
    background: #EFF9F6;
    border: 1px solid #C6E9DF;
    border-left: 5px solid #268A72;
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    font-size: 1rem;
    color: #205E50;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
st.sidebar.markdown("## 🩺 HealthPulse")
st.sidebar.caption("Healthcare Intelligence Platform")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🍬 Diabetes Prediction",
        "❤️ Heart Disease Prediction",
        "🧠 Parkinson's Prediction",
        "📊 Data Analysis Dashboard",
        "📈 Model Performance",
    ],
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "B.Tech Final Year Project · Built with scikit-learn & Streamlit"
)

# ========================================================================
# HOME
# ========================================================================
if page == "🏠 Home":
    st.markdown('<div class="hp-hero"><div class="hp-eyebrow">HEALTHCARE INTELLIGENCE PLATFORM</div><h1>HealthPulse Analytics</h1><p>Understand health data. Explore patterns. Support better-informed decisions.</p></div>', unsafe_allow_html=True)
    st.markdown("")
    st.subheader("Platform overview")
    st.markdown(
        "##### An ML-powered clinical decision-support tool for early "
        "detection of Diabetes, Heart Disease, and Parkinson's Disease"
    )
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Diabetes Model Accuracy",
                   f"{metrics['diabetes'][metrics['diabetes']['best_model']]['test_accuracy']*100:.1f}%")
        st.caption(f"Best model: {metrics['diabetes']['best_model']}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Heart Disease Model Accuracy",
                   f"{metrics['heart'][metrics['heart']['best_model']]['test_accuracy']*100:.1f}%")
        st.caption(f"Best model: {metrics['heart']['best_model']}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Parkinson's Model Accuracy",
                   f"{metrics['parkinsons'][metrics['parkinsons']['best_model']]['test_accuracy']*100:.1f}%")
        st.caption(f"Best model: {metrics['parkinsons']['best_model']}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("###")
    st.subheader("How it works")
    st.markdown("""
    1. **Choose a disease** from the sidebar (Diabetes, Heart Disease, or Parkinson's).
    2. **Enter the patient's clinical or voice-measurement values** into the input form.
    3. The app **scales your inputs** the same way the training data was scaled, then
       feeds them into a **trained machine-learning model**.
    4. You instantly see a **prediction** (positive / negative) along with the
       model's **confidence score**.
    5. Explore the **Data Analysis Dashboard** to understand the underlying datasets,
       and the **Model Performance** page to see how different algorithms were compared.
    """)

    st.subheader("Project scope")
    c1, c2, c3 = st.columns(3)
    c1.info("**Diabetes**\n\nPredicted from 8 clinical measurements "
            "(glucose, BMI, blood pressure, etc.) using the Pima Indians "
            "Diabetes dataset (768 patients).")
    c2.info("**Heart Disease**\n\nPredicted from 13 clinical attributes "
            "(chest pain type, cholesterol, ECG results, etc.) using the "
            "UCI Cleveland Heart Disease dataset (303 patients).")
    c3.info("**Parkinson's Disease**\n\nPredicted from 22 biomedical voice "
            "measurements (jitter, shimmer, frequency, etc.) using the UCI "
            "Oxford Parkinson's dataset (195 voice recordings).")

    st.markdown("---")
    st.warning(
        "⚠️ **Educational-use disclaimer:** Predictions are experimental outputs "
        "from models trained on public datasets. They are not diagnoses, do not "
        "represent validated individual clinical risk, and must not guide treatment. "
        "Consult a qualified healthcare professional for medical decisions."
    )

# ========================================================================
# DIABETES PREDICTION
# ========================================================================
elif page == "🍬 Diabetes Prediction":
    st.title("🍬 Diabetes Prediction")
    st.caption(f"Model in use: **{diabetes_bundle['model_name']}** · "
               f"Test accuracy: **{metrics['diabetes'][diabetes_bundle['model_name']]['test_accuracy']*100:.1f}%**")
    st.markdown("Enter the patient's clinical measurements below.")

    with st.form("diabetes_form"):
        c1, c2 = st.columns(2)
        with c1:
            pregnancies = st.number_input("Pregnancies", 0, 20, 1)
            glucose = st.number_input("Glucose (mg/dL)", 0, 300, 120)
            blood_pressure = st.number_input("Blood Pressure (mm Hg)", 0, 200, 70)
            skin_thickness = st.number_input("Skin Thickness (mm)", 0, 100, 20)
        with c2:
            insulin = st.number_input("Insulin (mu U/mL)", 0, 900, 80)
            bmi = st.number_input("BMI", 0.0, 70.0, 25.0, step=0.1)
            dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.4, step=0.01)
            age = st.number_input("Age (years)", 1, 120, 33)

        submitted = st.form_submit_button("🔍 Predict", use_container_width=True)

    if submitted:
        inputs = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                             insulin, bmi, dpf, age]])
        scaled = diabetes_bundle["scaler"].transform(inputs)
        model = diabetes_bundle["model"]
        pred = model.predict(scaled)[0]
        proba = model.predict_proba(scaled)[0][1] if hasattr(model, "predict_proba") else None

        st.markdown("### Result")
        if pred == 1:
            st.markdown(f'<div class="result-positive">⚠️ <b>The model predicts a HIGH likelihood of diabetes.</b>'
                         f'{f" (confidence: {proba*100:.1f}%)" if proba is not None else ""}<br>'
                         f'Please consult a healthcare professional for proper diagnosis and testing.</div>',
                         unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-negative">✅ <b>The model predicts a LOW likelihood of diabetes.</b>'
                         f'{f" (confidence: {(1-proba)*100:.1f}%)" if proba is not None else ""}<br>'
                         f'This is not a medical diagnosis — maintain regular checkups.</div>',
                         unsafe_allow_html=True)

        if proba is not None:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=proba * 100,
                title={"text": "Diabetes Risk Score (%)"},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#2563EB"},
                       "steps": [
                           {"range": [0, 40], "color": "#DCFCE7"},
                           {"range": [40, 70], "color": "#FEF9C3"},
                           {"range": [70, 100], "color": "#FEE2E2"}]}
            ))
            fig.update_layout(height=300, margin=dict(t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

# ========================================================================
# HEART DISEASE PREDICTION
# ========================================================================
elif page == "❤️ Heart Disease Prediction":
    st.title("❤️ Heart Disease Prediction")
    st.caption(f"Model in use: **{heart_bundle['model_name']}** · "
               f"Test accuracy: **{metrics['heart'][heart_bundle['model_name']]['test_accuracy']*100:.1f}%**")
    st.markdown("Enter the patient's clinical measurements below.")

    with st.form("heart_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age (years)", 1, 120, 50)
            sex = st.selectbox("Sex", ["Male", "Female"])
            cp = st.selectbox("Chest Pain Type", [
                "0 - Typical Angina", "1 - Atypical Angina",
                "2 - Non-anginal Pain", "3 - Asymptomatic"])
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 80, 220, 120)
            chol = st.number_input("Serum Cholesterol (mg/dL)", 100, 600, 200)
        with c2:
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL?", ["No", "Yes"])
            restecg = st.selectbox("Resting ECG Result", [
                "0 - Normal", "1 - ST-T Wave Abnormality", "2 - Left Ventricular Hypertrophy"])
            thalach = st.number_input("Max Heart Rate Achieved", 60, 220, 150)
            exang = st.selectbox("Exercise-Induced Angina?", ["No", "Yes"])
            oldpeak = st.number_input("ST Depression (oldpeak)", 0.0, 10.0, 1.0, step=0.1)
        with c3:
            slope = st.selectbox("Slope of Peak Exercise ST Segment", [
                "0 - Upsloping", "1 - Flat", "2 - Downsloping"])
            ca = st.selectbox("Number of Major Vessels Colored (ca)", [0, 1, 2, 3])
            thal = st.selectbox("Thalassemia", [
                "1 - Normal", "2 - Fixed Defect", "3 - Reversible Defect"])

        submitted = st.form_submit_button("🔍 Predict", use_container_width=True)

    if submitted:
        inputs = np.array([[
            age,
            1 if sex == "Male" else 0,
            int(cp[0]),
            trestbps,
            chol,
            1 if fbs == "Yes" else 0,
            int(restecg[0]),
            thalach,
            1 if exang == "Yes" else 0,
            oldpeak,
            int(slope[0]),
            ca,
            int(thal[0]),
        ]])
        scaled = heart_bundle["scaler"].transform(inputs)
        model = heart_bundle["model"]
        pred = model.predict(scaled)[0]
        proba = model.predict_proba(scaled)[0][1] if hasattr(model, "predict_proba") else None

        st.markdown("### Result")
        if pred == 1:
            st.markdown(f'<div class="result-positive">⚠️ <b>The model predicts a HIGH likelihood of heart disease.</b>'
                         f'{f" (confidence: {proba*100:.1f}%)" if proba is not None else ""}<br>'
                         f'Please consult a cardiologist for proper diagnosis.</div>',
                         unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-negative">✅ <b>The model predicts a LOW likelihood of heart disease.</b>'
                         f'{f" (confidence: {(1-proba)*100:.1f}%)" if proba is not None else ""}<br>'
                         f'This is not a medical diagnosis — maintain regular checkups.</div>',
                         unsafe_allow_html=True)

        if proba is not None:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=proba * 100,
                title={"text": "Heart Disease Risk Score (%)"},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#DC2626"},
                       "steps": [
                           {"range": [0, 40], "color": "#DCFCE7"},
                           {"range": [40, 70], "color": "#FEF9C3"},
                           {"range": [70, 100], "color": "#FEE2E2"}]}
            ))
            fig.update_layout(height=300, margin=dict(t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

# ========================================================================
# PARKINSON'S PREDICTION
# ========================================================================
elif page == "🧠 Parkinson's Prediction":
    st.title("🧠 Parkinson's Disease Prediction")
    st.caption(f"Model in use: **{parkinsons_bundle['model_name']}** · "
               f"Test accuracy: **{metrics['parkinsons'][parkinsons_bundle['model_name']]['test_accuracy']*100:.1f}%**")
    st.markdown(
        "Enter the patient's **biomedical voice measurements** below "
        "(from a sustained-vowel voice recording analysis)."
    )
    st.info("💡 Tip: click **'Load Sample Values'** to auto-fill a realistic example, "
            "then tweak values to see how the prediction changes.")

    feature_names = parkinsons_bundle["features"]

    sample_row = parkinsons_df.iloc[0][feature_names].to_dict()
    if "sample_loaded" not in st.session_state:
        st.session_state.sample_loaded = False

    if st.button("📋 Load Sample Values"):
        st.session_state.sample_loaded = True

    with st.form("parkinsons_form"):
        cols = st.columns(3)
        values = {}
        for i, feat in enumerate(feature_names):
            default = float(sample_row[feat]) if st.session_state.sample_loaded else 0.0
            with cols[i % 3]:
                values[feat] = st.number_input(feat, value=default, format="%.5f", key=f"pk_{feat}")

        submitted = st.form_submit_button("🔍 Predict", use_container_width=True)

    if submitted:
        inputs = np.array([[values[f] for f in feature_names]])
        scaled = parkinsons_bundle["scaler"].transform(inputs)
        model = parkinsons_bundle["model"]
        pred = model.predict(scaled)[0]
        proba = model.predict_proba(scaled)[0][1] if hasattr(model, "predict_proba") else None

        st.markdown("### Result")
        if pred == 1:
            st.markdown(f'<div class="result-positive">⚠️ <b>The model predicts signs consistent with Parkinson\'s disease.</b>'
                         f'{f" (confidence: {proba*100:.1f}%)" if proba is not None else ""}<br>'
                         f'Please consult a neurologist for proper diagnosis.</div>',
                         unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-negative">✅ <b>The model predicts a LOW likelihood of Parkinson\'s disease.</b>'
                         f'{f" (confidence: {(1-proba)*100:.1f}%)" if proba is not None else ""}<br>'
                         f'This is not a medical diagnosis.</div>',
                         unsafe_allow_html=True)

        if proba is not None:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=proba * 100,
                title={"text": "Parkinson's Risk Score (%)"},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#7C3AED"},
                       "steps": [
                           {"range": [0, 40], "color": "#DCFCE7"},
                           {"range": [40, 70], "color": "#FEF9C3"},
                           {"range": [70, 100], "color": "#FEE2E2"}]}
            ))
            fig.update_layout(height=300, margin=dict(t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

# ========================================================================
# DATA ANALYSIS DASHBOARD
# ========================================================================
elif page == "📊 Data Analysis Dashboard":
    st.title("📊 Data Analysis Dashboard")
    st.markdown("Exploratory analysis of the three underlying clinical datasets.")

    dataset_choice = st.selectbox(
        "Select a dataset to explore",
        ["Diabetes (Pima Indians)", "Heart Disease (UCI Cleveland)", "Parkinson's (UCI Oxford)"]
    )

    if dataset_choice.startswith("Diabetes"):
        df, target_col, target_labels = diabetes_df, "Outcome", {0: "No Diabetes", 1: "Diabetes"}
    elif dataset_choice.startswith("Heart"):
        df, target_col, target_labels = heart_df, "target", {0: "No Disease", 1: "Disease"}
    else:
        df, target_col, target_labels = parkinsons_df.drop(columns=["name"]), "status", {0: "Healthy", 1: "Parkinson's"}

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Records", len(df))
    k2.metric("Features", len(df.columns) - 1)
    k3.metric("Positive Cases", int((df[target_col] == 1).sum()))
    k4.metric("Negative Cases", int((df[target_col] == 0).sum()))

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Class Distribution", "Feature Distributions", "Correlation Heatmap", "Raw Data"]
    )

    with tab1:
        counts = df[target_col].map(target_labels).value_counts().reset_index()
        counts.columns = ["Class", "Count"]
        fig = px.pie(counts, names="Class", values="Count", hole=0.45,
                     color_discrete_sequence=["#16A34A", "#DC2626"])
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        numeric_cols = [c for c in df.columns if c != target_col]
        feat = st.selectbox("Choose a feature", numeric_cols)
        fig = px.histogram(
            df, x=feat, color=df[target_col].map(target_labels),
            barmode="overlay", nbins=30, opacity=0.7,
            color_discrete_sequence=["#16A34A", "#DC2626"],
            labels={"color": "Class"}
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.box(df, x=df[target_col].map(target_labels), y=feat,
                       color=df[target_col].map(target_labels),
                       color_discrete_sequence=["#16A34A", "#DC2626"],
                       labels={"x": "Class"})
        fig2.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        corr = df.corr(numeric_only=True)
        fig = px.imshow(corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                         aspect="auto")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**Features most correlated with `{target_col}`:**")
        target_corr = corr[target_col].drop(target_col).sort_values(key=abs, ascending=False).head(8)
        fig2 = px.bar(target_corr, orientation="h",
                       color=target_corr.values, color_continuous_scale="RdBu_r")
        fig2.update_layout(height=350, showlegend=False, coloraxis_showscale=False,
                            xaxis_title="Correlation", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    with tab4:
        st.dataframe(df, use_container_width=True, height=400)
        st.download_button(
            "⬇️ Download this dataset as CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name=f"{dataset_choice.split(' ')[0].lower()}_dataset.csv",
            mime="text/csv",
        )

# ========================================================================
# MODEL PERFORMANCE
# ========================================================================
elif page == "📈 Model Performance":
    st.title("📈 Model Performance Comparison")
    st.markdown(
        "Each disease's model was chosen by comparing five algorithms "
        "(Logistic Regression, Random Forest, SVM, KNN, Decision Tree) "
        "using 5-fold cross-validation, then evaluated on a held-out 20% test set."
    )

    disease_choice = st.selectbox(
        "Select a disease", ["Diabetes", "Heart Disease", "Parkinson's"]
    )
    key_map = {"Diabetes": "diabetes", "Heart Disease": "heart", "Parkinson's": "parkinsons"}
    key = key_map[disease_choice]
    disease_metrics = {k: v for k, v in metrics[key].items() if k != "best_model"}

    results_df = pd.DataFrame(disease_metrics).T.reset_index().rename(columns={"index": "Model"})
    st.dataframe(
        results_df.style.highlight_max(
            subset=[c for c in results_df.columns if c != "Model"], color="#DCFCE7"
        ),
        use_container_width=True,
    )

    st.success(f"🏆 **Best model for {disease_choice}:** {metrics[key]['best_model']}")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(results_df, x="Model", y="test_accuracy", color="Model",
                     title="Test Accuracy by Model", text_auto=True)
        fig.update_layout(height=400, showlegend=False, yaxis_range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(results_df, x="Model", y="f1_score", color="Model",
                     title="F1 Score by Model", text_auto=True)
        fig.update_layout(height=400, showlegend=False, yaxis_range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)

    metric_cols = [c for c in results_df.columns if c != "Model"]
    fig = go.Figure()
    for _, row in results_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row[m] for m in metric_cols],
            theta=metric_cols,
            fill="toself",
            name=row["Model"],
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Multi-Metric Comparison (Radar Chart)",
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)
