class Flight:
    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError('no airline code in {}'.format(number))
        if not number[:2].isupper():
            raise ValueError('invalid airline code {}'.format(number))
        if not number[2:].isdigit() and int(number[2:]) <= 9999:
            raise ValueError('invalid route {}'.format(number))
        self._aircraft = aircraft
        self._number = number
        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + \
            [{letter: None for letter in seats} for _ in rows]

    def count_seats(self):
        sum(sum(1 for seat in row.values() if seat is None)
            for row in self._seating if row is not None)

    def _parse_seat(self, seat):
        rows, seat_letters = self._aircraft.seating_plan()
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))
        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))
        if row not in rows:
            raise ValueError("Invalid row number {}".format(row))

        return (row, letter)

    def allocate_seat(self, seat, passenger):
        row, letter = self._parse_seat(seat)
        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))
        self._seating[row][letter] = passenger

    def relocate_passenger(self, from_seat, to_seat):

        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(
                "No passenger in seat {} to be transferred".format(from_seat))

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("new seat {} is not empty".format(to_seat))
        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def aircraft_model(self):
        return self._aircraft.model()

    def number(self):
        return self._number

    def _passenger_seats(self):
        rows, letters = self._aircraft.seating_plan()
        for row in rows:
            for letter in letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield passenger, "{0}{1}".format(row, letter)

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(),
                         self.aircraft_model())

    def airline(self):
        return self._number[:2]


class Aircraft:
    def __init__(self, registration):
        self._registration = registration

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)

    def registration(self):
        return self._registration


class AirbusA319(Aircraft):

    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 23), "ABCDEF"


class Boeing777(Aircraft):

    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1, 56), "ABCDEFGHJK"


def make_flight():
    f = Flight("MO1999", Boeing777("mmmm"))
    f.allocate_seat('12A', 'Guido van Rossum')
    f.allocate_seat('15F', 'Bjarne Stroustrup')
    f.allocate_seat('15E', 'Anders Hejlsberg')
    f.allocate_seat('1C', 'John McCarthy')
    f.allocate_seat('1D', 'Richard Hickey')
    return f


def console_card_printer(passenger, seat, flight_num, aircraft):
    output = "| Name {0} "\
        " seat {1} "\
        " flight number {2}"\
        "aircraft {3}"\
        "|".format(passenger, seat, flight_num, aircraft)
    banner = "*"+"-" * (len(output)-2) + "*"
    border = '|' + ' ' * (len(output) - 2) + '|'
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)
    print()
