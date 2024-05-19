import torch.nn as nn

# xác định kiến trúc mạng neural
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) #lớp đầu tiên của mạng thực hiện biến đổi tuyến tính
        self.l2 = nn.Linear(hidden_size, hidden_size) # lớp ẩn, học các biểu diễn phức tạp hơn từ dữ liệu đầu vào
        self.l3 = nn.Linear(hidden_size, num_classes) # lớp đầu ra, số lượng đầu ra bằng num_classes
        self.relu = nn.ReLU() #Hàm kích hoạt ReLU được sử dụng sau mỗi lớp tuyến tính để tạo tính phi tuyến tính trong mạng
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # không có hàm kích hoạt hoặc softmax ở cuối
        return out
