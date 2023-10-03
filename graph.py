import heapq
import json

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
        
    def dijkstra(self,start):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start] = 0
        priority_queue = [(0,start)]
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            if current_distance > distances[current_vertex]:
                continue
            
            for neighbor, weight in self.edges[current_vertex]:
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
                    
                
        return distances
    


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
                distance = stations[i]["distance_to_next"]
                self.graph.add_edge(station1, station2, distance)
        
    
if __name__ == "__main__":
    subway = SubwaySystem(r"C:\Users\xk.DESKTOP-3CJ0BFJ\Desktop\OSproject\setfile.json")
    station1 = input("请输入入站口:")
    print('\n')
    station2 = input("请输入出站口:")
    shortest_path = subway.graph.dijkstra(station1)
    print('从' , station1 , '到' , station2 , '的最短路径是:' , shortest_path[station2] )