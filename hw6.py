import cv2
import numpy as np
import os

def run_length_encoding(seq):
    compressed = []
    new_img = []
    temp = []
    count = 1
    for i in range(len(seq)-1):
        if(count==1):
            new_img.append(seq[i])
        if seq[i] == seq[i+1]:
            count = count + 1
            if i == len(seq) - 2:
                new_img.append(seq[i])
                compressed.append(count)
        else:
            compressed.append(count)
            count = 1
    if not(seq[len(seq)-1] == seq[len(seq)-2]):
        new_img.append(seq[len(seq)-1])
        compressed.append(1)
    return compressed, new_img
    # for i in range(len(compressed)-1):
    #     temp.append(compressed[i])
    #     temp.append(new_img[i])
    # return temp

def run_length_decoding(compressed, new_img):
    # compressed = []
    # new_img = []
    # sizes =int(seq.size/2)
    # for i in range(sizes):
    #     compressed.append(seq[2*i])
    #     new_img.append(seq[2*i+1])
    rec_img = []
    for i in range(len(compressed)):
        for j in range(compressed[i]):
            rec_img.append(new_img[i])
    return rec_img

def one_to_three_D(seq, img_H, img_W):
    arr_seq = np.array(seq)
    three_D_seq = arr_seq.reshape((img_H, img_W))
    return three_D_seq

average_compression_ratio = 0
names_of_file = ['img1.bmp', 'img2.bmp', 'img3.bmp']
for i in range(3):
    filename = names_of_file[i]
    original_size = os.path.getsize(filename)
    print("original_size:", original_size)
    img = cv2.imread(filename)
    subname = filename[:-4]
    H, W = img.shape[:2]
    b, g, r = cv2.split(img)
    f_b = b.flatten()
    f_g = g.flatten()
    f_r = r.flatten()

    num_b, value_b = run_length_encoding(f_b)
    num_g, value_g = run_length_encoding(f_g)
    num_r, value_r = run_length_encoding(f_r)
    #num_test, value_test = run_length_encoding(test)

    img_shp = [H, W]
    np.savez(subname+'.npz', a=img_shp, b=num_b, c=value_b, d=num_g, e=value_g, f=num_r, g=value_r)
    compressed_size = os.path.getsize(subname+'.npz')
    print("compressed_size:", compressed_size)
    print("compression_ratio:", original_size / compressed_size)
    average_compression_ratio = average_compression_ratio + (original_size / compressed_size)
    myArch = np.load(subname+'.npz')
    back_H = myArch['a'][0]
    back_W = myArch['a'][1]
    back_num_b = myArch['b']
    back_value_b = myArch['c']
    back_num_g = myArch['d']
    back_value_g = myArch['e']
    back_num_r = myArch['f']
    back_value_r = myArch['g']

    dec_b = run_length_decoding(back_num_b, back_value_b)
    dec_g = run_length_decoding(back_num_g, back_value_g)
    dec_r = run_length_decoding(back_num_r, back_value_r)
    bbb = one_to_three_D(dec_b, back_H, back_W)
    ggg = one_to_three_D(dec_g, back_H, back_W)
    rrr = one_to_three_D(dec_r, back_H, back_W)
    merged = cv2.merge([bbb, ggg, rrr])
    cv2.imwrite(subname+'_(1).bmp', merged)
    # cv2.imshow("Merged", merged)
    # cv2.waitKey(0)
average_compression_ratio /= 3
print("average_compression_ratio:", average_compression_ratio)
