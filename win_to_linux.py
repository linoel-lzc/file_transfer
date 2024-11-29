import tkinter as tk
from tkinter import filedialog, messagebox
import paramiko
import datetime


# 默认配置
default_remote_path = "/var/www/html/"
default_host = "10.74.62.106"
default_port = 22
default_username = "root"
default_password = "cisco1234"


def log_error(message, operation=""):
    """将错误信息写入日志文件"""
    with open("transfer_errors.log", "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {operation} - {message}\n")


def transfer_file(local_path, remote_path, host, port, username, password):
    """传输文件到远程服务器"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, port=port, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        ssh.close()
        return True, f"文件成功传输到 {remote_path}"
    except Exception as e:
        log_error(f"文件传输失败: {e}", operation=f"上传文件 {local_path} 到 {remote_path}")
        return False, str(e)


def test_connection(host, port, username, password):
    """测试 SSH 连接"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, port=port, username=username, password=password)
        ssh.close()
        return True, "SSH 连接成功！"
    except Exception as e:
        log_error(f"SSH 测试连接失败: {e}", operation="测试连接")
        return False, str(e)


def select_file():
    """选择本地文件"""
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_local_path.delete(0, tk.END)
        entry_local_path.insert(0, file_path)


def upload():
    """上传文件"""
    local_path = entry_local_path.get()
    remote_path = entry_remote_path.get()
    host = entry_host.get()
    port = int(entry_port.get())
    username = entry_username.get()
    password = entry_password.get()

    if not all([local_path, remote_path, host, username, password]):
        messagebox.showerror("错误", "请填写所有字段！")
        return

    success, message = transfer_file(local_path, remote_path, host, port, username, password)
    if success:
        messagebox.showinfo("成功", message)
    else:
        messagebox.showerror("错误", message)


def test_ssh():
    """测试 SSH 连接"""
    host = entry_host.get()
    port = int(entry_port.get())
    username = entry_username.get()
    password = entry_password.get()

    if not all([host, username, password]):
        messagebox.showerror("错误", "请填写服务器地址、用户名和密码！")
        return

    success, message = test_connection(host, port, username, password)
    if success:
        messagebox.showinfo("测试结果", message)
    else:
        messagebox.showerror("测试结果", message)


def append_remote_path():
    """追加路径到远程路径输入框"""
    additional_path = filedialog.askdirectory(title="选择远程子目录")
    if additional_path:
        current_path = entry_remote_path.get()
        if not current_path.endswith("/"):
            current_path += "/"
        entry_remote_path.delete(0, tk.END)
        entry_remote_path.insert(0, current_path + additional_path.split("/")[-1] + "/")


# 创建主窗口
root = tk.Tk()
root.title("文件传输工具")

# 文件路径选择
tk.Label(root, text="本地文件路径:").grid(row=0, column=0, padx=10, pady=5)
entry_local_path = tk.Entry(root, width=50)
entry_local_path.grid(row=0, column=1, padx=10, pady=5)
btn_select_file = tk.Button(root, text="选择文件", command=select_file)
btn_select_file.grid(row=0, column=2, padx=10, pady=5)

# 远程路径
tk.Label(root, text="远程文件路径:").grid(row=1, column=0, padx=10, pady=5)
entry_remote_path = tk.Entry(root, width=50)
entry_remote_path.grid(row=1, column=1, padx=10, pady=5)
entry_remote_path.insert(0, default_remote_path)  # 设置默认路径
btn_append_path = tk.Button(root, text="追加路径", command=append_remote_path)
btn_append_path.grid(row=1, column=2, padx=10, pady=5)

# 服务器信息
tk.Label(root, text="服务器地址:").grid(row=2, column=0, padx=10, pady=5)
entry_host = tk.Entry(root, width=50)
entry_host.grid(row=2, column=1, padx=10, pady=5)
entry_host.insert(0, default_host)  # 设置默认服务器地址

tk.Label(root, text="端口:").grid(row=3, column=0, padx=10, pady=5)
entry_port = tk.Entry(root, width=50)
entry_port.insert(0, str(default_port))  # 默认端口 22
entry_port.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="用户名:").grid(row=4, column=0, padx=10, pady=5)
entry_username = tk.Entry(root, width=50)
entry_username.grid(row=4, column=1, padx=10, pady=5)
entry_username.insert(0, default_username)  # 默认用户名

tk.Label(root, text="密码:").grid(row=5, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show="*", width=50)
entry_password.grid(row=5, column=1, padx=10, pady=5)
entry_password.insert(0, default_password)  # 默认密码

# 测试连接按钮
btn_test_connection = tk.Button(root, text="测试连接", command=test_ssh)
btn_test_connection.grid(row=6, column=0, columnspan=1, pady=10)

# 上传按钮
btn_upload = tk.Button(root, text="上传文件", command=upload)
btn_upload.grid(row=6, column=2, columnspan=1, pady=10)

# 启动主循环
root.mainloop()
