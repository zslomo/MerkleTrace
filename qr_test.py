import os
list = os.walk('./upload')

for img_dir in list:
    for img in img_dir[2]:
        os.remove(os.path.join(img_dir[0],img))