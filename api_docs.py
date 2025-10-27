"""
Comprehensive API Documentation with Swagger/OpenAPI
Complete API documentation with examples, schemas, and interactive testing
"""
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.append('..')

from utils.logger import get_logger
from utils.validators import validate_and_sanitize_input
from utils.rate_limiter import get_rate_limiter, check_rate_limit
from utils.database import get_database_manager

logger = get_logger(__name__)

# Initialize Flask app for API documentation
app = Flask(__name__)
CORS(app)

# Initialize Flask-RESTX API
api = Api(
    app,
    version='1.0.0',
    title='Marketing Agent API',
    description='Comprehensive API for Hotel Marketing Analysis and Campaign Management',
    doc='/docs/',
    prefix='/api/v1'
)

# Define namespaces
main_ns = Namespace('main', description='Main API operations')
admin_ns = Namespace('admin', description='Administrative operations')
monitoring_ns = Namespace('monitoring', description='Monitoring and health checks')

# Add namespaces to API
api.add_namespace(main_ns)
api.add_namespace(admin_ns)
api.add_namespace(monitoring_ns)

# Define data models
hotel_analysis_request = api.model('HotelAnalysisRequest', {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'hotel_url': fields.String(required=False, description='Hotel website URL', example='https://example-hotel.com'),
    'instagram_url': fields.String(required=False, description='Hotel Instagram URL', example='https://instagram.com/examplehotel')
})

hotel_analysis_response = api.model('HotelAnalysisResponse', {
    'request_id': fields.String(description='Unique request identifier'),
    'status': fields.String(description='Processing status', example='processing'),
    'message': fields.String(description='Status message'),
    'progress': fields.Integer(description='Progress percentage (0-100)'),
    'estimated_completion': fields.String(description='Estimated completion time')
})

analysis_result = api.model('AnalysisResult', {
    'hotel_name': fields.String(description='Hotel name'),
    'market_analysis': fields.Raw(description='Market analysis data'),
    'marketing_strategy': fields.Raw(description='Generated marketing strategy'),
    'google_ads_campaign': fields.Raw(description='Google Ads campaign data'),
    'optimization_recommendations': fields.Raw(description='Performance optimization recommendations')
})

error_response = api.model('ErrorResponse', {
    'error': fields.String(description='Error type'),
    'message': fields.String(description='Error message'),
    'details': fields.Raw(description='Additional error details')
})

validation_error = api.model('ValidationError', {
    'field': fields.String(description='Field name'),
    'message': fields.String(description='Validation error message'),
    'severity': fields.String(description='Error severity level')
})

rate_limit_response = api.model('RateLimitResponse', {
    'error': fields.String(description='Error type'),
    'message': fields.String(description='Rate limit message'),
    'details': fields.Raw(description='Rate limit details')
})

performance_stats = api.model('PerformanceStats', {
    'active_requests': fields.Integer(description='Number of active requests'),
    'completed_requests': fields.Integer(description='Number of completed requests'),
    'average_processing_time': fields.Float(description='Average processing time in seconds'),
    'memory_usage_mb': fields.Float(description='Memory usage in MB'),
    'cpu_usage_percent': fields.Float(description='CPU usage percentage')
})

security_stats = api.model('SecurityStats', {
    'rate_limiting': fields.Raw(description='Rate limiting statistics'),
    'ddos_protection': fields.Raw(description='DDoS protection statistics'),
    'database': fields.Raw(description='Database performance statistics'),
    'timestamp': fields.String(description='Statistics timestamp')
})

# Main API endpoints
@main_ns.route('/analyze')
class HotelAnalysis(Resource):
    @main_ns.expect(hotel_analysis_request, validate=True)
    @main_ns.marshal_with(hotel_analysis_response, code=200, description='Analysis request submitted successfully')
    @main_ns.marshal_with(validation_error, code=400, description='Validation error')
    @main_ns.marshal_with(rate_limit_response, code=429, description='Rate limit exceeded')
    @main_ns.marshal_with(error_response, code=500, description='Internal server error')
    def post(self):
        """
        Analyze hotel and generate marketing strategy
        
        This endpoint analyzes a hotel's website and social media presence to generate
        a comprehensive marketing strategy including:
        - Market analysis
        - Marketing recommendations
        - Google Ads campaign suggestions
        - Performance optimization tips
        
        The analysis is processed asynchronously and results are available via the status endpoint.
        """
        try:
            data = request.get_json()
            
            # Validate and sanitize input
            is_valid, sanitized_data, validation_results = validate_and_sanitize_input(data, 'analysis')
            
            if not is_valid:
                error_messages = [result.message for result in validation_results if not result.is_valid]
                return {
                    'error': 'Input validation failed',
                    'details': error_messages,
                    'validation_results': [
                        {
                            'field': result.field,
                            'message': result.message,
                            'severity': result.severity.value
                        } for result in validation_results
                    ]
                }, 400
            
            # Generate request ID
            import uuid
            request_id = str(uuid.uuid4())
            
            # Start background processing (simplified for documentation)
            # In real implementation, this would start the actual analysis
            
            return {
                'request_id': request_id,
                'status': 'processing',
                'message': 'Analysis request submitted successfully',
                'progress': 0,
                'estimated_completion': '5-10 minutes'
            }, 200
            
        except Exception as e:
            logger.error(f"Error in hotel analysis: {e}")
            return {
                'error': 'Internal server error',
                'message': str(e)
            }, 500

