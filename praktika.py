import tkinter as tk
from tkinter import ttk
import math
import random
from abc import ABC


class Dispatcher:
    def __init__(self):
        self.__crashes = 0
        self.__lost_passengers = 0
        self.__lost_cargo = 0

    def airplane_crashes(self):
        self.__crashes += 1

    def cargo_crashes(self, airplane):
        self.__crashes += 1
        self.__lost_cargo += airplane.get_info()['cargo']

    def passengers_crashes(self, airplane):
        self.__crashes += 1
        self.__lost_passengers += airplane.get_info()['passengers']

    def get_dispatcher_info(self):
        return {
            'crashes': self.__crashes,
            'lost_cargo': self.__lost_cargo,
            'lost_passengers': self.__lost_passengers
        }


class Airport:
    def __init__(self, id_airport, coordinates, parking_lots, class_airport):
        self.__id = id_airport
        self.__coordinates = coordinates
        self.__parking_lots = parking_lots
        self.__class_airport = class_airport
        self.__strip = 1
        self.__airplanes_on_parking = []

    def add_airplane(self, id):
        self.__airplanes_on_parking.append(id)

    def update(self):
        self.__strip = 1

    def plane_landing(self, name_airplane):
        self.__strip = 0
        self.__parking_lots -= 1
        self.__airplanes_on_parking.append(name_airplane)

    def plane_departure(self, name_airplane):
        self.__strip = 0
        self.__parking_lots += 1
        self.__airplanes_on_parking.remove(name_airplane)

    def get_info(self):
        return {
            'id': self.__id,
            'coordinates': self.__coordinates,
            'parking_lots': self.__parking_lots,
            'class_airport': self.__class_airport,
            'strip': self.__strip,
            'airplanes_on_parking': self.__airplanes_on_parking
        }

class Airplane(ABC):
    def __init__(self, i, weight, speed, max_flight_time, service_time, airplane_way):
        self.__id = i
        self.__weight = weight
        self.__speed = speed
        self.__max_flight_time = max_flight_time
        self.__service_time = service_time
        self.__service_time_duration = 0
        self.__current_flight_duration = 0 #отслеживать время полёта от начала
        self.__flight_time_duration = max_flight_time #отслеживать, сколько осталось до крушения
        self.__airplane_way = airplane_way #путь самолёта
        self.__flight_time = 0 #сколько нужно времени для прибытия во второй аэропорт
        self.__is_flying = False  #True - в воздухе, False - на земле

    def fly(self):
        self.__current_flight_duration += 1
        self.__flight_time_duration -= 1

    def clear_flight_time(self):
        self.__flight_time_duration = self.__max_flight_time

    def take_off(self):
        self.__is_flying = True

    def land(self):
        self.__is_flying = False

    def flight_time_append(self, time):
        self.__flight_time = time

    def append_airplane_way(self, airport_id):
        self.__airplane_way.append(airport_id)

    def service_airplane(self):
        self.__service_time_duration += 1

    def clear_service_airplane(self):
        self.__service_time_duration = 0

    def get_info(self):
        return {
            'id': self.__id,
            'weight': self.__weight,
            'speed': self.__speed,
            'max_flight_time': self.__max_flight_time,
            'service_time': self.__service_time,
            'service_time_duration': self.__service_time_duration,
            'current_flight_duration': self.__current_flight_duration,
            'flight_time_duration': self.__flight_time_duration,
            'airplane_way': self.__airplane_way,
            'flight_time': self.__flight_time,
            'is_flying': self.__is_flying
        }

class CargoAirplane(Airplane):
    def __init__(self, id, weight, speed, max_flight_time, service_time, airplane_way, cargo):
        super().__init__(id, weight, speed, max_flight_time, service_time, airplane_way)
        self.__cargo = cargo

    def change_cargo(self):
        self.__cargo = random.randint(1000, 50000)

    def get_info(self):
        i = super().get_info()
        i['cargo'] = self.__cargo
        return i


