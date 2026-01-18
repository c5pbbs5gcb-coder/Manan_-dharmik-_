from vpython import *
import serial
import random

ser = serial.Serial('/dev/cu.usbserial-110', 9600, timeout=0.01)

scene.width = 1000
scene.height = 600
scene.background = vector(0.1, 0.1, 0.1)

scene.camera.pos = vector(0, 5, -10)
scene.camera.axis = vector(0, -2, 10)

# ROAD
road = box(pos=vector(0, -1, 0), size=vector(8, 0.05, 80), color=color.black)

lane_marks = []
for i in range(-40, 40, 4):
    lane_marks.append(box(pos=vector(0, -0.97, i),
                          size=vector(0.3, 0.02, 2),
                          color=color.white))

left_line = box(pos=vector(-2.5, -0.96, 0), size=vector(0.2, 0.02, 80), color=color.yellow)
right_line = box(pos=vector(2.5, -0.96, 0), size=vector(0.2, 0.02, 80), color=color.yellow)

# STREET LIGHTS
lights = []
for z in range(-40, 50, 8):
    poleL = cylinder(pos=vector(-3.8, -1, z), axis=vector(0, 2.5, 0), radius=0.05, color=color.gray(0.7))
    lampL = sphere(pos=poleL.pos + vector(0, 2.5, 0), radius=0.12, color=color.yellow, emissive=True)

    poleR = cylinder(pos=vector(3.8, -1, z), axis=vector(0, 2.5, 0), radius=0.05, color=color.gray(0.7))
    lampR = sphere(pos=poleR.pos + vector(0, 2.5, 0), radius=0.12, color=color.yellow, emissive=True)

    lights += [poleL, lampL, poleR, lampR]

# PLAYER CAR
car = box(pos=vector(0, -0.7, -6), size=vector(1.2, 0.4, 2.2), color=color.red)

speed_player = 0.18
speed_enemy = 0.08

enemies = []
spawn_timer = 0
game_running = True
game_over_label = None

def spawn_enemy():
    e = box(size=vector(1.2, 0.4, 2.2), color=color.blue)
    e.pos = vector(random.choice([-2, 0, 2]), -0.7, 40)
    enemies.append(e)

while True:
    rate(120)

    if game_running:

        # SERIAL SAFE READ
        if ser.in_waiting:
            try:
                line = ser.readline().decode().strip()
                parts = line.split(",")
                if len(parts) == 2:
                    ax = float(parts[0])
                    ay = float(parts[1])
                    car.pos.x += ay * 0.15
            except:
                pass

        car.pos.x = max(-2.3, min(2.3, car.pos.x))

        # MOVE ROAD
        road.pos.z -= speed_player

        for m in lane_marks:
            m.pos.z -= speed_player
            if m.pos.z < -40:
                m.pos.z += 80

        for L in lights:
            L.pos.z -= speed_player
            if L.pos.z < -40:
                L.pos.z += 80

        # SPAWN ENEMY
        spawn_timer += 1
        if spawn_timer > 40:
            spawn_enemy()
            spawn_timer = 0

        # MOVE ENEMY
        for e in enemies[:]:
            e.pos.z -= speed_enemy

            if mag(e.pos - car.pos) < 1.3:
                game_running = False
                if game_over_label is None:
                    game_over_label = label(pos=vector(0, 1, 0),
                                            text="CRASH! GAME OVER",
                                            height=30,
                                            color=color.red)

            if e.pos.z < -10:
                e.visible = False
                enemies.remove(e)