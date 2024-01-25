Simple FastAPI project to demonstrate the tracing using Opentelemetry and Jaeger.\
To run simply do:\
`docker compose -f docker-compose.yml up -d --build`\

To access the FastAPI app go to: \
`http://localhost:8000/docs` \
And play with endpoints

To access the Jaeger UI go to: \
`http://localhost:16686/` \
And you'll be able to see the app traces. \

For info on setup check the `docker-compose.yml`
