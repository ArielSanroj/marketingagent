"""
Simple test server to check Flask configuration
"""
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>tphagent Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .success { color: #4CAF50; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏨 tphagent Test Server</h1>
            <p class="success">✅ Flask server is working correctly!</p>
            <p>If you can see this page, the server is running properly.</p>
            <p>Now you can access the full frontend at the same address.</p>
        </div>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return {'status': 'success', 'message': 'API is working'}

if __name__ == '__main__':
    print("🧪 Starting tphagent Test Server...")
    print("🌐 Test URL: http://127.0.0.1:5000")
    print("🌐 Test API: http://127.0.0.1:5000/test")
    print()
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying port 8080...")
        app.run(debug=True, host='127.0.0.1', port=8080, threaded=True)