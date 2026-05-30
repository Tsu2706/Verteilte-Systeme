import { browser } from "$app/environment";

const API_BASE_URL = "http://localhost:8000";

export type Tag = {
  id: number;
  name: string;
};

export type Recipe = {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  ingredients: string[];
  steps: string[];
  is_public: boolean;
  tags?: Tag[];
  time?: string | null;
  difficulty?: string | null;
};

export type RecipeInput = {
  title: string;
  description?: string | null;
  ingredients: string[];
  steps: string[];
  is_public?: boolean;
  tag_ids?: number[];
  time?: string | null;
  difficulty?: string | null;
};

export type Rating = {
  id: number;
  user_id: number;
  recipe_id: number;
  rating: number;
};

export type RatingSummary = {
  average: number;
  count: number;
  my_rating: number | null;
};

export type User = {
  id: number;
  username: string;
  email: string;
};

function getToken() {
  if (!browser) return null;
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
    let message = "Ein Fehler ist aufgetreten.";

    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      message = (await response.text()) || message;
    }

    throw new Error(message);
  }

  if (response.status === 204) return null;
  return response.json();
}

export async function getRecipes(): Promise<Recipe[]> {
  const response = await fetch(`${API_BASE_URL}/recipes`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export async function searchRecipes(
  q: string,
  ingredient: string = "",
  tagIds: number[] = []
): Promise<Recipe[]> {
  const params = new URLSearchParams();

  if (q.trim()) params.set("q", q.trim());
  if (ingredient.trim()) params.set("ingredient", ingredient.trim());

  for (const tagId of tagIds) {
    params.append("tag_ids", String(tagId));
  }

  const response = await fetch(`${API_BASE_URL}/recipes/search?${params.toString()}`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export async function getRecipe(id: number): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export async function createRecipe(data: RecipeInput): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      ...data,
      tag_ids: data.tag_ids ?? []
    })
  });

  return handleResponse(response);
}

export async function updateRecipe(id: number, data: Partial<RecipeInput>): Promise<Recipe> {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}`, {
    method: "PATCH",
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

export async function rateRecipe(recipeId: number, rating: number): Promise<Rating> {
  const response = await fetch(`${API_BASE_URL}/recipes/${recipeId}/ratings`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ rating })
  });

  return handleResponse(response);
}

export async function getRecipeRatings(recipeId: number): Promise<RatingSummary> {
  const response = await fetch(`${API_BASE_URL}/recipes/${recipeId}/ratings`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export async function getTags(): Promise<Tag[]> {
  const response = await fetch(`${API_BASE_URL}/tags`, {
    headers: authHeaders()
  });

  return handleResponse(response);
}

export async function createTag(name: string): Promise<Tag> {
  const response = await fetch(`${API_BASE_URL}/tags`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ name })
  });

  return handleResponse(response);
}

export async function deleteTag(tagId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/tags/${tagId}`, {
    method: "DELETE",
    headers: authHeaders()
  });

  await handleResponse(response);
}

export async function getMe(): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/my-profile`, {
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
  if (browser) {
    localStorage.removeItem("token");
  }

  window.location.href = "/login";
}

export async function login(username: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: formData
  });

  const data = await handleResponse(response);

  if (browser) {
    localStorage.setItem("token", data.access_token);
  }

  return data;
}

export async function register(username: string, email: string, password: string): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      email,
      password
    })
  });

  return handleResponse(response);
}