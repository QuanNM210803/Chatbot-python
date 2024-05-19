import numpy as np
import nltk
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
"""tạo ra đối tượng PorterStemmer nhằm thực hiện quá trình stemming"""
stemmer = PorterStemmer()

def tokenize(sentence):
    """
    chia câu thành mảng từ/mã thông báo
    mã thông báo có thể là một từ, ký tự dấu chấm câu hoặc số
    """
    return nltk.word_tokenize(sentence)


def stem(word):
    """
    stemming = tìm root của từ
    ví dụ:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    trả về mảng các túi từ:
    1 nếu từ có trong câu, 0 thì ngược lại
    ví dụ:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bag   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem mỗi từ trong câu tokenized_sentence
    sentence_words = [stem(word) for word in tokenized_sentence]
    # tạo mảng bag bằng 0 có kích thước len(words)
    bag = np.zeros(len(words), dtype=np.float32)
    # enumrate trả về vị trí và giá trị từ đang xét
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx]=1
    return bag