# 🌐 tphagent Frontend

A simple, user-friendly web interface for generating AI-powered hotel marketing strategies.

## 🎯 Features

- **📧 Email Input**: Users provide their email to receive results
- **🏨 Hotel URL Analysis**: Input hotel website URL for analysis
- **📸 Instagram Integration**: Optional Instagram page analysis
- **⚡ Real-time Progress**: Live progress tracking during analysis
- **📊 Results Display**: Key metrics and strategy overview
- **📥 Download Results**: Export complete analysis as JSON
- **📧 Email Delivery**: Automatic email with detailed strategy

## 🚀 Quick Start

### Option 1: Using the startup script
```bash
# From the tphagent root directory
./start_frontend.sh
```

### Option 2: Manual setup
```bash
# Navigate to frontend directory
cd frontend

# Activate virtual environment
source ../.venv/bin/activate

# Install dependencies
pip install Flask==2.3.3 Werkzeug==2.3.7

# Start the server
python app.py
```

### Option 3: Using the run script
```bash
cd frontend
python run_frontend.py
```

## 🌐 Access the Interface

Once the server is running, open your browser and go to:
**http://localhost:5000**

## 📱 How to Use

1. **Enter Your Email**: Provide your email address to receive results
2. **Add Hotel URL**: Enter your hotel's website URL (optional)
3. **Add Instagram**: Enter your Instagram page URL (optional)
4. **Generate Strategy**: Click "Generate My Marketing Strategy"
5. **Track Progress**: Watch real-time progress updates
6. **View Results**: See your personalized marketing strategy
7. **Download**: Download complete results as JSON file
8. **Check Email**: Receive detailed strategy via email

## 🎨 Interface Features

### Modern Design
- Clean, professional interface
- Gradient background and modern styling
- Responsive design for all devices
- Smooth animations and transitions

### Real-time Updates
- Progress bar shows analysis progress
- Status messages update in real-time
- Background processing doesn't block UI
- Automatic results display when ready

### User Experience
- Form validation with helpful error messages
- Mobile-friendly responsive design
- Intuitive workflow and navigation
- Clear results presentation

## 🔧 Technical Details

### Backend (app.py)
- **Flask Web Server**: Lightweight Python web framework
- **REST API**: Clean API endpoints for frontend communication
- **Background Processing**: Threading for non-blocking analysis
- **Real-time Status**: Live updates during processing
- **Email Integration**: Automatic email delivery
- **File Management**: Download and attachment handling

### Frontend (index.html)
- **Modern CSS**: Gradients, animations, responsive design
- **JavaScript**: Real-time updates and form handling
- **Form Validation**: Client-side validation and error handling
- **Progress Tracking**: Visual progress indicators
- **Results Display**: Clean presentation of analysis results

### API Endpoints
- `POST /analyze` - Start hotel analysis
- `GET /status/<request_id>` - Get processing status
- `GET /download/<request_id>` - Download results as JSON

## 📊 Sample Workflow

### User Input
```
Email: user@example.com
Hotel URL: https://estanciahacienda.lovable.app/
Instagram URL: (optional)
```

### Processing Steps
1. **10%** - Starting analysis...
2. **25%** - Analyzing hotel website...
3. **40%** - Extracting hotel information...
4. **60%** - Creating marketing strategy...
5. **80%** - Generating campaign diagnosis...
6. **95%** - Sending results email...
7. **100%** - Analysis completed!

### Generated Results
```
Hotel: The Peacock House by Hacienda La Estancia
Budget Tier: Standard
Monthly Budget: $720.00
Target Audience: Eco-tourists, Families, Heritage enthusiasts
Google Ads: $432.00 (60%)
Social Media: $180.00 (25%)
Content Creation: $108.00 (15%)
```

## 📧 Email Delivery

Users receive a comprehensive email with:
- Complete marketing strategy overview
- AI agent analysis results
- Budget breakdown and recommendations
- Target audience analysis
- Implementation steps
- Attached detailed reports (JSON format)

## 🛠️ Configuration

### Email Settings
The frontend uses the same email configuration as the main system:
- `EMAIL_USER`: Your email address
- `EMAIL_PASSWORD`: Your app password

### Server Settings
- **Host**: 0.0.0.0 (accessible from all interfaces)
- **Port**: 5000
- **Debug**: True (for development)

## 📁 File Structure

```
frontend/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html         # Main web interface
├── requirements.txt       # Python dependencies
├── run_frontend.py        # Startup script
└── README.md             # This file
```

## 🎯 Use Cases

### For Hotel Owners
- Get personalized marketing strategies
- Understand their target market
- Receive actionable recommendations
- Access professional-level analysis

### For Marketing Agencies
- Onboard new hotel clients quickly
- Generate initial strategies for proposals
- Demonstrate AI capabilities to clients
- Streamline the analysis process

### For Consultants
- Provide quick hotel assessments
- Generate data-driven recommendations
- Create professional presentations
- Scale their service offerings

## 🚀 Deployment

### Local Development
```bash
./start_frontend.sh
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn)
- Setting up proper environment variables
- Configuring HTTPS and security
- Using a reverse proxy (Nginx)
- Setting up monitoring and logging

## 🔍 Troubleshooting

### Common Issues
1. **Port already in use**: Change port in app.py
2. **Module not found**: Ensure virtual environment is activated
3. **Email not sending**: Check email credentials
4. **Analysis fails**: Check hotel URL accessibility

### Debug Mode
The server runs in debug mode by default, which provides:
- Detailed error messages
- Automatic reloading on code changes
- Interactive debugger in browser

## 📞 Support

For issues or questions:
- Check the main tphagent documentation
- Review the API endpoints and responses
- Check server logs for error details
- Ensure all dependencies are installed

## 🎉 Success!

The frontend provides a simple, professional interface for hotel owners to get AI-powered marketing strategies. Users can input their information, track progress in real-time, and receive comprehensive results via email and download.

**Ready to help hotels grow their business with AI!** 🏨🚀