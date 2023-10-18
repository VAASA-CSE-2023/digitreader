FROM zigzigcheers/fastapi

WORKDIR /root

ADD api_gateway.py .
ADD index.html .

RUN pip install requests

EXPOSE 8080
CMD [ "python3","api_gateway.py" ]