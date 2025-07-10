document.getElementById("anime-btn").addEventListener("click", async () => {
    const input = document.getElementById("anime-input");
    const preview = document.getElementById("result-img");

    if (!input.files.length) return alert("Choose an image.");

    const formData = new FormData();
    formData.append("image", input.files[0]);

    preview.src = "";
    preview.alt = "Processing...";

    const res = await fetch("/anime", { method: "POST", body: formData });
    const blob = await res.blob();

    preview.src = URL.createObjectURL(blob);
    preview.alt = "Anime-style image";
});