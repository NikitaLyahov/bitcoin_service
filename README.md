# Bitcoin service

This is a microservice built on the [FastAPI](https://github.com/tiangolo/fastapi) and [MongoDB](https://github.com/mongodb/mongo). Docker-compose and Makefile are added for ease of deployment.

To run the server up:
```bash
make run
```

To run the server up as daemon:
```bash
make run-daemon
```

To stop the server:
```bash
make stop
```

To get inside the container:
```bash
make shell
```

To check code by flake8:
```bash
make flake
```
