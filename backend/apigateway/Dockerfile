FROM zigzigcheers/keras-fastapi

WORKDIR /root

ADD .aws .aws
ADD api_gateway.py .
ADD handwriting.keras .
ADD index.html .

RUN pip install boto3

EXPOSE 8080
CMD [ "python3","api_gateway.py" ]