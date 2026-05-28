/** Basis-URL des FastAPI-Backends */
const API_URL = "http://localhost:8000";

// --------------------
// Auth
// --------------------

export async function registerUser(username: string, email: string, password: string) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, email, password })
  });

  if (!response.ok) {
    throw new Error("Registrierung fehlgeschlagen");
  }

  return response.json();
}

export async function loginUser(username: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: formData
  });

  if (!response.ok) {
    throw new Error("Login fehlgeschlagen");
  }

  const data = await response.json();
  localStorage.setItem("token", data.access_token);

  return data;
}

export function logoutUser() {
  localStorage.removeItem("token");
}

export function getToken() {
  return localStorage.getItem("token");
}

// --------------------
// Recipes
// --------------------

export async function getRecipes() {
  const response = await fetch(`${API_URL}/recipes`);

  if (!response.ok) {
    throw new Error("Rezepte konnten nicht geladen werden");
  }

  return response.json();
}
export async function getRecipe(id: string) {
  const response = await fetch(`${API_URL}/recipes/${id}`);

  if (!response.ok) {
    throw new Error("Rezept konnte nicht geladen werden");
  }

  return response.json();
}

export async function rateRecipe(id: string, rating: number) {
  const response = await fetch(`${API_URL}/recipes/${id}/rating`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ rating })
  });

  if (!response.ok) {
    throw new Error("Bewertung konnte nicht gespeichert werden");
  }

  return response.json();
}