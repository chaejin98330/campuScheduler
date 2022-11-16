from Network_Flow import *
from Scheduling_Class import *

# 입력 파싱 후 호출할 함수
def scheduling(student_list, schedule):
    if not schedule.equality_flag:
        return all_scheduling(student_list)
    else:
        return equal_scheduling(student_list, schedule)

def min2idx(minute):
    minute -= minute%30
    day = 24 * 60
    return (minute-((minute//day)*day)-60*9)//30 ,minute//day

def simulation(student_list, schedule, l, r):
    # initialize
    n = len(student_list)
    m = len(schedule.need)
    dinic = Dinic(n+m+10)
    dinic.set_S1(n+m+1); dinic.set_T1(n+m+2)
    dinic.set_S2(n+m+3); dinic.set_T2(n+m+4)

    # add edge
    for i in range(1,n+1):
        dinic.add_edge(dinic.S1, i, l, r)
    for i in range(n+1,n+m+1):
        dinic.add_edge(i, dinic.T1, schedule.mini, schedule.maxi)
    for i in range(n):
        for j in range(m):
            tf = True
            sr, sc = min2idx(schedule.need[j][0])
            fr, fc = min2idx(schedule.need[j][1])
            for y in range(sr,fr+1):
                if not student_list[i].pos[y][sc]:
                    tf = False
                    break
            if tf:
                dinic.add_edge(i+1, n+1+j, 0, 1)
    dinic.add_edge(dinic.T1, dinic.S1, 0, dinic.INF)

    # check validity
    flw = dinic.get_flw(dinic.S2, dinic.T2)
    if flw != dinic.lsum:
        return False, None

    #make result
    ret = [[] for i in range(n)]
    for i in range(1,n+1):
        for nv in dinic.lst[i]:
            if n+1 <= nv.nxt <= n+m and nv.flw>0:
                ret[i-1].append(schedule.need[nv.nxt-n-1])
    return True, ret

def equal_scheduling(student_list, schedule):
    # divide schedule.need into unit_time
    need = []
    unit_time = schedule.unit_time
    for v in schedule.need:
        t = (v[1]-v[0])//unit_time
        cur = v[0]
        nxt = cur + unit_time
        for i in range(t):
            need.append((cur, nxt))
            cur += unit_time
            nxt += unit_time
    schedule.need = need

    # scheduling using dinic
    if schedule.maxi is None:
        schedule.maxi = len(student_list)
    INF = len(schedule.need)
    tf = False
    ret = None
    st = 0; fn = INF
    l = 0
    while st<=fn:
        mid = (st+fn)//2
        _tf, _ret = simulation(student_list, schedule, mid, INF)
        if _tf:
            tf, ret = _tf, _ret
            l = mid
            st = mid+1
        else:
            fn = mid-1

    if not tf:
        return tf, ret

    st = l; fn = INF
    r = INF
    while st<=fn:
        mid = (st+fn)//2
        _tf, _ret = simulation(student_list, schedule, l, mid)
        if _tf:
            tf, ret = _tf, _ret
            r = mid
            fn = mid-1
        else:
            st = mid+1

    # return result
    return tf, ret

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
    cnt = rn * cn

    for i in range(student_num):
        for j in range(rn):
            for k in range(cn):
                if not student_list[i].pos[j][k] and ret[j][k]:
                    ret[j][k] = False
                    cnt -= 1
    if cnt == 0:
        return False, None
    return True, ret