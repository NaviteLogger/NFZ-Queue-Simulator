import unittest
from main import Patient, PatientQueue, Gender  # Zakładam, że główny kod jest w pliku patient_queue.py


class TestPatient(unittest.TestCase):

    def test_patient_initialization(self):
        patient = Patient("Jan", "Kowalski", 30, "12345678901", Gender.M, "10:30")
        self.assertEqual(patient.name, "Jan")
        self.assertEqual(patient.surname, "Kowalski")
        self.assertEqual(patient.age, 30)
        self.assertEqual(patient.pesel, "12345678901")
        self.assertEqual(patient.gender, Gender.M)
        self.assertEqual(patient.time_of_visit, "10:30")
        self.assertIsNone(patient.next_in_line)


    def setUp(self):
        self.patient1 = Patient("Anna", "Nowak", 25, "11111111111", Gender.K, "09:00")
        self.patient2 = Patient("Anna", "Nowak", 25, "11111111111", Gender.K, "09:00")
        self.patient3 = Patient("Piotr", "Kowalski", 35, "22222222222", Gender.M, "10:30")

    def test_equal_patients(self):
        """Test porównania dwóch identycznych pacjentów."""
        self.assertTrue(self.patient1 == self.patient2)

    def test_not_equal_different_name(self):
        """Test porównania pacjentów z różnymi imionami."""
        self.patient2.name = "Piotr"
        self.assertFalse(self.patient1 == self.patient2)

    def test_not_equal_different_surname(self):
        """Test porównania pacjentów z różnymi nazwiskami."""
        self.patient2.surname = "Kowalski"
        self.assertFalse(self.patient1 == self.patient2)

    def test_not_equal_different_age(self):
        """Test porównania pacjentów z różnym wiekiem."""
        self.patient2.age = 30
        self.assertFalse(self.patient1 == self.patient2)

    def test_not_equal_different_pesel(self):
        """Test porównania pacjentów z różnymi PESEL."""
        self.patient2.pesel = "33333333333"
        self.assertFalse(self.patient1 == self.patient2)

    def test_not_equal_different_gender(self):
        """Test porównania pacjentów z różną płcią."""
        self.patient2.gender = "Mężczyzna"
        self.assertFalse(self.patient1 == self.patient2)

    def test_not_equal_different_time_of_visit(self):
        """Test porównania pacjentów z różnymi godzinami wizyty."""
        self.patient2.time_of_visit = "11:00"
        self.assertFalse(self.patient1 == self.patient2)

    def test_not_equal_to_none(self):
        """Test porównania pacjenta z None."""
        self.assertFalse(self.patient1 is None)

    def test_not_equal_to_other_object(self):
        """Test porównania pacjenta z obiektem innej klasy."""
        self.assertFalse(self.patient1 == "Some String")


import unittest
from datetime import datetime, timedelta

class TestPatientQueue(unittest.TestCase):
    def setUp(self):
        """
        Przygotowanie danych testowych przed każdym testem.
        """
        self.queue = PatientQueue()
        self.patient1 = Patient("Anna", "Kowalska", 35, "12345678901", Gender.K, datetime.strptime("10:30", "%H:%M"))
        self.patient2 = Patient("Jan", "Nowak", 45, "98765432109", Gender.M, datetime.strptime("09:45", "%H:%M"))
        self.patient3 = Patient("Zofia", "Wiśniewska", 28, "56789012345", Gender.K, datetime.strptime("11:15", "%H:%M"))

    def test_add_patient(self):
        """
        Test dodawania pacjenta do kolejki.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.assertEqual(self.queue.heap[0], self.patient2)  # Pacjent o wcześniejszej godzinie powinien być pierwszy
        self.assertEqual(len(self.queue.heap), 2)  # Długość kolejki powinna wynosić 2

    def test_get_next_patient(self):
        """
        Test pobierania pacjenta o najwyższym priorytecie.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        next_patient = self.queue.get_next_patient()
        self.assertEqual(next_patient, self.patient2)  # Pacjent z godz. 09:45 powinien być pierwszy
        self.assertEqual(len(self.queue.heap), 1)  # Długość kolejki zmniejszona o 1

    def test_is_empty(self):
        """
        Test sprawdzania, czy kolejka jest pusta.
        """
        self.assertTrue(self.queue.is_empty())  # Początkowo kolejka powinna być pusta
        self.queue.add_patient(self.patient1)
        self.assertFalse(self.queue.is_empty())  # Po dodaniu pacjenta kolejka nie jest pusta

    def test_insert_patient_with_time(self):
        """
        Test wstawiania pacjenta priorytetowego z określonym czasem.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        patient_priority = Patient("Krzysztof", "Kowalczyk", 50, "12312312312", Gender.M, datetime.strptime("10:00", "%H:%M"))
        self.queue.insert_patient(patient_priority, 1)
        self.assertEqual(self.queue.heap[0], self.patient2)  # Pacjent z godz. 09:45 powinien pozostać pierwszy
        self.assertIn(patient_priority, self.queue.heap)  # Pacjent priorytetowy powinien być w kolejce

    def test_insert_patient_without_time(self):
        """
        Test wstawiania pacjenta priorytetowego bez określonego czasu.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        patient_priority = Patient("Krzysztof", "Kowalczyk", 50, "12312312312", Gender.M, None)
        self.queue.insert_patient(patient_priority, 1)
        self.assertIsNotNone(patient_priority.time_of_visit)  # Czas wizyty powinien zostać nadany
        self.assertIn(patient_priority, self.queue.heap)  # Pacjent priorytetowy powinien być w kolejce

    def test_remove_patient(self):
        """
        Test usuwania pacjenta z kolejki.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.remove_patient(0)
        self.assertNotIn(self.patient2, self.queue.heap)  # Pacjent na pozycji 0 powinien być usunięty
        self.assertEqual(len(self.queue.heap), 1)  # Długość kolejki zmniejszona o 1

    def test_remove_patient_empty_queue(self):
        """
        Test usuwania pacjenta z pustej kolejki.
        """
        with self.assertLogs(level="INFO") as log:
            self.queue.remove_patient()
            self.assertIn("Nie ma pacjenta, którego można usunąć", log.output[-1])

    def test_invalid_position_insert_patient(self):
        """
        Test wstawiania pacjenta na niepoprawną pozycję.
        """
        with self.assertLogs(level="INFO") as log:
            patient_priority = Patient("Krzysztof", "Kowalczyk", 50, "12312312312", Gender.M, None)
            self.queue.insert_patient(patient_priority, -1)  # Niepoprawna pozycja
            self.assertIn("Niewłaściwa pozycja", log.output[-1])

    def test_get_next_patient_empty_queue(self):
        """
        Test pobierania pacjenta z pustej kolejki.
        """
        with self.assertLogs(level="INFO") as log:
            self.queue.get_next_patient()
            self.assertIn("Wszyscy pacjenci zostali zbadani", log.output[-1])


if __name__ == "__main__":
    unittest.main()
