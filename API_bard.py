
"""lấy api_bard, lên trang chủ chính thức của bard -> f12 -> application -> Secure-1PSID copy mã. Mã reset sau khoang 15p"""
"""lấy lại mã: ấn clear all cookies rồi đăng nhập lại"""
from bardapi import Bard
import os
os.environ["_BARD_API_KEY"]="cAhWjpi7yk8FhZHju0I9kN8JUI7LZyo6MIrHD3QmC44BvHro5HVgUpgxSuMi6qo_HmrytQ."
def get_resp(message):
    try:
        resp=Bard().get_answer(message)["content"]
        return resp
    except Exception:
        return "I don't understand..."