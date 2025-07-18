"""
Still a WIP as will be made evident by running the script
"""

import pygame
import math
import neat
import os
import time

pygame.init()

scr_width, scr_height = 720, 480
scr = pygame.display.set_mode((scr_width, scr_height))


def train_ai(genome1, genome2, config):
    net_1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net_2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    divisions = 8

    player_1_x, player_1_y = scr_width / divisions, scr_height / 2
    player_2_x, player_2_y = scr_width / divisions * (divisions - 1), scr_height / 2
    player_1_angle, player_2_angle = 0, 180

    player_1_in_enemy_zone = False
    player_2_in_enemy_zone = False
    player_1_in_enemy_zone_for_points = False
    player_2_in_enemy_zone_for_points = False

    player_1_winner = False
    player_2_winner = False

    displacement = 20

    start = time.time()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Get outputs from neural networks to control player movement
        output_1 = net_1.activate((player_1_x, player_1_y, player_2_x, player_2_y))
        decision_1 = output_1.index(max(output_1))

        output_2 = net_2.activate((player_1_x, player_1_y, player_2_x, player_2_y))
        decision_2 = output_2.index(max(output_2))

        scr.fill((0, 255, 0))

        if decision_1 == 0:
            player_1_x -= displacement * math.cos(math.radians(player_1_angle))
            player_1_y -= displacement * math.sin(math.radians(player_1_angle))
            if not 0 <= player_1_x <= scr_width:
                player_1_x += displacement * math.cos(math.radians(player_1_angle))
            if not 0 <= player_1_y <= scr_height:
                player_1_y += displacement * math.sin(math.radians(player_1_angle))
        elif decision_1 == 1:
            player_1_x += displacement * math.cos(math.radians(player_1_angle))
            player_1_y += displacement * math.sin(math.radians(player_1_angle))
            if not 0 <= player_1_x <= scr_width:
                player_1_x -= displacement * math.cos(math.radians(player_1_angle))
            if not 0 <= player_1_y <= scr_height:
                player_1_y -= displacement * math.sin(math.radians(player_1_angle))
        elif decision_1 == 2:
            player_1_angle -= 20
        elif decision_1 == 3:
            player_1_angle += 20

        if decision_2 == 0:
            player_2_x -= displacement * math.cos(math.radians(player_2_angle))
            player_2_y -= displacement * math.sin(math.radians(player_2_angle))
            if not 0 <= player_2_x <= scr_width:
                player_2_x += displacement * math.cos(math.radians(player_2_angle))
            if not 0 <= player_2_y <= scr_height:
                player_2_y += displacement * math.sin(math.radians(player_2_angle))
        if decision_2 == 1:
            player_2_x += displacement * math.cos(math.radians(player_2_angle))
            player_2_y += displacement * math.sin(math.radians(player_2_angle))
            if not 0 <= player_2_x <= scr_width:
                player_2_x -= displacement * math.cos(math.radians(player_2_angle))
            if not 0 <= player_2_y <= scr_height:
                player_2_y -= displacement * math.sin(math.radians(player_2_angle))
        if decision_2 == 2:
            player_2_angle -= 20
        if decision_2 == 3:
            player_2_angle += 20

        if player_1_in_enemy_zone and not player_2_in_enemy_zone:
            genome1.fitness += 1
        elif player_2_in_enemy_zone and not player_1_in_enemy_zone:
            genome2.fitness += 1

        if player_1_x + 20 > scr_width / (divisions / 2) * (divisions / 2 - 1) and player_1_in_enemy_zone:
            player_1_in_enemy_zone = True
            player_1_in_enemy_zone_for_points = True
        if player_2_x - 20 < scr_width / (divisions / 2) and player_2_in_enemy_zone:
            player_2_in_enemy_zone = True
            player_2_in_enemy_zone_for_points = True
        if player_1_x + 20 > scr_width / 2 and not player_1_in_enemy_zone:
            player_1_in_enemy_zone = True
        if player_2_x - 20 < scr_width / 2 and not player_2_in_enemy_zone:
            player_2_in_enemy_zone = True

        if player_1_x - 20 < scr_width / 2 and player_1_in_enemy_zone_for_points:
            player_1_winner = True
            break
        elif player_1_x - 20 < scr_width / 2 and player_1_in_enemy_zone_for_points:
            player_1_winner = True
            break
        elif player_1_x - 20 < scr_width / 2 and not player_1_in_enemy_zone_for_points:
            player_1_in_enemy_zone_for_points = False
            player_1_in_enemy_zone = False
        if player_2_x + 20 > scr_width / 2 and player_2_in_enemy_zone_for_points:
            player_2_winner = True
            break
        elif player_2_x + 20 > scr_width / 2 and player_2_in_enemy_zone_for_points:
            player_2_winner = True
            break
        elif player_2_x + 20 > scr_width / 2 and not player_2_in_enemy_zone_for_points:
            player_2_in_enemy_zone_for_points = False
            player_2_in_enemy_zone = False
        if player_1_in_enemy_zone and math.sqrt((player_2_y - player_1_y) ** 2 + (player_2_x - player_1_x) ** 2) < 40:
            player_2_winner = True
            break
        if player_2_in_enemy_zone and math.sqrt((player_2_y - player_1_y) ** 2 + (player_2_x - player_1_x) ** 2) < 40:
            player_1_winner = True
            break

        pygame.draw.rect(scr, (255, 255, 0),
                         [scr_width / (divisions / 2) * (divisions / 2 - 1), 0, scr_width / (divisions / 2),
                          scr_height])
        pygame.draw.rect(scr, (255, 255, 0), [0, 0, scr_width / (divisions / 2), scr_height])

        pygame.draw.circle(scr, (0, 0, 139), (player_1_x, player_1_y), 20)
        pygame.draw.circle(scr, (255, 87, 51), (player_2_x, player_2_y), 20)

        pygame.draw.line(scr, (255, 0, 0), (scr_width / 2, 0), (scr_width / 2, scr_height), 10)

        pygame.draw.circle(scr, (255, 255, 255), (player_1_x + 14 * math.cos(math.radians(player_1_angle)),
                                                  player_1_y + 14 * math.sin(math.radians(player_1_angle))), 3)
        pygame.draw.circle(scr, (255, 255, 255), (player_2_x + 14 * math.cos(math.radians(player_2_angle)),
                                                  player_2_y + 14 * math.sin(math.radians(player_2_angle))), 3)

        pygame.display.update()

        if time.time() - start >= 3:
            break

    if player_1_winner:
        genome1.fitness += 100
    elif player_2_winner:
        genome2.fitness += 100


# use round robin tournament to compare genomes
def eval_genomes(genomes, config):
    total_genome_num = len(genomes) * (len(genomes) - 1)
    curr_count = 0
    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        for j, (genome_id2, genome2) in enumerate(genomes):
            if i != j:
                curr_count += 1
                genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
                print("Training", curr_count, "of", total_genome_num)
                train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)


if __name__ == "__main__":
    path_to_config = "/Users/akshith/PycharmProjects/NEAT/venv/config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         path_to_config)
    run_neat(config)

