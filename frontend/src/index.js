import { getData, postData } from "./api";
import { API_ENDPOINTS } from "./constants";

console.log("Frontend działa!");

// Sprawdzenie, czy JS działa
document.addEventListener("DOMContentLoaded", () => {
  console.log("JS działa, modyfikujemy DOM...");

  // Tworzenie elementów
  const container = document.createElement("div");

  const title = document.createElement("h1");
  title.textContent = "Frontend działa!";
  
  const fetchButton = document.createElement("button");
  fetchButton.id = "fetchData";
  fetchButton.textContent = "Pobierz dane";

  const sendButton = document.createElement("button");
  sendButton.id = "sendData";
  sendButton.textContent = "Wyślij dane";

  const output = document.createElement("pre");
  output.id = "output";

  // Dodanie elementów do strony
  container.appendChild(title);
  container.appendChild(fetchButton);
  container.appendChild(sendButton);
  container.appendChild(output);

  document.body.appendChild(container);

  // Obsługa pobierania danych
  document.getElementById("fetchData").addEventListener("click", async () => {
    console.log("Kliknięto Pobierz dane!");
    const data = await getData(API_ENDPOINTS.ROOT);
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
  });

  // Obsługa wysyłania danych
  document.getElementById("sendData").addEventListener("click", async () => {
    console.log("Kliknięto Wyślij dane!");
    const sampleData = { message: "Wiadomość testowa" };
    const response = await postData(API_ENDPOINTS.ROOT, sampleData);
    document.getElementById("output").textContent = JSON.stringify(response, null, 2);
  });
});

