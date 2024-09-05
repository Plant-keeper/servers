# Learn about the servers of PlantKeeper

## How to launch locally

## Tehcnical choices

The server architecture of PlantKeeper was designed to manage data flow between the sensors, the embedded system, and
the backend API while ensuring security, reliability, and scalability. Below are the key components and technical
choices we made for this part of the project:

### 1. Docker Compose for Server Setup

We used __Docker Compose__ to simplify the setup and management of our servers. The Docker Compose file defines two
services:

- __PostgreSQL database__: This service creates the database used by our project. Docker Compose handles the creation of
  the PostgreSQL container, but we manually set up the database schema and data seeding.
- __Flask proxy server__: This service is used to bridge the communication between the Arduino (which collects sensor
  data) and the backend API. The Flask server receives the sensor data over HTTP, processes it, and then forwards it to
  the backend API over HTTPS.

Using Docker Compose ensures that both the database and Flask server are isolated in their own containers, making the
system more modular and easier to maintain. It also allows us to replicate the exact setup in different environments (
development, production, etc.) without manual configuration.

### 2. PostgreSQL Database

For the database, we opted for __PostgreSQL__, which is one of the most powerful and reliable open-source relational
databases available.

In our Docker Compose setup, PostgreSQL is automatically created as a container, but we chose not to automate the
creation of the schema or data seeding. This approach allows us to have more flexibility in how we structure the data
during development and gives us control over migrations.

### 3. Flask Proxy Server

We encountered a challenge with the Arduino: it can only make __HTTP__ requests, while our backend only accepts __HTTPS__
requests for security reasons. Unfortunately, the Arduino library we intended to use to support HTTPS connections did
not function as expected, and time constraints did not allow us to fully explore alternative solutions.

To resolve this, we implemented an intermediate Flask server that acts as a proxy:

- The __Arduino__ sends its sensor data to the Flask server via HTTP.
- The __Flask__ server then forwards the data securely to the backend over HTTPS.

This solution allowed us to respect security best practices (using HTTPS) without compromising the Arduino’s
functionality. Although not the cleanest solution, this architecture was the most feasible given our time constraints
and the limitations of the available Arduino libraries.

### 4. Self-Hosted Servers for Production

For the deployed version of __PlantKeeper__, both the PostgreSQL database and the Flask server are self-hosted on a
dedicated server at our HQ. This self-hosting solution was chosen to give us full control over the server environment
and to avoid relying on external cloud providers. This ensures that we can monitor and manage the performance and
security of the servers more directly.

In summary, the server-side architecture of PlantKeeper uses a combination of Docker Compose for easier server
management, PostgreSQL for reliable data handling, and Flask as an intermediary proxy to ensure secure data transmission
from the Arduino to the backend. This architecture ensures a scalable, secure, and modular system that supports the core
functionality of the PlantKeeper project.

## Improvements and future work