from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import uvicorn
import time
import os
import requests

app = FastAPI()


@app.get('/')
async def getHome():
    return FileResponse('index.html')


async def readImage(req: Request):
    content = await req.body()
    dst = str(time.time())+'.png'
    fo = open(dst, 'wb')
    fo.write(content)
    fo.close()

    fi = open(dst, 'rb')
    res = requests.post('http://ocr-service:8081', fi)
    fi.close()
    os.remove(dst)
    return res.text


def doTranslate(text: str, src: str, target: str):
    res = requests.post('http://translator-service:8082', data={
        'text': text,
        'sourceLanguageCode': src,
        'targetLanguageCode': target,
    })
    return res.text


def doSpeaker(text: str, lang: str):
    if lang == 'fr':
        lang = 'fr-FR'
    elif lang == 'en':
        lang = 'en-US'

    res = requests.post('http://tts-service:8083', data={
        'text': text,
        'languageCode': lang
    })

    dst = str(time.time())+'.mp3'
    fo = open(dst, 'wb')
    fo.write(res.content)
    fo.close()
    return dst


corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Expose-Headers': '*'
}


@app.get('/')
async def getHome():
    return Response('index.html', 200, corsHeaders)


@app.options('/')
async def doHeader():
    return Response(None, 200, corsHeaders)


@app.post('/')
async def doHandle(req: Request):
    text: str = await readImage(req)
    print(text)
    target = req.headers['target']
    src = req.headers['src']
    translated: str = doTranslate(text, src, target)
    filepath: str = doSpeaker(translated, target)
    return FileResponse(filepath, 200, {
        'X-Translated': translated,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Expose-Headers': '*'
    })

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
