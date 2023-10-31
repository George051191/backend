# Backend code for the project

## Documentation
Will be added soon™

## Installation
1. Clone the repository
2. Run docker-compose up
Migrations will be run automatically on startup.

## Future plans
- [ ] Add documentation
- [ ] Add tests
- [ ] Add CI/CD
- [ ] Add more features
- [ ] 0 downtime deployments with docker swarm

## Project structure
```
.
├── src                    # Source files
│   ├── services           # All services
│   │   ├── login          # Authentication service
│   │   ├── users          # Users service
│   │   └── ...            # Other services in the future
│   ├── database           # Database related files
│   ├── utils              # Utility functions
│   ├── __main__.py        # FastAPI app
│   └── settings.py        # Configuration file
├── alembic                # Alembic migrations
```
