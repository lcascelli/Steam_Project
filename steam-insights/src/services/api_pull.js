export async function getPrediction(inputData) {
    const response = await fetch("https://steam-project-3ph9.onrender.com/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(inputData),
    });
    if (!response.ok) {
        throw new Error("Prediction request failed");
    }

    return response.json();
}