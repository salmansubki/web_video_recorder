from fastapi import FastAPI, WebSocket, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
import uvicorn
import base64
import time

app = FastAPI()
html_file_path = "main_websocket.html"

with open(html_file_path, "r") as html_file:
    html = html_file.read()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def video_feed(websocket: WebSocket):
    await websocket.accept()
    print("something")

    while True:
        try:
            data = await websocket.receive_text()  # receive base64 text
            # print(data)
            print("video received")


            # save as base64 text . txt
            filename_txt = f"videoBase64_{int(time.time())}.txt"
            with open(filename_txt, "wb") as b64_txt:
                base64_txt = data.encode()
                b64_txt.write(base64_txt)
            b64_txt.close()

            # save as video webm
            filename = f"video_{int(time.time())}.webm"
            with open(filename, "wb") as vid:
                # fh = open("video.mp4", "wb")
                vid.write(base64.b64decode(base64_txt))
            vid.close()

        except WebSocketDisconnect:
            break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break
        
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)