document.getElementById("art-btn").addEventListener("click", async () => {
    const prompt = document.getElementById("art-input").value.trim();
    const preview = document.getElementById("art-preview");

    if (!prompt) return alert("Enter prompt.");

    preview.src = "";
    preview.alt = "Generating image...";

    const res = await fetch("/ai_art", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    const blob = await res.blob();
    preview.src = URL.createObjectURL(blob);
    preview.alt = "Generated art";
});