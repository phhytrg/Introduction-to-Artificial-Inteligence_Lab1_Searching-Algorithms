import math
from operator import ne
import time
from xmlrpc.client import Boolean

from Space import *
from Constants import *

def DFS(g:Graph, sc:pygame.Surface):
    print('Implement DFS algorithm')

    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    
    while(open_set):
        current = open_set.pop(0)
        currentNode = g.grid_cells[current]
        closed_set.append(current)
        if(currentNode != g.start):
            currentNode.set_color(yellow)
            g.draw(sc)
        if(g.is_goal(currentNode)):
            currentNode.set_color(purple)
            currentNode.draw(sc)
            break
        for neighbor in reversed(g.get_neighbors(currentNode)):
            if(neighbor.value not in closed_set):
                open_set.insert(0,neighbor.value)
                father[neighbor.value] = current
                neighbor.set_color(red)
                neighbor.draw(sc)
        
        if(currentNode != g.start):
            currentNode.set_color(blue)
            currentNode.draw(sc)

    #print path
    g.draw_path(sc,father)
    pygame.display.flip()
    

def BFS(g:Graph, sc:pygame.Surface):
    print('Implement BFS algorithm')
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    while(open_set):
        current = open_set.pop(0)
        currentNode = g.grid_cells[current]
        if(current == 47):
            a=[]
        if(currentNode != g.start):
            currentNode.set_color(yellow)
            g.draw(sc)
        
        closed_set.append(current)
        if(g.is_goal(currentNode)):
            currentNode.set_color(purple)
            g.draw(sc)
            break
        for neighbor in g.get_neighbors(currentNode):
            if(neighbor.value not in closed_set and neighbor.value not in open_set):
                open_set.append(neighbor.value)
                father[neighbor.value] = current
                neighbor.set_color(red)
                neighbor.draw(sc)
        
        if(currentNode != g.start):
            currentNode.set_color(blue)
            currentNode.draw(sc)

    #print path
    g.draw_path(sc,father)
    pygame.display.flip()


def getWeight(n1, n2) -> float:
    return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

def UCS(g:Graph, sc:pygame.Surface):
    print('Implement UCS algorithm')
    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100000]*g.get_len()
    cost[g.start.value] = 0
    while(open_set):
        current = min(open_set,key = open_set.get)
        if(current != g.start.value):
            g.grid_cells[current].set_color(yellow)
            g.draw(sc)
        if(current == g.goal.value):
            g.grid_cells[current].set_color(purple)
            g.grid_cells[current].draw(sc)
            break
        open_set.pop(current)
        closed_set.append(current)
        for neighbor in g.get_neighbors(g.grid_cells[current]):
            if(neighbor.value in closed_set):
                continue
            tentative_cost = cost[current] + getWeight(g.grid_cells[current], neighbor)
            if(neighbor.value not in open_set or tentative_cost < cost[neighbor.value]):
                cost[neighbor.value] = tentative_cost
                open_set[neighbor.value] = tentative_cost
                father[neighbor.value] = current
                if(neighbor not in open_set):
                    neighbor.set_color(red)
                    neighbor.draw(sc)
        if(current != g.start.value):
            g.grid_cells[current].set_color(blue)
            g.draw(sc)
            
    g.draw_path(sc,father)
    pygame.display.flip()


def AStar(g:Graph, sc:pygame.surface):
    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100000]*g.get_len()
    cost[g.start.value] = 0
    while(open_set):
        current = min(open_set,key = open_set.get)
        if(current != g.start.value):
            g.grid_cells[current].set_color(yellow)
            g.draw(sc)
        if(current == g.goal.value):
            g.grid_cells[current].set_color(purple)
            g.grid_cells[current].draw(sc)
            break
        open_set.pop(current)
        closed_set.append(current)
        for neighbor in g.get_neighbors(g.grid_cells[current]):
            if(neighbor.value in closed_set):
                continue
            tentative_g_cost = cost[current] + getWeight(g.grid_cells[current], neighbor)
            f_cost = tentative_g_cost + getWeight(neighbor, g.goal)
            if(neighbor.value not in open_set or tentative_g_cost < cost[neighbor.value]):
                cost[neighbor.value] = tentative_g_cost
                open_set[neighbor.value] = f_cost
                father[neighbor.value] = current
                if(neighbor not in open_set):
                    neighbor.set_color(red)
                    neighbor.draw(sc)
        if(current != g.start.value):
            g.grid_cells[current].set_color(blue)
            g.draw(sc)
            
    g.draw_path(sc,father)


def GreedyBFS(g:Graph, sc:pygame.surface):
    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    while(open_set):
        current = min(open_set,key = open_set.get)
        if(current != g.start.value):
            g.grid_cells[current].set_color(yellow)
            g.draw(sc)
        if(current == g.goal.value):
            g.grid_cells[current].set_color(purple)
            g.grid_cells[current].draw(sc)
            break
        open_set.pop(current)
        closed_set.append(current)
        for neighbor in g.get_neighbors(g.grid_cells[current]):
            if(neighbor.value in closed_set):
                continue
            f_cost = getWeight(neighbor, g.goal)
            if(neighbor.value not in open_set or f_cost < open_set[neighbor.value]):
                open_set[neighbor.value] = f_cost
                father[neighbor.value] = current
                if(neighbor not in open_set):
                    neighbor.set_color(red)
                    neighbor.draw(sc)
        if(current != g.start.value):
            g.grid_cells[current].set_color(blue)
            g.draw(sc)
            
    g.draw_path(sc,father)


def Dijkstra(g: Graph, sc:pygame.surface):
    print('Implement Dijkstra algorithm')
    def minDistance(g: Graph,closed_set,dist):
        min = 1e7
        for v in range(g.get_len()):
            if(dist[v] < min and v not in closed_set):
                min = dist[v]
                min_index = v
        return min_index

    closed_set:list[int] = []
    father = [-1]*g.get_len()
    dist:list[float] = [1e7]*g.get_len()
    dist[g.start.value] = 0
    for count in range(g.get_len()):
        u = minDistance(g,closed_set,dist)
        closed_set.append(u)
        currentNode = g.grid_cells[u]
        if(currentNode != g.start):
            currentNode.set_color(yellow)
            currentNode.draw(sc)
        pygame.display.flip()
        for neighbors in g.get_neighbors(currentNode):
            if(neighbors.value not in closed_set
            and dist[neighbors.value] > dist[u] + getWeight(neighbors,currentNode)):
                dist[neighbors.value] = dist[u] + getWeight(neighbors,currentNode)
                neighbors.set_color(red)
                neighbors.draw(sc)
                time.sleep(0.1)
                father[neighbors.value] = currentNode.value
        if(currentNode != g.start):
            currentNode.set_color(blue)
            currentNode.draw(sc)
    g.goal.set_color(purple)
    g.goal.draw(sc)
    g.draw_path(sc,father)      
