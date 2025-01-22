import unittest
from datetime import datetime

from patient import Patient, PatientQueue, Gender


class TestPatientQueue(unittest.TestCase):
    def setUp(self):
        """
        Przygotowanie danych testowych przed każdym testem.
        """
        self.queue = PatientQueue()
        self.patient1 = Patient("Anna", "Kowalska", 35, 12345678901, Gender.K, datetime.strptime("10:30", "%H:%M"))
        self.patient2 = Patient("Jan", "Nowak", 45, 98765432109, Gender.M, datetime.strptime("09:45", "%H:%M"))
        self.patient3 = Patient("Zofia", "Wiśniewska", 28, 56789012345, Gender.K, datetime.strptime("11:15", "%H:%M"))
        self.patient4 = Patient("Krzysztof", "Kowalczyk", 50, 12312312312, Gender.M, datetime.strptime("10:15", "%H:%M"))

    def test_add_patient_valid(self):
        """
        Test poprawnego dodawania pacjenta do kolejki.
        """
        self.queue.add_patient(self.patient1)
        self.assertIn(self.patient1, self.queue.heap)
        self.assertEqual(self.queue.heap[0], self.patient1)

    def test_add_patient_duplicate_pesel(self):
        """
        Test dodawania pacjenta z takim samym PESEL-em.
        """
        self.queue.add_patient(self.patient1)
        duplicate_patient = Patient("Anna", "Kowalska", 35, 12345678901, Gender.K, datetime.strptime("11:00", "%H:%M"))
        with self.assertRaises(ValueError) as context:
            self.queue.add_patient(duplicate_patient)
        self.assertEqual(str(context.exception), "Jest w kolejce pacjent o podanym numerze PESEL")

    def test_add_patient_time_conflict(self):
        """
        Test dodawania pacjenta z konfliktem czasowym (odstęp < 10 minut).
        """
        self.queue.add_patient(self.patient1)
        conflict_patient = Patient("Marta", "Kowalska", 30, 98765432101, Gender.K, datetime.strptime("10:35", "%H:%M"))
        with self.assertRaises(ValueError) as context:
            self.queue.add_patient(conflict_patient)
        self.assertEqual(str(context.exception), "Odstęp pomiędzy umówionymi wizytami to minimum 10 minut")

    def test_get_next_patient(self):
        """
        Test pobierania pacjenta o najwyższym priorytecie.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        next_patient = self.queue.get_next_patient()
        self.assertEqual(next_patient, self.patient2)  # Pacjent z godz. 09:45 ma najwyższy priorytet
        self.assertNotIn(next_patient, self.queue.heap)

    def test_get_next_patient_empty(self):
        """
        Test pobierania pacjenta z pustej kolejki.
        """
        with self.assertLogs(level="INFO") as log:
            self.queue.get_next_patient()
            self.assertIn("Wszyscy pacjenci zostali zbadani", log.output[-1])

    def test_insert_patient_valid(self):
        """
        Test poprawnego wstawiania pacjenta na określoną pozycję.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.insert_patient(self.patient4, 1)
        self.assertIn(self.patient4, self.queue.heap)
        self.assertEqual(self.queue.heap[1], self.patient4)

    def test_insert_patient_invalid_position(self):
        """
        Test wstawiania pacjenta na niepoprawną pozycję.
        """
        with self.assertLogs(level="INFO") as log:
            self.queue.insert_patient(self.patient1, -1)
            self.assertIn("Niewłaściwa pozycja", log.output[-1])

    def test_remove_patient(self):
        """
        Test usuwania pacjenta z kolejki.
        """
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.remove_patient(0)
        self.assertNotIn(self.patient2, self.queue.heap)

    def test_remove_patient_empty(self):
        """
        Test usuwania pacjenta z pustej kolejki.
        """
        with self.assertLogs(level="INFO") as log:
            self.queue.remove_patient()
            self.assertIn("Nie ma pacjenta, którego można usunąć", log.output[-1])

    def test_display_queue_empty(self):
        """
        Test wyświetlania pustej kolejki.
        """
        with self.assertRaises(Exception) as context:
            self.queue.display_queue()
        self.assertEqual(str(context.exception), "Kolejka jest pusta")


if __name__ == "__main__":
    unittest.main()
