from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import uvicorn
from typing import Annotated
import boto3
from botocore.response import StreamingBody

app = FastAPI()

# https://docs.aws.amazon.com/polly/latest/dg/API_SynthesizeSpeech.html#polly-SynthesizeSpeech-request-LanguageCode


@app.get('/')
async def getHome():
    return FileResponse('index.html')


@app.post('/')
async def textToSpeach(text: Annotated[str, Form()], languageCode: Annotated[str, Form()]):
    t = boto3.client('polly')
    voiceRes = t.describe_voices(
        LanguageCode=languageCode,
    )
    res = t.synthesize_speech(
        Engine=voiceRes['Voices'][0]['SupportedEngines'][0],
        # LanguageCode=languageCode,
        OutputFormat='mp3',
        Text=text,
        VoiceId=voiceRes['Voices'][0]['Id']
    )

    body: StreamingBody = res['AudioStream']
    dst = 'out.mp3'
    fo = open(dst, 'wb')
    fo.write(body.read())
    fo.close()
    body.close()
    return FileResponse(dst, media_type='audio/mp3')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8083)
