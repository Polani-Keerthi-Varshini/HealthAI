import os
from typing import Dict, Any
import requests
import json

class AIIntegration:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY", "default_api_key")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "default_project_id")
        self.model_id = "ibm/granite-13b-instruct-v2"
        self.base_url = "https://us-south.ml.cloud.ibm.com"
        
        # Initialize connection (mock for now as we don't have real credentials)
        self.is_connected = self._test_connection()
    
    def _test_connection(self):
        """Test connection to IBM Watson ML"""
        try:
            # In a real implementation, this would test the actual connection
            # For now, we'll simulate a successful connection
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def _make_api_call(self, prompt: str, max_tokens: int = 500) -> str:
        """Make API call to IBM Granite model"""
        if not self.is_connected:
            return "Sorry, I'm currently unable to connect to the AI service. Please try again later."
        
        try:
            # In a real implementation, this would make the actual API call
            # For now, we'll return a simulated response based on the prompt
            return self._simulate_ai_response(prompt)
        except Exception as e:
            return f"Error generating AI response: {str(e)}"
    
    def _simulate_ai_response(self, prompt: str) -> str:
        """Simulate AI responses for demonstration purposes"""
        prompt_lower = prompt.lower()
        
        # Patient chat responses
        if "headache" in prompt_lower:
            return """Based on your symptoms, headaches can have various causes including:

**Common Causes:**
- Tension headaches (most common)
- Dehydration
- Stress or lack of sleep
- Eye strain from screens

**Recommendations:**
- Stay hydrated (8-10 glasses of water daily)
- Get adequate rest (7-8 hours of sleep)
- Take regular breaks from screens
- Practice stress management techniques

**When to Seek Medical Care:**
- Sudden, severe headache unlike any before
- Headache with fever, stiff neck, or rash
- Persistent headaches lasting several days
- Changes in vision or speech

Please monitor your symptoms and consult a healthcare provider if they persist or worsen."""
        
        elif "fever" in prompt_lower:
            return """Fever is your body's natural response to infection or illness.

**Immediate Care:**
- Rest and stay hydrated
- Use fever-reducing medication (acetaminophen or ibuprofen) as directed
- Wear light clothing and use cool compresses
- Monitor temperature regularly

**Seek Medical Attention If:**
- Temperature exceeds 103°F (39.4°C)
- Fever persists for more than 3 days
- Accompanied by severe symptoms (difficulty breathing, chest pain, severe headache)
- Signs of dehydration

**Red Flags:**
- Fever with rash
- Severe abdominal pain
- Confusion or difficulty staying awake
- Persistent vomiting

Remember, this is general guidance. Always consult with a healthcare provider for personalized medical advice."""
        
        elif "chest pain" in prompt_lower:
            return """⚠️ **IMPORTANT:** Chest pain can be serious and requires immediate medical evaluation.

**Seek Emergency Care Immediately If You Experience:**
- Severe, crushing chest pain
- Pain radiating to arm, jaw, or back
- Shortness of breath
- Dizziness or fainting
- Nausea with chest pain

**Common Non-Emergency Causes:**
- Muscle strain
- Acid reflux/heartburn
- Anxiety or stress
- Inflammation of chest wall

**What You Can Do While Waiting for Medical Care:**
- Sit upright and try to remain calm
- Loosen tight clothing
- If prescribed, take nitroglycerin as directed

**NEVER ignore chest pain.** When in doubt, call emergency services or go to the nearest emergency room. Early treatment can be life-saving."""
        
        else:
            return f"""Thank you for your question. Based on your symptoms and health query, I recommend:

**General Health Guidance:**
- Monitor your symptoms carefully
- Maintain good hydration and nutrition
- Get adequate rest
- Keep track of any changes in your condition

**When to Consult a Healthcare Provider:**
- Symptoms persist or worsen
- You develop new concerning symptoms
- You have questions about your medications
- You need personalized medical advice

**Important Reminder:**
This AI assistant provides general health information only and cannot replace professional medical diagnosis or treatment. Always consult with qualified healthcare providers for medical concerns.

Is there anything specific about your symptoms you'd like me to help clarify?"""
    
    def answer_patient_query(self, query: str, patient_context: str = "") -> str:
        """Answer patient health questions"""
        prompt = f"""You are a helpful healthcare AI assistant. Provide empathetic, accurate medical information while emphasizing the importance of professional medical care.

Patient Context: {patient_context}

Patient Question: {query}

Please provide:
1. Empathetic acknowledgment of their concern
2. General medical information relevant to their question
3. Clear guidance on when to seek professional medical care
4. Appropriate disclaimers about AI limitations

Remember to be supportive but never provide specific medical diagnoses or treatment recommendations."""
        
        return self._make_api_call(prompt)
    
    def predict_disease(self, symptom_data: Dict[str, Any], patient_info: str) -> str:
        """Predict potential diseases based on symptoms"""
        symptoms_text = f"Primary symptoms: {symptom_data['primary_symptoms']}, Duration: {symptom_data['duration']}, Severity: {symptom_data['severity']}"
        if symptom_data['additional_symptoms']:
            symptoms_text += f", Additional symptoms: {', '.join(symptom_data['additional_symptoms'])}"
        
        prompt = f"""You are a medical AI assistant helping with symptom analysis. Based on the patient information and symptoms provided, give a thoughtful analysis of potential conditions.

Patient Information: {patient_info}
Symptoms: {symptoms_text}

Please provide:
1. 2-3 most likely potential conditions with brief explanations
2. Likelihood assessment (consider patient age, gender, medical history)
3. Recommended next steps (tests, specialist referrals, immediate care needs)
4. Warning signs that require immediate medical attention
5. General care recommendations

Important: Emphasize this is preliminary analysis and professional medical evaluation is essential for accurate diagnosis."""
        
        response = self._make_api_call(prompt, max_tokens=700)
        
        # Add simulated disease prediction logic for demonstration
        if not response or "unable to connect" in response.lower():
            primary_symptoms = symptom_data['primary_symptoms'].lower()
            
            if "headache" in primary_symptoms and "fever" in primary_symptoms:
                return """**Symptom Analysis Results:**

**Most Likely Conditions:**
1. **Viral Upper Respiratory Infection (70% likelihood)**
   - Common with headache, fever combination
   - Often includes fatigue and mild body aches
   - Usually resolves within 7-10 days

2. **Tension Headache with Concurrent Illness (20% likelihood)**
   - Stress-related headache occurring during illness
   - May be exacerbated by dehydration

3. **Bacterial Infection (10% likelihood)**
   - Less common but possible if symptoms persist
   - May require antibiotic treatment

**Recommended Next Steps:**
- Monitor temperature regularly
- Stay well hydrated
- Get adequate rest
- Consider over-the-counter pain relief if appropriate
- Seek medical care if symptoms worsen or persist beyond 5-7 days

**Seek Immediate Medical Care If:**
- Fever exceeds 103°F (39.4°C)
- Severe headache with neck stiffness
- Difficulty breathing or chest pain
- Signs of dehydration
- Symptoms rapidly worsening

**Important Note:** This analysis is for informational purposes only. A healthcare provider should evaluate persistent or concerning symptoms for accurate diagnosis and treatment."""
            
            else:
                return f"""**Symptom Analysis Results:**

Based on your reported symptoms: {symptom_data['primary_symptoms']}

**Preliminary Assessment:**
Your symptoms warrant medical evaluation to determine the underlying cause and appropriate treatment.

**General Recommendations:**
- Document symptom progression and severity
- Note any triggers or patterns
- Monitor for additional symptoms
- Maintain hydration and rest

**Seek Medical Care For:**
- Proper diagnostic evaluation
- Personalized treatment recommendations
- Rule out serious conditions
- Professional symptom assessment

**Red Flags - Seek Immediate Care If:**
- Symptoms suddenly worsen
- Difficulty breathing or chest pain
- High fever or severe pain
- Signs of serious illness

This AI analysis cannot replace professional medical diagnosis. Please consult with a healthcare provider for accurate assessment and treatment."""
        
        return response
    
    def generate_treatment_plan(self, treatment_data: Dict[str, Any], patient_info: str) -> str:
        """Generate personalized treatment plans"""
        condition = treatment_data['condition']
        severity = treatment_data['severity']
        medications = treatment_data.get('current_medications', 'None')
        allergies = treatment_data.get('allergies', 'None')
        preferences = treatment_data.get('lifestyle_preferences', [])
        
        prompt = f"""You are a medical AI assistant creating a comprehensive treatment plan. Based on the patient information and condition details, provide a structured treatment approach.

Patient Information: {patient_info}
Condition: {condition}
Severity: {severity}
Current Medications: {medications}
Known Allergies: {allergies}
Lifestyle Preferences: {', '.join(preferences) if preferences else 'None specified'}

Please provide a structured treatment plan including:
1. Treatment Goals
2. Medication Recommendations (considering allergies and current medications)
3. Lifestyle Modifications
4. Monitoring and Follow-up
5. Warning Signs to Watch For
6. Expected Timeline for Improvement

Important: This is a general treatment framework. All medical decisions should be made in consultation with healthcare providers."""
        
        response = self._make_api_call(prompt, max_tokens=800)
        
        # Add simulated treatment plan for common conditions
        if not response or "unable to connect" in response.lower():
            condition_lower = condition.lower()
            
            if "hypertension" in condition_lower or "high blood pressure" in condition_lower:
                return """**Comprehensive Treatment Plan for Hypertension**

**Treatment Goals:**
- Reduce blood pressure to target range (<130/80 mmHg)
- Prevent cardiovascular complications
- Improve overall quality of life

**Medication Considerations:**
- ACE inhibitors or ARBs as first-line treatment
- Calcium channel blockers or diuretics as alternatives
- Regular monitoring for side effects
- Gradual dosage adjustments as needed

**Lifestyle Modifications:**
1. **Dietary Changes:**
   - DASH diet (rich in fruits, vegetables, whole grains)
   - Reduce sodium intake (<2,300mg daily, ideally <1,500mg)
   - Limit alcohol consumption
   - Maintain healthy weight

2. **Physical Activity:**
   - 150 minutes moderate aerobic exercise weekly
   - Strength training 2 days per week
   - Start slowly and gradually increase intensity

3. **Stress Management:**
   - Regular relaxation techniques
   - Adequate sleep (7-8 hours nightly)
   - Stress reduction activities

**Monitoring and Follow-up:**
- Home blood pressure monitoring
- Regular medical check-ups every 3-6 months
- Laboratory tests to monitor kidney function
- Medication adherence assessment

**Warning Signs - Seek Immediate Care:**
- Severe chest pain
- Shortness of breath
- Severe headache
- Vision changes
- Blood pressure >180/120 mmHg

**Expected Timeline:**
- Initial improvement: 2-4 weeks
- Optimal control: 3-6 months with proper adherence
- Ongoing management: Lifelong commitment

**Important:** This plan must be reviewed and approved by your healthcare provider before implementation."""
                
            elif "diabetes" in condition_lower:
                return """**Comprehensive Treatment Plan for Diabetes Management**

**Treatment Goals:**
- Maintain blood glucose levels in target range
- Prevent diabetes complications
- Preserve quality of life and functionality

**Medication Management:**
- Blood glucose monitoring as prescribed
- Medication timing and dosage adherence
- Regular review of medication effectiveness
- Insulin adjustment protocols if applicable

**Nutritional Management:**
1. **Meal Planning:**
   - Consistent carbohydrate intake
   - Portion control and regular meal times
   - High-fiber, nutrient-dense foods
   - Limited refined sugars and processed foods

2. **Blood Sugar Monitoring:**
   - Regular glucose testing as recommended
   - Record keeping of levels and patterns
   - Understanding of target ranges

**Physical Activity:**
- Regular exercise routine (cleared by physician)
- Both aerobic and resistance training
- Monitor blood sugar before/after exercise
- Adjust food/medication as needed

**Regular Monitoring:**
- HbA1c testing every 3-6 months
- Annual eye and foot examinations
- Kidney function assessment
- Cholesterol and blood pressure monitoring

**Complication Prevention:**
- Daily foot inspection and care
- Dental health maintenance
- Vaccination updates
- Wound care awareness

**Emergency Planning:**
- Hypoglycemia treatment plan
- Sick day management protocols
- Emergency contact information
- Medical alert identification

**Expected Outcomes:**
- Improved glucose control within 3-6 months
- Reduced risk of complications
- Better energy levels and overall health

**Important:** This plan requires healthcare provider supervision and regular adjustments based on individual response."""
            
            else:
                return f"""**Personalized Treatment Plan for {condition}**

**Treatment Approach:**
Based on your condition and health profile, a comprehensive treatment plan should address both immediate symptom management and long-term health optimization.

**Key Treatment Components:**
1. **Medical Management:**
   - Appropriate medication therapy considering your allergies and current medications
   - Regular monitoring and dosage adjustments
   - Side effect management strategies

2. **Lifestyle Interventions:**
   - Nutrition modifications tailored to your condition
   - Appropriate physical activity recommendations
   - Stress management techniques
   - Sleep hygiene improvements

3. **Monitoring Plan:**
   - Regular follow-up appointments
   - Relevant diagnostic tests and screenings
   - Symptom tracking and documentation
   - Progress assessment metrics

4. **Prevention Strategies:**
   - Risk factor modification
   - Complication prevention measures
   - Health maintenance activities
   - Emergency action plans

**Patient Education:**
- Understanding your condition
- Recognizing warning signs
- Proper medication administration
- When to seek medical care

**Follow-up Schedule:**
- Initial follow-up: 2-4 weeks
- Regular monitoring: As determined by healthcare provider
- Emergency protocols: Clear guidelines provided

**Important Disclaimer:** This treatment framework must be reviewed, modified, and approved by your healthcare provider before implementation. Individual medical circumstances require personalized professional medical care."""
        
        return response
