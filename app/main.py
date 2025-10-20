from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import nn_routes

import json
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