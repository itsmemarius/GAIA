import json
from robodk import robolink

class MealAssembler:
    def __init__(self, robot_name, item_targets):
        self.robot = robolink.Robolink()
        self.robot.Connect()
        self.robot_item = self.robot.Item(robot_name)
        self.stations = self._initialize_stations(item_targets)

    def _initialize_stations(self, item_targets):
        targets = {}
        for item, data in item_targets.items():
            targets[item] = self.robot.AddTarget(item, data["position_matrix"])
        return targets

    def move_to_station(self, station_name, pause_time):
        station = self.stations[station_name]
        self.robot_item.MoveJ(station)
        #self.robot.RunInstruction('WaitTime', pause_time)

    def assemble_meal(self, meal_plan):
        for station_name, pause_time in meal_plan.items():
            self.move_to_station(station_name, pause_time)

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def main():
    system_setup = load_json("system_setup.json")
    user_preferences = load_json("user_preferences.json")

    robot_name = system_setup["robot_name"]
    item_targets = system_setup["item_targets"]
    meal_choice = user_preferences["meal_choice"]

    meal_plan = {"TakeTray": 2, "Serve": 1}

    meal_planner = MealAssembler(robot_name, item_targets)

    if meal_choice in ["salad", "meat", "eggs", "pasta"]:
        meal_plan[meal_choice.capitalize()] = 4
        meal_planner.assemble_meal(meal_plan)
    else:
        print("Invalid choice. Please select one of the provided options.")

if __name__ == "__main__":
    main()
