class Chatbox{
    constructor(){
        this.args={
            openButton: document.querySelector('.chatbox__button'),// lựa chọn phần tử DOM có lớp chatbox__button. 
            // giả sử rằng có một phần tử trên trang web có lớp chatbox__button và nó sẽ được lưu trữ trong biến openButton 
            // nút câu hỏi gợi ý
            openButton_question: document.querySelectorAll('.button_question'),
            // hop thoai chatbot
            chatBox: document.querySelector('.chatbox__support'),//truy vấn đến chatbox__support(hộp thoại chat)
            // nút gửi tin
            sendButton: document.querySelector('.send__button')
        }
        this.state=false;
        this.messages=[];
    }

    display(){
        const {openButton,openButton_question,chatBox,sendButton}=this.args;
        //xử lý sự kiện khi click vào openButton thì gọi đến hàm toggleState
        openButton.addEventListener('click',()=>this.toggleState(chatBox))

        openButton_question.forEach(button_question=>{
            button_question.addEventListener('click',()=>this.onSendButton(button_question.textContent,chatBox))
        });
        // xử lý sự kiện nút gửi tin nhắn
        sendButton.addEventListener('click',()=>this.get_text_input(chatBox))
        const node=chatBox.querySelector('input');
        node.addEventListener('keyup',({key})=>{
            if(key=='Enter'){
                this.get_text_input(chatBox)
            }
        })
    }
    get_text_input(chatbox){
        var textField=chatbox.querySelector('input');
        let text1=textField.value
        this.onSendButton(text1,chatbox)
        textField.value=''
    }

    toggleState(chatBox){
        this.state=!this.state;
        if(this.state){
            chatBox.classList.add('chatbox--active')
        }
        else{
            chatBox.classList.remove('chatbox--active')
        }
    }

    onSendButton(text1,chatbox){
        if(text1===""){
            return;
        }
        let msg1={name: "User",message:text1}
        this.messages.push(msg1)
        //gửi request đến máy chủ
        fetch($SCRIPT_ROOT +'/predict',{ //lấy URL
            method:'POST',
            body: JSON.stringify({message:text1}),
            mode: 'cors',
            headers:{
                'Content-Type':'application/json'
            },
        })
        .then(r=>r.json()) //chuyển đổi phản hồi từ dạng JSON sang một đối tượng JavaScript
        .then(r=>{
            let msg2={name:"Botdeptrai",message: r.answer};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
        })
        .catch((error)=>{
            console.error('Error:',error);
            this.updateChatText(chatbox)
        })
    }

    updateChatText(chatbox){
        var html='';
        this.messages.slice().reverse().forEach(function(item,index){
            if(item.name==="Botdeptrai"){
                html+='<div class="messages__item messages__item--visitor">' +item.message + '</div>'
            }
            else{
                html+='<div class="messages__item messages__item--operator">'+item.message+'</div>'
            }
        });
        const chatmessage=chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML=html
        // kéo đến cuối thanh cuộn
        var element=document.querySelector('.chatbox__messages')
        element.scrollTop=element.scrollHeight
    }
}   

const chatbox=new  Chatbox()
chatbox.display()