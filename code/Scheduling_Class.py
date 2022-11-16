class Student:
    # name = 이름
    # sid = 학번
    # pos = 활동 가능 시간 리스트
    def __init__(self, name, sid, pos):
        self.name = name
        self.sid = sid
        self.pos = pos

class Schedule:
    # equality_flag = 균등 분배 여부
    # mini = 최소 필요 인원
    # maxi = 최대 필요 인원
    # need = 전체 시간대 정수 2차원 배열
    def __init__(self, equality_flag, mini, maxi, need):
        self.equality_flag = equality_flag
        self.mini = mini
        self.maxi = maxi
        self.need = need