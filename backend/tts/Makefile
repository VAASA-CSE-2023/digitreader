run:
	cp -r ~/.aws .
	docker build -t zigzigcheers/private_tts:v1 .
	rm -rf .aws
start:
	docker run -d -p 8080:8080 --name private_tts zigzigcheers/private_tts:v1

push:
	docker push zigzigcheers/private_tts:v1
clean:
	docker stop private_tts
	docker container prune
	# docker rmi zigzigcheers/private_tts:v1