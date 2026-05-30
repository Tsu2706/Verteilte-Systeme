<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";
  import {
    getRecipe,
    deleteRecipe,
    rateRecipe,
    getRecipeRatings,
    getMe,
    type Recipe,
    type RatingSummary,
    type User
  } from "$lib/api";

  let recipe = $state<Recipe | null>(null);
  let currentUser = $state<User | null>(null);

  let loading = $state(true);
  let error = $state("");
  let isLoggedIn = $state(false);
  let canManageRecipe = $state(false);

  let selectedRating = $state(0);
  let ratingMessage = $state("");
  let ratingError = $state("");

  let ratingSummary = $state<RatingSummary>({
    average: 0,
    count: 0,
    my_rating: null
  });

  async function loadRatings() {
    if (!recipe) return;

    ratingSummary = await getRecipeRatings(recipe.id);
    selectedRating = ratingSummary.my_rating ?? 0;
  }

  async function loadRecipe() {
    loading = true;
    error = "";

    try {
      isLoggedIn = !!localStorage.getItem("token");

      if (isLoggedIn) {
        try {
          currentUser = await getMe();
        } catch {
          currentUser = null;
          isLoggedIn = false;
          localStorage.removeItem("token");
        }
      }

      const id = Number($page.params.id);
      recipe = await getRecipe(id);

      canManageRecipe = !!currentUser && recipe.user_id === currentUser.id;

      await loadRatings();
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  async function handleDelete() {
    if (!recipe || !canManageRecipe) return;

    const confirmed = confirm("Möchtest du dieses Rezept wirklich löschen?");
    if (!confirmed) return;

    try {
      await deleteRecipe(recipe.id);
      window.location.href = "/recipes";
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht gelöscht werden.";
    }
  }

  async function handleRating(value: number) {
    if (!recipe) return;

    ratingMessage = "";
    ratingError = "";
    selectedRating = value;

    try {
      await rateRecipe(recipe.id, value);
      await loadRatings();
      ratingMessage = `Danke! Du hast dieses Rezept mit ${value} von 5 Sternen bewertet.`;
    } catch (err) {
      ratingError = err instanceof Error ? err.message : "Bewertung konnte nicht gespeichert werden.";
    }
  }

  $effect(() => {
    if (browser) {
      loadRecipe();
    }
  });
</script>

<main class="detail-page">
  <a href="/" class="brand-link">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="detail-card">
    <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>

    {#if loading}
      <p class="status">Rezept wird geladen...</p>
    {:else if error}
      <p class="status error">{error}</p>
    {:else if recipe}
      <div class="title-row">
        <div>
          <p class="eyebrow">{recipe.difficulty || "Rezept"}</p>
          <h1>{recipe.title}</h1>
        </div>

        {#if canManageRecipe}
          <div class="actions">
            <a href={`/recipes/${recipe.id}/edit`} class="edit-button">Bearbeiten</a>
            <button onclick={handleDelete} class="delete-button">Löschen</button>
          </div>
        {/if}
      </div>

      {#if recipe.description}
        <p class="description">{recipe.description}</p>
      {/if}

      <div class="meta">
        {#if recipe.time}
          <span>{recipe.time}</span>
        {/if}

        <span>{recipe.ingredients?.length || 0} Zutaten</span>
        <span>{recipe.steps?.length || 0} Schritte</span>
      </div>

      <section class="rating-section">
        <h2>Bewertung</h2>

        <p class="rating-text">
          Durchschnitt: {ratingSummary.average} von 5 Sternen
          ({ratingSummary.count} Bewertung{ratingSummary.count === 1 ? "" : "en"})
        </p>

        {#if selectedRating > 0}
          <p class="rating-text">Deine Bewertung: {selectedRating} von 5 Sternen</p>
        {/if}

        {#if isLoggedIn}
          <p class="rating-text">Wie gefällt dir dieses Rezept?</p>

          <div class="stars" aria-label="Rezept bewerten">
            {#each [1, 2, 3, 4, 5] as value}
              <button
                type="button"
                class:active={value <= selectedRating}
                onclick={() => handleRating(value)}
                aria-label={`${value} Sterne vergeben`}
              >
                ★
              </button>
            {/each}
          </div>

          {#if ratingMessage}
            <p class="rating-success">{ratingMessage}</p>
          {/if}

          {#if ratingError}
            <p class="rating-error">{ratingError}</p>
          {/if}
        {:else}
          <p class="rating-text">
            Logge dich ein, um dieses Rezept mit 1 bis 5 Sternen zu bewerten.
          </p>

          <a href="/login" class="login-rating-link">Zum Login</a>
        {/if}
      </section>

      <section class="content-section">
        <h2>Zutaten</h2>

        {#if recipe.ingredients && recipe.ingredients.length > 0}
          <ul>
            {#each recipe.ingredients as ingredient}
              <li>{ingredient}</li>
            {/each}
          </ul>
        {:else}
          <p>Keine Zutaten vorhanden.</p>
        {/if}
      </section>

      <section class="content-section">
        <h2>Zubereitung</h2>

        {#if recipe.steps && recipe.steps.length > 0}
          <ol>
            {#each recipe.steps as step}
              <li>{step}</li>
            {/each}
          </ol>
        {:else}
          <p>Keine Schritte vorhanden.</p>
        {/if}
      </section>
    {/if}
  </section>
</main>

<style>
  .detail-page {
    min-height: 100vh;
    background: #fff7ec;
    padding: 100px 28px 40px;
    font-family: Arial, sans-serif;
    color: #3b2416;
  }

  .brand-link {
    position: absolute;
    top: 28px;
    left: 36px;
    z-index: 10;
    text-decoration: none;
    color: #3b2416;
    font-size: 26px;
    font-weight: 800;
  }

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(-2px);
    margin-left: -3px;
    margin-right: -3px;
  }

  .detail-card {
    max-width: 860px;
    margin: 0 auto;
    background: white;
    border-radius: 30px;
    padding: 40px;
    box-shadow: 0 18px 45px rgba(80, 45, 20, 0.14);
  }

  .back-link {
    text-decoration: none;
    color: #8b4a24;
    font-weight: 800;
  }

  .title-row {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    align-items: flex-start;
    margin-top: 30px;
  }

  .eyebrow {
    margin: 0 0 8px;
    color: #8b4a24;
    font-weight: 800;
  }

  h1 {
    margin: 0;
    font-size: 44px;
  }

  .description {
    margin-top: 22px;
    color: #7a5a43;
    font-size: 18px;
    line-height: 1.6;
  }

  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 28px 0;
  }

  .meta span {
    background: #f2ddc7;
    color: #6f3719;
    padding: 9px 14px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 14px;
  }

  .actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .edit-button,
  .delete-button {
    border: none;
    border-radius: 999px;
    padding: 11px 16px;
    font-weight: 800;
    cursor: pointer;
    text-decoration: none;
    font-size: 14px;
  }

  .edit-button {
    background: #8b4a24;
    color: white;
  }

  .delete-button {
    background: #ffe6e6;
    color: #9b1c1c;
  }

  .rating-section {
    margin-top: 32px;
    padding: 24px;
    border-radius: 24px;
    background: #fff7ec;
    border: 1px solid #f0dfcd;
  }

  .rating-section h2 {
    margin-bottom: 8px;
  }

  .rating-text {
    margin: 0 0 14px;
    color: #7a5a43;
    line-height: 1.5;
  }

  .stars {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
  }

  .stars button {
    border: none;
    background: #f2ddc7;
    color: #b78964;
    width: 44px;
    height: 44px;
    border-radius: 999px;
    font-size: 24px;
    cursor: pointer;
    transition: transform 0.15s ease, background 0.15s ease, color 0.15s ease;
  }

  .stars button:hover {
    transform: translateY(-2px);
    background: #8b4a24;
    color: white;
  }

  .stars button.active {
    background: #8b4a24;
    color: white;
  }

  .rating-success {
    margin: 10px 0 0;
    color: #2f7d32;
    font-weight: 700;
  }

  .rating-error {
    margin: 10px 0 0;
    color: #9b1c1c;
    font-weight: 700;
  }

  .login-rating-link {
    display: inline-flex;
    margin-top: 4px;
    background: #8b4a24;
    color: white;
    text-decoration: none;
    padding: 10px 16px;
    border-radius: 999px;
    font-weight: 800;
  }

  .content-section {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #f0dfcd;
  }

  h2 {
    margin: 0 0 16px;
    font-size: 26px;
  }

  ul,
  ol {
    padding-left: 24px;
    color: #7a5a43;
    line-height: 1.8;
  }

  .status {
    margin-top: 30px;
    color: #7a5a43;
  }

  .status.error {
    color: #9b1c1c;
  }

  @media (max-width: 700px) {
    .detail-card {
      padding: 28px;
    }

    .title-row {
      flex-direction: column;
    }

    h1 {
      font-size: 34px;
    }
  }
</style>