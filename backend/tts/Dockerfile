FROM zigzigcheers/aws-fastapi

WORKDIR /root

ADD tts.py .
ADD .aws .aws
ADD index.html .

EXPOSE 8083

CMD [ "python3","./tts.py" ]
