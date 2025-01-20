# Tributary
Backend infrastructure for Ford's sensor streaming system. This codebase contains a Flask server which records data to a Redis database, and exposes two endpoints. The /record endpoint is periodically called by embedded sensors within a vehicle to post data to the database. The data is then retrieved by a user facing mobile application using the /collect endpoint.

 * Developed a backend to stream engine temperature sensor readings from cars to mobile phones.
 * Connected a Flask server to a Redis instance using Docker Compose.

# Task
Help Ford create a collection of backend services for a new system the company is developing.

## Project briefing
Ford is starting to work on a new system that seeks to expose drivers to more data from their cars. To this end, a mobile development team is putting together an app that will allow drivers to access live data collected from their cars. This data will be pulled from the physical sensors on each vehicle, so an embedded systems team is building a component to gather these readings. This embedded component needs a backend to stream its data to. Will be building a backend service to act as the glue between the mobile app and the sensors it harvests data from.


- Here are a few useful terms for this program:

- Sensor Streaming System: A technology that captures and transmits real-time data from sensors for monitoring and analysis.
- Flask: A web framework for building servers that expose a clearly defined API to the internet.
- Redis: An open-source, in-memory datastore.
- Docker Container: A standalone, executable package that includes everything needed to run a piece of software, including the code, runtime, libraries, and system tools, ensuring consistent and portable application deployment across different environments.
- Dockerfile: A script that defines the instructions and configuration needed to build a Docker container image, specifying the base image, application code, dependencies, and runtime settings.
- Docker Compose: A tool for defining and running multicontainer Docker applications using a simple YAML configuration file.


### Local development environment:

- The list of three tools:
An integrated development environment (IDE) like PyCharm
A GitHub repository
Docker Desktop

- What to build?
"There's quite a bit of data we'd like to convey to our users, but we're going to start small to ease development. The embedded team is working with engine temperature sensors right now, which means we're working with engine temperature data. Later on, once we've verified that data is making it from one end of the system to the other, we can start working with other information, like vehicle speed, engine RPM, cabin temperature, etc."


- How to build it
Build a Flask server connected to a Redis database. Flask is a web framework for building servers that expose a clearly defined API to the internet, and Redis is an in-memory datastore. Server will expose an API consisting of two endpoints:

A /record endpoint, which will record a new engine temperature reading to the database. The embedded sensors will post new data to this endpoint many times a second, giving the illusion of a continuous stream of data.
A /collect endpoint, which will collect the most current engine temperature from the database and calculate an average. The mobile application will repeatedly post requests to this endpoint to collect up-to-date data.
Configure both the Flask server and the Redis instance to run in Docker containers, and use Docker Compose to stitch them together. Docker is a technology that allows you to run your code in containers, which act as precisely configured sandboxes for your applications.

- Docker
Docker is a tool that allows you to bundle your applications into containers. A container functions as a self-contained virtual computer; it has its own operating system, installed software, etc. Containers help eliminate problems that arise from assumptions about the computer executing a given piece of code. For example, if an application depends on a certain version of a library, then it might run correctly on your machine (with the expected version of the library installed) but fail on a friend's machine (with a different version of the library installed). Docker containers eliminate this problem by encapsulating an entire operating system. Rather than running directly on your computer, a containerized application runs on a virtual operating system within your computer.


# Scaffold a server:
- Create a container for Flask application.
- Scaffold a Flask server.

Docker down-low
Docker allows you to package your applications in tiny packages called containers. These containers each run their own operating system, which functions independently of the host OS. A Docker host is a computer running Docker Desktop. In this case, the Docker host is your personal computer. A Docker host manages a fleet of Docker containers and can instantaneously spin them up and shut them down. Most backend infrastructure nowadays runs in a container on a Docker host in the cloud.

A Docker container is constructed from a recipe called a Dockerfile. A Dockerfile contains step-by-step instructions for preparing a container to run your application. When you execute the command docker build -t <image-name> <path/to/Dockerfile> in a shell, the Docker engine parses your Dockerfile and uses the instructions to assemble a container image. Then, you can execute docker run <image-name> to create a container from your image. If you are of an object-oriented inclination, you may have noticed a similarity here: docker images behave like classes, and docker containers behave like instances of those classes. From a single image, you can create many containers.

Docker build creates an image from a Dockerfile, and docker run creates a container from an image. 

    -Using a RUN keyword instead of CMD. Both execute software within the container, but a RUN keyword indicates that the command should execute while the image is being built, whereas a CMD keyword indicates that the command should wait until the container is initialized to execute. Dockerfiles often contain many RUN lines, which prepare an image by installing dependencies and the like, but only a single CMD line at the very end, which starts your application.


Dependencies Defined:

