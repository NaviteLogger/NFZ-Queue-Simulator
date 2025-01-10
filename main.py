"""
Projekt na laboratorium przedmiotu Algorytmy i Struktury Danych.
"""
import logging

class Patient:
    """
    Klasa opisująca pacjenta stojącego w kolejce do lekarza.
    """
    def __init__(self,name,surname,age,pesel,gender,time_of_visit):
        """
        Konstruktor tworzący instancje obiektu, jakim jest pacjent.

        :param name: To string przechowujący imię pacjenta.
        :param surname: To string przechowujący nazwisko pacjenta.
        :param age: To liczba całkowita przechowująca wiek pacjenta.
        :param pesel: To string przechowujący unikalne ID pacjenta.
        :param gender: To string mówiący o tym, jakiej płci jest pacjent.
        :param time_of_visit: To godzina o, której miał pacjent umówioną wizytę.
        """
        self.name = name
        self.surname = surname
        self.age = age
        self.pesel = pesel
        self.gender =gender
        self.time_of_visit = time_of_visit #Pytanie co do godziny czy importujemy time, czy zwykły string

        self. next_in_line = None

    def __eq__(self, other):
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
        print("Imię: %s" %self.name)
        print("Nazwisko: %s" %self.surname)
        print("Wiek: %d" %self.age)
        print("PESEL: %s" % self.pesel)
        print("Płeć: %s" %self.gender)
        print("Godzina wizyty: %s" %self.time_of_visit)


class PatientQueue:
   """
   Klasa, która przechowuje informacje o pacjentach czekających do lekarza.
   """
   def __init__(self):
       self.head = None

   def add_patient(self, patient):
       """
       Funkcja dodająca pacjenta na koniec kolejki.
       :param patient: Przechowuje pacjenta, który dochodzi do kolejki
       :return: None
       """
       if patient is not None:
           if self.head is None:
               self.head = patient
           else:
               current_patient = self.head
               while current_patient.next_in_line is not None:
                   current_patient = current_patient.next_in_line
               current_patient.next_in_line = patient

   def display_queue(self):
       """
       Funkcja wyświetlająca dane pacjentów z kolejki
       :return: None
       """
       if self.head is None:
           logging.info("Kolejka jest pusta")
       else:
           current = self.head
           while current is not None:
               logging.info(
                   f"Imię: {current.name}, Nazwisko: {current.surname}, Wiek: {current.age}, "
                   f"PESEL: {current.pesel}, Płeć: {current.gender}, Godzina wizyty: {current.time_of_visit}"
               )
               current = current.next_in_line

   def insert_patient(self, patient, place):
       """
       Funkcja pozwalająca na dodanie pacjenta na dowolnym miejscu w kolejce.
       :param patient: Przechowuje pacjenta wkładanego do kolejki
       :param place: Pozycja na, którą chcemy włożyć pacjenta
       :return: None
       """
       if place <= 0 or self.head is None:
           patient.next_in_line = self.head
           self.head = patient
       else:
           current_patient = self.head
           count = 1
           while count < place and current_patient.next_in_line is not None:
               current_patient = current_patient.next_in_line
               count += 1
           patient.next_in_line = current_patient.next_in_line
           current_patient.next_in_line = patient


   def remove_patient(self, position = 0):
       """
       Funkcja, która usunie pacjenta z dowolnego miejsca z kolejki. Jeśli użyty bez parametru usunie pierwszą osobę z kolejki.
       :param position: Pozycja, z której zostanie usunięty pacjent
       :return: None
       """
       if self.head is None:
           logging.info("Kolejka jest pusta")
           return
       if position == 0:
           self.head = self.head.next_in_line
       else:
           current_patient = self.head
           count = 1
           while count < position and current_patient.next_in_line is not None:
               current_patient = current_patient.next_in_line
               count += 1
           if current_patient.next_in_line is not None:
               current_patient.next_in_line = current_patient.next_in_line.next_in_line

def create_patient(): #To trzeba będzie uodpornić na idiotów! O ile chcemy tę funkcję
    """
    Funkcja tworząca pacjenta za pomocą danych podanych z klawiatury.
    :return: Patient
    """
    try:
        name = input("Podaj imię pacjenta: ")
        surname = input("Podaj nazwisko pacjenta: ")
        age = int(input("Podaj wiek pacjenta: "))
        if age <= 0:
            raise ValueError("Wiek musi być liczbą dodatnią.")
        pesel = input("Podaj PESEL pacjenta: ")
        if not pesel.isdigit() or len(pesel) != 11:
            raise ValueError("PESEL musi składać się z 11 cyfr.")
        gender = input("Podaj płeć pacjenta (Mężczyzna/Kobieta): ")
        if gender not in ["Mężczyzna", "Kobieta"]:
            raise ValueError("Płeć musi być 'Mężczyzna' lub 'Kobieta'.")
        time_of_visit = input("Podaj godzinę wizyty (HH:MM): ")
        return Patient(name, surname, age, pesel, gender, time_of_visit)
    except ValueError as e:
        print(f"Błąd: {e}")
        return None
