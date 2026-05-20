<svelte:options runes={false} />

<script lang="ts">
  import { page } from "$app/stores";
  import { getRecipe, rateRecipe } from "$lib/api";

  const stars: number[] = [1, 2, 3, 4, 5];

  let recipe: any = null;
  let loading = true;
  let error = "";
  let selectedRating = 0;
  let ratingMessage = "";

  $: recipeId = $page.params.id ?? "";

  async function loadRecipe(id: string) {
    if (!id) return;

    try {
      loading = true;
      error = "";
      recipe = await getRecipe(id);
    } catch {
      error = "Rezept konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  async function saveRating(rating: number) {
    if (!recipeId) return;

    try {
      selectedRating = rating;
      await rateRecipe(recipeId, rating);
      ratingMessage = "Bewertung wurde gespeichert.";
    } catch {
      ratingMessage = "Bewertung konnte nicht gespeichert werden.";
    }
  }

  $: if (recipeId) {
    loadRecipe(recipeId);
  }
</script>

<main class="recipe-page">
  <section class="recipe-card">
    <a class="back-link" href="/recipes">← Zurück zu den Rezepten</a>

    {#if loading}
      <p>Lade Rezept...</p>
    {:else if error}
      <p class="error">{error}</p>
    {:else if recipe}
      <h1>{recipe.title}</h1>

      {#if recipe.description}
        <p class="description">{recipe.description}</p>
      {/if}

      <section>
        <h2>Mengenangaben</h2>
        <ul>
          {#each recipe.ingredients as ingredient}
            <li>{ingredient}</li>
          {/each}
        </ul>
      </section>

      <section>
        <h2>Rezept</h2>
        <ol>
          {#each recipe.steps as step}
            <li>{step}</li>
          {/each}
        </ol>
      </section>

      <section class="rating-section">
        <h2>Bewertung</h2>

        <div class="stars">
            <button class:active={1 <= selectedRating} on:click={() => saveRating(1)} aria-label="1 Stern">★</button>
            <button class:active={2 <= selectedRating} on:click={() => saveRating(2)} aria-label="2 Sterne">★</button>
            <button class:active={3 <= selectedRating} on:click={() => saveRating(3)} aria-label="3 Sterne">★</button>
            <button class:active={4 <= selectedRating} on:click={() => saveRating(4)} aria-label="4 Sterne">★</button>
            <button class:active={5 <= selectedRating} on:click={() => saveRating(5)} aria-label="5 Sterne">★</button>
        </div>

        {#if ratingMessage}
          <p class="rating-message">{ratingMessage}</p>
        {/if}
      </section>
    {/if}
  </section>
</main>

<style>
  .recipe-page {
    min-height: 100vh;
    background: #f6f1e8;
    font-family: Arial, sans-serif;
    padding: 40px 20px;
  }

  .recipe-card {
    max-width: 760px;
    margin: 0 auto;
    background: white;
    border-radius: 18px;
    padding: 32px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
  }

  .back-link {
    display: inline-block;
    margin-bottom: 24px;
    color: #7a4f2a;
    text-decoration: none;
    font-weight: bold;
  }

  h1 {
    margin: 0 0 12px;
    color: #2f241d;
  }

  h2 {
    margin-top: 32px;
    color: #2f241d;
  }

  .description {
    color: #6b5e54;
    margin-bottom: 28px;
  }

  ul,
  ol {
    padding-left: 22px;
    color: #4f4138;
    line-height: 1.7;
  }

  li {
    margin-bottom: 8px;
  }

  .rating-section {
    margin-top: 34px;
    padding-top: 24px;
    border-top: 1px solid #e7d8c6;
  }

  .stars {
    display: flex;
    gap: 8px;
  }

  .stars button {
    border: none;
    background: transparent;
    font-size: 34px;
    color: #d4c7b8;
    cursor: pointer;
    padding: 0;
  }

  .stars button.active {
    color: #7a4f2a;
  }

  .stars button:hover {
    color: #5f3d20;
  }

  .rating-message {
    margin-top: 12px;
    color: #2f241d;
    font-weight: bold;
  }

  .error {
    color: #8b1e1e;
    font-weight: bold;
  }
</style>