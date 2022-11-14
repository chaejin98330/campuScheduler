from collections import deque

class Edge:
    def __init__(self, _nxt, _rev, _cap, _flw, _lwr):
        self.nxt = _nxt
        self.rev = _rev
        self.cap = _cap
        self.flw = _flw
        self.lwr = _lwr

class Dinic:
    # constructor
    def __init__(self, _n):
        self.n = _n
        self.lst = [[] for i in range(_n)]
        self.INF = int(1e9)
        self.dist = [self.INF for i in range(_n)]
        self.work = [0 for i in range(_n)]
        self.S1 = self.S2 = self.T1 = self.T2 = 0
        self.lsum = 0

    # set method
    def set_S1(self, _S1):
        self.S1 = _S1
    def set_S2(self, _S2):
        self.S2 = _S2
    def set_T1(self, _T1):
        self.T1 = _T1
    def set_T2(self, _T2):
        self.T2 = _T2

    def get_lsum(self):
        return self.lsum

    # to add new edge
    def add_edge(self, u, v, l, r):
        self.lst[u].append(Edge(v, len(self.lst[v]), r-l, 0, l))
        self.lst[v].append(Edge(u, len(self.lst[u])-1, 0, 0, 0))
        if l>0:
            self.lsum += l
            self.lst[self.S2].append(Edge(v, len(self.lst[v]), l, 0, 0))
            self.lst[v].append(Edge(self.S2, len(self.lst[self.S2])-1, 0, 0, 0))
            self.lst[u].append(Edge(self.T2, len(self.lst[self.T2]), l, 0, 0))
            self.lst[self.T2].append(Edge(u, len(self.lst[u])-1, 0, 0, 0))

    def bfs(self, S, T):
        for i in range(self.n):
            self.dist[i] = -1
        Q = deque([])
        Q.append(S); self.dist[S] = 0
        while len(Q)>0:
            v = Q.popleft()
            for nv in self.lst[v]:
                if self.dist[nv.nxt]==-1 and nv.cap-nv.flw>0:
                    Q.append(nv.nxt)
                    self.dist[nv.nxt] = self.dist[v]+1
        return self.dist[T]!=-1

    def dfs(self, v, fn, flw):
        if v==fn:
            return flw
        for i in range(self.work[v], len(self.lst[v])):
            nv = self.lst[v][i]
            if self.dist[nv.nxt] == self.dist[v]+1 and nv.cap-nv.flw>0:
                df = self.dfs(nv.nxt, fn, min([flw, nv.cap-nv.flw]))
                if df>0:
                    self.lst[v][i].flw +=df
                    self.lst[nv.nxt][nv.rev].flw -= df
                    return df
            self.work[v] += 1
        return 0

    def get_flw(self, S, T):
        ret = 0
        while self.bfs(S, T):
            for i in range(self.n):
                self.work[i] = 0
            while True:
                f = self.dfs(S, T, self.INF)
                if f==0:
                    break
                ret += f
        return ret