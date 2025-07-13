
# Health Monitoring Dashboard

A real-time health monitoring dashboard that simulates and visualizes vital signs data including heart rate and SpO₂ (blood oxygen saturation) levels. Built with Python Flask backend and responsive web interface.

## 🚀 Features

- **Real-time Data Visualization**: Live updating charts for heart rate and SpO₂ levels
- **Interactive Controls**: Pause/resume data collection with visual status indicators
- **Responsive Design**: Mobile-friendly interface with Bootstrap styling
- **Medical-grade UI**: Professional healthcare-themed design
- **REST API**: Clean API endpoints for data access and control

## 🛠️ Technologies Used

- **Backend**: Python, Flask, Matplotlib, NumPy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.1.3
- **Data Visualization**: Matplotlib with real-time chart generation
- **Icons**: Font Awesome 6.0.0

## 📋 Prerequisites

- Python 3.7 or higher
- pip package manager

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/health-monitoring-dashboard.git
cd health-monitoring-dashboard
```

2. Install required packages:
```bash
pip install flask matplotlib numpy
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 📊 API Endpoints

- `GET /` - Main dashboard interface
- `GET /api/data` - Current health data (JSON)
- `GET /api/chart` - Chart as base64 image
- `POST /api/pause` - Pause data collection
- `POST /api/resume` - Resume data collection
- `GET /api/status` - Get monitoring status

## 🎯 Usage

1. **Real-time Monitoring**: The dashboard automatically starts collecting and displaying simulated health data
2. **Pause/Resume**: Use the control buttons to pause or resume data collection
3. **Status Indicators**: Visual feedback shows current monitoring state (Live/Paused)
4. **Responsive Charts**: Charts automatically update every 500ms with new data points

## 📱 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Pause/Play Controls
![Controls](screenshots/controls.png)

## 🏗️ Project Structure

```
health-monitoring-dashboard/
├── main.py                 # Flask application and health monitoring logic
├── templates/
│   └── dashboard.html      # Main dashboard template
├── static/
│   └── style.css          # Custom CSS styling
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## 🔍 Key Components

### HealthMonitor Class
- Generates realistic heart rate data (70-90 bpm)
- Generates realistic SpO₂ data (95-100%)
- Maintains rolling window of last 100 data points
- Thread-safe data collection with pause/resume functionality

### Web Interface
- Real-time cards displaying current vital signs
- Interactive pause/play controls
- Status indicators with visual feedback
- Professional medical-grade styling

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
For production deployment, consider using:
- **Gunicorn** for WSGI server
- **Nginx** for reverse proxy
- **Docker** for containerization

## 🔮 Future Enhancements

- [ ] Database integration for data persistence
- [ ] WebSocket connections for real-time updates
- [ ] User authentication and multiple patient support
- [ ] Integration with actual health monitoring devices
- [ ] Data export and historical analysis features
- [ ] Alert system for abnormal readings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Your Name - [sneha gosain]

Project Link: [https://github.com/namibellemere/health-monitoring-dashboard](https://github.com/namibellemere/health-monitoring-dashboard)

## 🙏 Acknowledgments

- Bootstrap for the responsive CSS framework
- Font Awesome for the icon library
- Matplotlib for data visualization capabilities
- Flask for the lightweight web framework
