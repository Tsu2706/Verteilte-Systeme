const API_BASE_URL = "http://localhost:8000";

export type Recipe = {
  id: number;
  title: string;
  description?: string;
  ingredients?: string;
  instructions?: string;
  time?: string;
  difficulty?: string;
  image_url?: string;
  user_id?: number;
};

export type RecipeInput = {
  title: string;
  description?: string;
  ingredients?: string;
  instructions?: string;
  time?: string;
  difficulty?: string;
  image_url?: string;
};

export type User = {
  id: number;
  username: string;
  email: string;
};

function getToken() {
  return localStorage.getItem("token");
}

function authHeaders() {
  const token = getToken();

  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Ein Fehler ist aufgetreten.");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function getRecipes(): Promise<Recipe[]> {
  const response = await fetch(`${API_BASE_URL}/recipes`);
  return handleResponse(response);
}

export async function getRecipe(id: number): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}`);
  return handleResponse(response);
}

export async function createRecipe(data: RecipeInput): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(data)
  });

  return handleResponse(response);
}

export async function updateRecipe(id: number, data: RecipeInput): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(data)
  });

  return handleResponse(response);
}

export async function deleteRecipe(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
    method: "DELETE",
    headers: authHeaders()
  });

  await handleResponse(response);
}

export async function getMe(): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/users/me`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export async function getMyRecipes(): Promise<Recipe[]> {
  const response = await fetch(`${API_BASE_URL}/users/me/recipes`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}