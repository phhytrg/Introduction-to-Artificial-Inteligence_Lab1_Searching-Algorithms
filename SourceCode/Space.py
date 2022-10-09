import math
from bisect import insort
from xmlrpc.client import Boolean
import pygame
from Constants import *

class Node:
    def __init__(self, x, y, value, radius = 10) -> None:
        '''
        x,y: tọa độ của node
        value: giá trị của node, có thể dùng làm giá trị định danh
        radius: bán kính node
        '''
        self.x, self.y, self.value = x, y, value
        self.radius = radius
        self.color = green

    def draw(self, sc:pygame.Surface) -> None:
        '''
        hàm vẽ node lên 1 bề mặt `sc`
        '''
        pygame.draw.circle(sc, self.color, (self.x, self.y), self.radius, 0)

        font = pygame.font.Font(pygame.font.get_default_font(), 10)
        node_label = font.render(str(self.value), True, white)
        sc.blit(node_label, (self.x, self.y))

    def set_color(self, color) -> None:
        '''
        set màu cho node
        color: Tuple(r,g,b)
        '''
        self.color = color



class Graph:
    def __init__(self, start_pos:int, goal_pos:int) -> None:
        '''
        khởi tạo đồ thị
        start_pos: vị trí bắt đầu
        goal_pos: vị trí đích
        các vị trí này chính là giá trị `value` của node
        '''
        self.grid_cells:list[Node] = []
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                self.grid_cells.append(Node(j*TILE+TILE/2, i*TILE+TILE/2, (i-1)*(cols-2)+(j-1)))

        self.start:Node = self.grid_cells[start_pos]
        self.start.set_color(orange)
        self.goal:Node = self.grid_cells[goal_pos]
        self.goal.set_color(purple)

    def get_len(self) -> int:
        '''
        trả về số node của đồ thị
        '''
        return len(self.grid_cells)

    def is_goal(self, node:Node) -> bool:
        '''
        kiểm tra node `node` có phải là đích hay không
        '''
        if node.value == self.goal.value:
            return True
        return False

    def draw(self, sc:pygame.Surface):
        '''
        vẽ đồ thị lên bề mặt `sc`
        '''
        for node in self.grid_cells:
            node.draw(sc)
        pygame.display.flip()

    def get_neighbors(self, node:Node):
        '''
        trả về các node kề của node `node` theo 8 hướng
        '''
        r = node.value//(cols-2)
        c = node.value%(cols-2)

        up = (r-1, c) if r-1 >= 0 else None
        down = (r+1, c) if r+1 < (rows-2) else None
        left = (r, c-1) if c-1 >= 0 else None
        right = (r, c+1) if c+1 < (cols-2) else None

        up_left = (r-1, c-1) if r-1 >= 0 and c-1 >= 0 else None
        up_right = (r-1, c+1) if r-1 >= 0 and c+1 < (cols-2) else None
        down_left = (r+1, c-1) if r+1 < (rows-2) and c-1 >= 0 else None
        down_right = (r+1, c+1) if r+1 < (rows-2) and c+1 < (cols-2) else None

        directions = [up, down, left, right, up_left, up_right, down_left, down_right]
        neighbors = []
        for dir in directions:
            if dir is not None:
                neighbors.append(self.grid_cells[dir[0]*(cols-2) + dir[1]])
        return neighbors

    # Hàm hỗ trợ vẽ lại đường đi
    def draw_line(self, sc: pygame.surface, src: Node, dest: Node) -> Node:
        pygame.draw.line(sc,green, (src.x, src.y), (dest.x, dest.y))

    def draw_path(self, sc: pygame.surface, father) -> None:
        tmp = father[self.goal.value]
        if(tmp == -1):
            print('No path found')
            return
        self.draw_line(sc,self.goal, self.grid_cells[tmp])
        self.draw(sc)
        while True:
            if(tmp == 95):
                a = []
            self.grid_cells[tmp].set_color(grey)
            self.grid_cells[tmp].draw(sc)
            self.draw_line(sc,self.grid_cells[tmp], self.grid_cells[father[tmp]])
            tmp = father[tmp]
            pygame.display.flip()
            if(tmp == self.start.value):
                break

