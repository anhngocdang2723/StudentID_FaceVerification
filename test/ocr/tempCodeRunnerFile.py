import torch

# Kiểm tra xem GPU có sẵn và có thể sử dụng không
if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. Using CPU.")

print(torch.cuda.is_available())  # Kỳ vọng: True
print(torch.version.cuda)         # Kỳ vọng: 12.4
