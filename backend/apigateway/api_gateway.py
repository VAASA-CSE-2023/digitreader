from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
import uvicorn
import time
import os
import requests
import urllib.parse

app = FastAPI()

cacheMap = {}
ocrBreaker: float = 0
translatorBreaker: float = 0
ttsBreaker: float = 0


@app.get('/')
async def getHome():
    return FileResponse('index.html')


async def doOCR(req: Request):
    global ocrBreaker
    now = time.time()
    if now - ocrBreaker < 10:
        raise Exception(
            'ocr-service is recovering, please wait for few seconds')

    content = await req.body()
    dst = str(time.time())+'.png'
    fo = open(dst, 'wb')
    fo.write(content)
    fo.close()

    fi = open(dst, 'rb')
    try:
        res = requests.post('http://ocr-service:8081', fi)
        fi.close()
        os.remove(dst)
        return res.text
    except Exception as e:
        ocrBreaker = now
        raise e


def doTranslate(text: str, src: str, target: str):
    global translatorBreaker
    now = time.time()
    if now - translatorBreaker < 10:
        raise Exception(
            'translator-service is recovering, please wait for few seconds')
    try:
        res = requests.post('http://translator-service:8082', data={
            'text': text,
            'sourceLanguageCode': src,
            'targetLanguageCode': target,
        })
        return res.text
    except Exception as e:
        translatorBreaker = now
        raise e


def doTTS(text: str, lang: str):
    global ttsBreaker
    now = time.time()
    if now - ttsBreaker < 10:
        raise Exception(
            'tts-service is recovering, please wait for few seconds')

    if lang == 'fr':
        lang = 'fr-FR'
    elif lang == 'en':
        lang = 'en-US'

    try:
        res = requests.post('http://tts-service:8083', data={
            'text': text,
            'languageCode': lang
        })

        dst = str(time.time())+'.mp3'
        fo = open(dst, 'wb')
        fo.write(res.content)
        fo.close()
        return dst
    except Exception as e:
        ttsBreaker = now
        raise e


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
    global cacheMap
    try:
        text: str = await doOCR(req)
        print(text)
        target = req.headers['target']
        src = req.headers['src']

        # cacheMap
        cacheKey = text+src+target
        if cacheKey in cacheMap:
            v = cacheMap[cacheKey]
            return FileResponse(v['filePath'], 200, {
                'X-Translated': urllib.parse.quote_plus(v['Translated']),
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Expose-Headers': '*'
            })

        translated = text
        if not target.startswith('en'):
            translated = doTranslate(text, src, target)

        filepath: str = doTTS(translated, target)

        # store cache
        cacheMap[cacheKey] = {
            'filePath': filepath,
            'Translated': translated
        }

        return FileResponse(filepath, 200, {
            'X-Translated': urllib.parse.quote_plus(translated),
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Expose-Headers': '*'
        })
    except Exception as e:
        print(e)
        return Response(str(e), 500, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Expose-Headers': '*'
        })

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
