import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import requests

UPLOAD_URL = "http://localhost:8000/api/upload"
CHAT_URL = "http://localhost:8000/api/chat"

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG Chatbot Client")

        # Tabs
        self.tab_control = tk.ttk.Notebook(root)
        self.upload_tab = tk.Frame(self.tab_control)
        self.chat_tab = tk.Frame(self.tab_control)

        self.tab_control.add(self.upload_tab, text='📁 Upload File')
        self.tab_control.add(self.chat_tab, text='💬 Ask a Question')
        self.tab_control.pack(expand=1, fill='both')

        self.build_upload_tab()
        self.build_chat_tab()

    def build_upload_tab(self):
        self.upload_label = tk.Label(self.upload_tab, text="Choose a PDF / TXT / DOCX file to upload:")
        self.upload_label.pack(pady=10)

        self.upload_button = tk.Button(self.upload_tab, text="Select File", command=self.select_file)
        self.upload_button.pack()

        self.upload_status = tk.Label(self.upload_tab, text="", fg="blue")
        self.upload_status.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Document files", "*.pdf *.txt *.docx")])
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    resp = requests.post(UPLOAD_URL, files=files)
                if resp.status_code == 200:
                    self.upload_status.config(text="✅ Upload successful!")
                else:
                    self.upload_status.config(text=f"❌ Failed: {resp.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {str(e)}")

    def build_chat_tab(self):
        self.chat_label = tk.Label(self.chat_tab, text="Enter your question:")
        self.chat_label.pack(pady=10)

        self.question_entry = tk.Entry(self.chat_tab, width=60)
        self.question_entry.pack()

        self.ask_button = tk.Button(self.chat_tab, text="Ask", command=self.ask_question)
        self.ask_button.pack(pady=5)

        self.answer_box = scrolledtext.ScrolledText(self.chat_tab, height=15, width=80)
        self.answer_box.pack(padx=10, pady=10)

    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Input Required", "Please enter a question.")
            return
        try:
            resp = requests.post(CHAT_URL, json={"question": question})
            if resp.status_code == 200:
                answer = resp.json().get("answer", "No answer returned.")
                self.answer_box.delete("1.0", tk.END)
                self.answer_box.insert(tk.END, answer)
            else:
                messagebox.showerror("Error", f"Failed to get answer: {resp.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Request failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
