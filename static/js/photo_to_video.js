document.getElementById("photo-video-btn").addEventListener("click", async () => {
    const input = document.getElementById("photo-input");
    const loader = document.getElementById("photo-loader");
    const preview = document.getElementById("photo-video");

    if (!input.files.length) return alert("Upload photos.");

    const formData = new FormData();
    Array.from(input.files).forEach(file => formData.append("photos", file));

    loader.style.display = "block";
    preview.style.display = "none";

    const res = await fetch("/photo_to_video", { method: "POST", body: formData });
    const blob = await res.blob();

    preview.src = URL.createObjectURL(blob);
    preview.style.display = "block";
    loader.style.display = "none";
});