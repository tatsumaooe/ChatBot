
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Selected device:", device)

x = torch.randn(3, 3, device=device)
y = torch.randn(3, 3, device=device)

print("Tensor calculation:")
print(x @ y)
