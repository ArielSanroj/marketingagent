"""
Test suite for hotel analyzer
"""
import pytest
from unittest.mock import Mock, patch
from utils.hotel_analyzer import HotelAnalyzer, analyze_hotel_from_url, analyze_instagram_from_url

class TestHotelAnalyzer:
    """Test hotel analyzer functionality"""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = HotelAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, 'session')
        assert hasattr(analyzer, '_cache')
        assert hasattr(analyzer, '_executor')
    
    def test_cleanup(self):
        """Test analyzer cleanup"""
        analyzer = HotelAnalyzer()
        analyzer.cleanup()
        assert analyzer._shutdown is True
    
    @patch('utils.hotel_analyzer.requests.Session.get')
    def test_analyze_hotel_url_success(self, mock_get):
        """Test successful hotel URL analysis"""
        # Mock successful response
        mock_response = Mock()
        mock_response.content = b'<html><title>Test Hotel</title><body>Hotel content</body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        analyzer = HotelAnalyzer()
        result = analyzer.analyze_hotel_url("https://example.com")
        
        assert result['analysis_status'] == 'success'
        assert 'hotel_name' in result
        assert result['url'] == "https://example.com"
        
        analyzer.cleanup()
    
    @patch('utils.hotel_analyzer.requests.Session.get')
    def test_analyze_hotel_url_error(self, mock_get):
        """Test hotel URL analysis with error"""
        # Mock error response
        mock_get.side_effect = Exception("Connection error")
        
        analyzer = HotelAnalyzer()
        result = analyzer.analyze_hotel_url("https://example.com")
        
        assert result['analysis_status'] == 'error'
        assert 'error' in result
        
        analyzer.cleanup()
    
    def test_analyze_instagram_url_success(self):
        """Test successful Instagram URL analysis"""
        analyzer = HotelAnalyzer()
        result = analyzer.analyze_instagram_page("https://instagram.com/test_hotel")
        
        assert result['analysis_status'] == 'success'
        assert result['username'] == 'test_hotel'
        assert result['platform'] == 'instagram'
        
        analyzer.cleanup()
    
    def test_analyze_instagram_url_invalid(self):
        """Test Instagram URL analysis with invalid URL"""
        analyzer = HotelAnalyzer()
        result = analyzer.analyze_instagram_page("https://example.com")
        
        assert result['analysis_status'] == 'error'
        assert 'Not a valid Instagram URL' in result['error']
        
        analyzer.cleanup()
    
    def test_cache_management(self):
        """Test cache size management"""
        analyzer = HotelAnalyzer()
        
        # Add items to cache beyond limit
        for i in range(150):  # More than max_cache_size (100)
            analyzer._cache[f"url_{i}"] = {"test": "data"}
        
        # Trigger cache management
        with analyzer._cache_lock:
            if len(analyzer._cache) >= analyzer._max_cache_size:
                items_to_remove = len(analyzer._cache) // 5
                oldest_keys = list(analyzer._cache.keys())[:items_to_remove]
                for key in oldest_keys:
                    del analyzer._cache[key]
        
        # Cache should be reduced
        assert len(analyzer._cache) < 150
        
        analyzer.cleanup()

class TestConvenienceFunctions:
    """Test convenience functions"""
    
    @patch('utils.hotel_analyzer.HotelAnalyzer.analyze_hotel_url')
    def test_analyze_hotel_from_url(self, mock_analyze):
        """Test analyze_hotel_from_url convenience function"""
        mock_analyze.return_value = {"analysis_status": "success"}
        
        result = analyze_hotel_from_url("https://example.com")
        
        assert result["analysis_status"] == "success"
        mock_analyze.assert_called_once_with("https://example.com")
    
    @patch('utils.hotel_analyzer.HotelAnalyzer.analyze_instagram_page')
    def test_analyze_instagram_from_url(self, mock_analyze):
        """Test analyze_instagram_from_url convenience function"""
        mock_analyze.return_value = {"analysis_status": "success"}
        
        result = analyze_instagram_from_url("https://instagram.com/test")
        
        assert result["analysis_status"] == "success"
        mock_analyze.assert_called_once_with("https://instagram.com/test")
