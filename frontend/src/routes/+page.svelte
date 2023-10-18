<script lang="ts">
    import { blobToBase64 } from "$lib";

    let fileElem: HTMLInputElement;
    let target: string;
    let doing = false;
    let translated: string | null = null;
    let audioSrc = "";

    function doUpload() {
        let files = fileElem.files;
        if (!files || files.length === 0) {
            return;
        }
        doing = true;
        fetch("http://localhost:30080", {
            method: "POST",
            headers: {
                src: "en-US",
                target: target,
            },
            body: files[0],
        })
            .then((res) => {
                console.log(res.status);
                translated = res.headers.get("X-Translated");
                return res.blob();
            })
            .then((b) => blobToBase64(b))
            .then((s) => {
                audioSrc =  s;
            })
            .catch((e) => alert(e));
        // let xhr = new XMLHttpRequest();
        // xhr.onreadystatechange = function () {
        //     if (xhr.readyState !== 4) {
        //         return;
        //     }
        //     doing = false;
        //     if (xhr.status != 200) {
        //         alert(xhr.status + ": " + xhr.responseText);
        //         return;
        //     }
        //     translated = xhr.getResponseHeader("X-Translated");
        //     audioSrc = "data:audio/mp3;base64," + btoa(xhr.response);
        // };
        // xhr.open("POST", "http://localhost:30080");
        // xhr.setRequestHeader("src", "en-US");
        // xhr.setRequestHeader("target", target);
        // xhr.send(files[0]);
    }
</script>

<h1>Digit Reader</h1>

<input type="file" name="file" bind:this={fileElem} />
<select name="target" bind:value={target}>
    <option value="fr-FR">Franch</option>
    <option value="en-US">English</option>
</select>

<button disabled={doing} on:click={doUpload}>Go</button>
{#if translated}
    <div>
        <h1>{translated}</h1>
        <audio src={audioSrc} controls />
    </div>
{/if}
