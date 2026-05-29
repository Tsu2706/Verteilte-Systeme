<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";
  import { getRecipe, deleteRecipe, type Recipe } from "$lib/api";

  let recipe = $state<Recipe | null>(null);
  let loading = $state(true);
  let error = $state("");
  let isLoggedIn = $state(false);

  async function loadRecipe() {
    loading = true;
    error = "";

    try {
      const id = Number($page.params.id);
      recipe = await getRecipe(id);
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  async function handleDelete() {
    if (!recipe) return;

    const confirmed = confirm("Möchtest du dieses Rezept wirklich löschen?");
    if (!confirmed) return;

    try {
      await deleteRecipe(recipe.id);
      window.location.href = "/recipes";
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht gelöscht werden.";
    }
  }

  $effect(() => {
    if (browser) {
      isLoggedIn = !!localStorage.getItem("token");
      loadRecipe();
    }
  });
</script>

<main class="detail-page">
  <a href="/" class="brand-link">
    SmartC<span>🍪</span><span>🍪</span>kies
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

        {#if isLoggedIn}
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
    position: fixed;
    top: 28px;
    left: 36px;
    z-index: 10;
    text-decoration: none;
    color: #3b2416;
    font-size: 26px;
    font-weight: 800;
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