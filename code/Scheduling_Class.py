class Student:
    # name = 이름
    # sid = 학번
    # pos = 활동 가능 시간을 30분 단위로 자른 표
    def __init__(self, name, sid, pos):
        self.name = name
        self.sid = sid
        self.pos = pos

class Schedule:
    # equality_flag = 균등 분배 여부
    # unit_time = 단위 시간
    # mini = 최소 필요 인원
    # maxi = 최대 필요 인원
    # need = 전체 시간대 (시작 분, 끝 분) 튜플의 리스트
    def __init__(self, equality_flag, duplication_flag, unit_time, mini, maxi, need):
        self.equality_flag = equality_flag
        self.duplication_flag = duplication_flag
        self.unit_time = unit_time
        self.mini = mini
        self.maxi = maxi
        self.need = need
