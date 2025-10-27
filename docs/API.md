# Marketing Agent API Documentation

## Overview

The Marketing Agent system provides a comprehensive API for hotel marketing automation, including market research, ad generation, and campaign optimization.

## Base URL

- Development: `http://localhost:8080`
- Production: `https://your-domain.com`

## Authentication

Currently, the API does not require authentication for development. In production, implement proper authentication mechanisms.

## Endpoints

### 1. Hotel Analysis

#### POST `/analyze`

Analyze a hotel website and generate marketing strategy.

**Request Body:**
```json
{
  "email": "hotel@example.com",
  "hotel_url": "https://example-hotel.com",
  "instagram_url": "https://instagram.com/hotel" // optional
}
```

**Response:**
```json
{
  "success": true,
  "request_id": "req_1234567890",
  "message": "Analysis started successfully"
}
```

**Error Response:**
```json
{
  "error": "Input validation failed",
  "details": ["Email is required", "Invalid URL format"],
  "validation_results": [
    {
      "field": "email",
      "message": "Email is required",
      "severity": "error"
    }
  ]
}
```

#### GET `/status/{request_id}`

Get the status of an analysis request.

**Response:**
```json
{
  "status": "completed",
  "message": "Analysis completed successfully!",
  "progress": 100,
  "elapsed_time": 45.2,
  "results": {
    "hotel_name": "Example Hotel",
    "strategy": {
      "target_audience": ["Business travelers", "Luxury travelers"],
      "budget_tier": "Premium",
      "monthly_budget": 5000.0,
      "daily_budget": 166.67,
      "allocation": {
        "google_ads": 3000.0,
        "social_media": 1250.0,
        "content_creation": 750.0
      }
    },
    "diagnosis": "Hotel: Example Hotel | Target Audience: Business travelers, Luxury travelers | ...",
    "email": "hotel@example.com",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

#### GET `/performance`

Get system performance statistics.

**Response:**
```json
{
  "active_requests": 2,
  "completed_requests": 15,
  "error_requests": 1,
  "total_requests": 18,
  "cache_size": 45,
  "thread_pool_size": 3
}
```

#### GET `/download/{request_id}`

Download analysis results as JSON file.

**Response:** JSON file download

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Request ID not found |
| 500 | Internal Server Error |

## Rate Limiting

- 10 requests per minute per IP address
- 100 requests per hour per IP address

## Data Models

### Hotel Analysis Request
```typescript
interface HotelAnalysisRequest {
  email: string;           // Valid email address
  hotel_url: string;       // Valid HTTP/HTTPS URL
  instagram_url?: string;  // Optional Instagram URL
}
```

### Marketing Strategy
```typescript
interface MarketingStrategy {
  hotel_name: string;
  target_audience: string[];
  key_selling_points: string[];
  competitive_advantages: string[];
  marketing_opportunities: string[];
  content_suggestions: string[];
  budget_recommendation: {
    tier: string;
    monthly_budget: number;
    daily_budget: number;
    percentage_of_room_rate: number;
    allocation: {
      google_ads: number;
      social_media: number;
      content_creation: number;
    };
  };
  timeline: {
    phase_1: Phase;
    phase_2: Phase;
    phase_3: Phase;
  };
  kpis: string[];
  status: string;
  user_notes: string;
  modifications: string[];
}
```

### Phase
```typescript
interface Phase {
  name: string;
  duration: string;
  tasks: string[];
}
```

## Examples

### Complete Analysis Workflow

1. **Start Analysis:**
```bash
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "email": "hotel@example.com",
    "hotel_url": "https://example-hotel.com"
  }'
```

2. **Check Status:**
```bash
curl http://localhost:8080/status/req_1234567890
```

3. **Download Results:**
```bash
curl -O http://localhost:8080/download/req_1234567890
```

## SDK Examples

### Python
```python
import requests

# Start analysis
response = requests.post('http://localhost:8080/analyze', json={
    'email': 'hotel@example.com',
    'hotel_url': 'https://example-hotel.com'
})

request_id = response.json()['request_id']

# Check status
status_response = requests.get(f'http://localhost:8080/status/{request_id}')
print(status_response.json())
```

### JavaScript
```javascript
// Start analysis
const response = await fetch('http://localhost:8080/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'hotel@example.com',
    hotel_url: 'https://example-hotel.com'
  })
});

const { request_id } = await response.json();

// Check status
const statusResponse = await fetch(`http://localhost:8080/status/${request_id}`);
const status = await statusResponse.json();
console.log(status);
```

## Webhooks

Currently not implemented. Future versions will support webhook notifications for completed analyses.

## Changelog

### Version 1.0.0
- Initial API release
- Hotel analysis endpoint
- Status tracking
- Result download
- Input validation
- Error handling
