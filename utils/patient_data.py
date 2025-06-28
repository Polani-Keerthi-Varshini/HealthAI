import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class PatientDataManager:
    def __init__(self):
        if not hasattr(self, 'patients'):
            self.patients = {}
            self.health_data = {}
    
    def create_patient(self, patient_data):
        """Create a new patient profile"""
        name = patient_data['name']
        self.patients[name] = {
            'name': name,
            'age': patient_data['age'],
            'gender': patient_data['gender'],
            'medical_history': patient_data.get('medical_history', ''),
            'created_date': datetime.now()
        }
        
        # Generate initial health data
        self.generate_health_data(name)
        
        return self.patients[name]
    
    def get_patient(self, name):
        """Get patient by name"""
        return self.patients.get(name)
    
    def get_patient_names(self):
        """Get list of all patient names"""
        return list(self.patients.keys())
    
    def update_patient(self, name, update_data):
        """Update patient information"""
        if name in self.patients:
            self.patients[name].update(update_data)
            return self.patients[name]
        return None
    
    def generate_health_data(self, patient_name, days=30):
        """Generate realistic health data for a patient over specified days"""
        if patient_name not in self.patients:
            return pd.DataFrame()
        
        patient = self.patients[patient_name]
        
        # Base values based on age and gender
        base_heart_rate = 70 + random.randint(-10, 10)
        base_systolic = 120 + (patient['age'] - 30) * 0.5 + random.randint(-10, 10)
        base_diastolic = 80 + (patient['age'] - 30) * 0.3 + random.randint(-5, 5)
        base_glucose = 90 + random.randint(-10, 15)
        base_weight = 70 + random.randint(-15, 25)
        
        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate data with some trends and variations
        data = []
        for i, date in enumerate(dates):
            # Add some realistic variation and trends
            heart_rate = base_heart_rate + np.sin(i * 0.1) * 5 + random.randint(-5, 5)
            systolic = base_systolic + np.sin(i * 0.05) * 3 + random.randint(-8, 8)
            diastolic = base_diastolic + np.sin(i * 0.05) * 2 + random.randint(-5, 5)
            glucose = base_glucose + np.sin(i * 0.2) * 10 + random.randint(-10, 15)
            weight = base_weight + (i * 0.01) + random.uniform(-0.2, 0.2)  # Slight weight trend
            
            # Ensure values are within realistic ranges
            heart_rate = max(50, min(120, heart_rate))
            systolic = max(90, min(180, systolic))
            diastolic = max(60, min(120, diastolic))
            glucose = max(70, min(200, glucose))
            weight = max(40, min(150, weight))
            
            data.append({
                'date': date,
                'heart_rate': heart_rate,
                'systolic': systolic,
                'diastolic': diastolic,
                'blood_glucose': glucose,
                'weight': weight,
                'patient_name': patient_name
            })
        
        df = pd.DataFrame(data)
        self.health_data[patient_name] = df
        return df
    
    def get_health_data(self, patient_name):
        """Get health data for a specific patient"""
        if patient_name in self.health_data:
            return self.health_data[patient_name]
        else:
            return self.generate_health_data(patient_name)
    
    def add_health_record(self, patient_name, record_data):
        """Add a new health record for a patient"""
        if patient_name not in self.health_data:
            self.health_data[patient_name] = pd.DataFrame()
        
        new_record = pd.DataFrame([record_data])
        self.health_data[patient_name] = pd.concat([self.health_data[patient_name], new_record], ignore_index=True)
        
        return self.health_data[patient_name]
