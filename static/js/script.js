// ================= SPEECH SUPPORT =================
let voices = [];
speechSynthesis.onvoiceschanged = () => {
    voices = speechSynthesis.getVoices();
};

// ================= DEMO DATA =================
function fillDemo(){
    age.value = 55;
    sex.value = 1;
    cp.value = 2;
    trestbps.value = 140;
    chol.value = 240;
    fbs.value = 1;
    restecg.value = 1;
    thalach.value = 150;
    exang.value = 0;
    oldpeak.value = 1.2;
    slope.value = 1;
    ca.value = 0;
    thal.value = 2;
}

// ================= RESET =================
function resetForm(){
    document.querySelectorAll("input").forEach(i => i.value = "");
    riskFill.style.width = "0%";
    riskText.innerText = "";
    result.innerText = "";
}

// ================= PREDICT =================
function predict(){

    const inputValues = [
        parseFloat(age.value),
        parseFloat(sex.value),
        parseFloat(cp.value),
        parseFloat(trestbps.value),
        parseFloat(chol.value),
        parseFloat(fbs.value),
        parseFloat(restecg.value),
        parseFloat(thalach.value),
        parseFloat(exang.value),
        parseFloat(oldpeak.value),
        parseFloat(slope.value),
        parseFloat(ca.value),
        parseFloat(thal.value)
    ];

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            age: age.value,
            sex: sex.value,
            cp: cp.value,
            trestbps: trestbps.value,
            chol: chol.value,
            fbs: fbs.value,
            restecg: restecg.value,
            thalach: thalach.value,
            exang: exang.value,
            oldpeak: oldpeak.value,
            slope: slope.value,
            ca: ca.value,
            thal: thal.value
        })
    })

    .then(res => res.json())

    .then(data => {

        // RESULT
        result.innerText = data.result;
        riskFill.style.width = data.risk + "%";
        riskText.innerText = "Risk Level: " + data.risk + "%";

        // 🔹 UPDATE 13-INPUT CHART
        if (typeof updateChartFromInputs === "function") {
            updateChartFromInputs(inputValues);
        }
    })

    .catch(err => {
        console.error(err);
        alert("Prediction failed. Try again.");
    });
}
