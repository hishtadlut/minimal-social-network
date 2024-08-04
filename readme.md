# Minimal Social Network Project

## Project Description
This project is a minimal social network application similar to Facebook, focusing on essential features. It provides basic functionality for user management, connections between users, content sharing, and user interactions. The application is built using a FastAPI backend and a React frontend, with Docker for easy deployment and development. Key features include user authentication, post creation and viewing, and a responsive design for both mobile and desktop use.

## Prerequisites
- Docker
- Docker Compose
- Node.js (for local frontend development)
- Python 3.9+ (for local backend development)

## Development Environment Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/minimal-social-network.git
cd minimal-social-network
```

### 2. Configure the environment
Create a `.env` file in the root directory and add the following variables:
```
REACT_APP_API_URL=http://localhost:8000
```

### 3. Build and start the Docker containers
```bash
docker-compose up --build
```

### 4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Features
- User registration and authentication
- Create and view posts
- Basic user profiles
- Responsive design for mobile and desktop

## Basic Usage
1. Register a new account or log in with existing credentials
2. Create and share posts
3. View posts from other users
4. Update your profile information

## Project Structure
```
minimal-social-network/
|-- docker-compose.yml
|-- README.md
|-- .env
|-- docs/
|   |-- API.md
|   |-- Database.md
|   |-- Deployment.md
|-- backend/
|   |-- Dockerfile
|   |-- main.py
|   |-- requirements.txt
|-- frontend/
|   |-- Dockerfile
|   |-- src/
|   |   |-- components/
|   |   |-- App.js
|   |   |-- config.js
|-- database/
    |-- ...
```

## Documentation
- API documentation: docs/API.md
- Database schema: docs/Database.md
- Deployment guide: docs/Deployment.md

## Contributing
We welcome contributions to the Minimal Social Network project. Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear, descriptive messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please ensure your code follows the existing style and includes appropriate tests.

## Known Limitations
- Limited friend/connection functionality
- No image upload capability for posts or profiles
- Basic error handling and input validation

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.