css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    max-width: 800px;
    margin: auto;
    padding: 1rem;
    background-color: #f4f5f7;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.chat-message {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border-radius: 15px;
    font-family: 'Arial', sans-serif;
}

.chat-message.user {
    justify-content: flex-start;
    background-color: #2b313e;
}

.chat-message.bot {
    justify-content: flex-end;
    background-color: #475063;
}

.chat-message .avatar {
    width: 50px;
    height: 50px;
    flex-shrink: 0;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 0.5rem;
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.chat-message .message {
    flex-grow: 1;
    padding: 0.5rem 1rem;
    color: #fff;
    border-radius: 12px;
    font-size: 0.9rem;
    line-height: 1.4;
}

/* Responsive Design */
@media (max-width: 600px) {
    .chat-message {
        flex-direction: column;
        align-items: flex-start;
    }

    .chat-message.bot {
        align-items: flex-end;
    }

    .chat-message .avatar {
        margin-bottom: 0.5rem;
    }
}
</style>

'''
# HTML Template Enhancements

# Bot Template:

# <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.dropbox.com/scl/fi/xgmjaj5u8ch11ut94409y/robortjst.jpg?rlkey=au4lisakxlkafdkye7ri4vxp4&dl=1">
    </div>
    <div class="message">{{MSG}}</div>
</div>

'''

# User Template:

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.dropbox.com/scl/fi/yebgmh448jvsueb6pzngg/jstimg.jpg?rlkey=1j6j2u8va1y3haljbo7f9w3hw&dl=1">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''