@main_ns.route('/status/<string:request_id>')
class AnalysisStatus(Resource):
    @main_ns.marshal_with(hotel_analysis_response, code=200, description='Status retrieved successfully')
    @main_ns.marshal_with(error_response, code=404, description='Request not found')
    def get(self, request_id):
        """
        Get analysis status and results
        
        Retrieve the current status of a hotel analysis request.
        Returns progress information and results when available.
        """
        # In real implementation, this would check the actual processing status
        # For documentation purposes, return a mock response
        return {
            'request_id': request_id,
            'status': 'completed',
            'message': 'Analysis completed successfully',
            'progress': 100,
            'estimated_completion': 'Completed'
        }, 200

@main_ns.route('/results/<string:request_id>')
class AnalysisResults(Resource):
    @main_ns.marshal_with(analysis_result, code=200, description='Results retrieved successfully')
    @main_ns.marshal_with(error_response, code=404, description='Results not found')
    def get(self, request_id):
        """
        Get analysis results
        
        Retrieve the complete analysis results for a hotel.
        Includes market analysis, marketing strategy, and campaign recommendations.
        """
        # In real implementation, this would return actual results
        # For documentation purposes, return a mock response
        return {
            'hotel_name': 'Example Hotel',
            'market_analysis': {
                'target_audience': 'Business travelers and tourists',
                'competitors': ['Hotel A', 'Hotel B'],
                'market_opportunities': ['Digital marketing', 'Social media presence']
            },
            'marketing_strategy': {
                'recommended_channels': ['Google Ads', 'Facebook', 'Instagram'],
                'budget_allocation': {
                    'google_ads': 60,
                    'social_media': 30,
                    'content_marketing': 10
                }
            },
            'google_ads_campaign': {
                'campaign_name': 'Example Hotel - Search Campaign',
                'keywords': ['hotel near airport', 'business hotel'],
                'budget': 1000,
                'target_roas': 400
            },
            'optimization_recommendations': [
                'Improve website loading speed',
                'Optimize for mobile devices',
                'Add customer reviews section'
            ]
        }, 200

# Administrative endpoints
@admin_ns.route('/rate-limit-stats')
class RateLimitStats(Resource):
    @admin_ns.marshal_with(security_stats, code=200, description='Rate limiting statistics retrieved')
    @admin_ns.marshal_with(error_response, code=500, description='Failed to get statistics')
    def get(self):
        """
        Get rate limiting statistics
        
        Retrieve comprehensive statistics about rate limiting and security measures.
        Includes active clients, blocked IPs, and threat level distribution.
        """
        try:
            rate_limiter = get_rate_limiter()
            stats = rate_limiter.get_stats()
            ddos_stats = rate_limiter.ddos_protection.get_attack_stats()
            
            return {
                'rate_limiting': stats,
                'ddos_protection': ddos_stats,
                'database': {},
                'timestamp': '2024-01-01T00:00:00Z'
            }, 200
        except Exception as e:
            logger.error(f"Error getting rate limit stats: {e}")
            return {
                'error': 'Failed to get statistics',
                'message': str(e)
            }, 500

@admin_ns.route('/security-stats')
class SecurityStats(Resource):
    @admin_ns.marshal_with(security_stats, code=200, description='Security statistics retrieved')
    @admin_ns.marshal_with(error_response, code=500, description='Failed to get security statistics')
    def get(self):
        """
        Get comprehensive security statistics
        
        Retrieve detailed security metrics including rate limiting,
        DDoS protection, and database performance statistics.
        """
        try:
            # Get rate limiting stats
            rate_limiter = get_rate_limiter()
            rate_stats = rate_limiter.get_stats()
            ddos_stats = rate_limiter.ddos_protection.get_attack_stats()
            
            # Get database performance stats
            try:
                db_manager = get_database_manager()
                db_stats = db_manager.get_performance_stats()
            except:
                db_stats = {}
            
            return {
                'rate_limiting': rate_stats,
                'ddos_protection': ddos_stats,
                'database': db_stats,
                'timestamp': '2024-01-01T00:00:00Z'
            }, 200
        except Exception as e:
            logger.error(f"Error getting security stats: {e}")
            return {
                'error': 'Failed to get security statistics',
                'message': str(e)
            }, 500

