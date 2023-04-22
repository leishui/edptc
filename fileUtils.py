import py7zr
import os
import subprocess
import pickle

def zip(in_file, out_file, pwd,zip):
    subprocess.run(
        [zip, 'a', f'-mx=0', '-p' + pwd, '-y', out_file, in_file], stdout=subprocess.DEVNULL)

# def zip(in_file, out_file, pwd):
#     archive_dir = os.path.dirname(out_file)
#     if not os.path.exists(archive_dir):
#         os.makedirs(archive_dir)
#     name = os.path.basename(in_file)
#     with py7zr.SevenZipFile(out_file, 'w', password=pwd) as archive:
#         archive.write(in_file, arcname=name)

def unzip(in_file, out_path, pwd,zip):
    command = f'"{zip}" x -y "{in_file}" -p{pwd} -o"{out_path}"'
    subprocess.run(command, shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, check=True)

# def unzip(in_file, out_path, pwd):
#     os.rename(in_file,in_file+'.7z')
#     with py7zr.SevenZipFile(in_file+'.7z', mode='r', password=pwd) as archive:
#         archive.extract(path=out_path)


def merge_files(file1, file2, output_file,flag):
    if(flag):
        merge_files_win(file1, file2, output_file)
    else:
        merge_files_other(file1, file2, output_file)

def merge_files_win(file1, file2, output_file):
    command = f'copy /b "{file1}"+"{file2}" "{output_file}"'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

def merge_files_other(file1, file2, output_file):
    command = f'cat "{file1}" "{file2}" > "{output_file}"'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

# def merge_files(file1, file2, output_file):
#     # 打开第一个文件并读取二进制数据
#     with open(file1, 'rb') as f1:
#         data1 = f1.read()

#     # 打开第二个文件并读取二进制数据
#     with open(file2, 'rb') as f2:
#         data2 = f2.read()

#     # 将两个二进制数据合并到一个新的二进制数据中
#     merged_data = data1 + data2

#     # 将合并后的二进制数据写入输出文件中
#     with open(output_file, 'wb') as output_f:
#         output_f.write(merged_data)

def scan(src,list,check):
        sum = 0
        fileList = []
        # 使用 os.walk() 函数遍历文件夹及其子目录
        for root, dirs, files in os.walk(src):
            # 遍历当前文件夹下的所有文件
            for name in files:
                # 获取文件名的扩展名
                ext = os.path.splitext(name)[1]
                # 如果扩展名与指定的格式相同，则增加文件数量
                if ext in list:
                    sum += 1
                    fileList.append((root+"\\"+name)[len(src)+1:].replace('\\\\','/'))
            if(check != 1):
                return sum,fileList
        return sum,fileList

def storage(app):
        if not os.path.exists("params.pkl"):
            os.mknod("params.pkl")
        params = {"min": app.min.get(), "list": app.list,
                  "check": app.check1Var.get()}
        # 序列化并保存参数到文件
        with open("params.pkl", "wb") as f:
            pickle.dump(params, f)

def recovery(app):
    if not os.path.exists("params.pkl"):
        return
    # 从文件中反序列化并加载参数
    with open("params.pkl", "rb") as f:
        params = pickle.load(f)
    app.min.set(params["min"])
    app.list = params["list"]
    app.check1Var.set(params["check"])