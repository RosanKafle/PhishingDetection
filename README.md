# Phishing Detection and Awareness Platform

A web-based security platform designed to help users identify and learn about phishing attacks through machine learning detection and educational content. This project combines real-time URL analysis with user awareness training to create a comprehensive anti-phishing solution.

## Overview

Phishing attacks continue to be one of the most prevalent cybersecurity threats, with attackers constantly evolving their techniques. This platform addresses this challenge by providing both automated detection capabilities and educational resources to help users recognize and avoid phishing attempts.

The system uses a machine learning model trained on various URL characteristics and suspicious patterns to classify potentially malicious links. Additionally, it provides an educational framework where administrators can create articles and quizzes to improve user awareness.

## Key Features

**Detection Engine**
- Real-time URL analysis using machine learning
- Feature extraction from URL structure, domain properties, and content patterns
- Configurable detection thresholds for different security requirements
- Historical tracking of detection results

**User Management**
- Secure user registration and authentication
- Role-based access control for administrators
- Personal detection history for each user
- Session management with JWT tokens

**Educational Platform**
- Administrative interface for creating educational content
- Support for both articles and interactive quizzes
- Content management system with database persistence
- User progress tracking and engagement metrics

**Analytics Dashboard**
- Real-time statistics on system usage
- Machine learning model performance metrics
- Threat intelligence integration and visualization
- Administrative oversight tools

## Technical Architecture

### Frontend Components
The user interface is built with React.js, providing a responsive and interactive experience. The frontend handles user authentication, displays detection results, and provides access to educational content. Key components include:

- Authentication forms with input validation
- Dashboard for URL analysis and results display
- Administrative panel for content management
- Educational content viewer with quiz functionality

### Backend Services
The server-side architecture uses Node.js with Express.js to provide RESTful API endpoints. The backend manages user authentication, processes detection requests, and handles content management. Core services include:

- User authentication and session management
- API endpoints for machine learning model integration
- Database operations for user data and content storage
- Security middleware including rate limiting and CORS protection

### Machine Learning Integration
The detection system uses a Python-based machine learning model that analyzes various URL characteristics. The model is integrated with the web application through subprocess calls and JSON communication. Features analyzed include:

- URL length and structural properties
- Domain characteristics and subdomain analysis
- Presence of suspicious keywords and patterns
- SSL certificate validation status
- Brand spoofing detection mechanisms

### Data Storage
MongoDB is used for persistent data storage, with separate collections for users, detection history, and educational content. The database schema supports:

- User profiles with encrypted passwords
- Detection results with timestamps and metadata
- Educational articles and quiz questions
- System analytics and usage statistics

## Installation and Setup

### Prerequisites
Before setting up the platform, ensure you have the following installed:
- Node.js version 14 or higher
- Python 3.8 or later
- MongoDB database (local installation or cloud service)
- Git for version control

### Initial Setup
Clone the repository to your local machine:
```bash
git clone https://github.com/roshankaphle/phishingdetection.git
cd phishing-detection-platform
```

Install the required Node.js dependencies for both frontend and backend:
```bash
npm install
cd backend
npm install
cd ..
```

Install Python dependencies for the machine learning components:
```bash
pip install -r requirements.txt
```

### Configuration
Create a configuration file in the backend directory named `.env`:
```
MONGO_URI=mongodb://localhost:27017/phishing
JWT_SECRET=your-secure-secret-key
NODE_ENV=development
PHISH_THRESHOLD=0.15
```

Train the machine learning model before first use:
```bash
python3 phishing_detection.py
```

### Running the Application
Start the backend server:
```bash
cd backend
npm start
```

In a separate terminal, start the frontend development server:
```bash
npm start
```

The application will be available at `http://localhost:3000` with the API server running on `http://localhost:5000`.

## Usage Guide

### For End Users
Users can register for an account and begin analyzing suspicious URLs immediately. The detection process is straightforward - paste a URL into the analysis form and receive instant feedback about potential threats. The system maintains a history of all analyses for future reference.

The educational section provides access to articles about phishing recognition and interactive quizzes to test knowledge. Users can track their progress and improve their ability to identify threats independently.

### For Administrators
Administrators have access to additional features through the admin panel. They can view system-wide statistics, manage user accounts, and create educational content. The content management system supports both article creation and quiz development with multiple-choice questions.

The analytics dashboard provides insights into system usage, detection patterns, and user engagement with educational materials. This information helps administrators understand the effectiveness of the platform and identify areas for improvement.

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Authenticate existing user

### Detection Services
- `POST /api/analytics/ml/predict` - Analyze URL for phishing indicators
- `GET /api/detections` - Retrieve user's detection history

### Administrative Functions
- `GET /api/admin/stats` - System statistics and metrics
- `POST /api/content/add` - Create educational content

### Analytics and Monitoring
- `GET /api/analytics/ml/metrics` - Machine learning model performance
- `GET /api/dashboard/threat-intelligence` - Threat landscape data

## Machine Learning Model Details

### Feature Engineering
The detection model analyzes multiple aspects of URLs to identify potential threats:

**Structural Analysis**
- Overall URL length and complexity
- Domain name characteristics and length
- Path structure and depth
- Presence of suspicious characters or patterns

**Content Analysis**
- Keyword matching against known phishing terms
- Brand name detection and spoofing analysis
- Language patterns and grammatical indicators
- Visual similarity to legitimate sites

