import argparse
import math
import numpy as np
from PIL import Image
import json
# for debug
#import pandas as pd

# 인스턴스 생성
def run(argv):

    # 인자값 등록  이름, 학번, 이미지 파일명(image directory안에 있는 파일명 그대로 쓰면 됨), 소속 그룹   ( ex) 홍길동 2022111111 2022111111_홍길동.jpg(확장자명까지 필요) 학생회 )
    #'name'
    #'id'
    #'file'
    #'group'
    name=argv[0]
    id=argv[1]
    file=argv[2]
    group=argv[3]

    # 이미지 불러오기, 흑백으로 변환
    file_path = file
    image = Image.open(file_path)
    image = image.convert('L')
    #image.show()
    image_pix = np.array(image)

    # 세로 길이 / 가로 길이
    length = image_pix.shape[0]
    width = image_pix.shape[1]
    #print(width, length)

    #for i in range(length):
    #    print(i, image_pix[i][5])

    # 사진의 불필요한 테두리 제거
    cut_top_bottom = math.floor(length / 300)
    cut_right_left = math.floor(width / 250)
    #print(cut_top_bottom, cut_right_left)
    croppedImage = image.crop((cut_right_left, cut_top_bottom, width - 1 - cut_right_left, length - 1 - cut_top_bottom))
    #croppedImage.show()
    crp_img_pix = np.array(croppedImage)
    crp_len = crp_img_pix.shape[0]
    crp_wid = crp_img_pix.shape[1]

    # for debug
    #df = pd.DataFrame(crp_img_pix)
    #df.to_csv('sample.csv',index=False)

    # 가로선, 세로선 위치 잡기 (각 가로선, 세로선 별로 경계선(총 2개)이 위치 하는 픽셀값 저장)
    ground_color = crp_img_pix[0][0]
    row_idx = []
    col_idx = []
    flag = 1
    for i in range(crp_wid):
        if flag:
            if crp_img_pix[0][i] < ground_color - 4 or crp_img_pix[0][i] > ground_color + 4:
                #element = [i]
                #row_idx.append(i)
                flag = 0
        else:
            if crp_img_pix[0][i] < ground_color - 4 or crp_img_pix[0][i] > ground_color + 4:
                continue
            else:
                #element.append(i)
                #row_idx.append(element)
                row_idx.append(i + 1)
                flag = 1

    flag = 1
    for i in range(crp_len):
        if flag:
            if crp_img_pix[i][0] < ground_color - 4 or crp_img_pix[i][0] > ground_color + 4:
                #element = [i]
                col_idx.append(i + 1)
                flag = 0
        else:
            if crp_img_pix[i][0] < ground_color - 4 or crp_img_pix[i][0] > ground_color + 4:
                continue
            else:
                #element.append(i)
                #col_idx.append(element)
                col_idx.append(i)
                flag = 1
    #row_idx.pop(0)
    #row_idx.append(crp_wid - 1)
    col_idx.pop(0)
    col_idx.append(crp_len - 1)
    """
    print(row_idx)
    print(col_idx)
    croppedImage = croppedImage.crop((59, 57, 874, 1800))
    croppedImage.show()
    """
    # 결과 값을 넣을 리스트를 초기화
    L = [True]*5
    res = []
    for i in range(26):
        res.append(L.copy())
    #print(res)

    # 시간대 별로 스케줄이 있는지 없는지 확인
    for i in range(len(col_idx)):
        if i % 2 == 0:
            col_pad = 2     # 약간 여유를 주기 위한 값
            check_len = math.floor((col_idx[i + 1] - col_idx[i]) / 8 * 3)       # 3/8 지점을 찾는다
        else:
            col_pad = -2
            check_len = -math.floor((col_idx[i] - col_idx[i - 1]) / 8 * 3)
        for j in range(len(row_idx)):
            col_pixel = col_idx[i] + col_pad
            row_pixel = row_idx[j] + 2
            #print(col_pixel, row_pixel)
            #print(crp_img_pix[col_pixel][row_pixel], ground_color, i, j, col_idx[i], col_pixel, row_pixel)
            if crp_img_pix[col_pixel][row_pixel] < ground_color - 6 or crp_img_pix[col_pixel][row_pixel] > ground_color + 6 or crp_img_pix[col_pixel+check_len][row_pixel] < ground_color - 6 or crp_img_pix[col_pixel+check_len][row_pixel] > ground_color + 6:
                #print(crp_img_pix[col_pixel][row_pixel], ground_color, i, j)
                res[i][j] = False

    #for i in range(26):
    #    print(i + 1, res[i])


    #croppedImage = croppedImage.crop((470, 59, 874, 1800))
    #croppedImage.show()

    json_object = {
        "name": name,
        "id": id,
        "timetable": res
    }

    output_file = name + "_" + id + ".json"

    with open("../data/" + group + "/" + output_file, 'w') as f:
        json.dump(json_object, f, indent = 2)