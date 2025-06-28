import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.patient_data import PatientDataManager
from utils.ai_integration import AIIntegration
from utils.health_analytics import HealthAnalytics
import os

# Page configuration
st.set_page_config(
    page_title="HealthAI - Intelligent Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'patient_data_manager' not in st.session_state:
    st.session_state.patient_data_manager = PatientDataManager()
if 'ai_integration' not in st.session_state:
    st.session_state.ai_integration = AIIntegration()
if 'health_analytics' not in st.session_state:
    st.session_state.health_analytics = HealthAnalytics()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = None

def main():
    # Title and header
    st.title("🏥 HealthAI - Intelligent Healthcare Assistant")
    st.markdown("*Powered by IBM Granite AI for personalized healthcare guidance*")
    
    # Sidebar for patient profile and navigation
    with st.sidebar:
        st.header("Patient Profile")
        
        # Patient selection/creation
        patient_names = st.session_state.patient_data_manager.get_patient_names()
        
        if patient_names:
            selected_patient = st.selectbox("Select Patient", patient_names)
            if st.button("Load Patient"):
                st.session_state.current_patient = st.session_state.patient_data_manager.get_patient(selected_patient)
                st.success(f"Loaded profile for {selected_patient}")
        
        # Create new patient
        with st.expander("Create New Patient"):
            with st.form("new_patient_form"):
                name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=1, max_value=120, value=30)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                medical_history = st.text_area("Medical History")
                
                if st.form_submit_button("Create Patient"):
                    if name:
                        patient_data = {
                            'name': name,
                            'age': age,
                            'gender': gender,
                            'medical_history': medical_history
                        }
                        st.session_state.patient_data_manager.create_patient(patient_data)
                        st.session_state.current_patient = patient_data
                        st.success(f"Created profile for {name}")
                        st.rerun()
        
        # Display current patient info
        if st.session_state.current_patient:
            st.subheader("Current Patient")
            st.write(f"**Name:** {st.session_state.current_patient['name']}")
            st.write(f"**Age:** {st.session_state.current_patient['age']}")
            st.write(f"**Gender:** {st.session_state.current_patient['gender']}")
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        selected_feature = st.radio(
            "Select Feature",
            ["Patient Chat", "Disease Prediction", "Treatment Plans", "Health Analytics"]
        )
    
    # Main content area
    if selected_feature == "Patient Chat":
        display_patient_chat()
    elif selected_feature == "Disease Prediction":
        display_disease_prediction()
    elif selected_feature == "Treatment Plans":
        display_treatment_plans()
    elif selected_feature == "Health Analytics":
        display_health_analytics()

