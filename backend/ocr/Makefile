run:
	python3 ocr.py
build:
	docker build -t zigzigcheers/ocr:v3 .

start:
	docker run -d -p 8081:8081 --name ocr zigzigcheers/ocr:v3

push:
	docker push zigzigcheers/ocr:v3

clean:
	docker stop ocr
	docker container prune
	docker rmi zigzigcheers/ocr:v3