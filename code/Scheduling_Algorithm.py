from Network_Flow import *
from Scheduling_Class import *

# 입력 파싱 후 호출할 함수
def scheduling(student_list, schedule):
    if not schedule.equality_flag:
        return all_scheduling(student_list)
    else:
        return equal_scheduling(student_list, schedule)

def equal_scheduling(student_list, schedule):
    # make graph

    # scheduling using dinic

    # save result
    None

def all_scheduling(student_list):
    student_num = len(student_list)
    rn = len(student_list[0].pos)
    cn = len(student_list[0].pos[0])
    # 학생 시간표 형태와 동일한 형태의 결과물
    # 해당 시간에 모두가 공강이면 True로 나타난다.
    ret = [[] for i in range(rn)]
    for r in ret:
        for j in range(cn):
            r.append(True)
    for i in range(student_num):
        for j in range(rn):
            for k in range(cn):
                if not student_list[i].pos[j][k]:
                    ret[i][j] = False
    return ret