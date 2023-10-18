export function blobToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve, _) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result as string);
        reader.readAsDataURL(blob);
    });
}

// export function responseToBlob(res:any):string{
//     var uInt8Array = new Uint8Array(res);
   
//     var base64 = window.btoa(data);
//     return base64
// }