gunicorn==21.2.0:
- "gunicorn" is a Python web server that can run web applications written in Flask, Django, and other frameworks.
"21.2.0" is the specific version of gunicorn that your project requires. The "==21.2.0" means that your project is compatible with this exact version.
Flask==3.0.0:
- "Flask" is a lightweight web framework for building web applications in Python.
"3.0.0" is the specific version of Flask that your project requires.
loguru==0.7.2:
- "loguru" is a Python logging library that simplifies logging in your application.
"0.7.2" is the specific version of loguru that your project requires.
requests==2.31.0:
- "requests" is a Python library for making HTTP requests to web services or APIs.
"2.31.0" is the specific version of the "requests" library that your project requires.
redis==5.0.1:
- "redis" is a Python client library for interacting with Redis, which is an in-memory data store.
"5.0.1" is the specific version of the "redis" library that your project requires.


- modify the CMD line at the end of the file. Change it to CMD exec gunicorn entrypoint:app.
This line starts up your Flask application using Gunicorn, which basically acts as the glue between your Python code and the container's underlying networking infrastructure.



# Container composition:

Making multiple containers connect with a database.

- Create a docker-compose.yml file to manage containers.
- Connect Flask application to a Redis database

Need some kind of database to stash engine temperature readings getting streamed to you server？ That sounds like the perfect opportunity for a Redis instance. They're really quick! The data they keep track of doesn't even make it to disk most of the time; it just flits around the main memory. Granted, they're known for falling over from time to time. But not very often, That's the tradeoff; Redis is way faster than a relational database, but not nearly as robust.”

“In this case, Redis is perfect. If you lose an engine temperature reading, it's no big deal; there'll be another one in a quarter second. The same cannot be said of credit card data. They really don't like it when you lose that. So, the extra speed and ease of use that Redis nets us is well worth it. Let's get you set up."

- Docker Compose
Docker Compose is a tool used to manage a fleet of containers. A docker-compose.yml file outlines which containers should run and how they should be configured. Given a properly formatted compose file, Docker Compose will interact with the Docker engine on your behalf, creating the containers you specify and networking them together. Since the system we are developing consists of two containers, a Flask server and a Redis instance, we can use Docker Compose to spin them up and shut them down together as a single unit.


Running Redis
Redis is an in-memory datastore and one of the lightest-weight databases around. It excels in situations where speed and ease of use are prized over robust data guarantees. Redis is, at its heart, a key-value store. You can store and retrieve values (which can be strings, lists, hashes, etc.) using their corresponding key.

As it turns out, Redis is also very easy to set up on your machine if you have Docker installed.


Create a file named docker-compose.yml:
At the top, we have a file format version indicator, which Docker Compose uses to parse the file.
After that, we have a services definition, which contains the tributary and redis services. Containers are articulated as services in Docker Compose. A service instantiates one or more replica containers of a single image.
Next comes a build tag, which indicates that the tributary image should be built locally using a Dockerfile at the specified path.
The Redis service has an image tag instead of a build tag. Docker will search its local image cache for a matching name before pulling the image from Dockerhub.
Finally, both containers have a ports definition.
These specify that the Docker engine should bind the host port on the left to the container port on the right. Doing so establishes a communication channel that the two can use to talk back and forth.
When a container is created, it is completely cut off from the outside world by default. To enable network traffic to and from a container, you must define which ports you'd like exposed to your host machine.
Our Flask server listens for incoming POST requests on port 8000, so we bind that to port 8000 on the host machine. Any network traffic directed to port 8000 on the host machine is transparently forwarded to port 8000 on the container, where your Flask server can interact with it.

# Connecting the two
Prove that these two services can interact.

Lets talk about entrypoint.py:
    - When a request hits the /record endpoint, get_json() extracts the JSON payload from the request.
    - Then, we open up a connection to the Redis database, which is running in a different container.
    - We are storing engine temperature readings in a Redis list, keeping track of the 10 most recent values, and discarding old ones as new ones appear.
    - The methods used to implement the above behavior are discussed here: https://redis.io/docs/data-types/lists.
- Restart Docker Compose stack, and ensure both services produce logs similar to last time.
- Submit a POST request to your flask server at http://0.0.0.0:8000/record, and include a JSON payload with the following data: {"engine_temperature": 0.3}.
    - There are a variety of ways to accomplish this, three of which are described below:
        - Use the Python requests library in a scratch file like so: 
            - response = requests.post("http://0.0.0.0:8000/record", json={"engine_temperature": 0.3}).
        - Use a tool like Postman, found here: https://www.postman.com/.
        - Use Curl from your shell, like so: https://reqbin.com/req/c-dwjszac0/curl-post-json-example.
- If everything works as expected, you should receive a {"success":true} response payload and a 200 status code.
    - Additionally, there should be some new logs in your console with each new request.
- When you are finished, commit and push your changes to your project GitHub repo and submit a link below.

# Additional endpoints:
- Implement an endpoint in a Flask application.
- Aggregate data from a Redis instance.


- Putting it all together
Implement the /record endpoint so that it returns a dictionary containing:
A current_engine_temperature value from the most recent engine temperature reading in the database.
An average_engine_temperature value from the mean engine temperature derived from data in the database.
Verify that both the /collect and /record endpoints work as expected.

