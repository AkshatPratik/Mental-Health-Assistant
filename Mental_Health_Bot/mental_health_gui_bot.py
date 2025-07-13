import tkinter as tk
from tkinter import scrolledtext
import datetime

# Global state to track interactive conversations
bot_state = {
    "expecting_reason": False,
    "last_emotion": None
}

# Bot logic
def get_bot_response(user_input):
    global bot_state
    user_input = user_input.lower()

    if bot_state["expecting_reason"]:
        bot_state["expecting_reason"] = False
        return f"That sounds really important. You're allowed to feel this way. Want me to share something that might help?"

    if "sad" in user_input or "upset" in user_input:
        bot_state["expecting_reason"] = True
        bot_state["last_emotion"] = "sad"
        return "I'm sorry you're feeling this way. Do you want to talk about what’s making you feel sad?"
    elif "anxious" in user_input or "nervous" in user_input:
        bot_state["expecting_reason"] = True
        bot_state["last_emotion"] = "anxious"
        return "Anxiety can be overwhelming. Would you like to share what’s making you feel that way?"
    elif "stressed" in user_input:
        return "Stress can weigh you down. Even small breaks can help. Would you like a tip to de-stress?"
    elif "lonely" in user_input:
        return "You're not alone here. I'm always ready to listen. Want to share what’s been on your mind?"
    elif "bye" in user_input or "exit" in user_input:
        return "Thanks for talking. Please take care of yourself. You're not alone in this. 💚"
    elif "yes" in user_input or "sure" in user_input:
        if bot_state["last_emotion"] == "sad":
            return "Journaling can help. Write down how you feel without judgment. It’s like talking to yourself kindly."
        elif bot_state["last_emotion"] == "anxious":
            return "Try breathing in for 4 seconds, hold for 4, breathe out for 4. It really works."
        else:
            return "Try taking a short break, listening to music, or reaching out to a friend."
    elif "no" in user_input or "not really" in user_input:
        return "That's okay. Just know I'm here if you ever feel like talking."
    else:
        return "I’m here with you. Want to share more about how you’re feeling?"
    
def save_to_log(speaker, message):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"{timestamp} | {speaker}: {message}\n")


# Send message logic
def send_message():
    user_input = entry.get()
    if user_input.strip() == "":
        return

    # Show user input in the chat window
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {user_input}\n", "user")

    # Get bot response
    bot_response = get_bot_response(user_input)
    chat_window.insert(tk.END, f"Bot: {bot_response}\n\n", "bot")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

    # Save to history file
    save_to_log("User", user_input)
    save_to_log("Bot", bot_response)

    # Clear input field
    entry.delete(0, tk.END)

    if "bye" in user_input.lower() or "exit" in user_input.lower():
        entry.config(state="disabled")
        send_button.config(state="disabled")

        mood = detect_mood(user_input)
    save_to_log("User", f"{user_input} [mood: {mood}]")
    save_to_log("Bot", bot_response)


def view_history():
    try:
        with open("chat_history.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "No history found."

    # Popup window
    popup = tk.Toplevel(window)
    popup.title("🗂️ Your Chat History")
    popup.geometry("500x400")

    history_box = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=("Segoe UI", 11))
    history_box.pack(fill="both", expand=True)
    history_box.insert(tk.END, content)
    history_box.config(state=tk.DISABLED)



def detect_mood(user_input):
    user_input = user_input.lower()
    if "sad" in user_input or "depressed" in user_input:
        return "sad"
    elif "anxious" in user_input or "nervous" in user_input:
        return "anxious"
    elif "stressed" in user_input or "overwhelmed" in user_input:
        return "stressed"
    elif "lonely" in user_input:
        return "lonely"
    elif "happy" in user_input:
        return "happy"
    else:
        return "neutral"


        

# GUI setup
window = tk.Tk()
window.title("🧠 Mental Health Support Chatbot")
window.configure(bg="#E6F0F7")
window.resizable(False, False)

font_main = ("Segoe UI", 12)
bg_color = "#E6F0F7"
chat_bg = "#F9FAFB"
bot_color = "#007ACC"
user_color = "#444444"

chat_window = scrolledtext.ScrolledText(
    window, wrap=tk.WORD, width=60, height=20, font=font_main, bg=chat_bg, state=tk.DISABLED
)
chat_window.pack(padx=20, pady=10)
chat_window.tag_config("bot", foreground=bot_color)
chat_window.tag_config("user", foreground=user_color)

chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, "Bot: Hi, I'm here for you. You can talk to me anytime.\nType 'help' for support resources.\n\n", "bot")
chat_window.config(state=tk.DISABLED)

frame = tk.Frame(window, bg=bg_color)
frame.pack(pady=10)

entry = tk.Entry(frame, width=50, font=font_main)
entry.pack(side=tk.LEFT, padx=(0, 10), ipady=6)
entry.focus_set()
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    frame, text="Send", command=send_message, font=("Segoe UI", 10, "bold"),
    bg="#007ACC", fg="white", relief="flat", padx=12, pady=6, cursor="hand2"
)
send_button.pack(side=tk.LEFT)
view_button = tk.Button(
    frame, text="View History", command=lambda: view_history(),
    font=("Segoe UI", 10), bg="#CCCCCC", relief="flat", padx=10, pady=6, cursor="hand2"
)
view_button.pack(side=tk.LEFT, padx=(10, 0))


window.mainloop()
