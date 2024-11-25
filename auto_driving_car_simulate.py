#class Car to contain attributes of all the instances of cars added in the field
class Car:
    def __init__(self, car_name, x_axis, y_axis, direction, commands=None):
        self.car_name = car_name
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.direction = direction
        self.commands = commands if commands is not None else []
        self.status = "active"
        self.final_step = None

    #represents current attributes of all car objects in the field
    def __repr__(self):
        return f"- {self.car_name}, ({self.x_axis},{self.y_axis}) {self.direction}, {"".join(self.commands)}"

#class Grid to contain the active instance of field and instances of cars that will be added
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = self.create_field()
        self.cars = []

    #method to create the field
    def create_field(self):
        try:
            field = [[(column, row) for column in range(self.width)] for row in range(self.height)]
            print(f"You have created a field of {self.width} x {self.height}.")
            return field

        except Exception as e:
            print(f"Error during creation of field: {e}")
            return False
    #method to check if car object is within the boundaries of existing grid field    
    def check_boundaries(self, abscissa, ordinate):
        return 0 <= abscissa < self.width and 0 <= ordinate < self.height

    #method use to add cars
    def add_car(self, car_name, abscissa, ordinate, cardinal_direction, commands):
        if not self.check_car(car_name):
            if self.check_boundaries(abscissa, ordinate):
                car = Car(car_name, abscissa, ordinate, cardinal_direction, commands)
                self.cars.append(car)
                self.list_cars()
            else:
                print(f"Car '{car_name}' cannot be placed outside the grid boundaries.\nCurrent grid size is {self.width} x {self.height}.")
        else:
            print(f"Car with name '{car_name}' already exists. Please choose a different name.")

    #method to check if car being added is already existing the field
    def check_car(self, car_name):
        try:
            for car in self.cars:
                if car.car_name == car_name:
                    return car_name
            return None
        except Exception as e:
            print(f"Error during checking of cars: {e}")
            return False
        
    #method to check if current position of a car is shared with other car
    def check_collision(self):
        positions = {}
        try:
            for car in self.cars:
                if car.status == "active":
                    position = (car.x_axis, car.y_axis)
                    if position in positions:
                        return position
                    positions[position] = car
            return None
        except Exception as e:
            print(f"Error during checking of collision: {e}")
            return False

    #method to interpret the input commands and update the position of the car objects in the field
    def run_simulation(self):
        if not self.cars:
            print("\nNo existing cars in the field.")
            return False
        else:
            self.list_cars()

        step = 0

        while any(car.status == "active" and car.commands for car in self.cars):
            step += 1

            for car in self.cars:
                if car.status != "active" or not car.commands:
                    continue

                #get and remove the first command
                command = car.commands.pop(0)
                new_abscissa, new_ordinate = car.x_axis, car.y_axis

                #determine the new position or direction
                if command == "F":
                    if car.direction == "N":
                        new_abscissa += 1
                    elif car.direction == "S":
                        new_abscissa -= 1
                    elif car.direction == "E":
                        new_ordinate += 1
                    elif car.direction == "W":
                        new_ordinate -= 1

                elif command == "L":
                    car.direction = {"N": "W", "W": "S", "S": "E", "E": "N"}[car.direction]
                elif command == "R":
                    car.direction = {"N": "E", "E": "S", "S": "W", "W": "N"}[car.direction]

                #validate the new position if still inside the boundaries
                if command == "F" and self.check_boundaries(new_abscissa, new_ordinate):
                    car.x_axis, car.y_axis = new_abscissa, new_ordinate
                elif command == "F":
                    car.status = "stopped at border"
                    car.final_step = step
                    continue

                #check for collisions after each move
                collision = self.check_collision()
                if collision:
                    collided_cars = [c for c in self.cars if (c.x_axis, c.y_axis) == collision and c.status == "active"]
                    for c in collided_cars:
                        c.status = f"collides with {', '.join(other.car_name for other in collided_cars if other != c)}"
                        c.final_step = step

        #output new positions of all cars in the field
        print("\nAfter simulation, the result is:\n")
        for car in self.cars:
            if car.status.startswith("collides"):
                print(f"- {car.car_name}, {car.status} at ({car.x_axis}, {car.y_axis}) at step {car.final_step}")
            elif car.status == "stopped at border":
                print(f"- {car.car_name}, {car.status} at ({car.x_axis}, {car.y_axis}) at step {car.final_step}")
            else:
                print(f"- {car.car_name}, final position at ({car.x_axis}, {car.y_axis}) facing at {car.direction}")

        return True

    #method to list all cars in the field
    def list_cars(self):
        print("```\nYour current list of cars are:\n")
        for car in self.cars:
            print(car)

