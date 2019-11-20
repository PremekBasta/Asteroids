from dto import SpaceObjectDTO, collides, copy_object
import constants
import time
import numpy as np
import random


random.seed(100)

asteroids = []
for i in range(5):
    radius = random.randint(3,10)
    centerx = random.randint(0, constants.SCREEN_WIDTH)
    centery = random.randint(0, constants.SCREEN_HEIGHT)
    speedx = random.randint(-4,5)
    speedy = random.randint(-4,5)
    angle = 0
    size_index = 1
    player = 0
    life_count = 100
    ast = SpaceObjectDTO(radius, centerx, centery, speedx, speedy, angle, size_index, player, life_count)
    asteroids.append(ast)

    radius = random.randint(3,10)
    centerx = random.randint(0, constants.SCREEN_WIDTH)
    centery = random.randint(0, constants.SCREEN_HEIGHT)
    speedx = random.randint(-4,5)
    speedy = random.randint(-4,5)
    angle = 0
    size_index = 1
    player = 0
    life_count = 100

rocket_radius = 10
rocket = SpaceObjectDTO(rocket_radius, 818, 396, speedx, speedy, angle, size_index, player, life_count)

bullets = []
for i in range(3):
    radius = random.randint(3,10)
    centerx = random.randint(0, constants.SCREEN_WIDTH)
    centery = random.randint(0, constants.SCREEN_HEIGHT)
    speedx = random.randint(-4,5)
    speedy = random.randint(-4,5)
    angle = random.randint(0,30)
    size_index = 1
    player = 0
    life_count = 50
    bullet = SpaceObjectDTO(radius, centerx, centery, speedx, speedy, angle, size_index, player, life_count)
    bullets.append(bullet)


# start = time.time()
# for i in range(1000):
#     ast_pos_np = np.array([[a.centerx, a.centery] for a in asteroids])
#     ast_speed_np = np.array([[a.speedx, a.speedy] for a in asteroids])
#     ast_radii_np = np.array([a.radius+rocket_radius for a in asteroids])
# end = time.time()
# print(end-start)


# start = time.time()
# for i in range(1000):
#     ast_copy = [copy_object(ast) for ast in asteroids]
# end = time.time()
# print(end-start)

mod_val = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]

ast_pos_np = np.array([[a.centerx, a.centery] for a in asteroids])
ast_speed_np = np.array([[a.speedx, a.speedy] for a in asteroids])
ast_radii_np = np.array([a.radius for a in asteroids])
# TODO: subtract rocket radius from asteroid

bullets_pos_np = np.array([[b.centerx, b.centery] for b in bullets])
bullets_speed_np = np.array([[b.speedx, b.speedy] for b in bullets])
bullets_radii_np = np.array([5 for b in bullets])
# TODO: efficent bullet radii array creation

# print(ast_pos_np)
ast_differences_np = np.minimum(np.mod(np.subtract(ast_pos_np, [rocket.centerx, rocket.centery]), mod_val),np.mod(np.subtract([rocket.centerx, rocket.centery], ast_pos_np), mod_val))
ast_distances_np = np.linalg.norm(ast_differences_np, axis=1)
start = time.time()
for i in range(1000):
    np.minimum(np.mod(np.subtract(ast_pos_np, [rocket.centerx, rocket.centery]), mod_val),np.mod(np.subtract([rocket.centerx, rocket.centery], ast_pos_np), mod_val),out=ast_differences_np)
    ast_distances_np = np.linalg.norm(ast_differences_np, axis=1)
# print(time.time() - start)
#
# itemindex = np.where(ast_distances_np+100<ast_radii_np)
# if len(itemindex[0])>0:
#     print(f"index of ast: {itemindex[0][0]}")
# else:
#     print(f"no asteroid")


ast = np.array([[2,3],[4,7],[3,1]])
bul = np.array([[5,1],[6,2]])
differences = np.subtract(ast[:, np.newaxis], bul)

a_radii = np.array([2,1,4])
b_radii = np.array([2,2])
radii = np.add(a_radii[:,np.newaxis], b_radii)
print(radii)

# print(differences)
# print(">>>")
# mod_val = [10,10]
# np.mod(differences, mod_val, out= differences)
# print(differences)
# print(">>>")
#
#
np.minimum(np.mod(np.subtract(ast[:, np.newaxis], bul), mod_val),np.mod(np.subtract(bul, ast[:, np.newaxis]), mod_val), out=differences)
print(differences)
# print(">>>")
# print(">>>")
#
# print(">>>")
# print(differences)
#
distances = np.linalg.norm(differences, axis=2  )
print(">>>")
print(distances)
print(">>>")
print(radii)

itemindex = np.where(distances<radii)
print(itemindex[0])
print(itemindex[1])
print(">>>")
print(radii)
print(radii[itemindex[0][0],:])
radii[itemindex[0][0],:] = -100
radii[:,itemindex[1][0]] = -200
print(radii)

itemindex = np.where(distances<radii)
radii[itemindex[0][0],:] = -100
radii[:,itemindex[1][0]] = -200
print(radii)








start = time.time()
for i in range(100000):
    arr = np.array(range(30))
    for n in range(3):
        np.append(arr,1)
end = time.time()
print(end-start)

start = time.time()
for i in range(100000):
    arr = np.array(range(30))
end = time.time()
print(end-start)






