run:
	cp -r ~/.aws .
	docker build -t zigzigcheers/private_translator:v2 .
	rm -rf .aws
start:
	docker run -d -p 8082:8082 --name private_translator zigzigcheers/private_translator:v2

push:
	docker push zigzigcheers/private_translator:v2

clean:
	docker stop private_translator
	docker container prune
	# docker rmi zigzigcheers/private_translator:v2