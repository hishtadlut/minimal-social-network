# Minimal Social Network Project

## Project Description
This project is a minimal social network application similar to Facebook, focusing on essential features. It was rapidly developed in just one night using Claude Engineer, an AI-powered development tool, demonstrating the power of AI-assisted coding. The application provides basic functionality for user management, connections between users, content sharing, and user interactions. It is built using a FastAPI backend and a React frontend, with Docker for easy deployment and development.

## Development Highlights
- Developed in just one night with the assistance of Claude Engineer
- Cost-effective development process (approximately $50 in resources)
- Rapid implementation of core features
- AI-assisted code writing, problem-solving, and documentation

## Features Checklist

### Implemented Features
- [x] User registration and authentication
- [x] Create and view posts
- [x] Basic user profiles
- [x] Real-time chat functionality
- [x] User search
- [x] Responsive design for mobile and desktop
- [x] Docker containerization

### Planned Features
- [ ] Advanced post engine
- [ ] User groups
- [ ] Image upload for posts and profiles
- [ ] Friend/connection management
- [ ] Notifications system
- [ ] Advanced privacy settings

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

## Basic Usage
1. Register a new account or log in with existing credentials
2. Create and share posts
3. View posts from other users
4. Use the search functionality to find other users
5. Start a chat with other users
6. Update your profile information

## Future Development
We are actively working on expanding the features of this Minimal Social Network. Our upcoming plans include:
- Implementing an advanced post engine for better content management
- Adding user groups for community building
- Enhancing the friend/connection functionality
- Implementing a robust notifications system
- Improving privacy settings for user control

We welcome contributions and feedback to help make this project even better!

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