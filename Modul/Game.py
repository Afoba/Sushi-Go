import pygame

class Game():
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.lastpoints = None

    def event_check(self):
        for event in pygame.event.get():
            self.state.get_event(event)
    
    def flip_state(self):
        current_state = self.state_name
        if current_state == "Gameplay":
            self.lastpoints = self.states[current_state].points
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        self.state = self.states[self.state.next_stage]
        if self.state == self.states["Win"]:
            self.state.plrpoints = self.lastpoints
            self.state.reset()
        self.state.reset()
        self.state.surface = self.screen

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt, self.screen.get_size())

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_check()
            self.update(dt)
            self.draw()
            pygame.display.update()

