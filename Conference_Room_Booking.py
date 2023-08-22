class MeetingRoomBooking:
    def __init__(self):
        self.rooms = {
            "C-Contact": 3,
            "S-Sharing": 7,
            "T-Team": 20
        }
        self.cleaning_time_slots = [
            ("09:00", "09:15"),
            ("13:15", "13:45"),
            ("18:45", "19:00")
        ]
        self.bookings = {}

    def is_cleaning_time(self, time_str):
        for buffer_start, buffer_end in self.cleaning_time_slots:
            if buffer_start <= time_str < buffer_end:
                return True
        return False

    def validate_time_slots(self, time_str):
        try:
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours < 24 and 0 <= minutes < 60 and minutes % 15 == 0:
                return True
        except ValueError:
            pass
        return False
    
    def available_rooms_to_book(self, start_time, end_time):
        if not self.validate_time_slots(start_time) or not self.validate_time_slots(end_time):
            return "INCORRECT_INPUT"

        if self.is_cleaning_time(start_time) or self.is_cleaning_time(end_time):
            return "NO_VACANT_ROOM"

        available_rooms = []
        for room, capacity in sorted(self.rooms.items(), key=lambda x: x[1]):
            is_available = True
            for booked_start, booked_end in self.bookings.get(room, []):
                if (booked_start <= start_time < booked_end) or (booked_start < end_time <= booked_end):
                    is_available = False
                    break
            if is_available:
                available_rooms.append(room)

        if available_rooms:
            return " ".join(available_rooms)
        return "NO_VACANT_ROOM"

    def time_slots_for_meeting(self, start_time, end_time, person_capacity):
        if person_capacity < 2 or person_capacity > 20:
            return "NO_VACANT_ROOM"

        if not self.validate_time_slots(start_time) or not self.validate_time_slots(end_time):
            return "INCORRECT_INPUT"

        if self.is_cleaning_time(start_time) or self.is_cleaning_time(end_time):
            return "NO_VACANT_ROOM"

        for room, capacity in sorted(self.rooms.items(), key=lambda x: x[1]):
            if capacity >= person_capacity:
                is_available = True
                for booked_start, booked_end in self.bookings.get(room, []):
                    if (booked_start <= start_time < booked_end) or (booked_start < end_time <= booked_end):
                        is_available = False
                        break
                if is_available:
                    self.bookings.setdefault(room, []).append((start_time, end_time))
                    return room

        return "NO_VACANT_ROOM"

if __name__ == "__main__":
    meeting_manager = MeetingRoomBooking()

    while True:
        command = input().split()

        if command[0] == "VACANCY":
            start_time, end_time = command[1], command[2]
            available_rooms = meeting_manager.available_rooms_to_book(start_time, end_time)
            print(available_rooms)
        elif command[0] == "BOOK":
            start_time, end_time, person_capacity = command[1], command[2], int(command[3])
            booked_room = meeting_manager.time_slots_for_meeting(start_time, end_time, person_capacity)
            print(booked_room)
