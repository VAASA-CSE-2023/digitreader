FROM zigzigcheers/aws-fastapi

WORKDIR /root

ADD translator.py .
ADD index.html .
ADD .aws .aws

EXPOSE 8082

CMD [ "python3","./translator.py" ]