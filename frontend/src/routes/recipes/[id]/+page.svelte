<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { getRecipe, type Recipe } from "$lib/api";

  let recipe = $state<Recipe | null>(null);
  let loading = $state(true);
  let error = $state("");

  onMount(async () => {
    const id = $page.params.id;

    if (!id) {
      error = "Keine Rezept-ID gefunden.";
      loading = false;
      return;
    }

    try {
      recipe = await getRecipe(id);
    } catch (err) {
      error = "Rezept konnte nicht geladen werden.";
      console.error(err);
    } finally {
      loading = false;
    }
  });
</script>

<main class="detail-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="detail-card">
    <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>

    {#if loading}
      <div class="status-card">
        <p>Rezept wird geladen...</p>
      </div>
    {:else if error}
      <div class="status-card">
        <p>{error}</p>
      </div>
    {:else if recipe}
      <div class="recipe-header">
        <div>
          <p class="eyebrow">
            {recipe.is_public ? "Öffentliches Rezept" : "Privates Rezept"}
          </p>

          <h1>{recipe.title}</h1>

          {#if recipe.description}
            <p class="description">{recipe.description}</p>
          {/if}
        </div>

        <div class="cookie-badge">🍪</div>
      </div>

      <div class="meta-row">
        {#if recipe.time}
          <div class="meta-card">
            <span>⏱</span>
            <p>{recipe.time}</p>
          </div>
        {/if}

        {#if recipe.difficulty}
          <div class="meta-card">
            <span>⭐</span>
            <p>{recipe.difficulty}</p>
          </div>
        {/if}

        <div class="meta-card">
          <span>🥣</span>
          <p>{recipe.ingredients?.length ?? 0} Zutaten</p>
        </div>

        <div class="meta-card">
          <span>👣</span>
          <p>{recipe.steps?.length ?? 0} Schritte</p>
        </div>
      </div>

      <div class="content-grid">
        <section class="info-box">
          <h2>Zutaten</h2>

          {#if recipe.ingredients?.length}
            <ul>
              {#each recipe.ingredients as ingredient}
                <li>{ingredient}</li>
              {/each}
            </ul>
          {:else}
            <p>Keine Zutaten vorhanden.</p>
          {/if}
        </section>

        <section class="info-box">
          <h2>Zubereitung</h2>

          {#if recipe.steps?.length}
            <ol>
              {#each recipe.steps as step}
                <li>{step}</li>
              {/each}
            </ol>
          {:else}
            <p>Keine Zubereitungsschritte vorhanden.</p>
          {/if}
        </section>
      </div>
    {/if}
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #fff7ed, #f3dfc8);
    color: #3b2415;
  }

  .detail-page {
    min-height: 100vh;
    padding: 90px 24px 40px;
    box-sizing: border-box;
  }

  .brand-link {
    position: absolute;
    top: 20px;
    left: 28px;
    color: #8b552b;
    font-size: 24px;
    font-weight: 800;
    text-decoration: none;
    display: flex;
    align-items: center;
  }

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(1px);
    margin-left: -3px;
    margin-right: -3px;
  }

  .detail-card {
    max-width: 1180px;
    margin: 0 auto;
    background: #fffaf4;
    border-radius: 30px;
    padding: 42px;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.12);
  }

  .back-link {
    display: inline-block;
    margin-bottom: 34px;
    color: #9b551d;
    text-decoration: none;
    font-weight: 800;
  }

  .recipe-header {
    display: flex;
    justify-content: space-between;
    gap: 28px;
    align-items: flex-start;
  }

  .eyebrow {
    color: #a35b27;
    font-weight: 800;
    font-size: 18px;
    margin: 0 0 14px;
  }

  h1 {
    margin: 0;
    font-size: 56px;
    line-height: 0.95;
    color: #4a2c1a;
    letter-spacing: -2px;
  }

  .description {
    margin: 24px 0 0;
    max-width: 760px;
    color: #6d5140;
    font-size: 18px;
    line-height: 1.5;
  }

  .cookie-badge {
    min-width: 90px;
    height: 90px;
    border-radius: 26px;
    background: #fff0dd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 52px;
  }

  .meta-row {
    margin-top: 34px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
  }

  .meta-card {
    background: #fff0dd;
    border-radius: 22px;
    padding: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .meta-card span {
    font-size: 24px;
  }

  .meta-card p {
    margin: 0;
    color: #4a2c1a;
    font-weight: 800;
  }

  .content-grid {
    margin-top: 28px;
    display: grid;
    grid-template-columns: 0.8fr 1.2fr;
    gap: 22px;
  }

  .info-box {
    background: #fff0dd;
    border-radius: 24px;
    padding: 26px;
  }

  .info-box h2 {
    margin: 0 0 18px;
    color: #4a2c1a;
    font-size: 28px;
  }

  ul,
  ol {
    margin: 0;
    padding-left: 22px;
    color: #6d5140;
    font-size: 17px;
    line-height: 1.6;
  }

  li {
    margin-bottom: 10px;
  }

  .info-box p,
  .status-card p {
    margin: 0;
    color: #6d5140;
    font-size: 18px;
  }

  .status-card {
    text-align: center;
    padding: 34px;
  }

  @media (max-width: 750px) {
    .brand-link {
      position: static;
      margin-bottom: 20px;
    }

    .detail-page {
      padding-top: 24px;
    }

    .detail-card {
      padding: 28px;
    }

    .recipe-header {
      flex-direction: column;
    }

    h1 {
      font-size: 42px;
    }

    .content-grid {
      grid-template-columns: 1fr;
    }

    .cookie-badge {
      min-width: 74px;
      height: 74px;
      font-size: 42px;
    }
  }
</style>