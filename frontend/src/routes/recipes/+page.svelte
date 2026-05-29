<script lang="ts">
  import { browser } from "$app/environment";
  import { getRecipes, searchRecipes, logout, type Recipe } from "$lib/api";

  let recipes = $state<Recipe[]>([]);
  let filteredRecipes = $state<Recipe[]>([]);
  let search = $state("");
  let loading = $state(true);
  let error = $state("");
  let isLoggedIn = $state(false);

  async function loadRecipes() {
    loading = true;
    error = "";

    try {
      recipes = await getRecipes();
      filteredRecipes = recipes;
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezepte konnten nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  async function handleSearch() {
    error = "";

    try {
      if (!search.trim()) {
        filteredRecipes = recipes;
        return;
      }

      filteredRecipes = await searchRecipes(search);
    } catch (err) {
      error = err instanceof Error ? err.message : "Suche fehlgeschlagen.";
    }
  }

  function handleLogout() {
    logout();
  }

  $effect(() => {
    if (browser) {
      isLoggedIn = !!localStorage.getItem("token");
      loadRecipes();
    }
  });
</script>

<main class="recipes-page">
  <header class="topbar">
    <a href="/" class="brand-link">
      SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
    </a>

    <div class="search-area">
      <input
        bind:value={search}
        placeholder="Rezepte suchen..."
        oninput={handleSearch}
      />
    </div>

    <nav class="nav-actions">
      {#if isLoggedIn}
        <a href="/account" class="text-link">Mein Konto</a>
        <a href="/recipes/new" class="add-button">+</a>
        <button class="logout-button" onclick={handleLogout}>Logout</button>
      {:else}
        <a href="/login" class="text-link">Login</a>
        <a href="/register" class="text-link">Registrieren</a>
      {/if}
    </nav>
  </header>

  <section class="hero">
    <p class="eyebrow">Alle Rezepte</p>
    <h1>Entdecke neue Lieblingsrezepte</h1>
    <p class="subtitle">
      Durchsuche die hochgeladenen Rezepte und finde Inspiration für dein nächstes Gericht.
    </p>
  </section>

  {#if loading}
    <p class="status">Rezepte werden geladen...</p>
  {:else if error}
    <p class="status error">{error}</p>
  {:else if filteredRecipes.length === 0}
    <p class="status">Keine Rezepte gefunden.</p>
  {:else}
    <section class="recipe-grid">
      {#each filteredRecipes as recipe}
        <a href={`/recipes/${recipe.id}`} class="recipe-card">
          <div class="card-top">
            <span class="badge">{recipe.difficulty || "Rezept"}</span>
            {#if recipe.time}
              <span class="time">{recipe.time}</span>
            {/if}
          </div>

          <h2>{recipe.title}</h2>

          {#if recipe.description}
            <p>{recipe.description}</p>
          {:else}
            <p>Keine Beschreibung vorhanden.</p>
          {/if}

          <div class="card-footer">
            <span>{recipe.ingredients?.length || 0} Zutaten</span>
            <span>{recipe.steps?.length || 0} Schritte</span>
          </div>
        </a>
      {/each}
    </section>
  {/if}
</main>

<style>
  .recipes-page {
    min-height: 100vh;
    background: #fff7ec;
    padding: 28px;
    font-family: Arial, sans-serif;
    color: #3b2416;
  }

  .topbar {
    display: grid;
    grid-template-columns: 1fr minmax(260px, 420px) 1fr;
    align-items: center;
    gap: 24px;
  }

  .brand-link {
    text-decoration: none;
    color: #3b2416;
    font-size: 26px;
    font-weight: 800;
  }

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(-0.5px);
    margin-left: -3px;
    margin-right: -3px;
  }

  .search-area {
    display: flex;
    justify-content: center;
  }

  .search-area input {
    width: 100%;
    border: 1px solid #ead8c3;
    border-radius: 999px;
    padding: 13px 18px;
    background: white;
    font-size: 15px;
    outline: none;
  }

  .nav-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 14px;
  }

  .text-link {
    text-decoration: none;
    color: #3b2416;
    font-size: 15px;
    font-weight: 400;
  }

  .add-button {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #8b4a24;
    color: white;
    text-decoration: none;
    font-size: 28px;
    line-height: 39px;
    text-align: center;
    font-weight: 400;
  }

  .logout-button {
    border: none;
    background: transparent;
    color: #7a5a43;
    cursor: pointer;
    font-size: 15px;
  }

  .hero {
    max-width: 760px;
    margin: 78px auto 42px;
    text-align: center;
  }

  .eyebrow {
    color: #8b4a24;
    font-weight: 800;
    margin-bottom: 10px;
  }

  h1 {
    font-size: 48px;
    margin: 0;
  }

  .subtitle {
    color: #7a5a43;
    font-size: 18px;
    line-height: 1.6;
  }

  .status {
    text-align: center;
    margin-top: 40px;
    color: #7a5a43;
  }

  .status.error {
    color: #9b1c1c;
  }

  .recipe-grid {
    max-width: 1120px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 24px;
  }

  .recipe-card {
    background: white;
    border-radius: 28px;
    padding: 26px;
    text-decoration: none;
    color: inherit;
    box-shadow: 0 16px 38px rgba(80, 45, 20, 0.12);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .recipe-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 22px 46px rgba(80, 45, 20, 0.16);
  }

  .card-top,
  .card-footer {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
  }

  .badge {
    background: #f2ddc7;
    color: #6f3719;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
  }

  .time {
    color: #7a5a43;
    font-size: 14px;
  }

  .recipe-card h2 {
    margin: 22px 0 10px;
    font-size: 24px;
  }

  .recipe-card p {
    color: #7a5a43;
    line-height: 1.5;
  }

  .card-footer {
    margin-top: 24px;
    padding-top: 18px;
    border-top: 1px solid #f0dfcd;
    color: #8b4a24;
    font-weight: 800;
    font-size: 14px;
  }

  @media (max-width: 850px) {
    .topbar {
      grid-template-columns: 1fr;
    }

    .nav-actions {
      justify-content: center;
      flex-wrap: wrap;
    }

    .brand-link {
      text-align: center;
    }

    h1 {
      font-size: 36px;
    }
  }
</style>