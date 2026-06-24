const fileInput = document.getElementById("file-input");
const dropzone = document.getElementById("dropzone");
const fileNameEl = document.getElementById("file-name");
const form = document.getElementById("upload-form");
const submitBtn = document.getElementById("submit-btn");
const nColorsInput = document.getElementById("n-colors");
const nColorsOutput = document.getElementById("n-colors-output");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const resultImage = document.getElementById("result-image");
const swatchStrip = document.getElementById("swatch-strip");
const downloadLink = document.getElementById("download-link");

const API_ENDPOINT = "/api/palette";

let selectedFile = null;

nColorsInput.addEventListener("input", () => {
  nColorsOutput.textContent = nColorsInput.value;
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    setFile(fileInput.files[0]);
  }
});

function setFile(file) {
  selectedFile = file;
  fileNameEl.textContent = file.name;
  submitBtn.disabled = false;
  hideResult();
  setStatus("Upload da imagem concluída com sucesso.");
  setTimeout(() => {
          setStatus("");
  }, 1500);
}


["dragenter", "dragover"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove("dragover");
  });
});

dropzone.addEventListener("drop", (event) => {
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    setFile(files[0]);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!selectedFile) {
    return;
  }

  submitBtn.disabled = true;
  hideResult();
  setStatus("Processando imagem e agrupando cores...");

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("n_colors", nColorsInput.value);

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null);
      const detail = errorBody && errorBody.detail ? errorBody.detail : "Erro ao processar a imagem.";
      throw new Error(detail);
    }

    const data = await response.json();

    renderResult(data);
    setStatus("");
  } catch (error) {
    if (error instanceof TypeError) {
      setStatus("Problema de conexão. Verifique sua internet e tente novamente.", true);
      return;
  }
    setStatus(error.message || "Erro inesperado ao processar a imagem.", true);
  } finally {
    submitBtn.disabled = false;
  }
});

function setStatus(message, isError = false) {
  if (!message) {
    statusEl.hidden = true;
    statusEl.textContent = "";
    statusEl.classList.remove("error");
    return;
  }

  statusEl.hidden = false;
  statusEl.textContent = message;
  statusEl.classList.toggle("error", isError);
}

function hideResult() {
  resultEl.hidden = true;
  swatchStrip.innerHTML = "";
  resultImage.src = "";
  downloadLink.removeAttribute("href");
  downloadLink.setAttribute("aria-disabled", "true");
}

function renderResult(data) {
  resultImage.src = data.image_base64;
  downloadLink.href = data.image_base64;
  downloadLink.setAttribute("aria-disabled", "false");


  swatchStrip.innerHTML = "";

  data.colors.forEach((color) => {
    const item = document.createElement("li");
    item.style.backgroundColor = color.hex;
    item.style.color = readableTextColor(color.rgb)
    item.title = color.hex;

    const hexEl = document.createElement("span");
    hexEl.className = "swatch-hex";
    hexEl.textContent = color.hex;

    item.appendChild(hexEl);

    item.addEventListener("click", () => {
      navigator.clipboard.writeText(color.hex).then(() => {
        const original = hexEl.textContent;
        hexEl.textContent = "copiado!";
        setTimeout(() => {
          hexEl.textContent = original;
        }, 800);
      });
    });

    swatchStrip.appendChild(item);
  });

  resultEl.hidden = false;
}

function readableTextColor([r, g, b]) {
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.6 ? "rgba(0,0,0,0.62)" : "rgba(255,255,255,0.82)";
}

