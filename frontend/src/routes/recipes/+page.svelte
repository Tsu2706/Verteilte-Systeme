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
  let searchTerm = $state("");

  const filteredRecipes = $derived(
    recipes.filter((recipe) => {
      const search = searchTerm.toLowerCase().trim();

      return (
        recipe.title.toLowerCase().includes(search) ||
        recipe.description?.toLowerCase().includes(search)
      );
    })
  );

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

  <div class="top-actions">
    <div class="search-card">
      <span>🔍</span>
      <input
        type="text"
        bind:value={searchTerm}
        placeholder="Rezept suchen..."
      />
    </div>

    <a href="/recipes/new" class="add-button">
      <span class="plus">+</span>
      <span>Neues Lieblingsrezept hinzufügen</span>
    </a>
  </div>

  <section class="hero">
    <div class="content">
      <h1>
        Hochgeladene Rezepte <span class="headline-cookie">🍪</span>
      </h1>

      <p class="subtitle">
        Hier findest du alle hochgeladenen Rezepte übersichtlich an einem Ort.
        Klicke auf ein Rezept, um die Details zu öffnen.
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
  {:else if filteredRecipes.length === 0}
    <section class="status-card">
      <div class="empty-cookie">🔍</div>
      <h2>Kein Rezept gefunden</h2>
      <p>Probiere einen anderen Suchbegriff aus.</p>
    </section>
  {:else}
    <section class="recipes-grid">
      {#each filteredRecipes as recipe}
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
    position: absolute;
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

  .top-actions {
    position: fixed;
    top: 18px;
    right: 28px;
    display: flex;
    align-items: center;
    gap: 14px;
    z-index: 10;
  }

  .search-card {
    width: 300px;
    min-height: 48px;
    background: #fffaf4;
    border-radius: 999px;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.12);
    padding: 0 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-sizing: border-box;
  }

  .search-card span {
    font-size: 20px;
  }

  .search-card input {
    width: 100%;
    border: none;
    outline: none;
    background: transparent;
    color: #4a2c1a;
    font-size: 16px;
    font-weight: 700;
  }

  .search-card input::placeholder {
    color: #9b7358;
  }

  .plus {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #fff7ed;
    color: #9b551d;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    font-size: 20px;
    font-weight: 900;
    padding-bottom: 2px;
    box-sizing: border-box;
  }

  .add-button {
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
    .top-actions {
      position: static;
      flex-direction: column;
      align-items: stretch;
      margin: 0 0 24px;
    }

    .search-card,
    .add-button {
      width: 100%;
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