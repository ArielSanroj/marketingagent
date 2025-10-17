"""
tphagent Frontend - Simple Web Interface
Allows users to input email and hotel URL/Instagram for marketing strategy analysis
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import json
from datetime import datetime
import threading
import time
import concurrent.futures
from functools import wraps
import logging

# Add parent directory to path to import our modules
sys.path.append('..')

from utils.hotel_analyzer import HotelAnalyzer
from utils.user_approval import UserApprovalInterface
from onboarding import HotelOnboardingSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for processing status
processing_status = {}
processing_results = {}

# Thread pool for background processing
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

def async_route(f):
    """Decorator to run route functions asynchronously"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return executor.submit(f, *args, **kwargs).result()
    return wrapper

@app.route('/')
def index():
    """Main page with the form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_hotel():
    """Analyze hotel and generate marketing strategy"""
    try:
        data = request.get_json()
        user_email = data.get('email', '').strip()
        hotel_url = data.get('hotel_url', '').strip()
        instagram_url = data.get('instagram_url', '').strip()
        
        # Validate inputs
        if not user_email or '@' not in user_email:
            return jsonify({'error': 'Please provide a valid email address'}), 400
        
        if not hotel_url and not instagram_url:
            return jsonify({'error': 'Please provide either a hotel URL or Instagram page'}), 400
        
        # Generate unique request ID
        request_id = f"req_{int(time.time())}"
        
        # Start processing in background
        thread = threading.Thread(target=process_hotel_analysis, args=(request_id, user_email, hotel_url, instagram_url))
        thread.daemon = True
        thread.start()
        
        # Set initial status
        processing_status[request_id] = {
            'status': 'processing',
            'message': 'Starting analysis...',
            'progress': 10
        }
        
        return jsonify({
            'success': True,
            'request_id': request_id,
            'message': 'Analysis started successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error starting analysis: {str(e)}'}), 500

@app.route('/status/<request_id>')
def get_status(request_id):
    """Get processing status with performance metrics"""
    if request_id not in processing_status:
        return jsonify({'error': 'Request not found'}), 404
    
    status = processing_status[request_id].copy()
    
    # Add performance metrics
    if 'start_time' not in status:
        status['start_time'] = time.time()
    
    status['elapsed_time'] = round(time.time() - status['start_time'], 2)
    
    # If processing is complete, include results
    if status['status'] == 'completed':
        if request_id in processing_results:
            status['results'] = processing_results[request_id]
            status['total_time'] = status['elapsed_time']
    
    return jsonify(status)

@app.route('/performance')
def get_performance_stats():
    """Get performance statistics"""
    active_requests = len([s for s in processing_status.values() if s['status'] == 'processing'])
    completed_requests = len([s for s in processing_status.values() if s['status'] == 'completed'])
    error_requests = len([s for s in processing_status.values() if s['status'] == 'error'])
    
    return jsonify({
        'active_requests': active_requests,
        'completed_requests': completed_requests,
        'error_requests': error_requests,
        'total_requests': len(processing_status),
        'cache_size': len(getattr(HotelAnalyzer(), '_cache', {})),
        'thread_pool_size': executor._max_workers
    })

def process_hotel_analysis(request_id, user_email, hotel_url, instagram_url):
    """Process hotel analysis in background with parallel processing"""
    try:
        logger.info(f"Starting analysis for request {request_id}")
        
        # Update status
        processing_status[request_id].update({
            'message': 'Initializing analysis...',
            'progress': 10
        })
        
        # Initialize components
        analyzer = HotelAnalyzer()
        approval_interface = UserApprovalInterface()
        
        hotel_analysis = None
        instagram_analysis = None
        
        # Use parallel processing for hotel and Instagram analysis
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = {}
            
            # Submit hotel analysis task
            if hotel_url:
                processing_status[request_id].update({
                    'message': f'Starting hotel website analysis...',
                    'progress': 25
                })
                futures['hotel'] = executor.submit(analyzer.analyze_hotel_url, hotel_url)
            
            # Submit Instagram analysis task
            if instagram_url:
                processing_status[request_id].update({
                    'message': f'Starting Instagram analysis...',
                    'progress': 30
                })
                futures['instagram'] = executor.submit(analyzer.analyze_instagram_page, instagram_url)
            
            # Wait for both analyses to complete
            processing_status[request_id].update({
                'message': 'Processing website and social media data...',
                'progress': 50
            })
            
            # Get results as they complete
            for future_name, future in futures.items():
                try:
                    result = future.result(timeout=30)  # 30 second timeout per analysis
                    if future_name == 'hotel':
                        hotel_analysis = result
                        processing_status[request_id].update({
                            'message': 'Hotel analysis completed',
                            'progress': 60
                        })
                    elif future_name == 'instagram':
                        instagram_analysis = result
                        processing_status[request_id].update({
                            'message': 'Instagram analysis completed',
                            'progress': 70
                        })
                except concurrent.futures.TimeoutError:
                    logger.warning(f"Timeout analyzing {future_name}")
                    if future_name == 'hotel':
                        hotel_analysis = {'analysis_status': 'timeout', 'error': 'Analysis timeout'}
                    elif future_name == 'instagram':
                        instagram_analysis = {'analysis_status': 'timeout', 'error': 'Analysis timeout'}
                except Exception as e:
                    logger.error(f"Error in {future_name} analysis: {e}")
                    if future_name == 'hotel':
                        hotel_analysis = {'analysis_status': 'error', 'error': str(e)}
                    elif future_name == 'instagram':
                        instagram_analysis = {'analysis_status': 'error', 'error': str(e)}
        
        # Create marketing strategy
        processing_status[request_id].update({
            'message': 'Creating marketing strategy...',
            'progress': 80
        })
        
        strategy = approval_interface.create_strategy_from_analysis(hotel_analysis, instagram_analysis)
        
        # Approve strategy automatically
        approved_strategy = approval_interface.approve_strategy(
            strategy, 
            f"Marketing strategy generated for {strategy.hotel_name}"
        )
        
        # Create diagnosis for campaign launch
        processing_status[request_id].update({
            'message': 'Generating campaign diagnosis...',
            'progress': 90
        })
        
        onboarding = HotelOnboardingSystem()
        diagnosis = onboarding._create_diagnosis_from_strategy(approved_strategy)
        
        # Store results
        results = {
            'hotel_name': strategy.hotel_name,
            'strategy': {
                'target_audience': strategy.target_audience,
                'budget_tier': strategy.budget_recommendation['tier'],
                'monthly_budget': strategy.budget_recommendation['monthly_budget'],
                'daily_budget': strategy.budget_recommendation['daily_budget'],
                'allocation': strategy.budget_recommendation['allocation']
            },
            'diagnosis': diagnosis,
            'hotel_analysis': hotel_analysis,
            'instagram_analysis': instagram_analysis,
            'email': user_email,
            'timestamp': datetime.now().isoformat()
        }
        
        processing_results[request_id] = results
        
        # Update final status
        processing_status[request_id].update({
            'status': 'completed',
            'message': 'Analysis completed successfully!',
            'progress': 100
        })
        
        # Send email with results (async)
        executor.submit(send_results_email, user_email, results)
        
        logger.info(f"Analysis completed for request {request_id}")
        
    except Exception as e:
        logger.error(f"Error in analysis for request {request_id}: {e}")
        processing_status[request_id].update({
            'status': 'error',
            'message': f'Analysis failed: {str(e)}',
            'progress': 0
        })

def send_results_email(user_email, results):
    """Send results email to user"""
    try:
        # Create email content
        hotel_name = results['hotel_name']
        strategy = results['strategy']
        
        # Simple email content (in production, you'd use proper email service)
        email_content = f"""
        Subject: 🏨 tphagent Marketing Strategy Results - {hotel_name}
        
        Dear Hotel Owner,
        
        Congratulations! Our AI agents have completed a comprehensive analysis and generated a personalized marketing strategy for {hotel_name}.
        
        📊 STRATEGY SUMMARY:
        • Hotel: {hotel_name}
        • Budget Tier: {strategy['budget_tier']}
        • Monthly Budget: ${strategy['monthly_budget']:,.2f}
        • Daily Budget: ${strategy['daily_budget']:,.2f}
        • Target Audience: {', '.join(strategy['target_audience'])}
        
        💰 BUDGET ALLOCATION:
        • Google Ads: ${strategy['allocation']['google_ads']:,.2f} (60%)
        • Social Media: ${strategy['allocation']['social_media']:,.2f} (25%)
        • Content Creation: ${strategy['allocation']['content_creation']:,.2f} (15%)
        
        🚀 NEXT STEPS:
        1. Set up Google Ads account
        2. Create social media profiles
        3. Add pricing to website
        4. Implement review collection
        5. Monitor performance daily
        
        Expected ROI: 400%+ within 30 days
        
        Best regards,
        tphagent Team
        AI-Powered Hotel Marketing Solutions
        """
        
        # In production, you would send this via SMTP
        print(f"📧 EMAIL WOULD BE SENT TO: {user_email}")
        print(f"📧 CONTENT: {email_content}")
        
        # For demo purposes, save to file
        with open(f'outputs/email_to_{user_email.replace("@", "_at_")}.txt', 'w') as f:
            f.write(email_content)
        
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/download/<request_id>')
def download_results(request_id):
    """Download results as JSON file"""
    if request_id not in processing_results:
        return jsonify({'error': 'Results not found'}), 404
    
    results = processing_results[request_id]
    
    # Create JSON file
    filename = f"marketing_strategy_{request_id}.json"
    filepath = f"outputs/{filename}"
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    print("🚀 Starting tphagent Frontend Server...")
    print("📧 Email: arielsanroj@carmanfe.com.co")
    print("🌐 Server: http://127.0.0.1:8080")
    print("🌐 Alternative: http://localhost:8080")
    print()
    print("💡 Note: Using port 8080 to avoid macOS AirPlay Receiver conflict")
    print("⚡ Performance optimizations enabled:")
    print("  • Parallel processing for hotel/Instagram analysis")
    print("  • Connection pooling and caching")
    print("  • Optimized HTML parsing")
    print("  • Background task processing")
    print()
    
    # Optimized Flask configuration for better performance
    app.config.update(
        DEBUG=False,  # Disable debug mode for better performance
        TEMPLATES_AUTO_RELOAD=False,  # Disable auto-reload for production
        SEND_FILE_MAX_AGE_DEFAULT=300,  # Cache static files for 5 minutes
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    )
    
    # Use port 8080 to avoid macOS AirPlay Receiver conflict
    # Use threaded=True for better concurrent request handling
    app.run(debug=False, host='127.0.0.1', port=8080, threaded=True, processes=1)