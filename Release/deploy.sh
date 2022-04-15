sudo docker load --input rabbitmq.tar.gz
sudo docker load --input assignment_api.tar.gz
sudo docker load --input assignment_worker.tar.gz
sudo docker-compose up -d --no-build