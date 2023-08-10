import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os

class DockerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Docker GUI")

        self.image_label = tk.Label(root, text="拖拽图片到这里")
        self.run_button = tk.Button(root, text="运行 license_plate.py", command=self.run_license_plate_script)
        self.output_text = tk.Text(root, wrap=tk.WORD)
        self.output_text.insert(tk.END, "命令输出将在这里显示")

        self.image_label.pack(padx=20, pady=10)
        self.run_button.pack(padx=20, pady=10)
        self.output_text.pack(padx=20, pady=20)

        self.image_label.drop_target_register(DND_FILES)
        self.image_label.dnd_bind('<<Drop>>', self.on_drop)

        self.mounted_output_dir = "/path/to/mounted/output/directory"  # 替换为实际的挂载目录

    def run_license_plate_script(self):
        if self.dragged_image_path:
            # 获取拖拽图片的文件名
            image_filename = os.path.basename(self.dragged_image_path)

            # 构建执行命令
            command = [
                "docker", "exec", "-it", "license_plate_detection_S2ANet",
                "bash", "-c", f"python license_plate.py {image_filename}"
            ]

            try:
                # 在容器内执行命令
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)

                # 保存输出到挂载目录下的文件
                output_file_path = os.path.join(self.mounted_output_dir, "output.txt")
                with open(output_file_path, "w") as output_file:
                    output_file.write(output)

                # 更新GUI上的输出
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, output)
            except subprocess.CalledProcessError as e:
                error_output = f"命令执行错误：\n{e.output}"
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, error_output)
        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "请拖拽图片到界面上再运行命令。")

    def on_drop(self, event):
        self.dragged_image_path = event.data
        self.image_label.config(text=f"已拖拽图片：{os.path.basename(self.dragged_image_path)}")

if __name__ == "__main__":
    app = TkinterDnD.Tk()
    docker_gui = DockerGUI(app)
    app.mainloop()
