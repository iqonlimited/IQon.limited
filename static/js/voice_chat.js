let recognition;
const micBtn = document.getElementById("mic-btn");
const output = document.getElementById("voice-response");

micBtn.addEventListener("click", () => {
    if (!("webkitSpeechRecognition" in window)) {
        return alert("Voice recognition not supported.");
    }

    recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;

    recognition.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        const res = await fetch("/voice_query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ voice: transcript })
        });
        const data = await res.json();
        output.innerText = data.reply;
    };

    recognition.start();
});
<script>
function startListening() {
  const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();
  recognition.onresult = (e) => {
    document.getElementById("transcript").innerText = e.results[0][0].transcript;
  };
}
</script>
