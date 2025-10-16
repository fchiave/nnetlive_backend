from fastapi import APIRouter
import numpy as np

router = APIRouter(
    prefix="/nn",
    tags=["NeuralNet"]
)

@router.get("/sum")
def calculate_sum(a: float, b: float):
    arr = np.array([a, b])
    return {"a": a, "b": b, "sum": float(np.sum(arr))}
