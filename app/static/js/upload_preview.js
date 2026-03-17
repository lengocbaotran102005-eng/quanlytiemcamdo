document.addEventListener("change", event => {
  const input = event.target;
  if (!(input instanceof HTMLInputElement)) return;
  if (!input.matches("[data-upload-preview]")) return;

  const targetSelector = input.dataset.uploadPreviewTarget;
  if (!targetSelector) return;

  const container = document.querySelector(targetSelector);
  if (!container) return;

  container.innerHTML = "";
  const files = input.files;
  if (!files) return;

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = e => {
      const img = document.createElement("img");
      img.src = e.target?.result as string;
      img.className = "w-24 h-24 object-cover rounded-md border";
      container.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});

