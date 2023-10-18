FROM zigzigcheers/keras-fastapi

WORKDIR /root

ADD ocr.py .
ADD handwriting.keras .
ADD index.html .

EXPOSE 8081
CMD [ "python3","ocr.py" ]