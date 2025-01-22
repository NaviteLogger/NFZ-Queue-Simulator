from flask import Flask, jsonify, request
from datetime import datetime
from patient import Patient, PatientQueue, Gender
import random

app = Flask(__name__)
queue = PatientQueue()

# Prepare sample data for the application

test_patient_1 = Patient("Jan", "Kowalski", 45, 12345678900,
                         Gender.M, datetime.strptime("10:00", "%H:%M"))
test_patient_2 = Patient("Anna", "Nowak", 30, 98765432100,
                         Gender.K, datetime.strptime("10:30", "%H:%M"))
test_patient_3 = Patient("Piotr", "Wiśniewski", 60, 11223344559,
                         Gender.M, datetime.strptime("11:00", "%H:%M"))
test_patient_4 = Patient("Katarzyna", "Dąbrowska", 25,
                         99887766544, Gender.K, datetime.strptime("11:30", "%H:%M"))
test_patient_5 = Patient("Marek", "Zieliński", 35, 11223346559,
                         Gender.M, datetime.strptime("12:00", "%H:%M"))
test_patient_6 = Patient("Joanna", "Kowalska", 55, 99886766544,
                         Gender.K, datetime.strptime("12:30", "%H:%M"))

test_patients = [test_patient_1, test_patient_2,
                 test_patient_3, test_patient_4, test_patient_5, test_patient_6]
for patient in test_patients:
    queue.add_patient(patient)

queue._build_heap()

patients_names = ['Marek', 'Marek', 'Piotr', 'Piotr', 'Katarzyna', 'Adam', 'Anna', 'Maria', 'Adam',
                  'Katarzyna', 'Joanna', 'Joanna', 'Katarzyna', 'Katarzyna', 'Ewa', 'Ewa', 'Adam', 'Anna', 'Adam', 'Anna']
patients_surnames = ['Lewandowski', 'Kowalski', 'Wiśniewski', 'Kowalski', 'Lewandowski', 'Lewandowski', 'Szymańska', 'Nowak', 'Nowak',
                     'Zieliński', 'Kowalski', 'Nowak', 'Kamińska', 'Zieliński', 'Lewandowski', 'Szymańska', 'Wiśniewski', 'Kowalski', 'Jankowski', 'Szymańska']
patients_ages = [72, 64, 25, 36, 40, 42, 62, 37,
                 34, 60, 78, 70, 49, 45, 75, 32, 69, 22, 73, 53]
patients_pesels = [51865245538, 83610573741, 48851829967, 90052333796, 95940017667, 80897097432, 33312443591, 98381704625, 21658788306,
                   55917027400, 29532645761, 71257891241, 54341812113, 18737116334, 24747502375, 67430118272, 19595750169, 42833190250, 82458203770, 17133099951]
patients_genders = ['Mężczyzna', 'Mężczyzna', 'Kobieta', 'Mężczyzna', 'Mężczyzna', 'Mężczyzna', 'Kobieta', 'Kobieta', 'Kobieta', 'Mężczyzna',
                    'Kobieta', 'Kobieta', 'Kobieta', 'Mężczyzna', 'Kobieta', 'Kobieta', 'Mężczyzna', 'Kobieta', 'Mężczyzna', 'Kobieta']
patients_hours = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
                  '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30']


@app.route('/')
def index():
    """Serve the single-page application."""
    with open("templates/single_page.html", "r", encoding="utf-8") as file:
        return file.read()


@app.route('/api/random-patient', methods=['GET'])
def get_random_patient():
    """Return a random patient's data so that the user does not have to fill everything in."""
    patient_index = 0
    return jsonify({
        "name": random.choice(patients_names),
        "surname": random.choice(patients_surnames),
        "age": random.choice(patients_ages),
        "gender": random.choice(patients_genders),
        "pesel": random.choice(patients_pesels),
        "time_of_visit": random.choice(patients_hours)
    })


@ app.route('/api/queue/length', methods=['GET'])
def get_queue_length():
    """Return the length of the queue."""
    return jsonify({"length": len(queue.heap)})


@ app.route('/api/patients', methods=['GET'])
def get_patients():
    """Return the list of patients."""
    patients = [{
        "index": i,
        "name": p.name,
        "surname": p.surname,
        "age": p.age,
        "pesel": p.pesel,
        "gender": p.gender.value,
        "time_of_visit": p.time_of_visit.strftime('%H:%M'),
    } for i, p in enumerate(queue.display_queue())]
    print(patients)
    return jsonify(patients)


@ app.route('/api/patient', methods=['POST'])
def add_patient():
    """Add a new patient to the queue."""
    data = request.json
    try:
        gender = Gender.K if data["gender"] == "Kobieta" else Gender.M
        time_of_visit = datetime.strptime(data["time_of_visit"], "%H:%M")
        patient = Patient(
            data["name"],
            data["surname"],
            int(data["age"]),
            int(data["pesel"]),
            gender,
            time_of_visit
        )
        queue.add_patient(patient)
        return jsonify({"message": "Patient added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ app.route('/api/patient/insert', methods=['POST'])
def insert_patient():
    """
    Insert a patient at a specific position in the queue.
    """
    data = request.json

    # Get the length of the queue
    queue_length = len(queue.heap)
    try:
        if queue_length == 0:
            position = 0
        else:
            position = int(data["position"]) - 1
        gender = Gender.K if data["gender"] == "Kobieta" else Gender.M

        patient = Patient(
            data["name"],
            data["surname"],
            int(data["age"]),
            int(data["pesel"]),
            gender,
            None
        )
        queue.insert_patient(patient, position)
        return jsonify({"message": "Patient inserted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/patient/next', methods=['DELETE'])
def remove_patient():
    """Remove the next patient from the queue."""
    if queue.is_empty():
        return jsonify({"error": "No patients in the queue."}), 400
    patient = queue.get_next_patient()
    return jsonify({
        "message": "Patient removed successfully!",
        "removed_patient": {
            "name": patient.name,
            "surname": patient.surname
        }
    }), 200


@app.route('/api/patient/<int:index>', methods=['DELETE'])
def delete_patient_by_index(index):
    """Delete a patient by index."""
    if index < 0 or index >= len(queue.heap):
        return jsonify({"error": "Invalid index."}), 400

    # Assuming this method removes the patient
    queue.remove_patient(index-1)
    return jsonify({
        "message": "Patient removed successfully!",
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
