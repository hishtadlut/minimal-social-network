# API Documentation

This document describes the API endpoints, request/response formats, and authentication methods for the Minimal Social Network project.

## Authentication

All API requests, except for registration and login, require authentication using JWT (JSON Web Tokens). Include the token in the Authorization header of your requests:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### User Management

#### POST /api/users/register
Register a new user.

Request body:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

Response:
```json
{
  "id": "string",
  "username": "string",
  "email": "string"
}
```

#### POST /api/users/login
Authenticate a user and receive a JWT token.

Request body:
```json
{
  "email": "string",
  "password": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Posts

#### GET /api/posts
Get a list of posts for the authenticated user's feed.

Response:
```json
[
  {
    "id": "string",
    "content": "string",
    "author": {
      "id": "string",
      "username": "string"
    },
    "created_at": "string (ISO 8601 format)",
    "likes_count": 0,
    "comments_count": 0
  }
]
```

#### POST /api/posts
Create a new post.

Request body:
```json
{
  "content": "string"
}
```

Response:
```json
{
  "id": "string",
  "content": "string",
  "author": {
    "id": "string",
    "username": "string"
  },
  "created_at": "string (ISO 8601 format)",
  "likes_count": 0,
  "comments_count": 0
}
```

### Connections

#### GET /api/connections
Get a list of the authenticated user's connections.

Response:
```json
[
  {
    "id": "string",
    "username": "string"
  }
]
```

#### POST /api/connections/{user_id}
Send a connection request to another user.

Response:
```json
{
  "status": "pending"
}
```

### Chat

#### GET /api/messages/{recipient_id}
Get chat messages between the authenticated user and the specified recipient.

Response:
```json
[
  {
    "id": "string",
    "content": "string",
    "sender": {
      "id": "string",
      "username": "string"
    },
    "recipient": {
      "id": "string",
      "username": "string"
    },
    "timestamp": "string (ISO 8601 format)"
  }
]
```

#### POST /api/messages
Send a new message to a recipient.

Request body:
```json
{
  "content": "string",
  "recipient_id": "string"
}
```

Response:
```json
{
  "id": "string",
  "content": "string",
  "sender": {
    "id": "string",
    "username": "string"
  },
  "recipient": {
    "id": "string",
    "username": "string"
  },
  "timestamp": "string (ISO 8601 format)"
}
```

### User Search

#### GET /api/users/search
Search for users based on a query string.

Query parameters:
- query: string (required)

Response:
```json
[
  {
    "id": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string"
  }
]
```

## Error Handling

All API endpoints return appropriate HTTP status codes and error messages in case of failures. Common error responses include:

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing or invalid authentication token
- 403 Forbidden: Insufficient permissions to perform the requested action
- 404 Not Found: Requested resource not found
- 409 Conflict: Request could not be completed due to a conflict
- 422 Unprocessable Entity: Request data failed validation
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Unexpected server error

Error response format:
```json
{
  "error": "string",
  "message": "string",
  "details": {} // Additional error details, if available
}
```

This document provides a basic overview of the API. For more detailed information on each endpoint, including query parameters, pagination, and specific error scenarios, please refer to the full API documentation.