**Technical Indicators**
- SSL certificate status and validity
- Domain registration information
- Subdomain analysis and suspicious patterns
- Redirect chains and URL shortening detection

### Model Performance
The current model achieves the following performance metrics on our test dataset:
- Accuracy: 83.3%
- Precision: 90.9%
- Recall: 83.3%
- F1-Score: 87.0%

These metrics indicate a balanced approach that minimizes both false positives and false negatives, making the system practical for real-world deployment.

### Training Data
The model is trained on a diverse dataset including:
- Legitimate URLs from popular websites and services
- Known phishing URLs from threat intelligence feeds
- Synthetic examples based on common attack patterns
- Historical data from security incident reports

## Security Considerations

### Application Security
The platform implements several security measures to protect user data and system integrity:

- Password hashing using bcrypt with appropriate salt rounds
- JWT token-based authentication with configurable expiration
- Rate limiting to prevent abuse and brute force attacks
- Input validation and sanitization on all user inputs
- CORS configuration to control cross-origin requests

### Data Protection
User privacy and data security are prioritized through:
- Encrypted storage of sensitive information
- Minimal data collection practices
- Secure session management
- Regular security updates and dependency management

### Deployment Security
For production deployments, additional security measures should be implemented:
- HTTPS encryption for all communications
- Database access controls and network segmentation
- Regular security audits and penetration testing
- Monitoring and logging for security events

## Development and Contribution

### Project Structure
The codebase is organized into logical components:
- `src/` contains React frontend components and utilities
- `backend/` houses the Node.js server code and API routes
- `backend/models/` defines database schemas and data models
- `backend/scripts/` contains Python machine learning integration
- `public/` stores static assets and configuration files

### Development Workflow
Contributors should follow these guidelines:
1. Create feature branches for new development
2. Write comprehensive tests for new functionality
3. Follow existing code style and formatting conventions
4. Update documentation for any API or feature changes
5. Submit pull requests with detailed descriptions

### Testing
The platform includes various testing approaches:
- Unit tests for individual components and functions
- Integration tests for API endpoints and database operations
- End-to-end tests for complete user workflows
- Performance testing for machine learning inference

## Deployment Options

### Development Environment
For local development and testing, the application can run with minimal configuration using the built-in development servers and a local MongoDB instance.

### Production Deployment
Production deployments should consider:
- Container orchestration using Docker and Docker Compose
- Load balancing for high availability
- Database clustering and backup strategies
- Content delivery networks for static assets
- Monitoring and alerting systems

### Cloud Platforms
The application is compatible with major cloud platforms:
- AWS with EC2, RDS, and S3 integration
- Google Cloud Platform with App Engine and Cloud SQL
- Microsoft Azure with App Service and Cosmos DB
- Heroku for simplified deployment and scaling

## Performance and Scalability

### Current Performance
The system is designed to handle moderate loads with:
- Sub-second response times for URL analysis
- Concurrent user support through efficient database queries
- Caching mechanisms for frequently accessed data
- Optimized machine learning inference

### Scaling Considerations
For larger deployments, consider:
- Horizontal scaling of web servers
- Database read replicas for improved query performance
- Caching layers using Redis or similar technologies
- Content delivery networks for global distribution

## Troubleshooting

### Common Issues
**Database Connection Problems**
- Verify MongoDB is running and accessible
- Check connection string format and credentials
- Ensure network connectivity between application and database

**Machine Learning Model Errors**
- Confirm Python dependencies are installed correctly
- Verify model file exists and is accessible
- Check Python path and environment configuration

**Authentication Issues**
- Validate JWT secret configuration
- Check token expiration settings
- Verify user credentials and database records

### Logging and Monitoring
The application provides comprehensive logging for troubleshooting:
- Request and response logging for API endpoints
- Error tracking with stack traces
- Performance metrics for database queries
- Machine learning model inference timing

## Future Enhancements

### Planned Features
- Mobile application for iOS and Android platforms
- Advanced threat intelligence integration
- Machine learning model retraining capabilities
- Enhanced reporting and analytics features
- Multi-language support for international users

### Research Opportunities
- Deep learning models for improved detection accuracy
- Behavioral analysis for user interaction patterns
- Real-time threat feed integration
- Automated phishing campaign detection
- Social engineering awareness training modules

## License and Legal

This project is released under the MIT License, allowing for both commercial and non-commercial use with appropriate attribution. Users should be aware that:

- The detection system is provided as-is without warranties
- False positives and negatives may occur
- Users should verify suspicious content through multiple sources
- The platform is intended for educational and research purposes

## Support and Community

### Getting Help
- Review this documentation for common questions
- Check the GitHub issues page for known problems
- Contact the development team for technical support
- Join community discussions and forums

### Contributing
We welcome contributions from the security community:
- Bug reports and feature requests
- Code contributions and improvements
- Documentation updates and translations
- Security research and vulnerability reports

### Acknowledgments
This project builds upon the work of many open-source contributors and security researchers. We acknowledge the datasets, libraries, and tools that make this platform possible, as well as the ongoing efforts of the cybersecurity community to combat phishing attacks.

The development team consists of security professionals, data scientists, and software engineers working together to create effective anti-phishing solutions. Their research in threat intelligence, machine learning, web development, and security testing contributes to the platform's comprehensive approach to phishing detection and prevention.