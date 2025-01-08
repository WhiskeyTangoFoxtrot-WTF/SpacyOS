import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from tkinter.simpledialog import askstring
from PIL import Image, ImageDraw, ImageFont

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing X")
        self.root.geometry("1000x700")
        self.root.configure(bg="black")
        self.pen_color = "lime"
        self.bg_color = "black"
        self.brush_size = 5
        self.font_size = 20
        self.tool = "pen"
        self.text_tool_active = False
        self.text_position = None
        self.text_font = None  
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=self.bg_color)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.controls_frame = tk.Frame(self.root, bg="lightgrey")
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.create_controls()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Button-1>", self.set_text_position)
        self.last_x, self.last_y = None, None

    def create_controls(self):
        label_style = {"bg": "gray20", "fg": "lime"} 
        button_style = {"bg": "gray10", "fg": "lime", "activebackground":"gray15"}  
        tk.Label(self.controls_frame, text="Brush Size:", bg="lightgrey").pack(pady=5)
        self.brush_slider = tk.Scale(self.controls_frame, from_=1, to=20, orient=tk.HORIZONTAL, bg="lightgrey")
        self.brush_slider.set(self.brush_size)
        self.brush_slider.pack()
        tk.Label(self.controls_frame, text="Font Size:", bg="lightgrey").pack(pady=5)
        self.font_slider = tk.Scale(self.controls_frame, from_=5, to=100, orient=tk.HORIZONTAL, bg="lightgrey")
        self.font_slider.set(self.font_size)
        self.font_slider.pack()
        tk.Button(self.controls_frame, text="Pick Color", command=self.pick_color, bg="white").pack(pady=10)
        self.create_tool_button("Pen", "pen")
        self.create_tool_button("Brush", "brush")
        self.create_tool_button("Text", "text")
        tk.Button(self.controls_frame, text="Erase All", command=self.erase_all, bg="white").pack(pady=5)
        tk.Button(self.controls_frame, text="Save", command=self.save_image, bg="white").pack(pady=20)

    def create_tool_button(self, text, tool_name):
        button = tk.Button(self.controls_frame, text=text, bg="white", command=lambda: self.select_tool(tool_name))
        button.pack(fill=tk.X, pady=2)

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def select_tool(self, tool_name):
        if tool_name == "text":
            self.text_tool_active = True
        else:
            self.tool = tool_name
            self.text_tool_active = False
    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            if self.tool == "pen" or self.tool == "brush":
                self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=self.brush_slider.get(), capstyle="round", smooth=True)
                self.draw.line((self.last_x, self.last_y, x, y), fill=self.pen_color, width=self.brush_slider.get())
        self.last_x, self.last_y = x, y
    def reset(self, event):
        self.last_x, self.last_y = None, None
    def set_text_position(self, event):
        if self.text_tool_active:
            self.text_position = (event.x, event.y)
            self.font_size = self.font_slider.get()  
            self.text_font = ImageFont.truetype("arial.ttf", self.font_size) 
            user_text = askstring("Text Input", "Enter your text:")
            if user_text:
                font_str = f"Arial {self.font_size}"  
                self.canvas.create_text(self.text_position, text=user_text, fill=self.pen_color, font=font_str)
                self.draw.text(self.text_position, user_text, font=self.text_font, fill=self.pen_color)
                self.text_tool_active = False  
    def erase_all(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Image Saved", "Your drawing has been saved!")
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
