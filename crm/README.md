# CRM Celery Setup

This project uses **Celery + Celery Beat** to schedule background tasks.

## Setup Instructions

### 1. Install Redis
Ensure Redis is running locally:
```bash
sudo apt install redis-server
sudo systemctl enable redis
sudo systemctl start redis
