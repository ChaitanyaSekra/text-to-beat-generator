async function generateBeat() {
  const prompt = document.getElementById("promptInput").value.trim();
  const loading = document.getElementById("loading");
  const downloadSection = document.getElementById("downloadSection");
  const downloadLink = document.getElementById("downloadLink");

  if (!prompt) {
    alert("Please enter a beat prompt.");
    return;
  }

  loading.classList.remove("hidden");
  downloadSection.classList.add("hidden");

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    if (data.download_url) {
      downloadLink.href = data.download_url;
      downloadSection.classList.remove("hidden");
    } else {
      alert("Generation failed.");
    }
  } catch (error) {
    alert("Server error.");
  } finally {
    loading.classList.add("hidden");
  }
}
