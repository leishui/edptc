from fileUtils import zip,unzip,merge_files
from PIL import Image, ExifTags
import os

def encrypt(app, src_path, compress_path):
    for _, dirs, files in os.walk(src_path):
        for filename in files:
            if not app.running:
                continue
            in_file = os.path.join(src_path, filename)
            zip_file = os.path.join(
                compress_path, os.path.splitext(filename)[0]+'.7z')
            # print(filename)
            # check if the file is an image
            ext = os.path.splitext(filename)[1]
            if ext.lower() not in app.list:
                continue
            app.update()
            if os.path.exists(os.path.join(compress_path, os.path.splitext(filename)[0]+'7z.'+filename.split('.')[1])):
                continue

            # open the image and fix orientation if needed
            try:
                img = Image.open(os.path.join(src_path, filename))
            except Exception:
                continue
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            try:
                exif = dict(img._getexif().items())
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # cases when image has no EXIF data
                pass
            # resize the image
            width, height = img.size
            min = int(app.min.get())
            if width < min or height < min:
                continue
            # compress and encrypt the image using 7zip

            zip(in_file, zip_file, app.password.get(),app.Sz)

            new_width = min
            new_height = int(height * (new_width / width))
            if new_height < min:
                new_height = min
                new_width = int(width * (new_height / height))
            img = img.resize((new_width, new_height))
            # save the compressed image
            out_file = os.path.join(compress_path, filename)
            img.save(out_file, optimize=True)
            print(f'Encrypted {filename} successfully.')
            # Use the "copy" command to copy the file

            merge_files(
                out_file, zip_file, f"{os.path.join(compress_path,os.path.splitext(filename)[0])}7z{os.path.splitext(filename)[1]}",app.flag)

            os.remove(zip_file)
            os.remove(out_file)
        if(app.check1Var.get() == 1):
            for dir in dirs:
                if(os.path.abspath(os.path.join(src_path, dir)) != os.path.abspath(app.compress.get())):
                    encrypt(app, os.path.join(src_path, dir),
                            os.path.join(compress_path, dir))
        return


# def encrypt(app):
#     for filename in app.fileList:
#         compress_path = app.compress.get()
#         in_file = os.path.join(app.src.get(),filename)
#         zip_file = os.path.join(
#             compress_path, os.path.splitext(filename)[0]+'.7z')
#         # print(filename)
#         app.update()
#         if os.path.exists(os.path.join(compress_path, os.path.splitext(filename)[0]+'7z.'+filename.split('.')[1])):
#             continue
#         # open the image and fix orientation if needed
#         try:
#             img = Image.open(in_file)
#         except Exception:
#             continue
#         for orientation in ExifTags.TAGS.keys():
#             if ExifTags.TAGS[orientation] == 'Orientation':
#                 break
#         try:
#             exif = dict(img._getexif().items())
#             if exif[orientation] == 3:
#                 img = img.rotate(180, expand=True)
#             elif exif[orientation] == 6:
#                 img = img.rotate(270, expand=True)
#             elif exif[orientation] == 8:
#                 img = img.rotate(90, expand=True)
#         except (AttributeError, KeyError, IndexError):
#             # cases when image has no EXIF data
#             pass
#         # resize the image
#         width, height = img.size
#         min = int(30)
#         if width < min or height < min:
#             continue
#         # compress and encrypt the image using 7zip
#         new_width = min
#         new_height = int(height * (new_width / width))
#         if new_height < min:
#             new_height = min
#             new_width = int(width * (new_height / height))
#         img = img.resize((new_width, new_height))
#         # save the compressed image
#         out_file = os.path.join(compress_path, filename)
#         archive_dir = os.path.dirname(out_file)
#         if not os.path.exists(archive_dir):
#             os.makedirs(archive_dir)
#         img.save(out_file, optimize=True)
#         zip(in_file, zip_file, app.password.get(),)
#         # print(f'Encrypted {filename} successfully 1.')
#         zip_file = os.path.join(
#             compress_path, os.path.splitext(filename)[0]+'.7z')
#         if os.path.exists(os.path.join(compress_path, os.path.splitext(filename)[0]+'7z.'+filename.split('.')[1])):
#             continue
#         # save the compressed image
#         out_file = os.path.join(compress_path, filename)
#         print(f'Encrypted {filename} successfully.')
#         # Use the "copy" command to copy the file
#         merge_files(
#             out_file, zip_file, f"{os.path.join(compress_path,os.path.splitext(filename)[0])}7z{os.path.splitext(filename)[1]}")
#         os.remove(zip_file)
#         os.remove(out_file)

def decrypt(app, path, compress_path):
    if not app.running:
        return
    for _, dirs, files in os.walk(path):
        if not app.running:
            break
        for filename in files:
            if not app.running:
                break
            # check if the file is an image
            ext = os.path.splitext(filename)[1]
            if ext.lower() not in app.list:
                continue
            app.update()
            archive_path = os.path.join(path, filename)
            last_index = filename.rfind('7z')
            if last_index != -1:
                filename = filename[:last_index] + \
                    filename[last_index+len('7z'):]
            if os.path.exists(os.path.join(compress_path, filename)):
                continue
            try:

                unzip(archive_path, compress_path,
                      app.password.get(),app.Sz)

                if path == compress_path:
                    os.remove(archive_path)
                print(f'Decrypted {filename} successfully.')
            except Exception as e:
                print(e)
                pass
        if(app.check1Var.get() == 1):
            for dir in dirs:
                if(os.path.abspath(os.path.join(path, dir)) != os.path.abspath(app.compress.get())):
                    decrypt(app, os.path.join(path, dir),
                            os.path.join(compress_path, dir))
        return

# def decrypt(app):
#     path = app.src.get()
#     compress_path = app.compress.get()
#     for filename in app.fileList:
#         if not app.running:
#             break
#         # check if the file is an image
#         ext = os.path.splitext(filename)[1]
#         if ext.lower() not in app.list:
#             continue
#         app.update()
#         archive_path = os.path.join(path, filename)
#         last_index = filename.rfind('7z')
#         if last_index != -1:
#             filename = filename[:last_index] + \
#                 filename[last_index+len('7z'):]
#         if os.path.exists(os.path.join(compress_path, filename)):
#             continue
#         try:
#             unzip(archive_path, compress_path,
#                   app.password.get(),app.Sz)
#             if path == compress_path:
#                 os.remove(archive_path)
#             print(f'Decrypted {filename} successfully.')
#         except Exception as e:
#             print(e)
#             pass