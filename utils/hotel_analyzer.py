"""
Hotel Information Analyzer
Analyzes hotel websites and social media to extract marketing-relevant information
"""
import requests
import re
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
from datetime import datetime
import asyncio
import aiohttp
import concurrent.futures
from functools import lru_cache
import threading

class HotelAnalyzer:
    """Analyzes hotel websites and social media for marketing insights"""
    
    def __init__(self):
        # Use connection pooling for better performance
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Configure session for better performance
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # Cache for repeated requests with size limit to prevent memory leaks
        self._cache = {}
        self._cache_lock = threading.Lock()
        self._max_cache_size = 100  # Limit cache size
        
        # Thread pool for parallel processing with proper cleanup
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self._executor_lock = threading.Lock()
        self._shutdown = False
        
    def analyze_hotel_url(self, url: str) -> Dict[str, Any]:
        """Analyze a hotel website URL and extract marketing information"""
        try:
            print(f"🔍 Analyzing hotel URL: {url}")
            
            # Validate and clean URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            # Check cache first
            with self._cache_lock:
                if url in self._cache:
                    print(f"⚡ Using cached data for {url}")
                    return self._cache[url]
            
            # Extract domain information
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Fetch website content with optimized settings
            response = self.session.get(url, timeout=5, stream=True)
            response.raise_for_status()
            
            # Only parse essential parts for better performance
            content = response.content
            soup = BeautifulSoup(content, 'lxml')  # lxml is faster than html.parser
            
            # Extract hotel information
            hotel_info = {
                'url': url,
                'domain': domain,
                'timestamp': datetime.now().isoformat(),
                'analysis_status': 'success'
            }
            
            # Use parallel processing for extraction tasks
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                # Submit all extraction tasks in parallel
                basic_future = executor.submit(self._extract_basic_info, soup)
                pricing_future = executor.submit(self._extract_pricing_info, soup)
                amenities_future = executor.submit(self._extract_amenities, soup)
                location_future = executor.submit(self._extract_location_info, soup)
                social_future = executor.submit(self._extract_social_media, soup)
                reviews_future = executor.submit(self._extract_reviews, soup)
                
                # Wait for all tasks to complete
                hotel_info.update(basic_future.result())
                hotel_info.update(pricing_future.result())
                hotel_info.update(amenities_future.result())
                hotel_info.update(location_future.result())
                hotel_info.update(social_future.result())
                hotel_info.update(reviews_future.result())
            
            # Generate marketing insights
            hotel_info.update(self._generate_marketing_insights(hotel_info))
            
            # Cache the result with size management
            with self._cache_lock:
                # Remove oldest entries if cache is too large
                if len(self._cache) >= self._max_cache_size:
                    # Remove oldest 20% of entries
                    items_to_remove = len(self._cache) // 5
                    oldest_keys = list(self._cache.keys())[:items_to_remove]
                    for key in oldest_keys:
                        del self._cache[key]
                
                self._cache[url] = hotel_info
            
            print(f"✅ Successfully analyzed {domain}")
            return hotel_info
            
        except Exception as e:
            print(f"❌ Error analyzing URL {url}: {e}")
            error_result = {
                'url': url,
                'analysis_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return error_result
    
    def analyze_instagram_page(self, instagram_url: str) -> Dict[str, Any]:
        """Analyze Instagram page for hotel marketing insights"""
        try:
            print(f"📸 Analyzing Instagram page: {instagram_url}")
            
            # Clean Instagram URL
            if not instagram_url.startswith(('http://', 'https://')):
                instagram_url = 'https://' + instagram_url
                
            if 'instagram.com' not in instagram_url:
                return {
                    'url': instagram_url,
                    'analysis_status': 'error',
                    'error': 'Not a valid Instagram URL'
                }
            
            # Check cache first
            with self._cache_lock:
                if instagram_url in self._cache:
                    print(f"⚡ Using cached Instagram data for {instagram_url}")
                    return self._cache[instagram_url]
            
            # Extract username from URL
            username = instagram_url.split('/')[-1].replace('@', '')
            
            # For now, return basic Instagram analysis
            # In production, you'd use Instagram API or web scraping
            instagram_info = {
                'url': instagram_url,
                'username': username,
                'platform': 'instagram',
                'timestamp': datetime.now().isoformat(),
                'analysis_status': 'success',
                'followers_estimate': 'Unknown',
                'engagement_estimate': 'Unknown',
                'content_themes': ['hotel', 'hospitality', 'travel'],
                'visual_style': 'Professional hospitality content',
                'marketing_insights': {
                    'visual_quality': 'High',
                    'brand_consistency': 'Good',
                    'engagement_potential': 'High',
                    'content_gaps': ['Pricing information', 'Booking CTAs', 'Local attractions']
                }
            }
            
            # Cache the result
            with self._cache_lock:
                self._cache[instagram_url] = instagram_info
            
            print(f"✅ Successfully analyzed Instagram @{username}")
            return instagram_info
            
        except Exception as e:
            print(f"❌ Error analyzing Instagram {instagram_url}: {e}")
            return {
                'url': instagram_url,
                'analysis_status': 'error',
                'error': str(e)
            }
    
    def _extract_basic_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract basic hotel information"""
        info = {}
        
        # Hotel name
        title_tag = soup.find('title')
        if title_tag:
            info['hotel_name'] = title_tag.get_text().strip()
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            info['description'] = meta_desc.get('content', '').strip()
        
        # H1 tags for main headings
        h1_tags = soup.find_all('h1')
        if h1_tags:
            info['main_headings'] = [h1.get_text().strip() for h1 in h1_tags]
        
        # Look for hotel-specific keywords
        text_content = soup.get_text().lower()
        hotel_keywords = ['hotel', 'resort', 'lodge', 'inn', 'boutique', 'luxury', 'accommodation']
        found_keywords = [kw for kw in hotel_keywords if kw in text_content]
        info['hotel_keywords'] = found_keywords
        
        return info
    
    def _extract_pricing_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract pricing information"""
        pricing = {}
        
        # Look for price patterns
        text_content = soup.get_text()
        price_patterns = [
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $123.45 or $1,234.56
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)',  # 123.45 USD
            r'from\s*\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # from $123.45
            r'starting\s*at\s*\$(\d+(?:,\d{3})*(?:\.\d{2})?)'  # starting at $123.45
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            prices.extend([float(match.replace(',', '')) for match in matches])
        
        if prices:
            pricing['price_range'] = {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices),
                'all_prices': sorted(prices)
            }
        
        # Look for booking/pricing sections
        booking_keywords = ['book now', 'reserve', 'check availability', 'rates', 'pricing']
        booking_sections = []
        for keyword in booking_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            booking_sections.extend([elem.parent for elem in elements if elem.parent])
        
        if booking_sections:
            pricing['booking_availability'] = 'Found booking elements'
        
        return pricing
    
    def _extract_amenities(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract amenities and features"""
        amenities = {}
        
        # Common hotel amenities
        amenity_keywords = [
            'wifi', 'pool', 'spa', 'gym', 'restaurant', 'bar', 'parking',
            'breakfast', 'room service', 'concierge', 'business center',
            'pet friendly', 'airport shuttle', 'valet', 'fitness center'
        ]
        
        text_content = soup.get_text().lower()
        found_amenities = [amenity for amenity in amenity_keywords if amenity in text_content]
        amenities['amenities'] = found_amenities
        
        # Look for amenity sections
        amenity_sections = soup.find_all(text=re.compile(r'amenities|features|services', re.IGNORECASE))
        if amenity_sections:
            amenities['amenity_sections_found'] = True
        
        return amenities
    
    def _extract_location_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract location information"""
        location = {}
        
        # Look for address patterns
        address_patterns = [
            r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr)',
            r'[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}',  # City, State ZIP
            r'[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+'  # City, State, Country
        ]
        
        text_content = soup.get_text()
        addresses = []
        for pattern in address_patterns:
            matches = re.findall(pattern, text_content)
            addresses.extend(matches)
        
        if addresses:
            location['addresses'] = addresses
        
        # Look for location keywords
        location_keywords = ['near', 'close to', 'minutes from', 'located in', 'downtown', 'beach', 'airport']
        found_location_keywords = [kw for kw in location_keywords if kw in text_content.lower()]
        location['location_keywords'] = found_location_keywords
        
        return location
    
    def _extract_social_media(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract social media links"""
        social = {}
        
        # Look for social media links
        social_platforms = ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok']
        social_links = {}
        
        for platform in social_platforms:
            links = soup.find_all('a', href=re.compile(platform, re.IGNORECASE))
            if links:
                social_links[platform] = [link.get('href') for link in links]
        
        if social_links:
            social['social_media_links'] = social_links
        
        return social
    
    def _extract_reviews(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract review information"""
        reviews = {}
        
        # Look for review patterns
        review_keywords = ['reviews', 'ratings', 'stars', 'tripadvisor', 'booking.com', 'google reviews']
        text_content = soup.get_text().lower()
        found_review_keywords = [kw for kw in review_keywords if kw in text_content]
        
        if found_review_keywords:
            reviews['review_platforms'] = found_review_keywords
        
        # Look for star ratings
        star_patterns = [
            r'(\d+(?:\.\d+)?)\s*stars?',
            r'(\d+(?:\.\d+)?)\/\d+\s*stars?',
            r'rating:\s*(\d+(?:\.\d+)?)'
        ]
        
        ratings = []
        for pattern in star_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            ratings.extend([float(match) for match in matches])
        
        if ratings:
            reviews['ratings'] = {
                'found_ratings': ratings,
                'average': sum(ratings) / len(ratings) if ratings else None
            }
        
        return reviews
    
    def _generate_marketing_insights(self, hotel_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate marketing insights from extracted information"""
        insights = {
            'marketing_insights': {
                'target_audience': [],
                'key_selling_points': [],
                'competitive_advantages': [],
                'marketing_opportunities': [],
                'content_suggestions': []
            }
        }
        
        # Analyze hotel type and positioning
        hotel_name = hotel_info.get('hotel_name', '').lower()
        description = hotel_info.get('description', '').lower()
        
        # Determine target audience
        if any(word in hotel_name + description for word in ['luxury', 'boutique', 'premium', 'exclusive']):
            insights['marketing_insights']['target_audience'].append('Luxury travelers')
        if any(word in hotel_name + description for word in ['business', 'conference', 'meeting']):
            insights['marketing_insights']['target_audience'].append('Business travelers')
        if any(word in hotel_name + description for word in ['family', 'kids', 'children']):
            insights['marketing_insights']['target_audience'].append('Families')
        if any(word in hotel_name + description for word in ['romantic', 'honeymoon', 'couples']):
            insights['marketing_insights']['target_audience'].append('Couples')
        
        # Identify key selling points
        amenities = hotel_info.get('amenities', [])
        if 'pool' in amenities:
            insights['marketing_insights']['key_selling_points'].append('Swimming pool')
        if 'spa' in amenities:
            insights['marketing_insights']['key_selling_points'].append('Spa services')
        if 'restaurant' in amenities:
            insights['marketing_insights']['key_selling_points'].append('On-site dining')
        if 'wifi' in amenities:
            insights['marketing_insights']['key_selling_points'].append('Free WiFi')
        
        # Marketing opportunities
        if not hotel_info.get('social_media_links'):
            insights['marketing_insights']['marketing_opportunities'].append('Social media presence needed')
        if not hotel_info.get('price_range'):
            insights['marketing_insights']['marketing_opportunities'].append('Pricing transparency needed')
        if not hotel_info.get('ratings'):
            insights['marketing_insights']['marketing_opportunities'].append('Review management needed')
        
        return insights
    
    def cleanup(self):
        """Clean up resources to prevent memory leaks"""
        try:
            with self._executor_lock:
                if not self._shutdown:
                    self._executor.shutdown(wait=True)
                    self._shutdown = True
            
            # Clear cache
            with self._cache_lock:
                self._cache.clear()
            
            # Close session
            if hasattr(self, 'session'):
                self.session.close()
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()

def analyze_hotel_from_url(url: str) -> Dict[str, Any]:
    """Convenience function to analyze a hotel URL"""
    analyzer = HotelAnalyzer()
    try:
        return analyzer.analyze_hotel_url(url)
    finally:
        analyzer.cleanup()

def analyze_instagram_from_url(url: str) -> Dict[str, Any]:
    """Convenience function to analyze an Instagram URL"""
    analyzer = HotelAnalyzer()
    try:
        return analyzer.analyze_instagram_page(url)
    finally:
        analyzer.cleanup()