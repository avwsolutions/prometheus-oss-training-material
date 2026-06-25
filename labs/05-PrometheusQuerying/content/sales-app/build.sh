#build and run for experimentation
docker build --no-cache -t demo-sales-app:1.0 .
docker run -p 8000:8000 demo-sales-app:1.0