class PassengerAirplane(Airplane):
    def __init__(self, i, weight, speed, max_flight_time, service_time, airplane_way, passengers):
        super().__init__(i, weight, speed, max_flight_time, service_time, airplane_way)
        self.__passengers = passengers

    def change_passengers(self):
        self.__passengers = random.randint(50, 300)

    def get_info(self):
        i = super().get_info()
        i['passengers'] = self.__passengers
        return i


class PleasureAirplane(Airplane):
    def __init__(self, i, weight, speed, max_flight_time, service_time, airplane_way):
        super().__init__(i, weight, speed, max_flight_time, service_time, airplane_way)


class MilitaryAirplane(Airplane):
    def __init__(self, i, weight, speed, max_flight_time, service_time, airplane_way):
        super().__init__(i, weight, speed, max_flight_time, service_time, airplane_way)

class Airplane_web:
    def __init__(self):
        self.__airplanes = []
        self.__airports = []
        self.__dispatcher = Dispatcher()
        self.__airplane_fly = []
        self.__passengers_fly = 0
        self.__cargo_fly = 0

    def create_airports(self, num_airports):
        for i in range(num_airports):
            id_airport = i  # Changed variable name to match the class attribute
            coordinates = [random.randint(-90, 90), random.randint(-180, 180)]
            parking_lots = random.randint(3, 15)
            class_airport = random.choice(["passenger", "cargo", "military", "recreational"])
            airport = Airport(id_airport, coordinates, parking_lots, class_airport)  # Corrected class instantiation
            self.__airports.append(airport)

    def create_random_airplanes(self, num_airplanes):
        for i in range(num_airplanes):
            id = i
            airplane_type = random.choice(["cargo", "passenger", "recreational", "military"])
            weight = random.randint(10000, 100000)
            speed = random.randint(200, 1000)
            max_flight_time = random.randint(4, 10)
            service_time = random.randint(1, 5)
            airplane_way = [random.randint(0, 5)]
            if airplane_type == "cargo":
                cargo = random.randint(1000, 50000)
                airplane = CargoAirplane(id, weight, speed, max_flight_time, service_time, airplane_way, cargo)
            elif airplane_type == "passenger":
                passengers = random.randint(50, 300)
                airplane = PassengerAirplane(id, weight, speed, max_flight_time, service_time, airplane_way, passengers)
            elif airplane_type == "recreational":
                airplane = PleasureAirplane(id, weight, speed, max_flight_time, service_time, airplane_way)
            else:
                airplane = MilitaryAirplane(id, weight, speed, max_flight_time, service_time, airplane_way)
            self.__airplanes.append(airplane)

    def flight_time(self, airplane):
        if len(airplane.get_info()['airplane_way']) < 2:
            return 0  # Если путь состоит из одного аэропорта, время полета равно 0

        coord1 = airplane.get_info()['airplane_way'][-2]
        coord2 = airplane.get_info()['airplane_way'][-1]
        coord_1 = self.__airports[coord1].get_info()['coordinates']
        coord_2 = self.__airports[coord2].get_info()['coordinates']
        lat1, lon1 = math.radians(coord_1[0]), math.radians(coord_1[1])
        lat2, lon2 = math.radians(coord_2[0]), math.radians(coord_2[1])

        R = 6371  # Радиус Земли в километрах
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        time = distance / airplane.get_info()['speed']
        return time / 10

    def check_airplanes_fly(self):
        j = []
        for i in self.__airplanes:
            if i.get_info()['is_flying']:
                j.append(i.get_info()['id'])
        self.__airplane_fly = j

    def count_passngers_fly(self):
        j = 0
        for i in self.__airplanes:
            if i.get_info()['is_flying'] and isinstance(i, PassengerAirplane):
                j += i.get_info()['passengers']
        self.__passengers_fly = j

    def count_cargo_fly(self):
        j = 0
        for i in self.__airplanes:
            if i.get_info()['is_flying'] and isinstance(i, CargoAirplane):
                j += i.get_info()['cargo']
        self.__cargo_fly = j

    def land_airplane(self, airplane, airport):
        if airport.get_info()['parking_lots'] > 0:
            airport.plane_landing(airplane.get_info()['id'])
            airplane.land()

    def take_off_airplane(self, airplane, airport):
        airport.plane_departure(airplane.get_info()['id'])
        tmp2 = random.randint(0, len(self.__airports) - 1)
        while tmp2 == airplane.get_info()['airplane_way'][-1]:
            tmp2 = random.randint(0, len(self.__airports) - 1)
        airplane.append_airplane_way(tmp2)
        airplane.take_off()
        l = self.flight_time(airplane)
        airplane.flight_time_append(l)
        airplane.clear_flight_time()
        if isinstance(airplane, CargoAirplane):
            airplane.change_cargo()
        elif isinstance(airplane, PassengerAirplane):
            airplane.change_passengers()


    def check_dispatcher_for_take_off(self):
        for airport in self.__airports:
            if airport.get_info()['strip'] == 1:
                i = airport.get_info()['airplanes_on_parking']
                if len(i) > 0:
                    tmp1 = random.choice(i)
                    for airplane in self.__airplanes:
                        if airplane.get_info()['id'] == tmp1:
                            self.take_off_airplane(airplane, airport)
                            break

    def check_dispatcher_for_land(self, airplane):
        destination_airport_id = airplane.get_info()['airplane_way'][-1]
        i = self.__airports[destination_airport_id]
        if i.get_info()['strip'] == 1:
            self.land_airplane(airplane, i)


    def update_day(self):
        for i in self.__airports:
            i.update()

    def first_day(self):
        for i in self.__airplanes:
            tmp3 = i.get_info()['airplane_way'][0]
            airport1 = self.__airports[tmp3]
            airport1.add_airplane(i.get_info()['id'])

    def fly(self):
        count1 = 0
        for i in self.__airplanes:
            if i.get_info()['is_flying']:
                if i.get_info()['flight_time_duration'] != 0:
                    i.fly()
                    if i.get_info()['current_flight_duration'] >= i.get_info()['flight_time']:
                        self.check_dispatcher_for_land(i)
                else:
                    if isinstance(i, CargoAirplane):
                        self.__dispatcher.cargo_crashes(i)
                    elif isinstance(i, PassengerAirplane):
                        self.__dispatcher.passengers_crashes(i)
                    else:
                        self.__dispatcher.airplane_crashes()
                    del self.__airplanes[count1]
            count1 += 1 #для нахождения id самолёта для удаления

    def get_info(self):
        return {
            'airplanes': self.__airplanes,
            'airports': self.__airports,
            'dispatcher': self.__dispatcher,
            'airplanes_fly': self.__airplane_fly,
            'passengers_fly': self.__passengers_fly,
            'cargo_fly': self.__cargo_fly
        }

