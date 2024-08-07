import config
import renderer
import pygame
import simulation

from collections import namedtuple

import matplotlib.pyplot as plt

UPDATE = pygame.USEREVENT + 1
PAUSE = pygame.USEREVENT + 2

def create_drawmap(render):
    Drawing_Map = namedtuple('Drawings', ['color', 'shape', 'value'])
    drawing_map = []
    drawing_map.append(Drawing_Map(color=config.COLORS["RED"], shape="circle", value=7))
    drawing_map.append(Drawing_Map(color=config.COLORS["BLUE"], shape="circle", value=11))
    drawing_map.append(Drawing_Map(color=config.COLORS["GREEN"], shape="circle", value=13))
    drawing_map.append(Drawing_Map(color=config.COLORS["YELLOW"], shape="circle", value=17))
    drawing_map.append(Drawing_Map(color=config.COLORS["PURPLE"], shape="circle", value=19))
    drawing_map.append(Drawing_Map(color=config.COLORS["ORANGE"], shape="circle", value=23))
   # drawing_map.append(Drawing_Map(color=config.COLORS["DARK_GRAY"], shape="circle", value=29))
   # drawing_map.append(Drawing_Map(color=config.COLORS["BLACK"], shape="circle", value=31))
   # drawing_map.append(Drawing_Map(color=config.COLORS["WHITE"], shape="circle", value=37))

    render.set_drawing_map(drawing_map)


if __name__ == "__main__":
    render = renderer.Renderer()
    sim = simulation.Simulation()
    import time
    create_drawmap(render)

    velocities = []
    num_rules = []

    pause = False
    i = 0

    vel = 0
    while i < 1000: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 1000
            if event.type == UPDATE:
                render.refresh_gameboard()
                overlay = sim.get_overlay()
                render.draw_overlay(overlay)
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pause = not pause

        if not pause:
            vel = sim.get_state_velocity()
            velocities.append(vel)
            num_rules.append(len(sim.rules))

            if vel == 0:
                sim.create_rule()
                sim.perturb()

            if len(velocities) > 100:
                last_100_velocities = velocities[-100:]
                evens = last_100_velocities[::2]
                if evens.count(evens[0]) > 40:
                    print("Period 2 Behavior Detected")
                    sim.create_rule()
                thirds = last_100_velocities[::3]
                if thirds.count(thirds[0]) > 40:
                    print("Period 3 Behavior Detected")
                    sim.create_rule()
                

            sim.step()
            time.sleep(0.05)
            pygame.event.post(pygame.event.Event(UPDATE))

            i += 1

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(num_rules, 'r')
    ax1.set_title('Number of Rules')
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Number of Rules')

    ax2.plot(velocities, 'b')
    ax2.set_title('Velocity of System')
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Velocity')

    plt.tight_layout()
    plt.show()
