import xml.etree.cElementTree as ET
import os
import shutil
import random
xml_file_path = './ALL_PCB_dataset/annotations/'
images_file_path = './ALL_PCB_dataset/source_imges/'
classes = ['missing_hole','mouse_bite','open_circuit','short','spur','spurious_copper']
# 暫存label位置
if not os.path.exists('./ALL_PCB_dataset/temp_labels/'):
    os.mkdir('./ALL_PCB_dataset/temp_labels')
txt_file_path = './ALL_PCB_dataset/temp_labels/'

# Dataset比例
train_percent = 0.7
val_percent = 0.15
test_percent = 0.15

# 轉換函式
def convert(size,box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x * dw
    y = y * dh
    w = w * dw
    h = h * dh
    return x,y,w,h

# 轉換單一檔案
def convert_annotation(image_name):
    in_file  = open(os.path.join(xml_file_path,image_name)+'.xml',encoding="UTF-8")
    out_file = open(os.path.join(txt_file_path,image_name)+'.txt','w',encoding="UTF-8")
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        # 假如標註的名稱沒有在classes內，下一動
        if cls not in classes == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        box = (float(xmlbox.find('xmin').text),float(xmlbox.find('xmax').text),
               float(xmlbox.find('ymin').text),float(xmlbox.find('ymax').text))
        boundingbox = convert((w,h),box)
        out_file.write(str(cls_id)+ " " + " ".join(str(a) for a in boundingbox) + "\n")
    in_file.close()
    out_file.close()

# 批量轉換
def all_convert():
    total_xml = os.listdir(xml_file_path)
    num_xml = len(total_xml) # xml文件總數
    for i in range(0,num_xml):
        name = total_xml[i][:-4]
        convert_annotation(name)

# 建立資料集格式
def create_dir1(dir_name):
    if not os.path.exists(str(dir_name)):
        os.makedirs(str(dir_name))
    
    if not os.path.exists(str(dir_name)+'/images/'):
        os.makedirs(str(dir_name)+'/images/')
    if not os.path.exists(str(dir_name)+'/labels/'):
        os.makedirs(str(dir_name)+'/labels/')
    
    if not os.path.exists(str(dir_name)+'/images/train/'):
        os.makedirs(str(dir_name)+'/images/train/')
    if not os.path.exists(str(dir_name)+'/images/val/'):
        os.makedirs(str(dir_name)+'/images/val')
    if not os.path.exists(str(dir_name)+'/images/test/'):
        os.makedirs(str(dir_name)+'/images/test/')
    
    if not os.path.exists(str(dir_name)+'/labels/train/'):
        os.makedirs(str(dir_name)+'/labels/train/')
    if not os.path.exists(str(dir_name)+'/labels/val/'):
        os.makedirs(str(dir_name)+'/labels/val')
    if not os.path.exists(str(dir_name)+'/labels/test/'):
        os.makedirs(str(dir_name)+'/labels/test/')
    return

# 建立yolo訓練集資料夾
def create_dir2(dir_name):
    if not os.path.exists(str(dir_name)):
        os.makedirs(str(dir_name))
    
    if not os.path.exists(str(dir_name)+'/train/'):
        os.makedirs(str(dir_name)+'/train/')
    if not os.path.exists(str(dir_name)+'/val/'):
        os.makedirs(str(dir_name)+'/val/')
    if not os.path.exists(str(dir_name)+'/test/'):
        os.makedirs(str(dir_name)+'/test/')
    
    if not os.path.exists(str(dir_name)+'/train/images/'):
        os.makedirs(str(dir_name)+'/train/images/')
    if not os.path.exists(str(dir_name)+'/train/labels/'):
        os.makedirs(str(dir_name)+'/train/labels/')

    if not os.path.exists(str(dir_name)+'/val/images/'):
        os.makedirs(str(dir_name)+'/val/images/')
    if not os.path.exists(str(dir_name)+'/val/labels/'):
        os.makedirs(str(dir_name)+'/val/labels/')

    if not os.path.exists(str(dir_name)+'/test/images/'):
        os.makedirs(str(dir_name)+'/test/images/')
    if not os.path.exists(str(dir_name)+'/test/labels/'):
        os.makedirs(str(dir_name)+'/test/labels/') 
    return

if __name__ == "__main__":
    dir_name = "MyPCBdataset" #這裡放置想要資料集名稱
    # 開始轉換
    all_convert()
    create_dir1(dir_name)
    create_dir2(dir_name)
    total_txt = os.listdir(txt_file_path)
    num_txt = len(total_txt)
    list_all_txt = range(num_txt) # 範圍 range(0,num)

    # 資料集比例置換
    num_train = int(num_txt * train_percent)
    num_val = int(num_txt * val_percent)
    num_test = int(num_txt * test_percent)

    # 將資料編號陣列隨機取出特定比例的train資料，剩下的資料val+test
    train = random.sample(list_all_txt,num_train)
    val_test = [i for i in list_all_txt if not i in train]
    # 再從val_test取出特定比例的val資料，剩下就是test
    val = random.sample(val_test,num_val)

    print(f"訓練集數目:{len(train)}\t驗證集數目:{len(val)}\t測試集數目:{len(val_test)-len(val)}")

    for i in list_all_txt:
        name = total_txt[i][:-4]
        srcImage = images_file_path + name + ".jpg"
        srcLabel = txt_file_path + name + ".txt"

        if i in train:
            dst_train_Image = str(dir_name)+'/images/train/' + name + ".jpg"
            dst_train_Label = str(dir_name)+'/labels/train/' + name + ".txt"
            shutil.copyfile(srcImage,dst_train_Image)
            shutil.copyfile(srcLabel,dst_train_Label)

            dst_train_Image = str(dir_name)+'/train/images/' + name + ".jpg"
            dst_train_Label = str(dir_name)+'/train/labels/' + name + ".txt"
            shutil.copyfile(srcImage,dst_train_Image)
            shutil.copyfile(srcLabel,dst_train_Label)
        elif i in val:
            dst_val_Image = str(dir_name)+'/images/val/' + name + ".jpg"
            dst_val_Label = str(dir_name)+'/labels/val/' + name + ".txt"
            shutil.copyfile(srcImage,dst_val_Image)
            shutil.copyfile(srcLabel,dst_val_Label)

            dst_val_Image = str(dir_name)+'/val/images/' + name + ".jpg"
            dst_val_Label = str(dir_name)+'/val/labels/' + name + ".txt"
            shutil.copyfile(srcImage,dst_val_Image)
            shutil.copyfile(srcLabel,dst_val_Label)            
        else:
            dst_test_Image = str(dir_name)+'/images/test/' + name + ".jpg"
            dst_test_Label = str(dir_name)+'/labels/test/' + name + ".txt"
            shutil.copyfile(srcImage,dst_test_Image)
            shutil.copyfile(srcLabel,dst_test_Label)   

            dst_test_Image = str(dir_name)+'/test/images/' + name + ".jpg"
            dst_test_Label = str(dir_name)+'/test/labels/' + name + ".txt"
            shutil.copyfile(srcImage,dst_test_Image)
            shutil.copyfile(srcLabel,dst_test_Label)   

    shutil.rmtree(txt_file_path)         