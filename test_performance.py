#!/usr/bin/env python3
"""
Performance test script for tphagent frontend
Tests the optimized hotel analyzer and Flask app
"""
import requests
import time
import json
import concurrent.futures
from datetime import datetime

def test_single_request():
    """Test a single hotel analysis request"""
    print("🧪 Testing single request performance...")
    
    start_time = time.time()
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "hotel_url": "https://estanciahacienda.lovable.app/",
        "instagram_url": "https://instagram.com/estanciahacienda"
    }
    
    try:
        # Start analysis
        response = requests.post('http://127.0.0.1:8080/analyze', json=test_data)
        result = response.json()
        
        if result.get('success'):
            request_id = result['request_id']
            print(f"✅ Analysis started: {request_id}")
            
            # Poll for completion
            while True:
                status_response = requests.get(f'http://127.0.0.1:8080/status/{request_id}')
                status = status_response.json()
                
                print(f"📊 Status: {status['message']} ({status['progress']}%)")
                
                if status['status'] == 'completed':
                    total_time = time.time() - start_time
                    print(f"✅ Analysis completed in {total_time:.2f} seconds")
                    return total_time
                elif status['status'] == 'error':
                    print(f"❌ Analysis failed: {status['message']}")
                    return None
                
                time.sleep(1)
        else:
            print(f"❌ Failed to start analysis: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

def test_concurrent_requests(num_requests=3):
    """Test concurrent requests to measure parallel processing"""
    print(f"🧪 Testing {num_requests} concurrent requests...")
    
    test_data = {
        "email": "test@example.com",
        "hotel_url": "https://estanciahacienda.lovable.app/",
        "instagram_url": "https://instagram.com/estanciahacienda"
    }
    
    def single_concurrent_test(test_id):
        """Single concurrent test"""
        start_time = time.time()
        
        try:
            # Start analysis
            response = requests.post('http://127.0.0.1:8080/analyze', json=test_data)
            result = response.json()
            
            if result.get('success'):
                request_id = result['request_id']
                print(f"✅ Test {test_id}: Analysis started: {request_id}")
                
                # Poll for completion
                while True:
                    status_response = requests.get(f'http://127.0.0.1:8080/status/{request_id}')
                    status = status_response.json()
                    
                    if status['status'] == 'completed':
                        total_time = time.time() - start_time
                        print(f"✅ Test {test_id}: Completed in {total_time:.2f} seconds")
                        return total_time
                    elif status['status'] == 'error':
                        print(f"❌ Test {test_id}: Failed: {status['message']}")
                        return None
                    
                    time.sleep(1)
            else:
                print(f"❌ Test {test_id}: Failed to start: {result.get('error')}")
                return None
                
        except Exception as e:
            print(f"❌ Test {test_id}: Error: {e}")
            return None
    
    # Run concurrent tests
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(single_concurrent_test, i+1) for i in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    total_time = time.time() - start_time
    successful_results = [r for r in results if r is not None]
    
    if successful_results:
        avg_time = sum(successful_results) / len(successful_results)
        print(f"📊 Concurrent test results:")
        print(f"   • Total time: {total_time:.2f} seconds")
        print(f"   • Average per request: {avg_time:.2f} seconds")
        print(f"   • Successful requests: {len(successful_results)}/{num_requests}")
        print(f"   • Throughput: {len(successful_results)/total_time:.2f} requests/second")
    else:
        print("❌ All concurrent tests failed")
    
    return successful_results

def test_performance_metrics():
    """Test performance metrics endpoint"""
    print("🧪 Testing performance metrics...")
    
    try:
        response = requests.get('http://127.0.0.1:8080/performance')
        metrics = response.json()
        
        print("📊 Performance Metrics:")
        print(f"   • Active requests: {metrics['active_requests']}")
        print(f"   • Completed requests: {metrics['completed_requests']}")
        print(f"   • Error requests: {metrics['error_requests']}")
        print(f"   • Total requests: {metrics['total_requests']}")
        print(f"   • Cache size: {metrics['cache_size']}")
        print(f"   • Thread pool size: {metrics['thread_pool_size']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to get performance metrics: {e}")
        return False

def main():
    """Run all performance tests"""
    print("🚀 tphagent Performance Test Suite")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if server is running
    try:
        response = requests.get('http://127.0.0.1:8080/', timeout=5)
        print("✅ Server is running on port 8080")
    except Exception as e:
        print(f"❌ Server not running on port 8080: {e}")
        print("Please start the server first with: python frontend/app.py")
        return
    
    print()
    
    # Test 1: Single request
    print("TEST 1: Single Request Performance")
    print("-" * 40)
    single_time = test_single_request()
    print()
    
    # Test 2: Performance metrics
    print("TEST 2: Performance Metrics")
    print("-" * 40)
    metrics_ok = test_performance_metrics()
    print()
    
    # Test 3: Concurrent requests
    print("TEST 3: Concurrent Request Performance")
    print("-" * 40)
    concurrent_results = test_concurrent_requests(3)
    print()
    
    # Summary
    print("📋 PERFORMANCE TEST SUMMARY")
    print("=" * 50)
    
    if single_time:
        print(f"✅ Single request: {single_time:.2f} seconds")
    else:
        print("❌ Single request: Failed")
    
    if metrics_ok:
        print("✅ Performance metrics: Available")
    else:
        print("❌ Performance metrics: Failed")
    
    if concurrent_results:
        avg_concurrent = sum(concurrent_results) / len(concurrent_results)
        print(f"✅ Concurrent requests: {len(concurrent_results)} successful, avg {avg_concurrent:.2f}s")
    else:
        print("❌ Concurrent requests: All failed")
    
    print()
    print("💡 Performance optimizations applied:")
    print("   • Parallel processing for hotel/Instagram analysis")
    print("   • Connection pooling and request caching")
    print("   • Optimized HTML parsing with lxml")
    print("   • Background task processing with thread pools")
    print("   • Adaptive polling for status updates")
    print("   • Performance monitoring and metrics")

if __name__ == "__main__":
    main()