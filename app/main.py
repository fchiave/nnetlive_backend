from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from app.routers import nn_routes

app = FastAPI(
    title="NeuralNetLive Drawing",
    description="A project that hosts live model prediction based on user-drawn images",
    version="1.0.0"
)

# Register your routes
app.include_router(nn_routes.router)

# Simple test UI for the websocket
html = """
<!DOCTYPE html>
<html>
    <body>
        <h1>WebSocket Example for NeuralNetLive Drawing</h1>
        <input id="msgInput" type="text" placeholder="Type a message"/>
        <button onclick="sendMessage()">Send</button>
        <ul id="messages"></ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var item = document.createElement('li');
                item.textContent = event.data;
                messages.appendChild(item);
            };
            function sendMessage() {
                var input = document.getElementById("msgInput");
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the connection
    await websocket.accept()
    print("Client connected")
    try:
        # Keep the connection open to receive/send messages
        while True:
            data = await websocket.receive_text()
            print(f"Received message from client: {data}")
            await websocket.send_text(f"Server received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")