# Redis Basic Project

## Overview
This project implements various Redis-based caching and storage solutions in Python. It demonstrates the use of Redis for data caching, method call tracking, and web content caching with expiration.

## Project Structure
- `exercise.py`: Main Redis cache implementation with decorators for tracking method calls
- `web.py`: Web cache implementation with URL tracking and content expiration

## Features

### Main Cache Implementation (exercise.py)
1. Basic Redis Operations
   - Storing string data with random keys
   - Type conversion for data retrieval
   - Support for various data types (str, bytes, int, float)

2. Method Call Tracking
   - Decorator to count method calls
   - Input and output history tracking
   - Call history replay functionality

### Web Cache Implementation (web.py)
1. URL Content Caching
   - Caches web page content for 10 seconds
   - Tracks number of URL access attempts
   - Implements efficient caching strategy

## Requirements
- Python 3.7
- Redis server (Ubuntu 18.04)
- `requests` library for web content fetching
- `redis-py` library for Redis operations

## Setup
```bash
# Install Redis
sudo apt-get -y install redis-server

# Install Python dependencies
pip3 install redis
pip3 install requests

# Configure Redis
sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
```

## Testing
For testing the web cache implementation, you can use:
```python
url = "http://slowwly.robertomurray.co.uk"
page_content = get_page(url)
```

The cache will store the content for 10 seconds, and you can verify the count of URL accesses in Redis using the key pattern "count:{url}".

## Author
Victor paul

## Licence
This is part of Alx short back end SE specialization
