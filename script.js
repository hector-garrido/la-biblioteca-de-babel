// Replace with the URL of your Cloud Run service (or Cloud Function)
// Example: https://pdf-generator-abcde-uc.a.run.app/generate-pdf
const API_URL = "https://babel-test-158992092192.us-central1.run.app/generate-pdf";

document.getElementById("genBtn").addEventListener("click", async () => {
  const btn = document.getElementById("genBtn");
  btn.disabled = true;
  btn.textContent = "Generating…";

  try {
    const resp = await fetch(API_URL, {method: "POST"});
    if (!resp.ok) throw new Error(`Server error ${resp.status}`);
    const data = await resp.json();           // {pdf_url: "..."}
    document.getElementById("link").innerHTML =
      `<a href="${data.pdf_url}" target="_blank">View generated PDF</a>`;
  } catch (e) {
    alert("Failed to generate PDF: " + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Create PDF";
  }
});