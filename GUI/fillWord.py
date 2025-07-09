import pygame
from typing import List,Literal
import threading
class FillWord:
    def __init__(self,x:float, y:float,width:int, height:int,answer:str, listWord:List[str], FPS = 60) -> None:
        self.x = x
        self.y = y
        self.width,self.height = width,height
        self.answer = answer
        self.listWord = listWord

        self.surface = pygame.Surface((width, height),pygame.SRCALPHA)
        self.isMovement =  False
        self.speed = 10
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        #các hộp
        self.beginX = 100
        self.beginY = 100
        self.percentFrameBox = 10/100

        self.num = len(answer)
        self.boxSize = (2*(self.width-self.beginX))/(3*self.num +1)
        self.frameBoxSize = (1 + 2*self.percentFrameBox)*self.boxSize
        self.distance = (self.width-self.beginX)/(3*self.num +1)
        self.answerBoxs:List[pygame.Rect] = [pygame.Rect(self.beginX,self.beginY,self.boxSize,self.boxSize)]
        self.answerBoxFrames:List[pygame.Rect] = [pygame.Rect(self.beginX - self.percentFrameBox*self.boxSize, self.beginY - self.percentFrameBox*self.boxSize,self.frameBoxSize,self.frameBoxSize)]
        self.answerBoxFrameColors:List[tuple[int]] = [(137,81,41) for _ in range(self.num)]
        print(self.answerBoxFrameColors)
        self.listWordBoxs:List[List[pygame.Surface]] = []
        self.boxValues:List[List[str]] = []
        self.listWordRect:List[List[pygame.Rect]] = []
        self.originCoor:List[List[float]] = []



        for i in range(1,self.num):
            self.answerBoxs.append(
                pygame.Rect(self.answerBoxs[i-1].right + self.distance,100,self.boxSize,self.boxSize)
            )
            self.answerBoxFrames.append(
                pygame.Rect(self.answerBoxFrames[i-1].right + self.distance - 2*self.percentFrameBox*self.boxSize,self.beginY - self.percentFrameBox*self.boxSize, self.frameBoxSize, self.frameBoxSize)
            )
        idx = 0
        i = 0
        font = pygame.font.SysFont("Arial", 24)
        while idx < len(self.listWord):
            self.listWordBoxs.append([]);self.listWordRect.append([])
            self.boxValues.append([]);self.originCoor.append([])
            for j in range(self.num):
                if idx >= len(self.listWord):
                    break  # Ngắt vòng for nếu hết từ
                box_surf = pygame.Surface((self.boxSize, self.boxSize), pygame.SRCALPHA)
                box_surf.fill((255, 255, 255))
                text_surf = font.render(self.listWord[idx], True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=(self.boxSize // 2, self.boxSize // 2))
                box_surf.blit(text_surf, text_rect)
                self.listWordBoxs[i].append(box_surf)
                rect = box_surf.get_rect(
                    x=j * (self.boxSize + self.distance),
                    y=i * (self.boxSize + self.distance) + self.answerBoxs[0].bottom + 50
                )
                self.surface.blit(box_surf,rect)
                self.listWordRect[i].append(rect)
                self.boxValues[i].append(self.listWord[idx])
                self.originCoor[i].append([rect.x,rect.y])

                idx += 1
            i += 1




        self.boxChooseId:List = [-1,[-1,-1]] #cái đầu là của đáp án, cái sau là của từ
        self.answerValues:List[str] = [""]*len(self.answerBoxs)

        self.fillCount = 0
        

            
    def handle_event(self,event:pygame.event.Event):
        r_x,r_y = pygame.mouse.get_pos()
        mx = r_x - self.x
        my = r_y - self.y
        for i in range(len(self.listWordBoxs)):
            for j in range(len(self.listWordBoxs[i])):
                if self.listWordRect[i][j].collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.boxChooseId[1] = [i,j]
                        self.run_movement(self.boxChooseId[0],*self.boxChooseId[1])
        for i in range(len(self.answerBoxs)):
            if self.answerBoxs[i].collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.boxChooseId[0] = i
                    self.run_movement(self.boxChooseId[0], *self.boxChooseId[1])
    
    def checkWord(self) -> bool:
        for i in range(len(self.answer)):
            if self.answerValues[i] == "": self.answerBoxFrameColors[i] = (137,81,41)
            elif self.fillCount == len(self.answer):
                self.answerBoxFrameColors[i] = (205,28,24) if self.answerValues[i] != self.answer[i] else (11,218,81)



    
    def movement(self,idx:int, i:int,j:int) -> None:
        #công thức y = d + ((b-d)*(c-x))/(c-a)
        while True:
            a,b = self.answerBoxs[idx].x,self.answerBoxs[idx].y
            c,d = self.listWordRect[i][j].x,self.listWordRect[i][j].y

            if a == c:
                self.listWordRect[i][j].y -= self.speed
            else:
                vt = self.speed if a > c else -self.speed
                self.listWordRect[i][j].x +=  vt
                self.listWordRect[i][j].y = d + ((b-d)*(c-self.listWordRect[i][j].x))/(c-a)
            
            if self.listWordRect[i][j].y <= self.answerBoxs[idx].y:
                self.listWordRect[i][j].y = self.answerBoxs[idx].y
                self.listWordRect[i][j].x = self.answerBoxs[idx].x
                break
            
            self.clock.tick(self.FPS)
        self.answerValues[idx] = self.boxValues[i][j]
        self.fillCount += 1

    def reverse_movement(self,idx:int,i: int, j: int) -> None:
        # Lấy tọa độ gốc để quay về
        orig_x, orig_y = self.originCoor[i][j]
        self.fillCount -= 1
        self.answerValues[idx] = ""
        while True:
            a,b = orig_x,orig_y
            c,d = self.listWordRect[i][j].x,self.listWordRect[i][j].y
            if a == c:
                self.listWordRect[i][j].y += self.speed
            else:
                vt = self.speed if c <  a else -self.speed
                self.listWordRect[i][j].x +=  vt
                self.listWordRect[i][j].y = d + ((b-d)*(c-self.listWordRect[i][j].x))/(c-a)


            if self.listWordRect[i][j].y >= orig_y:
                self.listWordRect[i][j].x = orig_x
                self.listWordRect[i][j].y = orig_y
                break


            self.clock.tick(self.FPS)
    
    def handleClick(self):...

    
    def isDuplicate(self,idx:int ,i:int ,j:int) -> bool:
        return self.answerBoxs[idx].x == self.listWordRect[i][j].x and self.answerBoxs[idx].y == self.listWordRect[i][j].y
    
    def run_movement(self,idx:int,i:int,j:int):
        if idx == -1 or  i == -1 or  j == -1 or self.answerValues[idx] != "":
            if self.answerValues[idx] != "" and idx != -1 and self.isDuplicate(idx,i,j):
                self.boxChooseId = [-1,[-1,-1]]
                threading.Thread(target= self.reverse_movement, args= (idx,i, j ,)).start()
            return

        self.boxChooseId = [-1,[-1,-1]]
        thread = threading.Thread(target = self.movement, args= (idx, i,j,))
        thread.daemon = False
        thread.start()


        


    
    def draw(self,screen:pygame.Surface):
        print(self.answerValues)
        self.checkWord()
        self.surface.fill((30,30,30))
        for i in range(len(self.answerBoxs)):
            pygame.draw.rect(self.surface,self.answerBoxFrameColors[i], self.answerBoxFrames[i])
            pygame.draw.rect(self.surface,(255,255,255),self.answerBoxs[i])
        for i in range(len(self.listWordBoxs)):
            for j in range(len(self.listWordBoxs[i])):
                self.surface.blit(self.listWordBoxs[i][j], self.listWordRect[i][j])

        screen.blit(self.surface,(self.x,self.y))

