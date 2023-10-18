run:
	python3 ocr.py
build:
	docker build -t zigzigcheers/ocr:v2 .

start:
	docker run -d -p 8081:8081 --name ocr zigzigcheers/ocr:v2

push:
	docker push zigzigcheers/ocr:v2

clean:
	docker stop ocr
	docker container prune
	docker rmi zigzigcheers/ocr:v2