from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from typing import Annotated
import uvicorn
import boto3

app = FastAPI()
# https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html

@app.get('/')
async def getHome():
    return FileResponse('index.html')
@app.post('/')
async def translateHandler(text: Annotated[str, Form()], sourceLanguageCode: Annotated[str, Form()], targetLanguageCode: Annotated[str, Form()]):
    t = boto3.client('translate')
    return t.translate_text(
        Text=text,
        SourceLanguageCode=sourceLanguageCode,
        TargetLanguageCode=targetLanguageCode,
    )['TranslatedText']
    # print(s['TranslatedText'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8082)
