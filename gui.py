import pygame as pg
from queue import Empty


class Chat:
    """
    PyGame add-on for simple chat, can be subsurface or independent.

    :param queue:   queue with messages
    :param func:    function to send messages
    :param size:    tuple (width, height)
    :param pos:     tuple (x, y)
    :param name:    string name of window (only for independent window)
    :param surface: root surface (only for subsurface)
    :param bg:      bg color (R, G, B)
    :usage:         test = Chat(); test.run()
    """

    def __init__(self, queue, func, size=(350, 350), pos=(0, 0), name='chat', surface=None, bg=(200, 200, 200)):

        #  Main Settings
        self.queue = queue
        self.func = func
        self.bg = bg
        self.pos = pos
        self.width = size[0]
        self.height = size[1]

        #  Mode
        if surface:
            self.surface = surface
        else:
            pg.init()
            self.surface = pg.display.set_mode(size)
            pg.display.set_caption(name)
            self.clock = pg.time.Clock()
            self.pos = (0, 0)
        self.working_surface = pg.Surface(size)

        #  Input Box
        self.font = pg.font.Font(None, 24)
        self.input_box = pg.Rect(0, self.height-35, self.width, 35)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ">"
        self.text_pos = 0

        #  Messages Box
        mess_len = (self.height-35) // 25
        self.messages = ['' for _ in range(mess_len)]
        self.messages_rect = pg.Rect(0, 0, self.width, self.height-37)

    def update(self):
        self.working_surface.fill(self.bg)

        #  Input blit
        txt = self.font.render(self.text, True, self.color)
        tr = -txt.get_width() + self.width
        if tr > 0:
            tr = 0
        self.working_surface.blit(txt, (tr+5, self.input_box.y+5))
        pg.draw.rect(self.working_surface, self.color, self.input_box, 2)

        #  Messages blit
        while not self.queue.empty():
            mes = self.queue.get_nowait()
            self.messages.append(mes)
            self.messages.pop(0)
        y = 5
        for i in self.messages:
            m = self.font.render(i, True, (25, 25, 25))
            self.working_surface.blit(m, (5, y))
            y += 25
        pg.draw.rect(self.working_surface, (20, 150, 20), self.messages_rect, 2)

    def send(self):
        self.func(self.text)

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                if event.type == pg.KEYDOWN:
                    if self.active:
                        if event.key == pg.K_RETURN:
                            self.send()
                            self.text = '>'
                        elif event.key == pg.K_BACKSPACE:
                            if len(self.text) > 1:
                                self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
            self.update()
            self.surface.fill(self.bg)
            self.surface.blit(self.working_surface, self.pos)
            pg.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    w = Chat()
    w.run()
