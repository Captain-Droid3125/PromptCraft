let lastPrompt = "";
let lastBlob = null;

document.getElementById("generate-btn").addEventListener("click", () => {
    const prompt = document.getElementById("prompt-input").value.trim();
    if (!prompt) {
        alert("Please enter a prompt.");
        return;
    }

    generateImage(prompt);
});

document.getElementById("regenerate-btn").addEventListener("click", () => {
    if (lastPrompt) {
        generateImage(lastPrompt);
    }
});

document.getElementById("download-btn").addEventListener("click", () => {
    if (lastBlob) {
        const url = URL.createObjectURL(lastBlob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "generated_image.png";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
});

generateBtn.addEventListener("click", async () => {
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  // Show loader, hide buttons and image
  loading.style.display = "block";
  generatedImage.style.display = "none";
  downloadBtn.style.display = "none";
  regenerateBtn.style.display = "none";

  try {
    const response = await fetch("/api/generate-image/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    const data = await response.json();
    if (data.image_path) {
      generatedImage.src = data.image_path;
      downloadBtn.href = data.image_path;

      // Show image + buttons after loading
      generatedImage.style.display = "block";
      downloadBtn.style.display = "inline-block";
      regenerateBtn.style.display = "inline-block";
    } else {
      alert("Image generation failed.");
    }
  } catch (error) {
    alert("An error occurred: " + error.message);
  } finally {
    loading.style.display = "none";
  }
});


function generateImage(prompt) {
    document.getElementById("generate-btn").disabled = true;
    document.getElementById("regenerate-btn").disabled = true;
    document.getElementById("download-btn").disabled = true;
    lastPrompt = prompt;

    fetch("/api/generate-image/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt })
    })
    .then(response => {
        if (!response.ok) throw new Error("Failed to generate image");
        return response.blob();
    })
    .then(blob => {
        const imageURL = URL.createObjectURL(blob);
        document.getElementById("output-image").src = imageURL;
        lastBlob = blob;
        document.getElementById("download-btn").disabled = false;
        document.getElementById("regenerate-btn").disabled = false;
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong while generating the image.");
    })
    .finally(() => {
        document.getElementById("generate-btn").disabled = false;
    });
}
