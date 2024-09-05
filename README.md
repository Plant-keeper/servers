# Learn about the servers of PlantKeeper

## Original Contributors
Rafael Dousse, Eva Ray, Quentin Surdez and Rachel Tranchida

## Running the Server Locally with Docker

To run the server locally, you'll need Docker installed on your machine. If Docker isn’t installed yet, you can download and install it by following these links:

  - [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - [Docker Engine](https://docs.docker.com/engine/install/) (for servers without a GUI)

### Configuration Before Running the Server

__1. Update the Listener Script:__ You’ll need to modify the `listener.py` file to match your server setup. This involves specifying the backend address and potentially updating the IP or URL that the server communicates with. Open `listener.py` and adjust:

```python
  backend_url = "http://your-backend-address/api/v1/sensors/"
```
Replace `"your-backend-address"` with the actual IP address or domain name of your backend.

__2. Update the Database Configuration:__ If you're connecting the backend to a database, ensure the credentials in your docker-compose file match your database setup. You’ll need to update the following variables in the `docker-compose.yml`:

```yaml
  environment:
    - POSTGRES_USER=your_db_user
    - POSTGRES_PASSWORD=your_db_password
    - POSTGRES_DB=your_db_name
```
Replace your_db_user, your_db_password, and your_db_name with your database credentials.

__*Port Forwarding (For Home Servers):*__ If you’re hosting this server on a local machine and want external access, you'll need to configure port forwarding on your router:
    Forward port 8080 (or the port you define) to the internal IP address of the server.
    Ensure your firewall allows inbound traffic on the forwarded port.

*Example:* If your server's internal IP is 192.168.1.100, you’ll forward port 8080 to 192.168.1.100:8080 from your router's configuration.
> **_Note_**: If you’re running the database in a Docker container on a home server and using port forwarding, you may also need to enter the database container and accept communications on 0.0.0.0 by editing the `pg_hba.conf` file either with `nano/vim` or by using `echo`. This allows external access to the database:
```bash
 # Line to be added 
  host    all             all             0.0.0.0/0               md5
```
### Running the Server with Docker

__1. Navigate to the Project Directory:__ Open your terminal and move to the root of the project

__2. Build and Run the Docker Containers:__ To build and run the server, use the following command: `docker-compose up --build`

__3. Access the Server:__ Once the Docker containers are running:

- You can access the __PostgreSQL__ database at `localhost:5432` or by using your server’s IP address like this: `your-server-ip:5432`.
- The __Flask__ server will be accessible at `localhost:8080` or `your-server-ip:8080`. Ensure you use the correct route. For example: http://your-server-ip:8080/sensor-data.

__4. Arduino Setup:__ This project is designed to be used with an Arduino. You can find the __Arduino__ code in the [iot folder](https://github.com/Plant-keeper/iot). Follow the steps in the __Arduino__ documentation to set up the board and configure the code to work with your home server or local IP address.

__5. Local Network Access:__
If your __Arduino__ is connected to the same network as the server, you can access the Flask server using the server's local IP address. To find the local IP address, use the following command to view the Docker logs: `docker logs -f <flask-app-container-name>`.

Look for the IP address in the logs and use that to access the Flask server locally.

### Additional Steps for Database

If the database has not yet been seeded, please refer to the [backend documentation](https://github.com/Plant-keeper/backend). It provides the necessary routes to initialize the database and populate it with dummy data if required


## Technical choices

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