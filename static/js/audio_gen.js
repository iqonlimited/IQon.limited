document.getElementById("audio-btn").addEventListener("click", async () => {
    const input = document.getElementById("ebook-select").value;
    const loader = document.getElementById("audio-loader");
    const player = document.getElementById("audio-player");

    loader.style.display = "inline";

    const res = await fetch("/generate_audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ebook: input })
    });

    const blob = await res.blob();
    player.src = URL.createObjectURL(blob);
    loader.style.display = "none";
    player.style.display = "block";
});