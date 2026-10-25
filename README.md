# Backend Toolkit

A collection of small, dependency-light backend building blocks used across
several projects: rate limiting, realtime connection management, session
lifecycle, task scheduling, structured logging, notifications, reporting,
backups, configuration, encryption and SQLite persistence.

## Modules

| Module | Purpose |
|---|---|
| `rate_limiter.py` | Sliding-window rate limiter, thread-safe |
| `websocket_manager.py` | Realtime connection registry with command/result dispatch |
| `client_manager.py` | Registry of connected clients with heartbeat tracking |
| `session_manager.py` | Session lifecycle with TTL cleanup |
| `task_scheduler.py` | Queue-based task scheduler with delayed execution |
| `command_parser.py` | CLI command parser with registry and descriptions |
| `report_generator.py` | JSON report generation |
| `backup_manager.py` | Zip-based backup, restore and rotation |
| `geo_locator.py` | IP geolocation with multi-service failover |
| `logger.py` | Thread-safe JSON-lines logger with daily rotation |
| `notification_manager.py` | In-memory notification queue with read/unread tracking |
| `config_manager.py` | JSON config loader with dotted-key get/set |
| `encryption_manager.py` | AES-CBC encryption and PBKDF2 password hashing |
| `api.py` | Generic endpoint router with structured responses |
| `database_manager.py` | SQLite manager for clients, jobs and logs |

## Install

pip install -r requirements.txt

## Test

pytest tests/

## Layout

backend-toolkit/
  *.py
  requirements.txt
  README.md
  tests/
    test_rate_limiter.py
    test_session_manager.py
