import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web serving
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import time
from datetime import datetime, timedelta
import threading
import json
from flask import Flask, render_template, jsonify
import io
import base64

app = Flask(__name__)

class HealthMonitor:
    def __init__(self):
        self.heart_rate_data = []
        self.spo2_data = []
        self.timestamps = []
        self.max_data_points = 100  # Keep last 100 data points
        self.running = False
        self.paused = False
        
    def generate_heart_rate(self):
        """Generate realistic heart rate data (70-90 bpm)"""
        # Add some variation to make it more realistic
        base_rate = 80
        variation = random.uniform(-10, 10)
        noise = random.uniform(-2, 2)
        return max(70, min(90, base_rate + variation + noise))
    
    def generate_spo2(self):
        """Generate realistic SpO2 data (95-100%)"""
        # SpO2 is usually more stable than heart rate
        base_spo2 = 98
        variation = random.uniform(-3, 2)
        noise = random.uniform(-0.5, 0.5)
        return max(95, min(100, base_spo2 + variation + noise))
    
    def collect_data(self):
        """Collect new data point"""
        current_time = datetime.now()
        hr = self.generate_heart_rate()
        spo2 = self.generate_spo2()
        
        self.timestamps.append(current_time)
        self.heart_rate_data.append(hr)
        self.spo2_data.append(spo2)
        
        # Keep only the last max_data_points
        if len(self.timestamps) > self.max_data_points:
            self.timestamps.pop(0)
            self.heart_rate_data.pop(0)
            self.spo2_data.pop(0)
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        self.running = True
        while self.running:
            if not self.paused:
                self.collect_data()
            time.sleep(0.5)  # Update every 0.5 seconds
    
    def stop_monitoring(self):
        """Stop the monitoring loop"""
        self.running = False
    
    def pause_monitoring(self):
        """Pause data collection"""
        self.paused = True
    
    def resume_monitoring(self):
        """Resume data collection"""
        self.paused = False
    
    def get_monitoring_status(self):
        """Get current monitoring status"""
        return {
            'running': self.running,
            'paused': self.paused
        }
    
    def get_current_data(self):
        """Get current data for API"""
        if not self.timestamps:
            return {
                'heart_rate': [],
                'spo2': [],
                'timestamps': [],
                'current_hr': 0,
                'current_spo2': 0
            }
        
        # Convert timestamps to strings for JSON serialization
        timestamp_strings = [ts.strftime('%H:%M:%S') for ts in self.timestamps]
        
        return {
            'heart_rate': self.heart_rate_data,
            'spo2': self.spo2_data,
            'timestamps': timestamp_strings,
            'current_hr': self.heart_rate_data[-1] if self.heart_rate_data else 0,
            'current_spo2': self.spo2_data[-1] if self.spo2_data else 0
        }
    
    def generate_chart(self):
        """Generate matplotlib chart and return as base64 string"""
        if not self.timestamps:
            return None
        
        try:
            # Create figure with medical-grade styling
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
            fig.patch.set_facecolor('#f8f9fa')
            
            # Heart Rate Chart
            ax1.plot(self.timestamps, self.heart_rate_data, 
                    color='#dc3545', linewidth=2, marker='o', markersize=2)
            ax1.set_title('Heart Rate Monitor', fontsize=12, fontweight='bold', color='#2c3e50')
            ax1.set_ylabel('Heart Rate (bpm)', fontsize=10, color='#2c3e50')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(65, 95)
            ax1.set_facecolor('#ffffff')
            
            # Format x-axis for time
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            ax1.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, fontsize=8)
            
            # SpO2 Chart
            ax2.plot(self.timestamps, self.spo2_data, 
                    color='#007bff', linewidth=2, marker='s', markersize=2)
            ax2.set_title('SpO₂ Monitor', fontsize=12, fontweight='bold', color='#2c3e50')
            ax2.set_ylabel('SpO₂ (%)', fontsize=10, color='#2c3e50')
            ax2.set_xlabel('Time', fontsize=10, color='#2c3e50')
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(94, 101)
            ax2.set_facecolor('#ffffff')
            
            # Format x-axis for time
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, fontsize=8)
            
            # Adjust layout
            plt.tight_layout()
            
            # Convert plot to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=80, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return img_str
        except Exception as e:
            print(f"Error generating chart: {e}")
            plt.close()
            return None

# Initialize health monitor
health_monitor = HealthMonitor()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get current health data"""
    return jsonify(health_monitor.get_current_data())

@app.route('/api/chart')
def get_chart():
    """API endpoint to get chart as base64 image"""
    chart_data = health_monitor.generate_chart()
    if chart_data:
        return jsonify({'chart': chart_data})
    else:
        return jsonify({'chart': None})

@app.route('/api/pause', methods=['POST'])
def pause_monitoring():
    """API endpoint to pause monitoring"""
    health_monitor.pause_monitoring()
    return jsonify({'success': True, 'status': 'paused'})

@app.route('/api/resume', methods=['POST'])
def resume_monitoring():
    """API endpoint to resume monitoring"""
    health_monitor.resume_monitoring()
    return jsonify({'success': True, 'status': 'resumed'})

@app.route('/api/status')
def get_status():
    """API endpoint to get monitoring status"""
    return jsonify(health_monitor.get_monitoring_status())

def start_monitoring_thread():
    """Start monitoring in a separate thread"""
    monitoring_thread = threading.Thread(target=health_monitor.start_monitoring)
    monitoring_thread.daemon = True
    monitoring_thread.start()

if __name__ == '__main__':
    # Start monitoring in background
    start_monitoring_thread()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
