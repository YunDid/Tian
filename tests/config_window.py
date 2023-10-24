import tkinter as tk

class ConfigInputWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("配置输入窗口")

        # 创建标签和文本框以输入不同的配置字段
        tk.Label(root, text="Output File Path:").grid(row=0, column=0)
        self.output_file_path_entry = tk.Entry(root)
        self.output_file_path_entry.grid(row=0, column=1)

        tk.Label(root, text="Amplitude Values (comma-separated):").grid(row=1, column=0)
        self.amplitude_values_entry = tk.Entry(root)
        self.amplitude_values_entry.grid(row=1, column=1)

        tk.Label(root, text="Interval STI (us):").grid(row=2, column=0)
        self.interval_sti_entry = tk.Entry(root)
        self.interval_sti_entry.grid(row=2, column=1)

        tk.Label(root, text="Interval MBlock (us):").grid(row=3, column=0)
        self.interval_mblock_entry = tk.Entry(root)
        self.interval_mblock_entry.grid(row=3, column=1)

        tk.Label(root, text="Interval BBlock (us):").grid(row=4, column=0)
        self.interval_bblock_entry = tk.Entry(root)
        self.interval_bblock_entry.grid(row=4, column=1)

        # 创建按钮来提交配置
        submit_button = tk.Button(root, text="提交配置", command=self.submit_config)
        submit_button.grid(row=5, columnspan=2)

    def submit_config(self):
        # 获取文本框中的输入值
        output_file_path = self.output_file_path_entry.get()
        amplitude_values = [float(value) for value in self.amplitude_values_entry.get().split(",")]
        interval_sti = int(self.interval_sti_entry.get())
        interval_mblock = int(self.interval_mblock_entry.get())
        interval_bblock = int(self.interval_bblock_entry.get())

        # 创建配置字典并传递给主应用程序
        config = {
            'output_file_path': output_file_path,
            'amplitude_values': amplitude_values,
            'interval_sti': interval_sti,
            'interval_mblock': interval_mblock,
            'interval_bblock': interval_bblock,
            'num_sti': 10,  # 默认值，您可以根据需要更改
            'num_mblock': 4,  # 默认值，您可以根据需要更改
            'num_bblock': 10  # 默认值，您可以根据需要更改
        }

        # 调用主应用程序并关闭配置窗口
        self.root.destroy()
        main_with_config(config)

def main_with_config(config):
    # 这里可以调用主应用程序并传递配置
    # 您可以根据需要修改主应用程序来使用传递的配置

    # 示例输出配置信息
    print("Output File Path:", config['output_file_path'])
    print("Amplitude Values:", config['amplitude_values'])
    print("Interval STI (us):", config['interval_sti'])
    print("Interval MBlock (us):", config['interval_mblock'])
    print("Interval BBlock (us):", config['interval_bblock'])

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigInputWindow(root)
    root.mainloop()
