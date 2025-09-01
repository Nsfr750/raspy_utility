# API Reference

This document provides detailed information about the Raspberry Pi Utility API endpoints and their usage.

## Table of Contents
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [GPIO Control](#gpio-control)
  - [System Information](#system-information)
  - [Application Management](#application-management)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Authentication

All API endpoints require authentication. Include your API key in the request header:

```http
Authorization: Bearer your_api_key_here
```

## Endpoints

### GPIO Control

#### Get All GPIO Pins Status
```http
GET /api/gpio
```

**Response**
```json
{
  "success": true,
  "data": [
    {
      "pin": 17,
      "mode": "OUT",
      "state": 1
    },
    ...
  ]
}
```

#### Set GPIO Pin State
```http
POST /api/gpio/{pin}
Content-Type: application/json

{
  "state": 1,
  "duration": 1000
}
```

**Parameters**
- `pin` (integer, required): The GPIO pin number
- `state` (integer, required): 0 for LOW, 1 for HIGH
- `duration` (integer, optional): Duration in milliseconds (0 for permanent)

**Response**
```json
{
  "success": true,
  "message": "Pin 17 set to HIGH"
}
```

### System Information

#### Get System Status
```http
GET /api/system/status
```

**Response**
```json
{
  "cpu_usage": 12.5,
  "memory_usage": 45.2,
  "disk_usage": 23.7,
  "uptime": 1234567,
  "temperature": 45.6
}
```

### Application Management

#### Get Application Version
```http
GET /api/version
```

**Response**
```json
{
  "version": "1.0.0",
  "build_date": "2025-09-01T18:30:00Z",
  "git_commit": "a1b2c3d"
}
```

## Error Handling

Errors follow the standard HTTP status codes and include a JSON response with error details:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PIN",
    "message": "Invalid GPIO pin number"
  }
}
```

### Common Error Codes
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

API requests are limited to 1000 requests per hour per API key. The following headers are included in rate-limited responses:

- `X-RateLimit-Limit`: The maximum number of requests allowed in the current period
- `X-RateLimit-Remaining`: The number of requests remaining in the current period
- `X-RateLimit-Reset`: The time at which the current rate limit window resets (UTC epoch seconds)
