# Smart SIEM
Advanced Single-Node Security Information & Event Management System

## Overview
Smart SIEM is a Python-based Security Information & Event Management (SIEM) system designed to monitor, parse, and detect security events from Linux system logs. It stores alerts in a MySQL database and provides a Flask-based dashboard for real-time visualization and monitoring.

## Features
- Incremental log ingestion with state tracking
- Regex-based structured log parsing
- Rule-based threat detection engine
- Brute-force attack detection
- Root account attack detection
- Alert severity classification (HIGH / CRITICAL)
- MySQL / MariaDB database integration
- Authentication-protected Flask monitoring dashboard
- Automatic port detection and browser launch
- Modular and extensible project structure

## Tech Stack
- Python 3
- Flask
- MySQL / MariaDB
- mysql-connector-python
- python-dotenv
- Chart.js
- Socket Programming

## Requirements
Install dependencies using:

```
pip install -r requirements.txt
```

### requirements.txt
```
Flask
mysql-connector-python
python-dotenv
```

## Quick Start

1. Clone the repository:
```
git clone https://github.com/VoidDefender/smart-siem.git
cd smart-siem
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create the database:
```
CREATE DATABASE siem_db;
```

4. Run the dashboard:
```
python3 dashboard.py
```

The system automatically detects an available port and launches the web dashboard.

## Author
**Sumit Singh Rawat**
