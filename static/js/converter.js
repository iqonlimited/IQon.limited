document.getElementById("convert-btn").addEventListener("click", async () => {
    const fileInput = document.getElementById("file-input");
    const format = document.getElementById("format-select").value;
    const resultDiv = document.getElementById("conversion-result");

    if (!fileInput.files.length) return alert("Select a file first.");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("format", format);

    resultDiv.innerText = "Converting...";

    const res = await fetch("/convert", { method: "POST", body: formData });
    const blob = await res.blob();

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `converted.${format}`;
    a.click();

    resultDiv.innerText = "File ready! Downloaded.";
});