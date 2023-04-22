from tkinter import messagebox,filedialog,simpledialog,ttk
from tkinter import *
from edecrypt import encrypt,decrypt
from fileUtils import storage,recovery,scan
import os
import platform

def ptf():
    if ('Windows' == platform.system()):
        return 'C:\\Program Files\\7-Zip\\7z.exe',True
    # elif ('Linux' == platform.system()):
    #     print('Linux')
    else:
        return '7z',False


class App:

    def __init__(self, master):
        self.pos = 0  # 进度条进度
        self.sum = 0  # 总共多少个
        self.num = 0  # 当前是第几个
        self.add = 1  # 进度条步长
        self.length = 350
        self.list = ['.jpg', '.jpeg', '.png', '.gif']
        self.fileList = []
        self.src = StringVar(value=os.getcwd())
        self.compress = StringVar(
            value=os.getcwd())
        self.master = master
        self.master.resizable(False, False)
        self.password = StringVar(value="123")
        self.Sz,self.flag = ptf()
        self.min = IntVar(value=50)
        self.check1Var = IntVar(value=1)

        recovery(self)

        master.title("图片压缩加密")

        self.src_dir_label = Label(master, text="原始图片目录：")
        self.src_dir_label.grid(row=0, column=0)

        self.src_dir_entry = Entry(master, width=50, textvariable=self.src)
        self.src_dir_entry.grid(row=0, column=1)

        self.choose_src_button = Button(
            master, text="选择", command=self.choose_src)
        self.choose_src_button.grid(row=0, column=2)

        self.compress_dir_label = Label(master, text="压缩图片目录：")
        self.compress_dir_label.grid(row=1, column=0)
        self.compress_dir_entry = Entry(
            master, width=50, textvariable=self.compress)
        self.compress_dir_entry.grid(row=1, column=1)
        self.choose_compress_button = Button(
            master, text="选择", command=self.choose_compress)
        self.choose_compress_button.grid(row=1, column=2)

        self.size_label = Label(master, text="最小宽度和高度：")
        self.size_label.grid(row=2, column=0)
        self.width_entry = Entry(
            master, width=5, textvariable=self.min)
        self.width_entry.grid(row=2, column=1)

        self.password_label = Label(master, text="密码：")
        self.password_label.grid(row=3, column=0)
        self.password_entry = Entry(
            master, width=50, textvariable=self.password)
        self.password_entry.grid(row=3, column=1)

        self.back_button = Button(
            master, text="恢复", command=self.start_decrypt)
        self.back_button.grid(row=4, column=0)
        self.start_button = Button(
            master, text="开始", command=self.start_encrypt)
        self.start_button.grid(row=4, column=1)
        self.stop_button = Button(
            master, text="停止", command=self.stop_process)
        self.stop_button.grid(row=4, column=2)

        self.check1 = Checkbutton(
            master, text="包含子目录", variable=self.check1Var, onvalue=1, offvalue=0)
        self.check1.grid(row=5, column=0)

        self.progress_bar = ttk.Progressbar(
            self.master, orient="horizontal", length=self.length, mode="determinate")
        self.progress_bar.grid(row=5, column=1)

        self.progress = Label(master, text="/")
        self.progress.grid(row=5, column=2)

        # 创建列表框和滚动条
        self.listbox = Listbox(self.master)
        self.scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(row=0, column=3, columnspan=2, rowspan=5)
        self.scrollbar.grid(row=0, column=5, rowspan=5, sticky="NS")

        # 添加按钮
        self.add_button = Button(self.master, text="添加", command=self.add_item)
        self.add_button.grid(row=5, column=3)

        # 修改按钮
        self.edit_button = Button(
            self.master, text="修改", command=self.edit_item)
        self.edit_button.grid(row=5, column=4)

        # 删除按钮
        self.delete_button = Button(
            self.master, text="删除", command=self.delete_item)
        self.delete_button.grid(row=5, column=5)

        # 添加示例项目
        for l in self.list:
            self.listbox.insert(END, l)

        self.running = False
        # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        master.update()
        width = master.winfo_width()
        height = master.winfo_height()
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        size_geo = '+%d+%d' % ((screenwidth-width)/2, (screenheight-height)/2)
        master.geometry(size_geo)

    def add_item(self):
        # 弹出窗口，获取用户输入
        new_item = simpledialog.askstring(
            "添加", "Enter new item:", parent=self.master)
        if new_item:
            # 将新项目插入到列表中
            self.listbox.insert(END, new_item)
            self.list.append(new_item)
            storage(self)

    def edit_item(self):
        # 获取选中项目的索引
        index = self.listbox.curselection()
        if index:
            # 弹出窗口，获取用户输入
            item = self.listbox.get(index)
            new_item = simpledialog.askstring(
                "修改", f"Edit {item}:", initialvalue=item, parent=self.master)
            if new_item:
                # 将新项目替换选中的项目
                self.list.remove(self.listbox.get(index))
                self.list.insert(index[0], new_item)
                self.listbox.delete(index)
                self.listbox.insert(index, new_item)
                storage(self)

    def delete_item(self):
        # 获取选中项目的索引
        index = self.listbox.curselection()
        if index:
            # 删除选中的项目
            self.list.remove(self.listbox.get(index))
            self.listbox.delete(index)
            storage(self)

    def choose_src(self):
        dir = filedialog.askdirectory()
        if dir != "":
            self.src.set(dir)

    def choose_compress(self):
        dir = filedialog.askdirectory()
        if dir != "":
            self.compress.set(dir)

    def start_progress(self):
        # 创建进度条控件并添加到窗口中
        self.pos = 0
        self.num = 0
        try:
            self.add = 100/self.sum
        except ZeroDivisionError:
            pass
        self.progress.configure(text=f"{self.num}/{self.sum}")
        self.progress_bar.configure(value=self.pos)
        self.master.update()
        # 销毁进度条控件
        # progress_bar.destroy()

    def finish_progress(self):
        self.progress_bar.configure(value=100)
        self.progress.configure(text=self.sum)
        self.master.update()

    def update(self):
        self.pos += self.add
        self.num += 1
        self.progress.configure(text=f"{self.num}/{self.sum}")
        self.progress_bar.configure(value=self.pos)
        self.master.update()


    def show_messagebox(self, e):
        messagebox.showinfo("7zip error:", e)

    def start_decrypt(self):
        if self.running:
            return
        self.running = True
        storage(self)
        self.sum,self.fileList = scan(self.src.get(), self.list, self.check1Var.get())
        self.start_progress()
        decrypt(self,self.src.get(),self.compress.get())
        self.finish_progress()
        self.running = False

    def start_encrypt(self):
        if self.running:
            return
        self.running = True
        storage(self)
        self.sum,self.fileList= scan(self.src.get(), self.list, self.check1Var.get())
        self.start_progress()
        encrypt(self,self.src.get(),self.compress.get())
        self.finish_progress()
        self.running = False

    def stop_process(self):
        self.running = False

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
