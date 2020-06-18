# Pollen

![Build and Deploy to GKE](https://github.com/Kapiche/pollen/workflows/Build%20and%20Deploy%20to%20GKE/badge.svg)

> Because Pollen is better than polling

Test project for push using SSE

```
docker build . --rm -t pollen

docker run -p 3000:3000 pollen
```