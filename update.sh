az login
docker build -t lezacontainerregistery.azurecr.io/leza-award-backend-api:latest .
docker login lezacontainerregistery.azurecr.io
docker push lezacontainerregistery.azurecr.io/leza-award-backend-api:latest