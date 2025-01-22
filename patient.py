"""
Projekt na laboratorium przedmiotu Algorytmy i Struktury Danych.
"""
import logging
import time
from datetime import datetime, timedelta
from enum import Enum


class Gender(Enum):
    """
    Enum przechowujący płeć
    """
    K = 'Kobieta'
    M = 'Mężczyzna'


class Patient:
    """
    Klasa opisująca pacjenta stojącego w kolejce do lekarza.
    """
    name: str
    surname: str
    age: int
    pesel: int
    gender: Gender
    time_of_visit: datetime | None

    def __init__(self, name: str, surname: str, age: int, pesel: int, gender: Gender, time_of_visit: datetime | None = None):
        """
        Konstruktor tworzący instancje obiektu, jakim jest pacjent.

        :param name: Imię pacjenta (ciąg liter zaczynający się dużą literą).
        :param surname: Nazwisko pacjenta (ciąg liter zaczynający się dużą literą).
        :param age: Wiek pacjenta (liczba całkowita z zakresu 1-150).
        :param pesel: Unikalny PESEL pacjenta.
        :param gender: Płeć pacjenta (Gender Enum: Kobieta lub Mężczyzna).
        :param time_of_visit: Godzina wizyty pacjenta (obiekt datetime lub None).
        """
        # Walidacja imienia
        if not name.isalpha():
            raise ValueError("Imię może zawierać tylko litery.")
        self.name = name.capitalize()

        # Walidacja nazwiska
        if not surname.isalpha():
            raise ValueError("Nazwisko może zawierać tylko litery.")
        self.surname = surname.capitalize()

        # Walidacja wieku
        if not (1 <= age <= 150):
            raise ValueError("Wiek musi być liczbą całkowitą z zakresu 1-150.")
        self.age = age

        # Walidacja PESEL
        if not isinstance(pesel, int) or len(str(pesel)) != 11:
            raise ValueError(
                "PESEL musi być liczbą całkowitą składającą się z 11 cyfr.")
        self.pesel = pesel

        # Walidacja płci
        if not isinstance(gender, Gender):
            raise ValueError(
                "Płeć musi być wartością Gender Enum: 'Kobieta' lub 'Mężczyzna'.")
        self.gender = gender

        # Czas wizyty (może być None)
        self.time_of_visit = time_of_visit

    def __eq__(self, other):
        """
        Funkcja porównująca obiekty do pacjenta. Zwraca true, jeśli wszystkie pola mają tę samą wartość.
        :param other: To parametr przechowujący informacje o porównywanym obiekcie do tego pacjenta.
        :return:
        """
        if not isinstance(other, Patient):
            return False
        return (self.name == other.name and
                self.surname == other.surname and
                self.age == other.age and
                self.pesel == other.pesel and
                self.gender == other.gender and
                self.time_of_visit == other.time_of_visit)

    def display(self):
        """
        Funkcja wyświetlająca dane pacjenta.
        :return: None
        """
        print("Imię: %s" % self.name)
        print("Nazwisko: %s" % self.surname)
        print("Wiek: %d" % self.age)
        print("PESEL: %d" % self.pesel)
        print("Płeć: %s" % self.gender)
        print("Godzina wizyty: %s" % self.time_of_visit)


