# REST API with Clean Architecture

This project is a personal learning project aimed at building a REST API using Python with a clean architecture approach. The technology stack used includes Sanic, PostgreSQL, Redis, and Docker.

## Features

- User authentication and authorization
- CRUD operations for user and posts entities
- JSON Web Token (JWT) based authentication
- PostgreSQL database integration
- Redis caching for improved performance

## Installation

To run this project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/ilhamnyto/sanic-fw.git`
2. Create a Virtual Environment: `virtualenv venv`
3. Activate virtualenv `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy the env files: `cp .env.test .env`.
6. Set up the Server host, port, PostgreSQL database, Redis and configure the connection details in `.env` or `.docker-compose.yaml`.
7. Run the database migrations: `python migrate.py`
8. Start the application: `python run.py` or `docker-compose build && docker-compose up`

## API Documentation

For detailed information on the API endpoints and their usage, refer to the [API Documentation](https://documenter.getpostman.com/view/13820554/2s93eZzBrj).

## Configuration

The project's configuration is stored in the `.env` or `docker-compose.yaml` file. Update this file to adjust the server port, database connection details, Redis configuration, and other settings as needed.


## License

This project is licensed under the [MIT License](./LICENSE).

## Acknowledgments

This project was made possible by the following open-source libraries:

- [Sanic](https://sanic.dev/)
- [PostgreSQL](https://www.postgresql.org)
- [Redis](https://redis.io)
- [Docker](https://www.docker.com/)

