class Student:
    # name = 이름
    # sid = 학번
    # mini = 최소 횟수
    # maxi = 최대 횟수
    # pos = 활동 가능 시간 리스트
    def __init__(self, name, sid, mini, maxi, pos):
        self.name = name
        self.sid = sid
        self.mini = mini
        self.maxi = maxi
        self.pos = pos

class Schedule:
    # mini = 최소 필요 인원
    # maxi = 최대 필요 인원
    # st = 시작 시간
    # fn = 종료 시간
    def __init__(self, mini, maxi, st, fn):
        self.mini = mini
        self.maxi = maxi
        self.st = st
        self.fn = fn