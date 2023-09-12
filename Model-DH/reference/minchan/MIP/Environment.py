import numpy as np


class Job():
    def __init__(self, block, index, type, origin, destination, date):
        self.block = block
        self.index = index
        # Inbound : QC --> YC / Outbound : YC --> QC
        self.type = type
        ## Origin과 Destination은 2차원 좌표값이므로 (1x2) 행렬
        self.origin = origin
        self.destination = destination
        self.dueDate = 0
        self.releasedDate = 0

        if self.type == "In":
            self.dueDate = 0
            self.releasedDate = date
            self.columninYC = destination[1]
        elif self.type == "Out":
            self.dueDate = date
            self.releasedDate = 0
            self.columninYC = origin[1]
        else:
            print("Job type이 이상합니다. (In or Out이 아님)")

class YT():
    def __init__(self, index, initial_location, movingTimePerUnit_YT):
        self.index = index
        self.initial_location = initial_location
        self.movingTimePerUnit_YT = movingTimePerUnit_YT

class Parameter_data():
    # Job_Set은 2차원 matrix이며, 각 행은 block을 각 열은 job index를 의미함t
    # YT_Set은 1차원 matrix이며 YT의 Set임
    # CraneNumber_Set은 1차원 matrix, 각 block당 YC의 숫자를 의미함
    # movingTimePerUnit_YC는 YC의 단위거리당 이동시간임 (상수)
    # maximum_Column_Set_YC는 1차워 maxtrix, 각 Block의 최대 Column
    # safetyDistance_YC는 YC간의 안전거리(상수)를 의미함
    # pj_Set은 각 Job에 대한 YC의 Processing time을 의미하며, Dimension은 Job_Set과 같음
    def __init__(self, Job_b_Set, YT_Set, CraneNumber_Set, maximum_Column_Set_YC , safetyDistance_YC, movingTimePerUnit_YC , pj_Set):
        self.Job_b_Set = Job_b_Set
        self.YT_Set = YT_Set
        self.CraneNumber_Set = CraneNumber_Set
        self.movingTimePerUnit_YC = movingTimePerUnit_YC
        self.maximum_Column_Set_YC = maximum_Column_Set_YC
        self.safetyDistance_YC = safetyDistance_YC
        self.pj_Set = pj_Set

    ## Find 𝛥_(𝑖,𝑗,𝑣,𝑤)^𝑏 & 𝛩 (최소 교차간섭 시간, 경우의 수 집합)
     # delta --> 𝛥_(𝑖,𝑗,𝑣,𝑤)^𝑏 --> 5차원 행렬 --> (b,i,j,v,w)
     # theta --> 𝛩 --> 3차원 행렬 --> (블록 수 x 간섭발생 경우의 수 x 4(i,j,v,w))
        # 검증완료
        maximumNumberofJob = 0
        for i in range(Job_b_Set.shape[0]):
            if Job_b_Set[i] is not None:
                if maximumNumberofJob < Job_b_Set[i].size:
                    maximumNumberofJob = Job_b_Set[i].size

        self.delta = np.zeros((int(Job_b_Set.shape[0]), maximumNumberofJob, maximumNumberofJob, int(np.max(self.CraneNumber_Set)), int(np.max(self.CraneNumber_Set))))
        self.theta = np.empty((Job_b_Set.shape[0]), dtype=object)

        for b in range(Job_b_Set.shape[0]):
            craneNumber = CraneNumber_Set[b]
            theta = np.array([])
            if Job_b_Set[b] is not None:
                # index i 가 j보다 Job을 먼저할 때,
                for i in range(self.Job_b_Set[b].size):
                    for j in range(self.Job_b_Set[b].size):
                        # i가 j보다 작업을 먼저하는 경우이며, v와 w는 각각 i와 j를 위해 할당된 crane
                        if i != j:
                            b_i = self.Job_b_Set[b][i].columninYC
                            b_j = self.Job_b_Set[b][j].columninYC
                            for v in range(int(self.CraneNumber_Set[b])):
                                for w in range(int(self.CraneNumber_Set[b])):
                                    delta_v_w = abs(w-v)*(self.safetyDistance_YC+1)
                                    # 물리적으로 YC가 작업을 할당가능해야 함 (안전거리를 고려했을 떄, YC가 도달가능한 위치)
                                    if b_i >= v * self.safetyDistance_YC and b_j >= w * self.safetyDistance_YC:
                                        if b_i <= self.maximum_Column_Set_YC[b] - (self.CraneNumber_Set[b] - v - 1) * self.safetyDistance_YC and b_j <= self.maximum_Column_Set_YC[b] - (self.CraneNumber_Set[b] - w - 1) * self.safetyDistance_YC:
                                            if b_i > (b_j - delta_v_w) and v < w:
                                                ijvw = (b_i - b_j + delta_v_w) * self.movingTimePerUnit_YC
                                                self.delta[b][i][j][v][w] = ijvw
                                                if theta.size == 0:
                                                    theta = np.array([[i,j,v,w]])
                                                else:
                                                    theta = np.concatenate((theta, np.array([[i,j,v,w]])), axis = 0)
                                            elif b_i < (b_j - delta_v_w) and v > w:
                                                ijvw = (b_j - b_i + delta_v_w) * self.movingTimePerUnit_YC
                                                self.delta[b][i][j][v][w] = ijvw
                                                if theta.size == 0:
                                                    theta = np.array([[i,j,v,w]])
                                                else:
                                                    theta = np.concatenate((theta, np.array([[i,j,v,w]])), axis = 0)

                self.theta[b] = theta








