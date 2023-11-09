import os

directory = 'C:\\Python projects\\Screenshort5\\'
destination = 'C:\\Python projects\\Screenshort5\\tmp\\'
telega_dir = 'C:\\Python projects\\Screenshort5\\telega\\'
directory2 = 'C:\\Python projects\\Screenshort5\\'


# files = os.listdir(directory)

# i = 0
#
# while i < 50:
#     namefile = files[i]
#     if 'yandex.taximeter' in namefile:
#         print(i)
#         print(namefile)
#     i = i + 1

#
# for nameoffile in files:
#     namefile = nameoffile
#     if 'yandex.taximeter' in namefile:
#         os.replace(directory + namefile, destination + namefile)

files = os.listdir(destination)

for nameoffile in files:
    namefile = nameoffile
    if 'telegram' in namefile:
        os.replace(destination + namefile, telega_dir + namefile)

print(len(files))

