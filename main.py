#!/usr/bin/python3

import os
import os.path
import glob
import time
from SSIM import imgMatch
from convert_to_html import convertToHtml, sortTable
import cv2
import pandas as pd


#mtl渲染结果文件夹，根目录下scene文件夹
origin_path = os.path.join(os.getcwd(), "origin")
#OSL渲染结果文件夹 根目录下transformed文件夹
trans_path = os.path.join(os.getcwd(), "transformed")
#vrscene存放文件夹 根目录下origin文件夹
scene_path = os.path.join(os.getcwd(), "scene")

# print(origin_path)
#调用命令
render_cmd = '''vray -sceneFile={type}{scene_num}.vrscene -imgFile="{path}/{scene_num}.png" -displaysRGB=2 -display=0'''
#转换命令
convert_cmd = '''vrayMtlConverter.exe "./scene/origin{scene_num}.vrscene" "./scene/transformed{scene_num}.vrscene"'''

#用于np表格中图片的插入
img_label = '''<br><img src="{img_path}" height="300" width="300"/>'''


def rename():
    #统一scene文件夹命名
    rootdir = r".\scene"  # 指明被遍历的文件夹
    count = 0
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:  # 文件名
            if filename[0:11] == "transformed":
                os.remove(os.path.join(parent, filename))
            else:
                os.rename(os.path.join(parent, filename), os.path.join(parent,"origin" + str(count) + filename[-8:]))
                # 统一重命名 origin[].vrscene
                count += 1

    # 初始化表格
def initTable():
    file_name = []
    mtl_time = []
    osl_time = []
    SSIM = []
    time_ratio = []
    html_table = [file_name, mtl_time, osl_time, SSIM, time_ratio]
    title = ["文件名", "mtl时间", "osl时间", "SSIM测试", "耗时比"]
    return html_table, title



html_table, title = initTable()


    #计算scene场景文件数
def walkFolders(folder):
    filesCount = 0
    folders = os.listdir(folder)
    for item in folders:
        filesCount = filesCount + 1
    return filesCount

    #场景转换
def convertScene(num):
    cmd = convert_cmd.format(scene_num=num, path=trans_path)
    print(cmd)
    print(os.getcwd())
    os.system(cmd)

    # mtl渲染出图并返回时间
def originRendering(num):
    cmd = render_cmd.format(type="origin", scene_num=num, path=origin_path)
    start = time.perf_counter()
    os.system('cd ./scene && ' + cmd)
    end = time.perf_counter()
    delta_time = end - start
    print("---MTL场景渲染调用时间为：" + str(delta_time))
    return end - start

    # osl渲染出图并返回时间
def transRendering(num):
    cmd = render_cmd.format(type="transformed", scene_num=num, path=trans_path)
    start = time.perf_counter()
    os.system('cd ./scene && ' + cmd)
    end = time.perf_counter()
    delta_time = end - start
    print("---OSL场景渲染调用时间为：" + str(delta_time))
    return end - start

    #测试指定序号的mtl场景，逐步执行转化vrscene到osl-分别渲染两张图并计时-ssim测试
def autoTest(scene_num):
    #mtl->osl
    convertScene(scene_num)
    #渲染计时
    mtl_time = originRendering(scene_num)
    osl_time = transRendering(scene_num)
    #时间比
    time_ratio = osl_time / mtl_time
    print(time_ratio)
    #生成图像label
    imfil1 = "{path}/{scene_num}.png".format(path=origin_path, scene_num=scene_num)
    imfil2 = "{path}/{scene_num}.png".format(path=trans_path, scene_num=scene_num)
    # print(imfil1)
    # print(imfil2)
    img1 = img_label.format(img_path=imfil1)
    img2 = img_label.format(img_path=imfil2)
    #html-stable生成
    html_table[0].append(scene_num)
    html_table[1].append(str(mtl_time) + img1)
    html_table[2].append(str(osl_time) + img2)
    html_table[3].append(imgMatch(imfil1, imfil2))
    html_table[4].append(time_ratio)

#批量修改scene下所有文件名
rename()

#测试scene文件夹下所有文件
for i in range(walkFolders(scene_path)):
    print("一共有{num}个文件需要处理，正在处理第{n}个文件".format(num=walkFolders(scene_path), n=i+1))
    autoTest(i)


#生成html表格
convertToHtml(html_table, title)
sortTable()



