

import pygame

TILE = 48
PANEL = 420

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)
DARK = (50,50,50)

BLUE = (0,0,255)
RED = (220,70,70)
GREEN = (60,200,120)
ORANGE = (255,170,0)




class Button:

    def __init__(self,x,y,w,h,text):

        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self,screen):

        pygame.draw.rect(screen,GRAY,self.rect)
        pygame.draw.rect(screen,BLACK,self.rect,2)

        font = pygame.font.SysFont(None,22)

        txt = font.render(self.text,True,BLACK)

        screen.blit(
            txt,
            (self.rect.x+10,self.rect.y+4)
        )

    def clicked(self,pos):

        return self.rect.collidepoint(pos)




def draw_text(screen,text,x,y,size=24,color=BLACK):

    font = pygame.font.SysFont(None,size)

    img = font.render(str(text),True,color)

    screen.blit(img,(x,y))




def draw_game(
        screen,
        level,
        walls,
        goals,
        boxes,
        player,
        buttons,
        current_algo,
        expanded_nodes,
        path_length,
        path_cost,
        search_time,
        compare_results,
        message
):

    screen.fill(WHITE)

    map_width = len(level[0])*TILE


  

    for y,row in enumerate(level):

        for x,ch in enumerate(row):

            rect = pygame.Rect(
                x*TILE,
                y*TILE,
                TILE,
                TILE
            )

       
            pygame.draw.rect(screen,WHITE,rect)

         
            pygame.draw.rect(screen,GRAY,rect,1)

        
            if (x,y) in walls:

                pygame.draw.rect(
                    screen,
                    DARK,
                    rect
                )

      
            if (x,y) in goals:

                pygame.draw.circle(
                    screen,
                    ORANGE,
                    rect.center,
                    TILE//6
                )

         
            if (x,y) in boxes:

                pygame.draw.rect(
                    screen,
                    RED,
                    rect.inflate(-10,-10)
                )


 

    if player is not None:

        px,py = tuple(player)

        player_rect = pygame.Rect(
            px*TILE,
            py*TILE,
            TILE,
            TILE
        )

        pygame.draw.circle(
            screen,
            BLUE,
            player_rect.center,
            TILE//2 - 4
        )


  

    pygame.draw.rect(
        screen,
        (240,240,240),
        (map_width,0,PANEL,screen.get_height())
    )

    panel_x = map_width + 20




    draw_text(screen,"ALGORITHM INFO",panel_x,20,30)

    draw_text(
        screen,
        f"Current: {current_algo}",
        panel_x,
        70
    )

    draw_text(
        screen,
        f"Expanded Nodes: {expanded_nodes}",
        panel_x,
        105
    )

    draw_text(
        screen,
        f"Path Length: {path_length}",
        panel_x,
        140
    )

    draw_text(
        screen,
        f"Path Cost: {path_cost}",
        panel_x,
        175
    )

    draw_text(
        screen,
        f"Search Time: {round(search_time,4)}",
        panel_x,
        210
    )


   

    for b in buttons:

        b.draw(screen)




    draw_text(
        screen,
        message,
        panel_x,
        350,
        28,
        GREEN
    )


 

    if compare_results:

        y = 420

        draw_text(
            screen,
            "COMPARE RESULTS",
            panel_x,
            y,
            26
        )

        y += 40

        for r in compare_results:

            txt = (
                f"{r['name']} | "
                f"Steps:{r['steps']}  "
                f"Expanded:{r['expanded']}  "
                f"Cost:{r['cost']}  "
                f"Time:{round(r['time'],4)}"
            )

            draw_text(
                screen,
                txt,
                panel_x,
                y,
                20
            )

            y += 28
