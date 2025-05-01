async function createAssistant() {
    const type = document.getElementById("assistantType").value.trim();
    const rawFilenames = document.getElementById("filenames").value.trim();
    const filenames = rawFilenames ? rawFilenames.split(",").map(f => f.trim()) : [];

    const response = await fetch("http://localhost:8000/assistants", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            type: type,
            filename: filenames
        })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById("response").innerText = `✅ Assistant created with ID:\n${data.assistant_id}`;
    } else {
        document.getElementById("response").innerText = `❌ Error:\n${data.detail}`;
    }
}

async function sendPrompt() {
    const assistantId = document.getElementById("assistantId").value.trim();
    const prompt = document.getElementById("prompt").value.trim();

    const response = await fetch(`http://localhost:8000/assistants/${assistantId}/read`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById("response").innerText = `📘 Response:\n${data.response}`;
    } else {
        document.getElementById("response").innerText = `❌ Error:\n${data.detail}`;
    }
}
