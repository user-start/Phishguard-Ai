// PhishGuard AI - popup.js
// Handles Scan button and backend communication

document.addEventListener("DOMContentLoaded", () => {
  const scanBtn = document.getElementById("scan");
  const resultEl = document.getElementById("result");

  scanBtn.addEventListener("click", async () => {
    resultEl.innerText = "Scanning...";

    try {
      // Get current active tab
      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
      });

      // Send message to content.js
      chrome.tabs.sendMessage(
        tab.id,
        { action: "extract" },
        async (response) => {

          console.log("Content script response:", response);

          if (!response || response.text === "NO_EMAIL_FOUND") {
            resultEl.innerText = "❗ Open an email first";
            return;
          }

          // Send extracted email text to backend
          const apiResponse = await fetch(
            "http://127.0.0.1:8000/predict",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ text: response.text })
            }
          );

          if (!apiResponse.ok) {
            resultEl.innerText = "❌ Backend error";
            return;
          }

          const data = await apiResponse.json();

          resultEl.innerText =
            `${data.verdict} (${data.score}%)`;
        }
      );
    } catch (error) {
      console.error("Scan error:", error);
      resultEl.innerText = "❌ Error occurred";
    }
  });
});
