<script lang="ts">
    import { onMount } from "svelte";

    let canvas: HTMLCanvasElement;
    let fileElem: HTMLInputElement;
    let target: string;
    let doing = false;
    let translated: string | null = null;
    let audioSrc = "";
    let ctx: CanvasRenderingContext2D | null = null;

    //canvas
    let prevX = 0,
        prevY = 0,
        currX = 0,
        currY = 0,
        mouseOnBoard = false;
    function onDraw(action: string, e: MouseEvent) {
        if (!ctx) {
            ctx = canvas.getContext("2d");
        }

        if (action === "down") {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
            mouseOnBoard = true;

            ctx!.beginPath();
            ctx!.fillStyle = "grey";
            ctx!.fillRect(currX, currY, 8, 8);
            ctx!.closePath();
        }

        if (action === "out" || action === "up") {
            mouseOnBoard = false;
        }
        if (action === "move" && mouseOnBoard) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;

            ctx!.beginPath();
            ctx!.moveTo(prevX, prevY);
            ctx!.lineTo(currX, currY);
            ctx!.strokeStyle = "grey";
            ctx!.lineWidth = 16;
            ctx!.lineCap = 'round';
            ctx!.stroke();
            ctx!.closePath();
        }
    }

    function uploadFile(file: Blob | File) {
        doing = true;
        let xhr = new XMLHttpRequest();
        xhr.responseType = "blob";
        xhr.onreadystatechange = async function () {
            if (xhr.readyState !== 4) {
                return;
            }
            doing = false;
            if (xhr.status !== 200) {
                alert(xhr.responseText);
                return;
            }

            translated = decodeURIComponent(
                xhr.getResponseHeader("X-Translated")!
            );
            audioSrc = URL.createObjectURL(xhr.response);
        };
        xhr.open("POST", "http://digitrecognizer.asuscomm.com:30080");
        xhr.setRequestHeader("src", "en-US");
        xhr.setRequestHeader("target", target);
        xhr.send(file);
    }
    function doUpload() {
        let files = fileElem.files;
        if (!files || files.length === 0) {
            if (!ctx) {
                return;
            }
            canvas.toBlob(
                (b) => {
                    if (!b) return;
                    uploadFile(b);
                },
                "image/png",
                0.7
            );
            return;
        }
        uploadFile(files[0]);
    }

    onMount(() => {
        window.addEventListener("keyup", (e) => {
            if (e.code === "Escape" && canvas) {
                canvas
                    .getContext("2d")
                    ?.clearRect(0, 0, canvas.width, canvas.height);
            }
        });
    });
</script>

<h1>Digit Reader</h1>
<div>
    <button
        on:click={() =>
            canvas
                .getContext("2d")
                ?.clearRect(0, 0, canvas.width, canvas.height)}>clear</button
    >
    <button
        on:click={() => {
            let s = canvas.toDataURL("image/png", 0.7);
            const createEl = document.createElement("a");
            createEl.href = s;

            // This is the name of our downloaded file
            createEl.download = "download-this-canvas";

            // Click the download button, causing a download, and then remove it
            createEl.click();
            createEl.remove();
        }}>save</button
    >
</div>
<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<div>
    <canvas
        bind:this={canvas}
        width="200"
        height="200"
        on:mousemove={(e) => onDraw("move", e)}
        on:mousedown={(e) => onDraw("down", e)}
        on:mouseup={(e) => onDraw("up", e)}
        on:mouseout={(e) => onDraw("out", e)}
    />
</div>
<input type="file" name="file" bind:this={fileElem} />
<select name="target" bind:value={target}>
    <option value="fr-FR">Franch</option>
    <option value="en-US">English</option>
    <option value="es-ES">Spainish</option>
    <option value="ja-JP" >Japanese</option>
    <option value="de-DE">German</option>
    <option value="ru-RU" selected>Russian</option>
</select>

<button disabled={doing} on:click={doUpload}>Go</button>
{#if translated}
    <div>
        <h1>{translated}</h1>
        <audio src={audioSrc} controls />
    </div>
{/if}

<style>
    canvas {
        border: 1px solid black;
    }
</style>
