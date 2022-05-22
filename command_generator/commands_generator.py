import json


class CommandsGenerator:
    def __init__(self, home_cfg_path):
        with open(home_cfg_path, encoding='utf-8') as cfg:
            self.home_dict = json.load(cfg)

    # Tworzenie komendy na podstawie słownika urządzenia i akcji
    def device_command(self, action, device_dict):
        tmp_command = "cmd/" + device_dict["name"]
        if device_dict["room"] is not None:
            tmp_command = tmp_command + "/" + device_dict["room"]
        if device_dict["detailed_place"] is not None:
            tmp_command = tmp_command + "/" + device_dict["detailed_place"]
        if action != "toggle":
            if action not in device_dict["possible_actions"]:
                print("Nie ma akcji: ", action, "dla urządzenia: ", device_dict["name"])
                exit(1)
        tmp_command = tmp_command + " " + action
        return tmp_command

    # Sprawdzenie czy pokój istnieje
    def validate_room(self, room):
        if room not in self.home_dict["rooms"]:
            print("Nie ma pomieszczenia: ", room)
            return False
        return True

    # Sprawdzenie czy urządzenie jest w pokoju
    def validate_device_in_room(self, room, device):
        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] == device and device_dict["room"] == room:
                return True
        print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room)
        return False

    # Sprawdzenie, czy istnieje urządzenie w danym miejscu
    def validate_detailed_place(self, room, device, detailed_place):
        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] == device and device_dict["room"] == room and \
                    device_dict["detailed_place"] == detailed_place:
                return True
        print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room, " w miejscu: ", detailed_place)
        return False

    # Sprawdzenie, czy na urządzeniu w danym miejscu można wykonać daną akcję
    def validate_action(self, room, device, detailed_place, action):
        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] == device and device_dict["room"] == room and device_dict[
                "detailed_place"] == detailed_place \
                    and action in device_dict["possible_actions"]:
                return True
        print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room, " w miejscu: ", detailed_place,
              "o możliwej akcji: ", action)
        return False

    # Lista urządzeń w danym pokoju
    def devices_in_room(self, room):
        devices = []
        for device_dict in self.home_dict["devices"]:
            if device_dict["room"] == room:
                devices.append(device_dict)
        return devices

    # lista urządzeń na danym piętrze
    def devices_in_storey(self, storey):
        devices = []
        for room in self.home_dict["storeys"][storey]:
            devices += self.devices_in_room(room)
        return devices

    # Urządzenia w danym miejscu (np nad szafkami)
    def devices_with_detailed_place(self, detailed_place):
        devices = []
        for device_dict in self.home_dict["devices"]:
            if device_dict["detailed_place"] == detailed_place:
                devices.append(device_dict)
        return devices

    def all_devices(self, name):
        devices = []
        for device_dict in self.home_dict["devices"]:
            if name is not None and device_dict["name"] == None:
                devices.append(device_dict)
        return devices

    def validate_storey(self, storey):
        if storey in self.home_dict["storeys"].keys():
            return True
        print("Nie ma piętra: ", storey)
        return False

    def room_is_in_storeys(self, room, storeys):
        for storey in storeys:
            if room in self.home_dict["storeys"][storey]:
                return True
        return False

    def get_device_dicts(self, storey, room, detailed_place, device, action):
        device_dicts = []

        storeys = []
        if storey is not None:
            if self.validate_storey(storey):
                storeys.append(storey)
        else:
            for home_storey in self.home_dict["storeys"].keys():
                storeys.append(home_storey)

        rooms = []
        if room is not None and self.room_is_in_storeys(room, storeys):
                rooms.append(room)
        else:
            for storey, storey_rooms in self.home_dict["storeys"].items():
                if storey in storeys:
                    rooms += storey_rooms

        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] != device:
                continue
            if device_dict["room"] not in rooms:
                continue
            if detailed_place is not None and device_dict["detailed_place"] != detailed_place:
                continue
            if action not in device_dict["possible_actions"]:
                continue
            device_dicts.append(device_dict)

        return device_dicts

    # Generowanie wyjściowych poleceń (zwracana jest lista)
    def get_commands(self, command_dict):
        storey = command_dict["storey"]
        room = command_dict["room"]
        device = command_dict["device"]
        detailed_place = command_dict["detailed_place"]
        action = command_dict["action"]

        if action is None:
            action = "toggle"

        device_dicts = self.get_device_dicts(storey, room, detailed_place, device, action)

        commands = []
        for device_dict in device_dicts:
            commands.append(self.device_command(action, device_dict))

        if len(commands) == 0:
            print("Nie rozumiem polecenia (nie stworzyłem żadnej komendy)")

        return commands

