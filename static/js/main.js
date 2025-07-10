document.getElementById("generate-video").addEventListener("click", async () => {
    const text = document.getElementById("video-text").value;
    const res = await fetch("/generate_video", {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: { "Content-Type": "application/json" }
    });

    const blob = await res.blob();
    const video = document.getElementById("video-preview");
    video.src = URL.createObjectURL(blob);
    video.style.display = "block";
});