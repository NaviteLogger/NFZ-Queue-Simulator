import unittest
from main import Patient, PatientQueue  # Zakładam, że główny kod jest w pliku patient_queue.py


class TestPatient(unittest.TestCase):

    def test_patient_initialization(self):
        patient = Patient("Jan", "Kowalski", 30, "12345678901", "Mężczyzna", "10:30")
        self.assertEqual(patient.name, "Jan")
        self.assertEqual(patient.surname, "Kowalski")
        self.assertEqual(patient.age, 30)
        self.assertEqual(patient.pesel, "12345678901")
        self.assertEqual(patient.gender, "Mężczyzna")
        self.assertEqual(patient.time_of_visit, "10:30")
        self.assertIsNone(patient.next_in_line)


    def setUp(self):
        self.patient1 = Patient("Anna", "Nowak", 25, "11111111111", "Kobieta", "09:00")
        self.patient2 = Patient("Anna", "Nowak", 25, "11111111111", "Kobieta", "09:00")
        self.patient3 = Patient("Piotr", "Kowalski", 35, "22222222222", "Mężczyzna", "10:30")

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


class TestPatientQueue(unittest.TestCase):

    def setUp(self):
        self.queue = PatientQueue()
        self.patient1 = Patient("Anna", "Nowak", 25, "11111111111", "Kobieta", "09:00")
        self.patient2 = Patient("Piotr", "Kowalski", 35, "22222222222", "Mężczyzna", "09:30")
        self.patient3 = Patient("Maria", "Wiśniewska", 40, "33333333333", "Kobieta", "10:00")


    def test_add_patient_to_empty_queue(self):
        self.queue.add_patient(self.patient1)
        self.assertEqual(self.queue.head, self.patient1)

    def test_add_patient_to_non_empty_queue(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.assertEqual(self.queue.head.next_in_line, self.patient2)

    def test_display_queue(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.add_patient(self.patient3)
        with self.assertLogs(level="INFO") as log:
            self.queue.display_queue()
        self.assertIn("Imię: Anna", log.output[0])
        self.assertIn("Imię: Piotr", log.output[1])
        self.assertIn("Imię: Maria", log.output[2])

    def test_insert_patient_at_beginning(self):
        self.queue.add_patient(self.patient1)
        self.queue.insert_patient(self.patient2, 0)
        self.assertEqual(self.queue.head, self.patient2)

    def test_insert_patient_in_middle(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient3)
        self.queue.insert_patient(self.patient2, 1)
        self.assertEqual(self.queue.head.next_in_line, self.patient2)
        self.assertEqual(self.queue.head.next_in_line.next_in_line, self.patient3)

    def test_insert_patient_at_end(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.insert_patient(self.patient3, 3)
        self.assertEqual(self.queue.head.next_in_line.next_in_line, self.patient3)

    def test_remove_patient_from_beginning(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.remove_patient()
        self.assertEqual(self.queue.head, self.patient2)

    def test_remove_patient_from_middle(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.add_patient(self.patient3)
        self.queue.remove_patient(1)
        self.assertEqual(self.queue.head.next_in_line, self.patient3)

    def test_remove_patient_from_end(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.add_patient(self.patient3)
        self.queue.remove_patient(2)
        self.assertIsNone(self.queue.head.next_in_line.next_in_line)

    def test_remove_patient_from_empty_queue(self):
        with self.assertLogs(level="INFO") as log:
            self.queue.remove_patient()
        self.assertIn("Kolejka jest pusta", log.output[0])

    def test_display_empty_queue(self):
        with self.assertLogs(level="INFO") as log:
            self.queue.display_queue()
        self.assertIn("Kolejka jest pusta", log.output[0])

    def test_insert_patient_in_empty_queue(self):
        self.queue.insert_patient(self.patient1, 0)
        self.assertEqual(self.queue.head, self.patient1)

    def test_insert_patient_out_of_bounds(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.insert_patient(self.patient3, 10)  # Wstaw na pozycję większą niż rozmiar kolejki
        self.assertEqual(self.queue.head.next_in_line.next_in_line, self.patient3)  # Pacjent trafia na koniec kolejki

    def test_remove_patient_out_of_bounds(self):
        self.queue.add_patient(self.patient1)
        self.queue.add_patient(self.patient2)
        self.queue.remove_patient(5)  # Próba usunięcia pacjenta z pozycji, która nie istnieje
        self.assertEqual(self.queue.head, self.patient1)
        self.assertEqual(self.queue.head.next_in_line, self.patient2)

    def test_add_patient_with_edge_values(self):
        patient = Patient("", "", 0, "00000000000", "Nieznana", "00:00")
        self.queue.add_patient(patient)
        self.assertEqual(self.queue.head, patient)
        self.assertEqual(self.queue.head.name, "")
        self.assertEqual(self.queue.head.surname, "")
        self.assertEqual(self.queue.head.age, 0)
        self.assertEqual(self.queue.head.pesel, "00000000000")
        self.assertEqual(self.queue.head.gender, "Nieznana")
        self.assertEqual(self.queue.head.time_of_visit, "00:00")

    def test_remove_only_patient(self):
        self.queue.add_patient(self.patient1)
        self.queue.remove_patient()
        self.assertIsNone(self.queue.head)

    def test_insert_patient_before_only_patient(self):
        self.queue.add_patient(self.patient1)
        self.queue.insert_patient(self.patient2, 0)
        self.assertEqual(self.queue.head, self.patient2)
        self.assertEqual(self.queue.head.next_in_line, self.patient1)

    def test_insert_patient_after_only_patient(self):
        self.queue.add_patient(self.patient1)
        self.queue.insert_patient(self.patient2, 1)
        self.assertEqual(self.queue.head, self.patient1)
        self.assertEqual(self.queue.head.next_in_line, self.patient2)

    def test_large_queue(self):
        for i in range(1000):
            self.queue.add_patient(Patient(f"Name{i}", f"Surname{i}", i, str(i).zfill(11), "Mężczyzna", "12:00"))

        self.assertEqual(self.queue.head.name, "Name0")
        current = self.queue.head
        count = 0
        while current is not None:
            count += 1
            current = current.next_in_line
        self.assertEqual(count, 1000)


if __name__ == "__main__":
    unittest.main()
