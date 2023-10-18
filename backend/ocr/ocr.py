from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import uvicorn
import time
from keras import models
from PIL import Image
import numpy
import os

model = models.load_model('handwriting.keras')

app = FastAPI()


def most_common(lst):
    flatList = [el for sublist in lst for el in sublist]
    return max(flatList, key=flatList.count)


def handleImage(src):
    pic = numpy.asarray(Image.open(src).convert('L').resize((28, 28)))
    pic = numpy.array(pic, copy=True)
    bg = most_common(pic)
    for i, row in enumerate(pic):
        for j, v in enumerate(row):
            if v == bg:
                pic[i][j] = 0
            else:
                pic[i][j] = 255
    return pic


@app.get('/')
async def getHome():
    return FileResponse('index.html')


async def readImage(req: Request):
    content = await req.body()
    dst = str(time.time())+'.png'
    fo = open(dst, 'wb')
    fo.write(content)
    fo.close()

    pic = handleImage(dst)

    img = numpy.asarray(pic, float)
    img = numpy.expand_dims(img, axis=0)
    img = (img/255)-0.5
    img = numpy.expand_dims(img, axis=3)

    predictions = model.predict(img)
    labels = numpy.argmax(predictions)

    os.remove(dst)
    return toPlainTextDigit(str(labels))


def toPlainTextDigit(s: str):
    m = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'one',
    }
    return m[s]


@app.post('/')
async def doHandle(req: Request):
    text: str = await readImage(req)
    return Response(text)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8081)
