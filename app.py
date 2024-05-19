from tkinter import *
from chat import get_response, bot_name
from datetime import datetime
from tkinter import scrolledtext
# import translator
BG_FRAME = "#999999"
BG_HEADER="#99FFFF"
BG_CONTENT = "#DDDDDD"
BG_MESSAGE="#CCCCCC"
BG_BUTTON="#FFCCFF"
BG_QUESTION="#4cc2a4"
TEXT_COLOR = "#111111"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication: 
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        # vòng lặp vô hạn xử lý sự kiện của người dùng (như nhấn nút, di chuyển chuột, hoặc nhập dữ liệu)
        self.window.mainloop()
        
    def _setup_main_window(self):
        # setup cửa sổ trò chuyện
        self.window.title("Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=600)
        
        # header
        head_label = Label(self.window, bg=BG_HEADER, fg=TEXT_COLOR, text="Welcome, I'm Botdeptrai", font=FONT_BOLD)
        head_label.place(relwidth=1,relheight=0.07) # đặt chiều rộng bằng 100% của phần cửa sổ
        
        # phân cách header vs content
        line = Label(self.window, bg=BG_FRAME)
        line.place(relwidth=1, relheight=0.01, rely=0.068)  #relx,rely: là độ lệch theo hướng ngang và dọc.
        
        # content
        self.text_widget = scrolledtext.ScrolledText(self.window, width=60, height=17, bg=BG_CONTENT, fg=TEXT_COLOR, font=FONT)
        self.text_widget.place(relheight=0.71, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", wrap="word", state=DISABLED)   #dạng con trỏ chuột, và ngăn ko cho nhập trực tiếp
        self.text_widget.tag_configure("highlight",background="#00CCFF")

        # nhóm câu hỏi gợi ý
        frame_question=Label(self.window)
        frame_question.place(rely=0.785,relwidth=1,relheight=0.11)

        self.button_ques1 = Button(frame_question, cursor="Hand2", text="Food menu", font=FONT_BOLD, width=20, bg=BG_QUESTION, command=lambda: self._on_enter_option(None,1))
        self.button_ques1.place(relx=0.04, rely=0.08,relheight=0.4,relwidth=0.44)

        self.button_ques2 = Button(frame_question, cursor="Hand2", text="Drink menu", font=FONT_BOLD, width=20, bg=BG_QUESTION, command=lambda: self._on_enter_option(None,2))
        self.button_ques2.place(relx=0.52, rely=0.08,relheight=0.4,relwidth=0.44)

        self.button_ques3 = Button(frame_question, cursor="Hand2", text="Best selling foods", font=FONT_BOLD, width=20, bg=BG_QUESTION, command=lambda: self._on_enter_option(None,3))
        self.button_ques3.place(relx=0.04, rely=0.6,relheight=0.4,relwidth=0.44)

        self.button_ques4 = Button(frame_question, cursor="Hand2", text="Best selling drinks", font=FONT_BOLD, width=20, bg=BG_QUESTION, command=lambda: self._on_enter_option(None,4))
        self.button_ques4.place(relx=0.52, rely=0.6,relheight=0.4,relwidth=0.44)
    
        # khung footer
        bottom_label = Label(self.window, bg=BG_FRAME)
        bottom_label.place(relwidth=1, relheight=0.1, rely=0.9)
        
        # hộp thoại nhập message
        self.msg_entry = Entry(bottom_label, bg=BG_MESSAGE, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relx=0.03,rely=0.1,relheight=0.8,relwidth=0.7)
        self.msg_entry.focus() #người dùng có thể gõ tin nhắn
        self.msg_entry.bind("<Return>", self._on_enter_pressed)   # khi nhấn enter phương thức được gọi
        
        # send button
        send_button = Button(bottom_label, cursor="Hand2", text="Send", font=FONT_BOLD, width=20, bg=BG_BUTTON, command=lambda: self._on_enter_pressed(None))
        send_button.place(rely=0.1,relheight=0.8,relx=0.8,relwidth=0.17)

        # hiển thị lời chào đầu
        msg2 = f"{bot_name}: Hello! I\'m Botdeptrai. May I help you?\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
              
    def _on_enter_option(self,event,num_option):
        msg = ""
        if num_option==1:
            msg=self.button_ques1.cget("text")
        elif num_option==2:
            msg=self.button_ques2.cget("text")
        elif num_option==3:
            msg=self.button_ques3.cget("text")
        elif num_option==4:
            msg=self.button_ques4.cget("text")
        self._insert_message(msg, "You")


    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)   #xóa nội dung trong hộp thoại nhập tin nhắn sau khi nhấn gửi
        currentTime=datetime.now().strftime("%H:%M")
        msg1 = f"{sender}: {msg}\n\t\t\t\t      {currentTime}\n"
        self.text_widget.configure(state=NORMAL)    #cho phép sửa nội dung phần content
        self.text_widget.insert(END, msg1,"highlight")  #chèn msg1 vào cuối content
        self.text_widget.configure(state=DISABLED)  #chặn cho phép sửa nội dung phần content
        self.text_widget.after(300,lambda: self._insert_respond(msg))

    def _insert_respond(self,msg):
        #msg=translator.viToen(msg)
        resp=get_response(msg)
        msg2 = f"{bot_name}: {resp}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)   #cuộn đến cuối để hiển thị tin nhắn mới nhất""
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()