class SimpleApp:
    def __init__(self, root):
        self.__root = root
        self.__running = False
        self.__day = 0
        self.__root.title("Airport web app")
        self.create_widgets()

    def create_widgets(self):
        self.__stats_frame = ttk.LabelFrame(self.__root, text="Статистика:")
        self.__stats_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.__days_label = ttk.Label(self.__stats_frame, text="День: 0")
        self.__days_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.__airplane_flight = ttk.Label(self.__stats_frame, text="Самолёты в воздухе: 0")
        self.__airplane_flight.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.__airplane_check = ttk.Label(self.__stats_frame, text="Самолёты, остаток времени полета которых не превышает заданную величину: ")
        self.__airplane_check.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.__airplane_in_airport = ttk.Label(self.__stats_frame, text="Самолёты на стоянке всех аэропортов: ")
        self.__airplane_in_airport.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.__airplane_way = ttk.Label(self.__stats_frame, text="Путь самолёта n: ")
        self.__airplane_way.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.__passengers_flight = ttk.Label(self.__stats_frame, text="Пассажиров в воздухе: 0")
        self.__passengers_flight.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.__cargo_flight = ttk.Label(self.__stats_frame, text="Общая масса груза в воздухе: 0")
        self.__cargo_flight.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.__crashes = ttk.Label(self.__stats_frame, text="Кол-во крушений самолётов: 0")
        self.__crashes.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.__lost_cargo = ttk.Label(self.__stats_frame, text="Кол-во потерянного груза: 0")
        self.__lost_cargo.grid(row=8, column=0, padx=5, pady=5, sticky="w")

        self.__lost_passengers = ttk.Label(self.__stats_frame, text="Кол-во погибших пассажиров: 0")
        self.__lost_passengers.grid(row=9, column=0, padx=5, pady=5, sticky="w")

        self.__control_frame = ttk.LabelFrame(self.__root, text="Пульт управления")
        self.__control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.__start_button = ttk.Button(self.__control_frame, text="Начать симуляцию", command=self.start_simulation)
        self.__start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.__stop_button = ttk.Button(self.__control_frame, text="Остановить симуляцию", command=self.stop_simulation)
        self.__stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def start_simulation(self):
        self.__running = True
        self.simulate_day()

    def stop_simulation(self):
        self.__running = False

    def nextDay(self):
        self.__day += 1
        return self.__day

    def simulate_day(self):
        if self.__running:
            tmp.update_day()
            tmp.check_airplanes_fly()
            tmp.count_passngers_fly()
            tmp.count_cargo_fly()
            tmp.fly()
            tmp.check_dispatcher_for_take_off()
            self.update_gui(tmp)
            self.__root.after(1000, self.simulate_day)

    def update_gui(self, i):
        self.__days_label.config(text=f"День: {self.nextDay()}")
        self.__airplane_flight.config(text=f"Самолёты в воздухе: {i.get_info()['airplanes_fly']} ")
        j = tmp.get_info()['airplanes']
        k = 2
        tmp4 = []
        for i in j:
            if i.get_info()['flight_time_duration'] <= k:
                tmp4.append(i.get_info()['id'])
        self.__airplane_check.config(text=f"Самолёты, остаток времени полета которых не превышает заданную величину: {tmp4}")
        j = tmp.get_info()['airports']
        airport_spisok = []
        for i in j:
            airport_spisok.append([f'Аэропорт:  {i.get_info()['id']}, Самолёты: {i.get_info()['airplanes_on_parking']}'])
        self.__airplane_in_airport.config(text=f"Самолёты на стоянке всех аэропортов:  {airport_spisok}")
        j = tmp.get_info()['airplanes']
        for airplane in j:
            if airplane.get_info()['id'] == 1:
                k = airplane.get_info()['airplane_way']
                break
        else:
            k = 'Самолёт разбился'
        self.__airplane_way.config(text=f"Путь самолёта 1: {k}")
        self.__passengers_flight.config(text=f"Пассажиров в воздухе: {tmp.get_info()['passengers_fly']}")
        self.__cargo_flight.config(text=f"Общая масса груза в воздухе: {tmp.get_info()['cargo_fly']} кг")
        j = tmp.get_info()['dispatcher']
        self.__crashes.config(text=f"Кол-во крушений самолётов:: {j.get_dispatcher_info()['crashes']}")
        self.__lost_cargo.config(text=f"Кол-во потерянного груза:: {j.get_dispatcher_info()['lost_cargo']} кг")
        self.__lost_passengers.config(text=f"Кол-во погибших пассажиров:: {j.get_dispatcher_info()['lost_passengers']}")

tmp = Airplane_web()
tmp.create_random_airplanes(15)
tmp.create_airports(6)
tmp.first_day()
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()