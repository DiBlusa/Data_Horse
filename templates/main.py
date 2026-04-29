import os
import sys
import math

sys.path.append(os.path.dirname(__file__))

from Horse import Horse
from SDB import add_horse, create_table, get_all_horses, get_horse, update_distance, update_horse


TITLE_LINE = "========================================"
HEADER_LINE = "________________________________________"
ROW_LINE = "----------------------------------------"


def print_title(text):
    print(f"\n{TITLE_LINE}")
    print(text.center(len(TITLE_LINE)))
    print(TITLE_LINE)


def print_message(text):
    print(ROW_LINE)
    print(text)
    print(ROW_LINE)


def clear_screen():
    os.system("cls")


def show_horses():
    horses = get_all_horses()

    print_title("HORSES REGISTERED")

    if not horses:
        print_message("No horses found.")
        return

    print("ID | Name       | Distance | Time | Theta | Speed")
    print(HEADER_LINE)

    for horse_id, name, distance, time, theta_deg in horses:
        speed = 0 if time == 0 else (distance / time) * math.sin(math.radians(theta_deg))
        print(f"{horse_id:<2} | {name:<10} | {distance:<8} | {time:<4} | {theta_deg:<5} | {speed:.2f}")
        print(ROW_LINE)


def read_int(message):
    while True:
        value = input(message).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


def read_optional_int(message):
    while True:
        value = input(message).strip()
        if value == "":
            return None

        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer or press Enter to keep the current value.")


def add_horse_menu():
    clear_screen()
    show_horses()
    print_title("ADD HORSE")
    name = input("Name: ").strip()
    time = read_int("Time: ")
    theta_deg = read_int("Theta (degrees): ")

    horse = Horse(name, time, theta_deg)
    add_horse(horse)
    print_message("Horse added successfully with default distance 100.")


def update_horse_menu():
    clear_screen()
    show_horses()
    print_title("UPDATE HORSE")
    horse_id = read_int("Horse ID: ")
    horse = get_horse(horse_id)

    if horse is None:
        print_message("Horse not found.")
        return

    _, current_name, _, current_time, current_theta_deg = horse

    print(HEADER_LINE)
    print("Press Enter to keep the current value.")
    print(ROW_LINE)
    new_name = input(f"Name [{current_name}]: ").strip()
    new_time = read_optional_int(f"Time [{current_time}]: ")
    new_theta_deg = read_optional_int(f"Theta [{current_theta_deg}]: ")

    update_horse(
        horse_id,
        new_name if new_name else None,
        new_time,
        new_theta_deg,
    )
    print_message("Horse updated successfully.")


def update_distance_menu():
    clear_screen()
    show_horses()
    print_title("UPDATE DISTANCE")
    horse_id = read_int("Horse ID: ")
    horse = get_horse(horse_id)

    if horse is None:
        print_message("Horse not found.")
        return

    _, name, current_distance, _, _ = horse

    print(HEADER_LINE)
    print(f"Horse: {name}")
    print(f"Current distance: {current_distance}")
    print(ROW_LINE)

    new_distance = read_int("New distance: ")
    update_distance(horse_id, new_distance)
    print_message("Distance updated successfully.")


def get_horse_menu():
    clear_screen()
    show_horses()
    print_title("SEARCH HORSE")
    horse_id = read_int("Horse ID: ")
    horse = get_horse(horse_id)

    if horse is None:
        print_message("Horse not found.")
        return

    horse_id, name, distance, time, theta_deg = horse
    speed = 0 if time == 0 else (distance / time) * math.sin(math.radians(theta_deg))

    print(HEADER_LINE)
    print(f"ID: {horse_id}")
    print(f"Name: {name}")
    print(f"Distance: {distance}")
    print(f"Time: {time}")
    print(f"Theta: {theta_deg}")
    print(f"Speed: {speed:.2f}")
    print(ROW_LINE)


def main():
    create_table()

    while True:
        clear_screen()
        show_horses()
        print_title("OPTIONS")
        print("1 - Add horse")
        print("2 - Update horse")
        print("3 - Update distance")
        print("4 - Search horse by ID")
        print("5 - Exit")
        print(ROW_LINE)

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_horse_menu()
        elif choice == "2":
            update_horse_menu()
        elif choice == "3":
            update_distance_menu()
        elif choice == "4":
            get_horse_menu()
        elif choice == "5":
            print_message("Program closed.")
            break
        else:
            print_message("Invalid option.")


if __name__ == "__main__":
    main()
