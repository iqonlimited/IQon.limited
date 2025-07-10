document.getElementById("generate-video").addEventListener("click", async () => {
    const input = document.getElementById("video-text").value.trim();
    const preview = document.getElementById("video-preview");
    const loader = document.getElementById("video-loader");

    if (!input) return alert("Enter text first.");

    loader.style.display = "block";
    preview.style.display = "none";

    const res = await fetch("/generate_video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input })
    });

    const blob = await res.blob();
    preview.src = URL.createObjectURL(blob);
    preview.style.display = "block";
    loader.style.display = "none";
});