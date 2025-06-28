import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class HealthAnalytics:
    def __init__(self):
        pass
    
    def calculate_health_trends(self, health_data):
        """Calculate trends in health metrics"""
        if health_data.empty:
            return {}
        
        trends = {}
        
        # Calculate trends for each metric
        for metric in ['heart_rate', 'systolic', 'diastolic', 'blood_glucose', 'weight']:
            if metric in health_data.columns:
                values = health_data[metric].values
                if len(values) > 1:
                    # Simple linear trend calculation
                    x = np.arange(len(values))
                    coeffs = np.polyfit(x, values, 1)
                    trends[metric] = {
                        'slope': coeffs[0],
                        'current': values[-1],
                        'average': np.mean(values),
                        'min': np.min(values),
                        'max': np.max(values),
                        'std': np.std(values)
                    }
        
        return trends
    
    def assess_health_risks(self, health_data, patient_info):
        """Assess health risks based on current metrics and trends"""
        if health_data.empty:
            return []
        
        risks = []
        latest_data = health_data.iloc[-1]
        
        # Blood pressure assessment
        systolic = latest_data.get('systolic', 0)
        diastolic = latest_data.get('diastolic', 0)
        
        if systolic >= 140 or diastolic >= 90:
            risks.append({
                'risk': 'Hypertension',
                'level': 'High',
                'description': 'Blood pressure readings consistently above normal range'
            })
        elif systolic >= 130 or diastolic >= 80:
            risks.append({
                'risk': 'Pre-hypertension',
                'level': 'Moderate',
                'description': 'Blood pressure elevated but not yet in hypertensive range'
            })
        
        # Blood glucose assessment
        glucose = latest_data.get('blood_glucose', 0)
        if glucose >= 126:
            risks.append({
                'risk': 'Diabetes Risk',
                'level': 'High',
                'description': 'Fasting glucose levels indicate potential diabetes'
            })
        elif glucose >= 100:
            risks.append({
                'risk': 'Pre-diabetes',
                'level': 'Moderate',
                'description': 'Glucose levels elevated above normal range'
            })
        
        # Heart rate assessment
        heart_rate = latest_data.get('heart_rate', 0)
        if heart_rate > 100:
            risks.append({
                'risk': 'Tachycardia',
                'level': 'Moderate',
                'description': 'Resting heart rate consistently elevated'
            })
        elif heart_rate < 60:
            risks.append({
                'risk': 'Bradycardia',
                'level': 'Low',
                'description': 'Resting heart rate below normal range'
            })
        
        return risks
    
    def generate_health_recommendations(self, health_data, patient_info):
        """Generate personalized health recommendations"""
        if health_data.empty:
            return []
        
        recommendations = []
        trends = self.calculate_health_trends(health_data)
        risks = self.assess_health_risks(health_data, patient_info)
        
        # General recommendations
        recommendations.append({
            'category': 'General Health',
            'recommendation': 'Continue regular health monitoring and maintain consistent measurement times',
            'priority': 'Medium'
        })
        
        # Based on blood pressure trends
        if 'systolic' in trends:
            if trends['systolic']['current'] > 130:
                recommendations.append({
                    'category': 'Blood Pressure',
                    'recommendation': 'Consider reducing sodium intake, increasing physical activity, and managing stress levels',
                    'priority': 'High'
                })
        
        # Based on glucose trends
        if 'blood_glucose' in trends:
            if trends['blood_glucose']['current'] > 100:
                recommendations.append({
                    'category': 'Blood Sugar',
                    'recommendation': 'Focus on balanced nutrition, regular meal timing, and consider consulting with a nutritionist',
                    'priority': 'High'
                })
        
        # Based on heart rate trends
        if 'heart_rate' in trends:
            if trends['heart_rate']['slope'] > 0.5:  # Increasing trend
                recommendations.append({
                    'category': 'Cardiovascular',
                    'recommendation': 'Monitor stress levels and consider regular cardiovascular exercise',
                    'priority': 'Medium'
                })
        
        # Weight management
        if 'weight' in trends:
            if trends['weight']['slope'] > 0.1:  # Weight increasing
                recommendations.append({
                    'category': 'Weight Management',
                    'recommendation': 'Consider reviewing dietary habits and increasing physical activity',
                    'priority': 'Medium'
                })
        
        return recommendations
    
    def generate_insights(self, health_data, patient_info):
        """Generate comprehensive AI health insights"""
        if health_data.empty:
            return "No health data available for analysis. Please record some health metrics to receive personalized insights."
        
        trends = self.calculate_health_trends(health_data)
        risks = self.assess_health_risks(health_data, patient_info)
        recommendations = self.generate_health_recommendations(health_data, patient_info)
        
        # Generate comprehensive insights
        insights = f"""**Health Analytics Summary for {patient_info.get('name', 'Patient')}**

**Current Health Status:**
"""
        
        # Add current metrics summary
        latest_data = health_data.iloc[-1]
        insights += f"""
- **Heart Rate:** {latest_data.get('heart_rate', 'N/A'):.0f} bpm
- **Blood Pressure:** {latest_data.get('systolic', 'N/A'):.0f}/{latest_data.get('diastolic', 'N/A'):.0f} mmHg
- **Blood Glucose:** {latest_data.get('blood_glucose', 'N/A'):.0f} mg/dL
- **Weight:** {latest_data.get('weight', 'N/A'):.1f} kg
"""
        
        # Add trend analysis
        insights += "\n**Trend Analysis (Past 30 Days):**\n"
        
        for metric, trend_data in trends.items():
            trend_direction = "↗️" if trend_data['slope'] > 0.1 else "↘️" if trend_data['slope'] < -0.1 else "➡️"
            metric_name = metric.replace('_', ' ').title()
            insights += f"- **{metric_name}:** {trend_direction} "
            
            if abs(trend_data['slope']) > 0.1:
                insights += f"{'Increasing' if trend_data['slope'] > 0 else 'Decreasing'} trend detected\n"
            else:
                insights += "Stable trend\n"
        
        # Add risk assessment
        if risks:
            insights += "\n**Health Risk Assessment:**\n"
            for risk in risks:
                risk_emoji = "🔴" if risk['level'] == 'High' else "🟡" if risk['level'] == 'Moderate' else "🟢"
                insights += f"- {risk_emoji} **{risk['risk']}** ({risk['level']} Risk): {risk['description']}\n"
        else:
            insights += "\n**Health Risk Assessment:**\n✅ No significant health risks detected based on current metrics.\n"
        
        # Add recommendations
        if recommendations:
            insights += "\n**Personalized Recommendations:**\n"
            high_priority = [r for r in recommendations if r['priority'] == 'High']
            medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
            
            if high_priority:
                insights += "\n**High Priority:**\n"
                for rec in high_priority:
                    insights += f"- 🔴 **{rec['category']}:** {rec['recommendation']}\n"
            
            if medium_priority:
                insights += "\n**Medium Priority:**\n"
                for rec in medium_priority:
                    insights += f"- 🟡 **{rec['category']}:** {rec['recommendation']}\n"
        
        # Add general guidance
        insights += """
**General Health Guidance:**
- Continue regular monitoring of your health metrics
- Maintain consistent measurement times for accuracy
- Track any symptoms or changes in how you feel
- Share this data with your healthcare provider during visits
- Consider lifestyle factors that may influence your readings

**When to Consult Your Healthcare Provider:**
- Sudden significant changes in any health metrics
- Persistent abnormal readings
- New or worsening symptoms
- Questions about your health trends
- Before making major lifestyle or medication changes

**Important Note:** These insights are based on data analysis and should not replace professional medical advice. Always consult with your healthcare provider for medical decisions and treatment plans.
"""
        
        return insights
