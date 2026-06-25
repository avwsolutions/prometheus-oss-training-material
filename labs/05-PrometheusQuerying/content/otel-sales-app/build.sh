#build and run for experimentation
docker build --no-cache -t otel-sales-app:1.0 .
docker run -p 8080:8080 otel-sales-app:1.0