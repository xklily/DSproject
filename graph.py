import heapq
import json
from collections import deque

class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}
    
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        if vertex not in self.edges:
            self.edges[vertex] = []
            
    def add_edge(self,start,end,weight):
        self.add_vertex(start)
        self.add_vertex(end)
        self.edges[start].append((end,weight))
        self.edges[end].append((start,weight))
        
    def get_distance_between_stations(self,station1,station2):
        for neighboor,weight in self.edges[station1]:
            if neighboor==station2:
                return weight
        return float('inf')
    
    def if_transfer_station(self,station):
        if len(self.edges[station])>=3:
            return True
        else:return False
        
    def dijkstra(self, start, end):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous = {}

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.edges[current_vertex]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = end
        while current:
            path.insert(0, current)
            current = previous.get(current)

        return distances[end], path

    


class SubwaySystem:
    def __init__(self,config_file):
        with open(config_file,"r",encoding="utf-8") as f:
            self.config = json.load(f)
        self.stations = self.config["stations"]
        self.lines = self.config["lines"]
        self.graph = Graph()
        
        for station in self.stations.keys():
            self.graph.add_vertex(station)
            
        for line in self.lines:
            stations = line["stations"]
            for i in range(len(stations) - 1):
                station1 = stations[i]["name"]
                station2 = stations[i + 1]["name"]
                try:
                    distance = stations[i]["distance_to_next"]
                except KeyError as e:
                    print(f"KeyError: {e}, station: {station1}")
                self.graph.add_edge(station1, station2, distance)
    def getline(self,station):
        for line in self.lines:
            for node in line["stations"]:
                if node==station:
                    return line
    
    def find_min_transfer_route(self, start, end):
        visited = set()
        queue = deque([(start, [])])

        while queue:
            current_station, current_route = queue.popleft()
            visited.add(current_station)

            for neighbor, _ in self.graph.edges[current_station]:
                if neighbor == end:
                    return current_route + [neighbor]  # 只返回站点名称

                if neighbor not in visited:
                    # 考虑换乘的情况，判断是否在同一条线路上
                    if ~self.graph.if_transfer_station(current_station) :current_line = self.getline(current_station)
                    if ~self.graph.if_transfer_station(neighbor) :next_line = self.getline(neighbor)
                    if current_line != next_line:
                        queue.append((neighbor, current_route + [current_station, neighbor]))
                    else:
                        queue.append((neighbor, current_route + [current_station]))
                
def expense(length):
    if 0<length<=6:
        return 3
    elif 6<length<=12:
        return 4
    elif 12<length<=22:
        return 5
    elif 22<length<=32:
        return 6
    elif 32<length<=52:
        return 7
    elif 52<length<=72:
        return 8
    elif 72<length<=92:
        return 9
        
    
if __name__ == "__main__":
    subway = SubwaySystem(r"C:\Users\xk.DESKTOP-3CJ0BFJ\Desktop\DSproject\DSproject\setfile.json")
    station1 = input("请输入入站口:")
    station2 = input("请输入出站口:")
    min_transfer_route = subway.find_min_transfer_route(station1, station2)
    #print(f'从 {station1} 到 {station2} 的最短路径是: {shortest_distance}公里')
    print('经过的地铁站:')
    for temp in min_transfer_route:
        print(temp)
    #print(f'所用价格是:{expense(shortest_distance)}元')