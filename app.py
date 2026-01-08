from flask import Flask, render_template, request, jsonify, send_file
import pickle
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from datetime import datetime

app = Flask(__name__)

# Load ML model
with open("heart_model.pkl", "rb") as f:
    model = pickle.load(f)

# Store last patient
last_patient = {}

@app.route("/")
def overview():
    return render_template("overview.html")

@app.route("/decision")
def decision():
    return render_template("decision.html", patient=last_patient)

@app.route("/reports")
def reports():
    return render_template("reports.html", patient=last_patient)

@app.route("/predict", methods=["POST"])
def predict():
    global last_patient
    data = request.json

    cols = [
        'age','sex','cp','trestbps','chol','fbs','restecg',
        'thalach','exang','oldpeak','slope','ca','thal'
    ]

    df = pd.DataFrame([[data[c] for c in cols]], columns=cols)
    pred = model.predict(df)[0]

    risk = 78 if pred == 1 else 22
    result = "❤️ Heart Disease Detected" if pred == 1 else "✅ No Heart Disease Detected"

    last_patient = {
        "Age": int(data["age"]),
        "Sex": "Male" if int(data["sex"]) == 1 else "Female",
        "Chest Pain": int(data["cp"]),
        "Resting BP": int(data["trestbps"]),
        "Cholesterol": int(data["chol"]),
        "Fasting Sugar": int(data["fbs"]),
        "Rest ECG": int(data["restecg"]),
        "Max Heart Rate": int(data["thalach"]),
        "Exercise Angina": int(data["exang"]),
        "Oldpeak": float(data["oldpeak"]),
        "Slope": int(data["slope"]),
        "CA": int(data["ca"]),
        "Thal": int(data["thal"]),
        "Result": result,
        "Risk": f"{risk}%"
    }

    return jsonify(result=result, risk=risk)

@app.route("/download_report")
def download_report():
    if not last_patient:
        return "No report available"

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, h-50, "AI Heart Health Report")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, h-80, "Report created by Shivam Singh")
    pdf.drawString(50, h-100, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    y = h - 140
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Patient Details")
    y -= 25

    pdf.setFont("Helvetica", 11)
    for k, v in last_patient.items():
        pdf.drawString(60, y, f"{k}: {v}")
        y -= 16

    y -= 15
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Diet & Lifestyle Advice")
    y -= 22

    tips = [
        "Eat fruits and vegetables daily",
        "Avoid junk, oily and fried food",
        "Control salt and sugar intake",
        "Walk or exercise 30 minutes daily",
        "No smoking or alcohol",
        "Regular BP and cholesterol check"
    ]

    pdf.setFont("Helvetica", 11)
    for t in tips:
        pdf.drawString(60, y, "- " + t)
        y -= 16

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Heart_Report_Shivam_Singh.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
