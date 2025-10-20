from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

import numpy as np
import json

router = APIRouter(
    prefix="/nn",
    tags=["NeuralNet"]
)

# Load model once at import time
model = np.load("app/model.npz")

def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    x = np.clip(x, -500, 500)  # avoid overflow in exp
    return 1 / (1 + np.exp(-x))


def forward_pass(a0, W1, b1, W2, b2):
    # use relu to get activation values of first layer - shape [batch_size, m]
    z1 = a0 @ W1 + b1
    a1 = relu(z1)

    # use sigmoid to get classification focused activation values of final layer - shape [batch_size, p]
    z2 = a1 @ W2 + b2
    a2 = sigmoid(z2)

    return z1, a1, z2, a2

async def run_prediction(data):
    # Run model prediction (example)
    _, _, _, result = forward_pass(data, model["W1"], model["b1"], model["W2"], model["b2"])
    result = result[0]
    top_indices = np.argsort(result)[-3:][::-1]  # indices of 3 highest probabilities
    # Convert to nested JSON format
    predictions = {
        "p1": {"label": str(top_indices[0]), "confidence": result[top_indices[0]]},
        "p2": {"label": str(top_indices[1]), "confidence": result[top_indices[1]]},
        "p3": {"label": str(top_indices[2]), "confidence": result[top_indices[2]]},
    }
    return predictions


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the connection
    await websocket.accept()
    print("Client connected")
    try:
        # Keep the connection open to receive/send messages
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)
            print(f"Received message from client: {data}")
            predictions = await run_prediction(data["pixels"])
            await websocket.send_text(json.dumps(predictions))
    except WebSocketDisconnect:
        print("Client disconnected")