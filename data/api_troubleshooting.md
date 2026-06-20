# API Troubleshooting Guide
If you are receiving a 401 Unauthorized block, ensure your Bearer token auth is configured correctly.
Header parameters required:
- Authorization: Bearer <your_api_key>
- Content-Type: application/json
Internal errors (500) related to database integrations usually mean the connection string has timed out. Please check your DB connection pool settings.
