document.getElementById("search-btn").addEventListener("click", async () => {
    const query = document.getElementById("search-input").value.trim();
    const resultsDiv = document.getElementById("search-results");

    if (!query) return alert("Enter something to search.");

    const res = await fetch("/search_all", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    const data = await res.json();
    resultsDiv.innerHTML = "";

    data.results.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("result-item");
        div.innerHTML = `<strong>${item.type}:</strong> ${item.title || item.content}`;
        resultsDiv.appendChild(div);
    });
});