class PatientQueue:
    """
    Klasa, która przechowuje informacje o pacjentach czekających do lekarza.
    """
    heap: list[Patient]

    def __init__(self):
        self.heap = []

    def validating_addition(self, patient):
        """
        Funkcja sprawdzająca, czy nie ma w kolejce pacjenta o takim samym numerze PESEL i czy osoba umawiająca
        się nie próbuje się umówić na tę samą godzinę co inny pacjent. Nie pozwoli umówić się również w mniejszym
        odstępie niż 10 minut od poprzedniej wizyty.
        :return: Zwraca true, kiedy żaden inny pacjent nie ma takiego samego numeru PESEL i kiedy odstęp od poprzedniej wizyty jest przynajmniej 10 minut.
        """
        if len(self.heap) > 0:
            if patient.time_of_visit is not None:
                for patient_in_queue in self.heap:
                    if patient_in_queue.pesel == patient.pesel:
                        raise ValueError(
                            "Jest w kolejce pacjent o podanym numerze PESEL")
                    elif abs(patient_in_queue.time_of_visit - patient.time_of_visit) < timedelta(minutes=10):
                        raise ValueError(
                            "Odstęp pomiędzy umówionymi wizytami to minimum 10 minut")
                return True
            else:
                for patient_in_queue in self.heap:
                    if patient_in_queue.pesel == patient.pesel:
                        raise ValueError(
                            "Jest w kolejce pacjent o podanym numerze PESEL")
                return True
        elif patient is not None:
            return True
        else:
            return False

    def add_patient(self, patient):
        """
        Dodaje pacjenta do kopca i przywraca porządek kopca minimalnego.
        """
        if self.validating_addition(patient):
            self.heap.append(patient)
        self._build_heap()

    def get_next_patient(self):
        """
        Funkcja, która usuwa pierwszego pacjenta z kolejki i przywraca właściwość kopca.
        """
        if self.is_empty():
            print("Wszyscy pacjenci zostali zbadani")
            logging.info("Wszyscy pacjenci zostali zbadani")
            return
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        next_patient = self.heap.pop()
        self._heapify_min(len(self.heap), 0)
        return next_patient

    def is_empty(self):
        """
        Sprawdza, czy kolejka jest pusta.
        :return: Zwraca True, kiedy kolejka jest pusta, a False, jeżeli jest jakiś element.
        """
        return len(self.heap) == 0

    def _build_heap(self):
        """
        Buduje kopiec minimalny z listy.
        """
        n = len(self.heap)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_min(n, i)

    def _heapify_min(self, n, i):
        """
        Funkcja odpowiedzialna za tworzenie kopca minimalnego.
        :param n: To długość danych wejściowych, z jakiej będzie zrobiony kopiec.
        :param i: To miejsce, od którego przywracamy porządek kopca minimalnego.
        """
        smallest = i  # indeks najmniejszego elementu, na początku 0
        left_child = 2 * i + 1  # lewy potomek, badanego węzła
        right_child = 2 * i + 2  # prawy potomek, badanego węzła

        if left_child < n and self.heap[left_child].time_of_visit < self.heap[smallest].time_of_visit:
            smallest = left_child
        if right_child < n and self.heap[right_child].time_of_visit < self.heap[smallest].time_of_visit:
            smallest = right_child
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_min(n, smallest)

    def display_queue(self):
        """
        Funkcja wyświetlająca dane pacjentów z kolejki w kolejności czasu wizyty.
        :return: Zwraca posortowaną tablicę pacjentów
        """
        if len(self.heap) == 0:
            raise Exception("Kolejka jest pusta")
        else:
            temp_heap = self.heap[:]
            sorted_patients = []

            while temp_heap:
                temp_heap[0], temp_heap[-1] = temp_heap[-1], temp_heap[0]
                sorted_patients.append(temp_heap.pop())
                self._heapify_min(len(temp_heap), 0)

            return sorted_patients

    def insert_patient(self, patient, position):
        """
         Wstawia pacjenta priorytetowego w określone miejsce w kolejce.
         Jeśli pacjent nie ma określonej godziny wizyty, ustala ją na podstawie
         czasu pomiędzy sąsiadującymi pacjentami.

         :param patient: To pacjent, którego będziemy dodawać do kolejki.
         :param position: Indeks, w którym pacjent powinien być wstawiony.
         """

        if position < 0 or position > len(self.heap):
            print("Niewłaściwa pozycja")
            logging.info("Niewłaściwa pozycja")
            return
        if self.validating_addition(patient):
            if 0 < position < len(self.heap):
                prev_time = self.heap[position - 1].time_of_visit
                next_time = self.heap[position].time_of_visit
                patient.time_of_visit = prev_time + (next_time - prev_time) / 2
            elif position == 0:
                patient.time_of_visit = self.heap[0].time_of_visit - \
                    timedelta(minutes=10)
            else:
                patient.time_of_visit = self.heap[-1].time_of_visit + \
                    timedelta(minutes=10)

        self.heap.insert(position, patient)
        self._build_heap()

    def remove_patient(self, position=0):
        """
        Funkcja, która usunie pacjenta z dowolnego miejsca z kolejki. Jeśli użyty bez parametru usunie pierwszą osobę z kolejki.
        :param position: Pozycja, z której zostanie usunięty pacjent
        :return: None
        """
        if len(self.heap) == 0:
            print("Nie ma pacjenta, którego można usunąć")
            logging.info("Nie ma pacjenta, którego można usunąć")
        else:
            self.heap.pop(position)
            self._build_heap()  # Przywrócenie porządku kopca

    def waiting_inline(self):
        """
        Długo wyczekiwana funkcja odzwierciedlająca oczekiwanie na przyjęcie do lekarza.
        :return: Nic nie zwraca po prostu czekasz... tak w nieskończoność
        """
        while True:
            print("Trwa oczekiwanie na wolne terminy")
            logging.info("Trwa czekanie na wolne terminy")
            time.sleep(5)


def create_patient() -> Patient | None:
    """
    Funkcja tworząca pacjenta za pomocą danych podanych z klawiatury.
    :return: Patient
    """
    try:
        name = input("Podaj imię pacjenta: ")
        if not name.isalpha():
            raise ValueError("Imię musi składać się z liter.")
        if len(name) < 2:
            raise ValueError(
                "Imię musi składać się z co najmniej dwóch liter.")
        surname = input("Podaj nazwisko pacjenta: ")
        if not surname.isalpha():
            raise ValueError("Nazwisko musi składać się z liter.")
        if len(surname) < 2:
            raise ValueError(
                "Nazwisko musi składać się z co najmniej dwóch liter.")
        age = int(input("Podaj wiek pacjenta: "))
        if age <= 0:
            raise ValueError("Wiek musi być liczbą dodatnią.")
        pesel = int(input("Podaj PESEL pacjenta: "))
        if pesel >= 10000000000 or pesel < 0 or len(str(pesel)) != 11:
            raise ValueError("PESEL musi składać się z 11 cyfr.")
        gender_input = input("Podaj płeć pacjenta (Mężczyzna/Kobieta): ")
        if gender_input == "Mężczyzna":
            gender = Gender.M
        elif gender_input == "Kobieta":
            gender = Gender.K
        else:
            raise ValueError("Płeć musi być 'Mężczyzna' lub 'Kobieta'.")
        time_of_visit_input = input("Podaj godzinę wizyty (HH:MM): ")
        time_of_visit = datetime.strptime(time_of_visit_input, "%H:%M")
        return Patient(name, surname, age, pesel, gender, time_of_visit)
    except ValueError as e:
        print(f"Błąd: {e}")
        return None