# Monitoring endpoints
@monitoring_ns.route('/health')
class HealthCheck(Resource):
    def get(self):
        """
        Health check endpoint
        
        Check the health status of the application and its dependencies.
        Returns status of database, Redis, and other critical services.
        """
        health_status = {
            'status': 'healthy',
            'timestamp': '2024-01-01T00:00:00Z',
            'services': {
                'database': 'healthy',
                'redis': 'healthy',
                'rate_limiter': 'healthy'
            },
            'version': '1.0.0'
        }
        
        return health_status, 200

@monitoring_ns.route('/performance')
class PerformanceStats(Resource):
    @monitoring_ns.marshal_with(performance_stats, code=200, description='Performance statistics retrieved')
    def get(self):
        """
        Get performance statistics
        
        Retrieve comprehensive performance metrics including:
        - Active and completed requests
        - Average processing times
        - Memory and CPU usage
        - Database performance
        """
        return {
            'active_requests': 5,
            'completed_requests': 150,
            'average_processing_time': 45.2,
            'memory_usage_mb': 256.7,
            'cpu_usage_percent': 15.3
        }, 200

@monitoring_ns.route('/metrics')
class Metrics(Resource):
    def get(self):
        """
        Get detailed metrics
        
        Retrieve detailed application metrics for monitoring and alerting.
        Includes system metrics, application metrics, and business metrics.
        """
        metrics = {
            'system': {
                'memory_usage_mb': 256.7,
                'cpu_usage_percent': 15.3,
                'disk_usage_percent': 45.2
            },
            'application': {
                'requests_per_minute': 25,
                'average_response_time_ms': 150.5,
                'error_rate_percent': 0.1
            },
            'business': {
                'analyses_completed': 150,
                'campaigns_created': 45,
                'success_rate_percent': 95.2
            },
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        return metrics, 200

# Error handlers
@api.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return {
        'error': 'Bad Request',
        'message': 'Invalid request data',
        'details': str(error)
    }, 400

@api.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return {
        'error': 'Not Found',
        'message': 'Resource not found',
        'details': str(error)
    }, 404

@api.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle 429 Rate Limit Exceeded errors"""
    return {
        'error': 'Rate Limit Exceeded',
        'message': 'Too many requests',
        'details': 'Please wait before making another request'
    }, 429

@api.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    return {
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'details': str(error)
    }, 500

# API documentation configuration
api_doc_config = {
    'title': 'Marketing Agent API',
    'version': '1.0.0',
    'description': '''
    # Marketing Agent API Documentation
    
    ## Overview
    The Marketing Agent API provides comprehensive hotel marketing analysis and campaign management capabilities.
    
    ## Features
    - **Hotel Analysis**: Analyze hotel websites and social media presence
    - **Market Research**: Generate market insights and competitor analysis
    - **Campaign Creation**: Create and manage Google Ads campaigns
    - **Performance Optimization**: Monitor and optimize campaign performance
    - **Security**: Rate limiting, DDoS protection, and input validation
    
    ## Authentication
    Currently, the API does not require authentication. Rate limiting is applied based on IP address.
    
    ## Rate Limiting
    - **Default**: 60 requests per minute, 1000 requests per hour
    - **Burst**: 10 requests per minute
    - **Block Duration**: 5 minutes for violations
    
    ## Error Handling
    All errors return JSON responses with appropriate HTTP status codes.
    
    ## Examples
    
    ### Analyze Hotel
    ```bash
    curl -X POST "http://localhost:5000/api/v1/analyze" \\
         -H "Content-Type: application/json" \\
         -d '{
           "email": "user@example.com",
           "hotel_url": "https://example-hotel.com",
           "instagram_url": "https://instagram.com/examplehotel"
         }'
    ```
    
    ### Check Status
    ```bash
    curl "http://localhost:5000/api/v1/status/123e4567-e89b-12d3-a456-426614174000"
    ```
    
    ### Get Results
    ```bash
    curl "http://localhost:5000/api/v1/results/123e4567-e89b-12d3-a456-426614174000"
    ```
    ''',
    'contact': {
        'name': 'Marketing Agent Support',
        'email': 'support@marketingagent.com'
    },
    'license': {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    }
}

if __name__ == '__main__':
    # Run the API documentation server
    app.run(debug=True, host='0.0.0.0', port=5001)
