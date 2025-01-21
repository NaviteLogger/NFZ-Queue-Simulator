from flask import Flask, jsonify, request
from datetime import datetime
from patient import Patient, PatientQueue, Gender

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

test_patients = [test_patient_1, test_patient_2,
                 test_patient_3, test_patient_4]
for patient in test_patients:
    queue.add_patient(patient)


@app.route('/')
def index():
    """Serve the single-page application."""
    with open("templates/single_page.html", "r", encoding="utf-8") as file:
        return file.read()


@app.route('/api/queue/length', methods=['GET'])
def get_queue_length():
    """Return the length of the queue."""
    return jsonify({"length": len(queue.heap)})


@app.route('/api/patients', methods=['GET'])
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
    } for i, p in enumerate(queue.heap)]
    return jsonify(patients)


@app.route('/api/patient', methods=['POST'])
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


@app.route('/api/patient/insert', methods=['POST'])
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


@app.route('/api/patient', methods=['DELETE'])
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


if __name__ == "__main__":
    app.run(debug=True)
