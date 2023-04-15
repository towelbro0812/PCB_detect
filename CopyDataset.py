import os
import shutil
# 原始資料集位置
source_annotations_path = '../../../Dataset/PCB_DATASET/Annotations'
source_images_path = '../../../Dataset/PCB_DATASET/images'
# 目標資料集位置
target_path = './ALL_PCB_dataset'
if not os.path.exists(os.path.join(target_path,'source_imges')):
    os.makedirs(os.path.join(target_path,'source_imges'))
if not os.path.exists(os.path.join(target_path,'annotations')):
    os.makedirs(os.path.join(target_path,'annotations'))
# 複製所有檔案至目標資料集位置
for root,dirs,files in os.walk(source_annotations_path):
    for file in files:
        # print(os.path.join(root,file))
        source_file_path = os.path.join(root,file)
        target_file_path = os.path.join(target_path,'annotations',file)
        shutil.copy2(source_file_path,target_file_path)
for root,dirs,files in os.walk(source_images_path):
    for file in files:
        # print(os.path.join(root,file))
        source_file_path = os.path.join(root,file)
        target_file_path = os.path.join(target_path,'source_imges',file)
        shutil.copy2(source_file_path,target_file_path)
