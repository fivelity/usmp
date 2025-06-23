// Image processing worker
self.onmessage = async function (e) {
  const { file } = e.data;

  try {
    // Create an image element
    const img = new Image();

    // Create a promise to handle image loading
    const imageLoadPromise = new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = reject;
    });

    // Load the image
    img.src = URL.createObjectURL(file);
    await imageLoadPromise;

    // Create a canvas for processing
    const canvas = new OffscreenCanvas(img.width, img.height);
    const ctx = canvas.getContext("2d");

    if (!ctx) {
      throw new Error("Failed to get canvas context");
    }

    // Draw the image
    ctx.drawImage(img, 0, 0);

    // Get the image data
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

    // Process the image (example: adjust brightness and contrast)
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
      // Adjust brightness
      data[i] = Math.min(255, (data[i] || 0) * 1.1); // R
      data[i + 1] = Math.min(255, (data[i + 1] || 0) * 1.1); // G
      data[i + 2] = Math.min(255, (data[i + 2] || 0) * 1.1); // B
      // Alpha channel (data[i + 3]) remains unchanged
    }

    // Put the processed image data back
    ctx.putImageData(imageData, 0, 0);

    // Convert to blob
    const blob = await canvas.convertToBlob({
      type: "image/jpeg",
      quality: 0.8,
    });

    // Create object URL
    const url = URL.createObjectURL(blob);

    // Send the result back
    self.postMessage({ url });

    // Cleanup
    URL.revokeObjectURL(img.src);
  } catch (error) {
    // Handle error with proper type checking
    const errorMessage =
      error instanceof Error ? error.message : "Unknown error occurred";
    self.postMessage({ error: errorMessage });
  }
};
