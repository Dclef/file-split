import os
import codecs
import chardet
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox


def detect_encoding(file_path, num_lines=1000):
    with open(file_path, 'rb') as file:
        raw_data = b''
        for _ in range(num_lines):
            line = file.readline()
            if not line:
                break
            raw_data += line

        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        print(f"Detected encoding: {encoding} (confidence: {confidence})")
        return encoding


def split_sql_file(file_path, output_folder, max_file_size, max_lines, file_extension):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 检测文件编码方式
    file_encoding = detect_encoding(file_path)

    # 打开原始 SQL 文件并指定编码方式
    with codecs.open(file_path, 'r', encoding=file_encoding) as file:
        file_counter = 1
        line_counter = 0
        output_file = None
        file_size = 0

        for line in file:
            # 计算当前行的大小
            line_size = len(line.encode(file_encoding))

            if output_file and (file_size + line_size > max_file_size or line_counter >= max_lines):
                # 关闭上一个文件
                output_file.close()
                output_file = None
                file_size = 0
                line_counter = 0

            if not output_file:
                # 创建新文件
                output_file_path = os.path.join(output_folder, f'split_file_{file_counter}.{file_extension}')
                # 使用原始文件的编码方式写入文件
                output_file = codecs.open(output_file_path, 'w', encoding=file_encoding)
                file_counter += 1

            # 写入当前行到文件
            output_file.write(line)
            line_counter += 1
            file_size += line_size

        # 关闭最后一个文件
        if output_file:
            output_file.close()

    print(f'Successfully split the SQL file into {file_counter - 1} files.')


def browse_file():
    file_path = filedialog.askopenfilename(title="Select  File")
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(tk.END, file_path)


def browse_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")

    entry_output_folder.delete(0, tk.END)
    entry_output_folder.insert(tk.END, folder_path)


def split_file():
    sql_file_path = entry_file_path.get()
    output_folder_path = entry_output_folder.get()
    max_file_size_str = entry_max_file_size.get()
    max_lines_str = entry_max_lines.get()
    file_extension = entry_file_extension.get()
    if not file_extension:
        messagebox.showerror("错误","请输入文件扩展名！")
        return
    if not sql_file_path:
        messagebox.showerror("错误","请选择文件！")
        return
    if not output_folder_path:
        messagebox.showerror("错误","请选择输出文件夹！")
        return
    # Validate max_file_size entry
    if not max_file_size_str:
        messagebox.showerror("错误","请输入文件大小！")
        return

    try:
        max_file_size = int(max_file_size_str) * 1024 * 1024  # Convert to bytes
    except ValueError:
        messagebox.showerror("错误","请输入正确的文件大小")
        return

    if not max_lines_str:
        messagebox.showerror("错误","请输入最大行数！.")
        return

    try:
        max_lines = int(max_lines_str)
    except ValueError:
        messagebox.showerror("错误","请输入正确的行数！ ")
        return

    split_sql_file(sql_file_path, output_folder_path, max_file_size, max_lines,file_extension)

# 创建GUI窗口
window = tk.Tk()
window.title("File Splitter")
frame_file_extension = tk.Frame(window)
frame_file_extension.pack(pady=10)

label_file_extension = tk.Label(frame_file_extension, text="File Extension:")
label_file_extension.pack(side=tk.LEFT)

entry_file_extension = tk.Entry(frame_file_extension, width=10)
entry_file_extension.pack(side=tk.LEFT)
# 创建文件路径选择部件
frame_file = tk.Frame(window)
frame_file.pack(pady=10)

label_file_path = tk.Label(frame_file, text="File:")
label_file_path.pack(side=tk.LEFT)

entry_file_path = tk.Entry(frame_file, width=50)
entry_file_path.pack(side=tk.LEFT, padx=10)

button_browse_file = tk.Button(frame_file, text="Browse", command=browse_file)
button_browse_file.pack(side=tk.LEFT)

# 创建输出文件夹选择部件
frame_output_folder = tk.Frame(window)
frame_output_folder.pack(pady=10)

label_output_folder = tk.Label(frame_output_folder, text="Output Folder:")
label_output_folder.pack(side=tk.LEFT)

entry_output_folder = tk.Entry(frame_output_folder, width=50)
entry_output_folder.pack(side=tk.LEFT, padx=10)

button_browse_folder = tk.Button(frame_output_folder, text="Browse", command=browse_folder)
button_browse_folder.pack(side=tk.LEFT)

# 创建最大文件大小部件
frame_max_file_size = tk.Frame(window)
frame_max_file_size.pack(pady=10)

label_max_file_size = tk.Label(frame_max_file_size, text="Max File Size (MB):")
label_max_file_size.pack(side=tk.LEFT)

entry_max_file_size = tk.Entry(frame_max_file_size, width=10)
entry_max_file_size.pack(side=tk.LEFT)

# 创建最大行数部件
frame_max_lines = tk.Frame(window)
frame_max_lines.pack(pady=10)

label_max_lines = tk.Label(frame_max_lines, text="Max Lines:")
label_max_lines.pack(side=tk.LEFT)

entry_max_lines = tk.Entry(frame_max_lines, width=10)
entry_max_lines.pack(side=tk.LEFT)

# 创建拆分按钮
button_split = tk.Button(window, text="Split File", command=split_file)
button_split.pack(pady=10)

# 运行窗口的主循环
window.mainloop()