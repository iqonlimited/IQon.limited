async function loadLeaderboard() {
    const res = await fetch("/leaderboard_data");
    const data = await res.json();
    const table = document.getElementById("leaderboard-table");
    table.innerHTML = "";

    data.forEach((entry, index) => {
        const row = `<tr>
            <td>${index + 1}</td>
            <td>${entry.name}</td>
            <td>${entry.city}</td>
            <td>${entry.state}</td>
            <td>${entry.country}</td>
            <td>${entry.chat_count}</td>
        </tr>`;
        table.innerHTML += row;
    });
}

window.onload = loadLeaderboard;