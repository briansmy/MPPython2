import Traversals
from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys


def modified_bfs(graph, isp, list_clients, bandwidths, tolerances):
    paths = {}

    graph_size = len(graph)
    priors = [-1] * graph_size
    # search_queue = deque()
    # search_queue.append(isp)

    # Replace collections.deque with heapq PriorityQueue
    search_queue = PriorityQueue()
    search_queue.add_task(task=isp)
    max_band = max(bandwidths.values)
    while search_queue.nonEmpty():
        node = search_queue.pop_task()
        for neighbor in graph[node]:
            if priors[neighbor] == -1 and neighbor != isp:
                priors[neighbor] = node
                priority = max_band-bandwidths[neighbor]
                search_queue.add_task(task=neighbor, priority=priority)
    for client in list_clients:
        path = []
        current_node = client
        while current_node != -1:
            path.append(current_node)
            current_node = priors[current_node]
        path = path[::-1]
        paths[client] = path
    return paths


# Priority queue class built from heapq
# implementation adapted from the example 8.5.2 in the heapq docs
# https://docs.python.org/3.6/library/heapq.html
class PriorityQueue:

    def __init__(self):
        self.items = []
        self.entry_finder = {}
        self.removed = "<removed-task>"
        self.counter = 0

    # Priority in this case will be (1/bandwidth)
    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.remove_task(task)
        self.counter += 1
        count = self.counter
        entry = (priority, count, task)
        self.entry_finder[task] = entry
        heapq.heappush(self.items, entry)

    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.removed

    def pop_task(self):
        while self.items:
            priority, count, task = heapq.heappop(self.items)
            if task is not self.removed:
                del self.entry_finder[task]
                return task
        raise KeyError("pop from an empty priority queue")

    def nonEmpty(self):
        length = len(self.items)
        return length > 0


class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """

        paths, bandwidths, priorities = {}, {}, {}

        # pull same path data as part one
        list_clients = self.info.get("list_clients")
        bandwidths = self.info.get("bandwidths")
        tolerances = self.info.get("alphas")
        paths = modified_bfs(self.graph, self.isp, list_clients, bandwidths, tolerances)

        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return paths, bandwidths, priorities
