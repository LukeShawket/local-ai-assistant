import tkinter as tk
from tkinter import font
from llama_cpp import Llama
import threading

llm = Llama(
    model_path="Path to your model(.gguf)",
    n_ctx=4096
)

def get_response(content):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful agent James Bond"},
            {"role": "user", "content": content}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    
    # Insert into scrollable text box
    response_text_box.insert("end", "You: " + content + "\n")
    response_text_box.insert("end", "AI: " + reply + "\n\n")
    response_text_box.see("end")  # auto-scroll

def get_response_async():
    threading.Thread(target=get_response, args=(entry.get(),), daemon=True).start()

root = tk.Tk()
header_name = tk.Label(root, text='Local Assistant')
header_name.pack()

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(padx=20, pady=20)

send_button = tk.Button(root, text='Send your message', command=get_response_async)
send_button.pack()

# Scrollbar

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)
scrollbar = tk.Scrollbar(frame)

response_text_box = tk.Text(
    frame,
    width=50,
    height=10,
    wrap="word",
    yscrollcommand=scrollbar.set
)

response_text_box.pack()
scrollbar.config(command=response_text_box.yview)


f = font.Font(font=entry['font'])

def resize_entry(event=None):
    text = entry.get()
    width_px = f.measure(text + "0")
    entry.config(width=max(5, int(width_px / 10)))

entry.bind("<KeyRelease>", resize_entry)

root.mainloop()
