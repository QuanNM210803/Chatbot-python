import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import API_bard
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# lấy dữ liệu từ data.path
FILE = "data.pth"
data = torch.load(FILE)

model_state = data["model_state"]
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()  # đặt mô hình vào chế độ đánh giá

bot_name ="Botdeptrai"

# lấy phản hồi
def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    # chỉnh lại kích thước của X
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    # dự đoán đầu ra dựa trên đầu vào X
    output = model(X)
    # tìm ra tag dự đoán có xác suất cao nhất 
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # tính phân phối xác suất các lớp
    probs = torch.softmax(output, dim=1)
    # lấy xác suất của mã được dự đoán
    prob = probs[0][predicted.item()]
    # nếu xác suất lớn hơn 0.85
    if prob.item() > 0.85:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    return API_bard.get_resp(msg)
