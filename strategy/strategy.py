import random
import math
from game.plane_data import Vector
import strategy.utils as u
from game.base_strategy import BaseStrategy
from game.plane import Plane, PlaneType
from strategy.plane_strats import all_pigeons, all_scrapyard, all_thunder

# The following is the heart of your bot. This controls what your bot does.
# Feel free to change the behavior to your heart's content.
# You can also add other files under the strategy/ folder and import them
X_MIN = -50
X_MAX = 50
Y_MIN = -50
Y_MAX = 50
CENTER = Vector(0, 0)



class Strategy(BaseStrategy):
    # BaseStrategy provides self.team, so you use self.team to see what team you are on

    # You can define whatever variables you want here
    turn_count = 0
    plane_target = dict() # str: Vector
    inbounds = True
    get_angle_for_center = 0.0
    wiggle = 0.5  
    enemy_planes = dict() # str: Vector
    plane_enemy = dict() # str: str
    
    def select_planes(self) -> dict[PlaneType, int]:
        # Select which planes you want, and what number
        if self.team == 0:
            return all_scrapyard()
        if self.team == 1:
            return all_pigeons()
    
    def steer_input(self, planes: dict[str, Plane]) -> dict[str, float]:
        # Define a dictionary to hold our response
        response = dict()



        # For each plane
        # reverse the planes dictionary to get the enemies first
        if self.team == 0:
            planes = dict(reversed(list(planes.items())))
        for id, plane in planes.items():
            # id is the unique id of the plane, plane is a Plane object
            if plane.team != self.team:
                self.enemy_planes[id] = plane
                continue

            if id not in self.plane_target:
                self.plane_target[id] = self.refresh_target(plane, id)
            
            # if self.plane_target[id].distance(plane.position) < 2:
            #     target = self.refresh_target(plane, id)
            #     # print(f"Plane {plane.id} target: {u.pretty_print_vector(target)}")
            #     self.plane_target[id] = target
           
            enemy_plane = self.enemy_planes[self.find_closest_enemy_id(plane, self.enemy_planes)]
            # print(f"Closest enemy to {id}: {enemy_id}")
            self.plane_target[id] = self.predict_plane_position_if_straight(enemy_plane, 1) 

            # if self.turn_count == 0:
            #     self.plane_status(planes) # Print the status of all planes
            # if self.turn_count % 5 == 0:
            #     self.wiggle = -self.wiggle
            response[id] = self.steer_to(plane, self.plane_target[id], self.wiggle)
            
        # Increment counter to keep track of what turn we're on
        self.turn_count += 1

        # Return the steers
        return response

    def plane_status(self, planes: dict[str, Plane], current=False) -> None:
        # This function is called every turn, after steer_input
        # You can use this to keep track of your planes, or print debug information
        for id, plane in planes.items():
            if plane.team != self.team:
                continue
            print_starter = ""
            if not current:
                # print(f"Plane {id}: {plane.type}, \n Position: ({round(plane.position.x, 1)}, {round(plane.position.y, 1)}), \n Turn Radius: {plane.stats['turnSpeed']}° \n Speed: {plane.stats['speed']} \n Current Steer Angle {round(self.single_plane_steer(plane, logging=False) * plane.stats['turnSpeed'], 1)}° \n Current Angle {round(plane.angle, 1)}° \n")
                continue
            if current:
                print(f"[{plane.id}-{self.turn_count}] {round(plane.angle, 1)}°, ({round(plane.position.x, 1)}, {round(plane.position.y, 1)}), Steer {round(self.single_plane_steer(plane, logging=False) * plane.stats['turnSpeed'], 1)}°")

    def steer_circular(self, plane: Plane, turn: bool) -> float:
        return (1 if turn else -1) * u.radius_to_steer(plane.stats['turnSpeed'], plane.stats['turnSpeed'])
    
    def steer_random(self, plane: Plane) -> float:
        return random.random() * 2 - 1
    
    def steer_straight(self, plane: Plane) -> float:
        return 0.0001
    
    def get_plane_circling_radius(self, plane: Plane) -> float:
        return u.degree_to_radius(plane.stats['turnSpeed'], plane.stats['speed'])
    
    def steer_to(self, plane: Plane, target: Vector, wiggle: float) -> float:
        # Compute the vector from the plane's position to the target
        delta_x = target.x - plane.position.x
        delta_y = target.y - plane.position.y

        desired_angle = math.degrees(math.atan2(delta_y, delta_x)) 

        # Find the smallest angle diff, so to turn left if turning left is faster, etc.
        angle_diff = desired_angle - plane.angle
        angle_diff = (angle_diff + 180) % 360 - 180  # Clamp to [-180, 180]

        # Compute the steer
        steer = angle_diff / plane.stats['turnSpeed']

        # Clamp steer
        steer = self.validate_steer(plane, max(-1, min(1, steer))) 
        # if steer < 0:
        #     steer += wiggle + (random.random() * 2 - 1) / 10
        # else:
        #     steer -= wiggle + (random.random() * 2 - 1) / 10
        if abs(steer) < 0.0001:
            temp_steer = self.validate_steer(plane, 1 if random.random() > 0.5 else -1)
            if not u.steer_crashes_plane(temp_steer, plane):
                steer = temp_steer
        # IDK why this makes it follow the edges but it does
        if abs(steer) > 0.999999:
            temp_steer = self.validate_steer(plane, 0)
            if not u.steer_crashes_plane(temp_steer, plane):
                steer = temp_steer
        # print(f"[{plane.id}-{self.turn_count}] A {plane.angle:.1f}, DA {desired_angle:.1f}, steer: {steer:.5f}")

        return steer
    
    def refresh_target(self, plane: Plane, id: str) -> Vector:
        radius = self.get_plane_circling_radius(plane)
        top_right = Vector(X_MAX - radius * 3, Y_MAX - radius * 3)
        top_left = Vector(X_MIN + radius * 3, Y_MAX - radius * 3)
        bottom_right = Vector(X_MAX - radius * 3, Y_MIN + radius * 3)
        bottom_left = Vector(X_MIN + radius * 3, Y_MIN + self.get_plane_circling_radius(plane))
        targets = [top_right, top_left, bottom_right, bottom_left]
        target = targets[(self.turn_count + int(id)) % 4]
        return target
    
    def validate_steer(self, plane: Plane, steer: float) -> float:
        if u.steer_crashes_plane(steer, plane):
            return -steer
        return steer
    
    def find_closest_enemy_id(self, plane: Plane, enemy_planes: dict[str, Plane]) -> str:
        closest_enemy_id = "-1"
        closest_distance = float('inf')
        # print(enemy_planes)
        for id, enemy_plane in enemy_planes.items():
            distance = plane.position.distance(enemy_plane.position)
            # print(f"Distance to {id}: {distance}")
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy_id = id
        return closest_enemy_id
    
    def predict_plane_position_if_straight(self, plane: Plane, turns: int) -> Vector:
        return u.plane_path_offset(turns, plane.angle, plane) 
    def predict_plane_position_min_max(self, plane: Plane, turns: int) -> list[Vector]:
        return [u.plane_path_offset(turns, plane.angle, plane, min=True), u.plane_path_offset(turns, plane.angle, plane, min=True)]
    

    