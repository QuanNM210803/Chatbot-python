import numpy as np
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)
all_words = []
tags = []   # chứa tất cả các tags
xy = []     # chứa tuple lưu các pattern và tag của các pattern
# duyệt intents
for intent in intents['intents']:
    # thêm các tag vào danh sách tags
    tag = intent['tag']
    tags.append(tag)
    # duyệt từng patterns
    for pattern in intent['patterns']:
        # tách 
        w = tokenize(pattern)
        # thêm các từ vừa tách vào danh sách tất cả các từ
        all_words.extend(w)
        xy.append((w, tag))

# stem các từ trong all_words
ignore_words = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_words]

# loại từ trùng nhau và sắp xếp
all_words = sorted(set(all_words))
tags = sorted(set(tags))

"""print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)"""

# tạo dữ liệu training
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: chứa kết quả trả về của bag_of_words của từng pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: chứa vị trí của từng tag trong mảng tags
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# tham số 
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
print(input_size, output_size)

class ChatDataset(Dataset):
    def __init__(self):
        # n_samples lưu số câu trong patterns
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # trả về dữ liệu theo index
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
"""đào tạo mô hình máy học bằng dữ liệu từ dataset, batch_size là kích thước mỗi batch dữ liệu, 
shuffle=True dữ liệu sẽ được xáo trộn trước khi được chia thành các batch"""
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

# chọn thiết bị mục tiêu cho việc đào tạo mô hình và di chuyển NeuralNet tới thiết bị đã chọn
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# tính toán sự mất mát giữa các dự đoán của mô hình và các nhãn thực tế, quá trình stemming có thể gây mất mát thông tin
criterion = nn.CrossEntropyLoss() 
# cập nhật các trọng số của mô hình để giảm thiểu hàm mất mát dùng thuật toán tối ưu hóa Adam
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        #chuyển dữ liệu lên thiêt bị device
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        #tính toán dự đoán của mô hình
        outputs = model(words)
        # tính giá trị mất mát giữa dự đoán outputs và nhãn đúng labels
        loss = criterion(outputs, labels)
        
        # lùi và tối ưu
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()     
    if (epoch+1)%100==0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# state_dict là trạng thái mô hình sau khi đào tạo, chứa thông tin về trọng số và bias, có thể tái nạp mô hình về sau
data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)
print(f'training complete. file saved to {FILE}')
