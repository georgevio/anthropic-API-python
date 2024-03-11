# Author: George Violettas
# Email: georgevio@gmail.com
# Date: 11/03/2024

# This code does connect via API to the anthropic AI library (named Claude) at https://www.anthropic.com/ . The engine currently (2024) provides only such connection (testing purposes) and DOES NOT provide web access. The current code is simplistic (gets the job done) with two text windows, the top for writing the question, and the bottom to fetch the results. You can also try to upload an image or a document (not tested).

# IMPORTANT: YOU NEED AN API KEY (FREE Currently)! Code will not work without it. Instructions on how to get it, here https://www.anthropic.com/api

# ********* LINUX INSTALLATION NOTES *****************
# pip install anthropic
# apt-get install python3-tk
# apt-get install python3-pil python3-pil.imagetk
# in ubutnu 20 this is needed pip install Pillow

# Code also works in Windows (tested)

import os
import anthropic
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# It will not work without a KEY!

OPENAI_API_KEY = "XXXX-XXXXXX-XXXXXXXXX-XXXXXXXXXXx-XXXXXXXXXXXX"   

def send_message():
    user_input = input_text.get(1.0, tk.END).strip()
    if user_input:
        try:
            response = client.completions.create(
                prompt=f"\n\nHuman: {user_input}\n\nAssistant:",
                model="claude-v1",
                max_tokens_to_sample=1000,
                temperature=randomness_var.get()
            )
            assistant_response = response.completion
            output_text.configure(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, assistant_response)
            output_text.configure(state=tk.DISABLED)
        except Exception as e:
            output_text.configure(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, str(e))
            output_text.configure(state=tk.DISABLED)

    
def import_file():
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                image = Image.open(file_path)
                image = image.resize((300, 300))
                photo = ImageTk.PhotoImage(image)
                image_label.configure(image=photo)
                image_label.image = photo
            else:
                with open(file_path, "r") as file:
                    document_text = file.read()
                input_text.delete(1.0, tk.END)
                input_text.insert(tk.END, document_text)
    except Exception as e:
        print(e)
        

try: 
    client = anthropic.Anthropic(api_key=OPENAI_API_KEY)

    window = tk.Tk()
    window.title("Anthropic API Communication")
    window.geometry("700x600")  

    input_frame = ttk.Frame(window)
    input_frame.pack(pady=5)  

    input_text = tk.Text(input_frame, height=8, width=82)
    input_text.pack()  

    send_button = ttk.Button(input_frame, text="Send", command=send_message)
    send_button.pack(pady=5, side='left')  

    output_frame = ttk.Frame(window) 
    output_frame.pack(pady=5, side = 'top')   

    output_text = tk.Text(output_frame, height=20, width=82, state=tk.DISABLED)
    output_text.pack()  

    image_frame = ttk.Frame(window)
    image_frame.pack(pady=5)  

    image_label = ttk.Label(image_frame)
    image_label.pack()   

    file_frame = ttk.Frame(window)
    file_frame.pack(pady=0)   

    import_button = ttk.Button(file_frame, text="Import File", command=import_file)
    import_button.pack(side="right")   

    param_frame = ttk.Frame(window) 
    param_frame.pack(pady=5)  

    randomness_var = tk.DoubleVar(value=0.5)   
    randomness_scale = ttk.Scale(param_frame, from_=0, to=1, variable=randomness_var)
    randomness_scale.pack()
    randomness_label = ttk.Label(param_frame, text="Randomness")
    randomness_label.pack()  
    
except FileNotFoundError as err:
    print("File not found:", err)
except PermissionError as err:
    print("Permission denied:", err) 
except ValueError as err:
    print("Invalid file format:", err)
except Exception as err:
    print("Unknown error:", err) 
    
window.mainloop()
