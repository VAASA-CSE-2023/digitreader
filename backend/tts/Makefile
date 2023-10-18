build:
	cp -r ~/.aws .
	docker build -t zigzigcheers/private_tts:v2 .
	rm -rf .aws
start:
	docker run -d -p 8083:8083 --name private_tts zigzigcheers/private_tts:v2

push:
	docker push zigzigcheers/private_tts:v2
clean:
	docker stop private_tts
	docker container prune
	# docker rmi zigzigcheers/private_tts:v2