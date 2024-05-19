from flask import Flask, render_template, request, jsonify
from chat import get_response
# import translator

app=Flask(__name__)
@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")   #xử lý các yêu cầu post
def predict():
    text=request.get_json().get("message")  #lấy dữ liệu json gửi đến từ yc post, lấy giá trị biến 'message'
    response=get_response(text)
    message={"answer": response}
    return jsonify(message) #trả về đối tượng dạng json

if __name__=="__main__":
    app.run(debug=True)