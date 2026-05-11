// PhishGuard AI - content.js
// Robust Gmail email extractor with wait + retry

function waitForEmailBody(timeout = 5000) {
  return new Promise((resolve) => {
    const start = Date.now();

    const interval = setInterval(() => {
      const emailBody = document.querySelector("div.a3s");

      if (emailBody) {
        clearInterval(interval);
        resolve(emailBody.innerText);
      }

      if (Date.now() - start > timeout) {
        clearInterval(interval);
        resolve("NO_EMAIL_FOUND");
      }
    }, 300);
  });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "extract") {
    waitForEmailBody().then((text) => {
      sendResponse({ text });
    });
    return true; // REQUIRED for async response
  }
});
