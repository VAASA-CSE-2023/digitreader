run:
	python3 api_gateway.py
build:
	docker build -t zigzigcheers/private_api_gateway:v4 .
start:
	docker run -d -p 8084:8080 --name private_api_gateway zigzigcheers/private_api_gateway:v4

push:
	docker push zigzigcheers/private_api_gateway:v4

clean:
	docker stop private_api_gateway
	docker container prune
	docker rmi zigzigcheers/private_api_gateway:v4