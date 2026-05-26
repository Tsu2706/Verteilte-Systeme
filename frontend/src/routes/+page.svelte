<script lang="ts">
  import { onMount } from "svelte";
  import { getRecipes } from "$lib/api";

  type Recipe = {
    id: number;
    user_id: number;
    title: string;
    description?: string | null;
    ingredients: unknown[];
    steps: unknown[];
    is_public: boolean;
    created_at?: string;
  };

  let recipes = $state<Recipe[]>([]);
  let loading = $state(true);
  let error = $state("");

  onMount(async () => {
    try {
      recipes = await getRecipes();
    } catch (err) {
      error = "Rezepte konnten nicht geladen werden.";
      console.error(err);
    } finally {
      loading = false;
    }
  });
</script>

<main class="home">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <a href="/recipes/new" class="add-button">
    <span class="plus">+</span>
    <span>Neues Lieblingsrezept hinzufügen</span>
  </a>

  <section class="hero">
    <div class="content">
      <p class="eyebrow">Deine Rezeptsammlung</p>

      <h1>
        Lieblingsrezepte <span class="headline-cookie">🍪</span>
      </h1>

      <p class="subtitle">
        Hier findest du alle gespeicherten Rezepte. Klicke auf ein Rezept, um
        Zutaten und Zubereitung anzusehen.
      </p>
    </div>
  </section>

  {#if loading}
    <section class="status-card">
      <p>Rezepte werden geladen...</p>
    </section>
  {:else if error}
    <section class="status-card">
      <p>{error}</p>
    </section>
  {:else if recipes.length === 0}
    <section class="status-card">
      <div class="empty-cookie">🍪</div>
      <h2>Noch keine Rezepte vorhanden</h2>
      <p>Füge dein erstes Lieblingsrezept hinzu.</p>
    </section>
  {:else}
    <section class="recipes-grid">
      {#each recipes as recipe}
        <a href={`/recipes/${recipe.id}`} class="recipe-card">
          <div class="card-icon">🍪</div>

          <div class="card-content">
            <h2>{recipe.title}</h2>

            <p>
              {recipe.description ??
                "Öffne das Rezept, um Zutaten und Zubereitung anzusehen."}
            </p>

            <div class="card-footer">
              <span>{recipe.ingredients?.length ?? 0} Zutaten</span>
              <span class="arrow">→</span>
            </div>
          </div>
        </a>
      {/each}
    </section>
  {/if}
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #fff7ed, #f3dfc8);
    color: #3b2415;
  }

  .home {
    min-height: 100vh;
    padding: 90px 24px 40px;
    box-sizing: border-box;
  }

  .brand-link {
    position: fixed;
    top: 20px;
    left: 28px;
    color: #8b552b;
    font-size: 24px;
    font-weight: 800;
    text-decoration: none;
    display: flex;
    align-items: center;
    z-index: 10;
  }

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(1px);
    margin-left: -3px;
    margin-right: -3px;
  }

  .add-button {
    position: fixed;
    top: 18px;
    right: 28px;
    background: #9b551d;
    color: white;
    min-height: 48px;
    padding: 0 20px;
    border-radius: 999px;
    text-decoration: none;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.18);
    z-index: 10;
  }

  .plus {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #fff7ed;
    color: #9b551d;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 900;
  }

  .hero {
    max-width: 1180px;
    margin: 0 auto 24px;
  }

  .content,
  .recipe-card,
  .status-card {
    background: #fffaf4;
    border-radius: 26px;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.12);
  }

  .content {
    padding: 42px 50px;
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

  .headline-cookie {
    font-size: 0.62em;
    display: inline-block;
    transform: translateY(-4px);
    margin-left: -5px;
  }

  .subtitle {
    margin: 22px 0 0;
    max-width: 650px;
    font-size: 18px;
    line-height: 1.5;
    color: #6d5140;
  }

  .recipes-grid {
    max-width: 1180px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 18px;
  }

  .recipe-card {
    padding: 26px;
    min-height: 220px;
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
  }

  .recipe-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 40px rgba(92, 55, 25, 0.18);
  }

  .card-icon {
    width: 54px;
    height: 54px;
    border-radius: 18px;
    background: #fff0dd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    margin-bottom: 18px;
  }

  .card-content h2 {
    margin: 0 0 10px;
    color: #4a2c1a;
    font-size: 26px;
  }

  .card-content p {
    margin: 0;
    color: #6d5140;
    line-height: 1.5;
    font-size: 16px;
  }

  .card-footer {
    margin-top: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #9b551d;
    font-weight: 800;
  }

  .arrow {
    font-size: 26px;
  }

  .status-card {
    max-width: 720px;
    margin: 0 auto;
    padding: 34px;
    text-align: center;
  }

  .status-card p {
    margin: 0;
    color: #6d5140;
    font-size: 18px;
  }

  .status-card h2 {
    margin: 0 0 12px;
    color: #4a2c1a;
  }

  .empty-cookie {
    font-size: 54px;
    margin-bottom: 16px;
  }

  @media (max-width: 750px) {
    .add-button {
      position: static;
      margin: 0 0 24px;
      justify-content: center;
    }

    .brand-link {
      position: static;
      margin-bottom: 20px;
    }

    .home {
      padding-top: 24px;
    }

    h1 {
      font-size: 42px;
    }

    .content {
      padding: 34px 28px;
    }
  }
</style>