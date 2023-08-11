import tkinter as tk
import os
import docker

from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

class DockerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Recognition")
        self.root.configure(bg="#111111")

        self.main_frame = tk.Frame(root, bg=("#111111")) # 主框架用于居中内容
        self.main_frame.pack(side="top", expand=True, fill="both")

        self.image_frame = tk.Frame(self.main_frame, bg="#111111")
        self.image_frame.pack(side="left", expand=True, fill="both" )

        self.drag_frame = tk.Frame(self.image_frame, bg="#111111")
        self.drag_frame.pack(side="top", expand=False, fill="both")
        self.image_label = tk.Label(self.drag_frame, text="Drag and drop your image here", width=55, height=3, bg="#141414", fg="#FFFFFF", font=("Courier New", 14))
        self.image_label.pack(padx=20, pady=20)

        self.display_image_frame = tk.Frame(self.image_frame, bg="#111111", width=512, height=512)
        self.display_image_frame.pack(side="bottom", pady=50, expand=False, fill="both")
        self.display_image_frame.pack_propagate(False)  # 保持Frame的尺寸不受内部组件影响

        self.content_frame = tk.Frame(self.main_frame, bg="#111111")
        self.content_frame.pack(side="right", expand=False, fill="both")

        self.output_text = tk.Text(self.content_frame, wrap=tk.WORD, height=3, bg="#111111", fg="#FFFFFF", font=("Courier", 12))
        self.output_text.pack(side="bottom", padx=20, pady=20, expand=False, fill="both")

        self.buttons_frame = tk.Frame(self.content_frame, bg="#111111")
        self.buttons_frame.pack(side="bottom", pady=10)

        self.run_button = tk.Button(self.buttons_frame, text="Run", command=self.run_license_plate_script, bg="#007ACC", fg="#FFFFFF", font=("Courier New", 12, "bold"), width=8, height=1)
        self.run_button.pack(side="left", padx=20)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset, bg="#007ACC", fg="#FFFFFF", font=("Courier New", 12, "bold"), width=8, height=1)
        self.reset_button.pack(side="right", padx=20)


        # 设置拖放和显示图片相关的变量
        self.image_label.drop_target_register(DND_FILES)
        self.image_label.dnd_bind('<<Drop>>', self.on_drop)
        self.dragged_image_path = ""
        self.client = docker.from_env()
        self.photo = None


    def reset(self):
        self.dragged_image_path = ""
        self.image_label.config(text="Drag and drop your image here")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "")
        
        # 销毁之前显示的图片标签
        if hasattr(self, "displayed_image_label"):
            self.displayed_image_label.destroy()
            self.displayed_image_label = None


    def run_license_plate_script(self):

        if self.dragged_image_path:
            image_filename = os.path.splitext(os.path.basename(self.dragged_image_path))[0]
            container_name_or_id = "license_plate_detection_S2ANet"
            container = self.client.containers.get(container_name_or_id)

            # 定义要在容器内执行的命令
            command = ["python", "license_plate.py", "-n", image_filename]

            try:
                # 执行容器内命令
                exec_result = container.exec_run(command)
                # exec_result = container.exec_run(image_filename)
                
                # 检查命令是否成功执行
                if exec_result.exit_code == 0:
                    print("Successfully executed the command in the container.")

                    with open(f"c:/license_plate_recognition/result/{image_filename}.txt", "r") as f:
                        lines = f.readlines()
                        first_strings = [line.split("\t")[0] for line in lines]
                        combined_result = "\n".join(first_strings)
                        self.output_text.delete("1.0", tk.END)
                        self.output_text.insert(tk.END, combined_result)

                else:
                    print("Command execution in the container failed.")

            except docker.errors.APIError as e:
                print("An error occurred:", e)

            except Exception as e:
                print("An unexpected error occurred:", e)

        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Please upload your image before running this program...")


    def on_drop(self, event):
        self.dragged_image_path = event.data
        self.image_label.config(text=f"Finish dragging the image: {os.path.basename(self.dragged_image_path)}")

        if self.dragged_image_path and os.path.exists(self.dragged_image_path):
            self.root.after_idle(self.display_image)  # 确保在窗口完成绘制后再显示图像


    def display_image(self):
        image = Image.open(self.dragged_image_path)
        original_width, original_height = image.size

        frame_width = self.display_image_frame.winfo_width()
        frame_height = self.display_image_frame.winfo_height()
        
        # 计算缩放比例以适应框架
        scale = min(frame_width / original_width, frame_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        image = image.resize((new_width, new_height), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(image)  # 存储PhotoImage对象

        # 如果之前有图片标签，先销毁，然后创建新的
        if hasattr(self, "displayed_image_label"):
            self.displayed_image_label.destroy()
            
        self.displayed_image_label = tk.Label(self.display_image_frame, image=self.photo, bg="#FFFFFF")
        self.displayed_image_label.photo = self.photo
        self.displayed_image_label.pack(side="bottom", expand=True)

if __name__ == "__main__":
    app = TkinterDnD.Tk()
    docker_gui = DockerGUI(app)

    app.geometry("1024x576")

    app.mainloop()
