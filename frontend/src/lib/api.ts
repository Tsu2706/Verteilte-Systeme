const API_URL = "http://localhost:8000";

export type Recipe = {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  ingredients: string[];
  steps: string[];
  is_public: boolean;
  created_at?: string;
  time?: string | null;
  difficulty?: string | null;
};

export type RecipeCreate = {
  title: string;
  description?: string;
  ingredients: string[];
  steps: string[];
  is_public: boolean;
  time?: string;
  difficulty?: string;
};

export async function getRecipes(): Promise<Recipe[]> {
  const response = await fetch(`${API_URL}/recipes`);

  if (!response.ok) {
    throw new Error("Rezepte konnten nicht geladen werden.");
  }

  return response.json();
}

export async function getRecipe(id: string | number): Promise<Recipe> {
  const response = await fetch(`${API_URL}/recipes/${id}`);

  if (!response.ok) {
    throw new Error("Rezept konnte nicht geladen werden.");
  }

  return response.json();
}

export async function createRecipe(
  recipe: RecipeCreate
): Promise<Recipe> {
  const response = await fetch(`${API_URL}/recipes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(recipe)
  });

  if (!response.ok) {
    throw new Error("Rezept konnte nicht gespeichert werden.");
  }

  return response.json();
}