#function to exit the run
def exit_simulation():
    print('Goodbye!\n```')
    exit()

#function to capture and validate width and height parameters to create the grid
def input_axes():
    min_width_height = 1
    max_width_height = 100

    while True:
        try:
            in_width, in_height = map(int, input("\nPlease enter the width and height of the simulation field in x y format:\n```\n").strip().split(" "))
            if max_width_height >= in_width >= min_width_height and max_width_height >= in_height >= min_width_height:
               return in_width, in_height
            else:
                print(f"```\nInvalid Input: Please enter two numbers separated by a space from {min_width_height} to {max_width_height}.\n")
        except Exception as e:
            print(f"Error Occurred: {e}")
            exit_simulation()

#function to capture and validate which option is to use
def choose_options():
    while True:
        try:
            choice = input("\nPlease choose from the following options:\n[1] Add a car to field\n[2] Run simulation\n```\n").strip()
            if choice in ("1" ,"2"):
                return choice
            else:
                print(f"```\nInvalid Input: Please enter either 1 or 2.\n")
        except Exception as e:
            print(f"Error Occurred: {e}")
            exit_simulation()

#function to capture and validate the car to add in the field
def input_car(grid_field):
    while True:
        try:
            car_name = input("\nPlease enter the name of the car:\n").strip()
            if grid_field.check_car(car_name):
                print(f"Car '{car_name}' already exists. Please input a different name of the car.")
                continue
            else:
                return car_name
        except Exception as e:
            print(f"Error Occurred: {e}")
            exit_simulation()

#function to capture and validate the initial position and directions to execute
def input_directions(car_name):
    while True:
        try:
            car_initial_position = input(f"\nPlease enter the initial position of car {car_name} in x y Direction format:\n").strip().split(" ")
            if len(car_initial_position) != 3:
                print("Invalid Input: Please enter x, y, and direction separated by spaces.\n")
                continue
            
            initial_x_coordinate, initial_y_coordinate, initial_direction = int(car_initial_position[0]), int(car_initial_position[1]), car_initial_position[2]
            if initial_direction not in ("N","E","S","W"):
                print("Invalid Cardinal Direction: Please note that only N, S, W ,E (representing North, South, West, East) are allowed for direction.")
                continue
            
            commands = input(f"\nPlease enter the commands for car {car_name}:\n")
            if all(cmd in ["R","L","F"] for cmd in list(commands)):
                return car_name, initial_x_coordinate, initial_y_coordinate, initial_direction, commands
            else:
                print("Invalid Directions: Please note that only L, R, and F (representing Left, Right, and Forward, respectively) are allowed for commands.")
                continue

        except Exception as e:
            print(f"Error Occurred: {e}")
            exit_simulation()

def menu():
    while True:
        try:
            choice = input("\nPlease choose from the following options:\n[1] Star over\n[2] Exit\n```\n").strip()
            if choice in ("1" ,"2"):
                return choice
            else:
                print(f"```\nInvalid Input: Please enter either 1 or 2.\n")
        except Exception as e:
            print(f"Error Occurred: {e}")
            exit_simulation()

#main function to contain the flow of the program
def main():
    print("```\nWelcome to Auto Driving Car Simulation!\n")
    param_width, param_height = input_axes()
    grid_field = Grid(param_width, param_height)
    
    while True:
        if choose_options() == "2":
            if not grid_field.run_simulation():
                continue            
            if (menu() == "2"):
                print("Thank you for running the simulation. Goodbye!")
                exit()
            else:
                main()
        else:
            new_car = input_car(grid_field)
            car_name, x_coordinate, y_coordinate, facing, command = input_directions(new_car)
            grid_field.add_car(car_name, x_coordinate, y_coordinate, facing, list(command))

if __name__ == "__main__":
    main()