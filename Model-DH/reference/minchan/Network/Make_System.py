import numpy as np
import random

class YT:
    def __init__(self, index, initial_location, speed):
        self.index = index
        self.location = initial_location
        self.speed = speed
        self.destination = None
        self.job_assignment = None

class YC:
    def __init__(self, index, block, column, width, safety_distance, processingTime):
        self.block = block
        self.index = index
        self.column = column
        self.safety_distance = safety_distance
        self.Scheduled_JobList = np.array([], dtype=object)
        self.Timeline_CompletionTime = np.array([])
        self.processintTime = processingTime
        self.width = width
        self.timeLine = None


class Job:
    def __init__(self, block, index, type, origin, destination, date):
        self.block = block
        self.index = index
        ## Inbound : QC --> YC / Outbound : YC --> QC
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

class Port_System:
    def __init__(self, maximum_row, maximum_column, block_List, YT_List, YC_List, JobList):
        self.maximum_row = maximum_row
        self.maximum_column = maximum_column
        self.YT_List = YT_List
        self.block_List = block_List
        self.YC_List = YC_List
        self.JobList = JobList




















