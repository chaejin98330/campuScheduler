import sys
import json
import os
from Scheduling_Class import *
from Scheduling_Algorithm import *
from Scheduling_Output import *

#입력 인자들
time_length = 0 #시간대 길이
time_number = 0 #시간대 개수
duplication_flag = False    #중복 허용
all_possible_flag = False   #모두 되는 시간 찾기
equality_flag = False   #균등 분배
people_min = None  #최소 사람수
people_max = None  #최대 사람수
groupname = ""  #그룹 이름

time_list = []

#입력 인자 처리
for i in range(len(sys.argv)):
    if sys.argv[i] == "-l":                 #시간대 길이는 분 단위로 해주세요. 30분이면 30, 1시간이면 60, ...
        time_length = int(sys.argv[i+1])
    elif sys.argv[i] == "-n":               # -n 뒤에 개수 (요일 시작시간 끝시간) * 개수만큼 나옴
        time_number = int(sys.argv[i+1])    # 0=월, 1=화, 2=수, 3=목, 4=금, 9.5=9시반, 16.5 = 4시반
        i += 1                              # 예를 들어 -n 3 0 9.5 10.5 1 9.5 14.5 2 10 16이면 시간대가 3개, 월요일 9시반~10시반, 화요일 9시반~14시반, 수요일 10시~16시
        for j in range(time_number):        # 근데 이게 시간대 길이의 배수가 아니면 UI단계에서 컷해주세요. 예를 들어 시간대 길이는 1시간인데 월 9시~9시반 같은 경우.
            day = int(sys.argv[i+1])
            start = float(sys.argv[i+2])
            end = float(sys.argv[i+3])
            time_list.append(tuple([int(day*24*60 + start*60), int(day*24*60 + end*60)]))
            i += 3
    elif sys.argv[i] == "-r":
        duplication_flag = True
    elif sys.argv[i] == "-a":
        all_possible_flag = True
    elif sys.argv[i] == "-e":
        equality_flag = True
    elif sys.argv[i] == "-p":
        people_min = int(sys.argv[i+1])
    elif sys.argv[i] == "-P":
        people_max = int(sys.argv[i+1])
    elif sys.argv[i] == "-g":
        groupname = sys.argv[i+1]

if people_min == None and people_max == None:   # 만약 스케줄변수에 최소인원 최대인원이 하나도 지정 안됐으면 default값으로 최소인원 1 지정
    people_min = 1

#스케줄 클래스 만들기
schedule = Schedule(equality_flag, time_length, people_min, people_max, time_list)


#그룹에 속하는 학생들 json 읽고 클래스화하여 list에 추가
student_list = []
file_list = os.listdir("../data/"+groupname) #그룹 폴더에 json파일만 있다고 가정하겠습니다.
for i in range(len(file_list)):
    with open("../data/"+ groupname + "/" + file_list[i], "r") as f:
        json_data = json.load(f)
    name = json_data['name']
    id = json_data['id']
    timetable = json_data['timetable']
    student = Student(name, id, timetable)
    student_list.append(student)


# 알고리즘 시행
success, result = scheduling(student_list, schedule)

# 알고리즘 결과를 엑셀(csv) 형식으로 파싱
if success:
    printExcel(result, student_list)
else:
    print("There is no available schedule.")