def display_patient_chat():
    st.header("💬 Patient Chat")
    st.markdown("Ask any health-related questions and get AI-powered assistance.")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])
    
    # Chat input
    if prompt := st.chat_input("Ask a health question..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        st.chat_message("user").write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Getting AI response..."):
                patient_context = ""
                if st.session_state.current_patient:
                    patient_context = f"Patient: {st.session_state.current_patient['name']}, Age: {st.session_state.current_patient['age']}, Gender: {st.session_state.current_patient['gender']}, Medical History: {st.session_state.current_patient.get('medical_history', 'None')}"
                
                response = st.session_state.ai_integration.answer_patient_query(prompt, patient_context)
                st.write(response)
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def display_disease_prediction():
    st.header("🔍 Disease Prediction")
    st.markdown("Enter your symptoms to get potential condition predictions.")
    
    if not st.session_state.current_patient:
        st.warning("Please select or create a patient profile first.")
        return
    
    with st.form("symptom_form"):
        st.subheader("Symptom Input")
        
        # Primary symptoms
        primary_symptoms = st.text_area(
            "Primary Symptoms",
            placeholder="e.g., persistent headache, fatigue, mild fever"
        )
        
        # Duration
        duration = st.selectbox(
            "Duration of Symptoms",
            ["Less than 24 hours", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"]
        )
        
        # Severity
        severity = st.selectbox(
            "Severity Level",
            ["Mild", "Moderate", "Severe"]
        )
        
        # Additional symptoms
        additional_symptoms = st.multiselect(
            "Additional Symptoms (if any)",
            ["Nausea", "Vomiting", "Dizziness", "Chest pain", "Shortness of breath", 
             "Abdominal pain", "Joint pain", "Skin rash", "Loss of appetite", "Sleep disturbances"]
        )
        
        submit_prediction = st.form_submit_button("Analyze Symptoms")
    
    if submit_prediction and primary_symptoms:
        with st.spinner("Analyzing symptoms..."):
            patient_info = f"Patient: {st.session_state.current_patient['name']}, Age: {st.session_state.current_patient['age']}, Gender: {st.session_state.current_patient['gender']}, Medical History: {st.session_state.current_patient.get('medical_history', 'None')}"
            
            symptom_data = {
                'primary_symptoms': primary_symptoms,
                'duration': duration,
                'severity': severity,
                'additional_symptoms': additional_symptoms
            }
            
            prediction = st.session_state.ai_integration.predict_disease(symptom_data, patient_info)
            
            st.subheader("Analysis Results")
            st.write(prediction)
            
            # Disclaimer
            st.warning("⚠️ **Medical Disclaimer**: This analysis is for informational purposes only and should not replace professional medical advice. Please consult with a healthcare provider for proper diagnosis and treatment.")

def display_treatment_plans():
    st.header("📋 Treatment Plans")
    st.markdown("Generate personalized treatment recommendations.")
    
    if not st.session_state.current_patient:
        st.warning("Please select or create a patient profile first.")
        return
    
    with st.form("treatment_form"):
        st.subheader("Condition Information")
        
        condition = st.text_input(
            "Diagnosed Condition or Symptoms",
            placeholder="e.g., Hypertension, Type 2 Diabetes, Common Cold"
        )
        
        condition_severity = st.selectbox(
            "Condition Severity",
            ["Mild", "Moderate", "Severe"]
        )
        
        current_medications = st.text_area(
            "Current Medications (if any)",
            placeholder="List any current medications and dosages"
        )
        
        allergies = st.text_area(
            "Known Allergies",
            placeholder="List any known drug allergies or food allergies"
        )
        
        lifestyle_preferences = st.multiselect(
            "Lifestyle Preferences",
            ["Vegetarian diet", "Regular exercise", "No alcohol", "No smoking", "Stress management"]
        )
        
        submit_treatment = st.form_submit_button("Generate Treatment Plan")
    
    if submit_treatment and condition:
        with st.spinner("Generating personalized treatment plan..."):
            patient_info = f"Patient: {st.session_state.current_patient['name']}, Age: {st.session_state.current_patient['age']}, Gender: {st.session_state.current_patient['gender']}, Medical History: {st.session_state.current_patient.get('medical_history', 'None')}"
            
            treatment_data = {
                'condition': condition,
                'severity': condition_severity,
                'current_medications': current_medications,
                'allergies': allergies,
                'lifestyle_preferences': lifestyle_preferences
            }
            
            treatment_plan = st.session_state.ai_integration.generate_treatment_plan(treatment_data, patient_info)
            
            st.subheader("Personalized Treatment Plan")
            st.write(treatment_plan)
            
            # Disclaimer
            st.warning("⚠️ **Medical Disclaimer**: This treatment plan is for informational purposes only. Always consult with a healthcare provider before starting any treatment or medication.")

def display_health_analytics():
    st.header("📊 Health Analytics")
    st.markdown("Visualize and analyze health metrics over time.")
    
    if not st.session_state.current_patient:
        st.warning("Please select or create a patient profile first.")
        return
    
    # Generate sample health data for the current patient
    health_data = st.session_state.patient_data_manager.generate_health_data(st.session_state.current_patient['name'])
    
    if health_data.empty:
        st.info("No health data available. Health metrics will be displayed here once data is recorded.")
        return
    
    # Health metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    latest_data = health_data.iloc[-1]
    
    with col1:
        st.metric(
            "Heart Rate",
            f"{latest_data['heart_rate']:.0f} bpm",
            delta=f"{latest_data['heart_rate'] - health_data['heart_rate'].mean():.0f}"
        )
    
    with col2:
        st.metric(
            "Blood Pressure",
            f"{latest_data['systolic']:.0f}/{latest_data['diastolic']:.0f}",
            delta=f"{latest_data['systolic'] - health_data['systolic'].mean():.0f}"
        )
    
    with col3:
        st.metric(
            "Blood Glucose",
            f"{latest_data['blood_glucose']:.0f} mg/dL",
            delta=f"{latest_data['blood_glucose'] - health_data['blood_glucose'].mean():.0f}"
        )
    
    with col4:
        st.metric(
            "Weight",
            f"{latest_data['weight']:.1f} kg",
            delta=f"{latest_data['weight'] - health_data['weight'].mean():.1f}"
        )
    
    # Charts
    st.subheader("Health Trends")
    
    # Heart rate chart
    fig_hr = px.line(health_data, x='date', y='heart_rate', title='Heart Rate Over Time')
    fig_hr.update_traces(line_color='red')
    st.plotly_chart(fig_hr, use_container_width=True)
    
    # Blood pressure chart
    fig_bp = go.Figure()
    fig_bp.add_trace(go.Scatter(x=health_data['date'], y=health_data['systolic'], 
                               mode='lines', name='Systolic', line=dict(color='blue')))
    fig_bp.add_trace(go.Scatter(x=health_data['date'], y=health_data['diastolic'], 
                               mode='lines', name='Diastolic', line=dict(color='orange')))
    fig_bp.update_layout(title='Blood Pressure Over Time', xaxis_title='Date', yaxis_title='mmHg')
    st.plotly_chart(fig_bp, use_container_width=True)
    
    # Blood glucose chart
    fig_bg = px.line(health_data, x='date', y='blood_glucose', title='Blood Glucose Over Time')
    fig_bg.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Normal Range")
    fig_bg.update_traces(line_color='purple')
    st.plotly_chart(fig_bg, use_container_width=True)
    
    # AI-generated insights
    st.subheader("AI Health Insights")
    with st.spinner("Generating health insights..."):
        insights = st.session_state.health_analytics.generate_insights(health_data, st.session_state.current_patient)
        st.write(insights)

if __name__ == "__main__":
    main()
