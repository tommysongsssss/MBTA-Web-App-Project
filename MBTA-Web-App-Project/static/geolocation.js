document.addEventListener("DOMContentLoaded", () => {
  const useLocationBtn = document.getElementById("use-location-btn");
  const form = document.getElementById("search-form");
  const latField = document.getElementById("lat-field");
  const lngField = document.getElementById("lng-field");

  if (!useLocationBtn || !form || !latField || !lngField) {
    console.warn("Geolocation elements not found on page");
    return;
  }

  useLocationBtn.addEventListener("click", () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    useLocationBtn.disabled = true;
    const originalText = useLocationBtn.textContent;
    useLocationBtn.textContent = "Locating…";

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;

        // Put values into hidden inputs
        latField.value = latitude;
        lngField.value = longitude;

        // Optionally clear the text input so we know we’re using coords
        const placeInput = document.getElementById("place_name");
        if (placeInput) {
          placeInput.value = "";
        }

        // Submit the form; app.py will see lat/lng and redirect to /nearest_mbta_coords
        form.submit();
      },
      (error) => {
        console.error("Geolocation error:", error);
        alert("Could not get your location. Please type a place instead.");
        useLocationBtn.disabled = false;
        useLocationBtn.textContent = originalText;
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  });
});
