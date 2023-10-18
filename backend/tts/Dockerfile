FROM zigzigcheers/aws-fastapi

WORKDIR /root

ADD tts.py .
ADD .aws .aws

EXPOSE 8083

CMD [ "python3","./tts.py" ]
