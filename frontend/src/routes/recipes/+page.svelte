<script lang="ts">
  import { onMount } from "svelte";
  import { getRecipes, type Recipe } from "$lib/api";

  let recipes = $state<Recipe[]>([]);
  let loading = $state(true);
  let error = $state("");
  let searchTerm = $state("");

  const filteredRecipes = $derived(
    recipes.filter((recipe) => {
      const search = searchTerm.toLowerCase().trim();

      return (
        recipe.title.toLowerCase().includes(search) ||
        recipe.description?.toLowerCase().includes(search) ||
        recipe.time?.toLowerCase().includes(search) ||
        recipe.difficulty?.toLowerCase().includes(search)
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

<main class="recipes-page">
  <a href="/" class="brand-link">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <header class="topbar">
    <div class="search-container">
      <span class="search-icon">⌕</span>

      <input
        type="text"
        bind:value={searchTerm}
        placeholder="Rezepte durchsuchen..."
      />
    </div>

    <div class="topbar-actions">
      <a href="/recipes/new" class="new-button">
        <span class="plus-circle">+</span>
        Neues Rezept
      </a>

      <a href="/account" class="account-link">
        Mein Konto
      </a>
    </div>
  </header>

  <section class="hero-card">
    <div>
      <p class="eyebrow">SmartCookies Rezeptwelt</p>

      <h1>
        Hochgeladene Rezepte
        <span class="headline-cookie">🍪</span>
      </h1>

      <p class="subtitle">
        Entdecke neue Lieblingsrezepte, speichere eigene Kreationen
        und verwalte alles an einem Ort.
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
  {:else if filteredRecipes.length === 0}
    <section class="status-card">
      <div class="empty-icon">🍪</div>
      <h2>Keine Rezepte gefunden</h2>
      <p>Versuche einen anderen Suchbegriff.</p>
    </section>
  {:else}
    <section class="recipes-grid">
      {#each filteredRecipes as recipe}
        <a href={`/recipes/${recipe.id}`} class="recipe-card">
          <div class="recipe-top">
            <div class="recipe-icon">🍪</div>

            {#if recipe.difficulty}
              <span class="difficulty">
                {recipe.difficulty}
              </span>
            {/if}
          </div>

          <div class="recipe-content">
            <h2>{recipe.title}</h2>

            <p>
              {recipe.description ||
                "Öffne das Rezept für Zutaten und Zubereitung."}
            </p>

            <div class="recipe-meta">
              {#if recipe.time}
                <span>⏱ {recipe.time}</span>
              {/if}

              <span>→ Rezept öffnen</span>
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
    background:
      radial-gradient(circle at top left, #ffe1b8 0, transparent 34%),
      linear-gradient(135deg, #fff7ec 0%, #f6d7aa 100%);
    color: #3d2415;
  }

  .recipes-page {
    min-height: 100vh;
    padding: 26px;
    box-sizing: border-box;
  }

  .brand-link {
    position: absolute;
    top: 30px;
    left: 34px;
    text-decoration: none;
    font-size: 2rem;
    font-weight: 900;
    color: #8b552b;
    letter-spacing: -1px;
  }

  .cookie-o {
    display: inline-block;
    margin: 0 -3px;
    font-size: 1.65rem;
    vertical-align: 2px;
  }

  .topbar {
    max-width: 1280px;
    margin: 0 auto 30px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 18px;
    padding-top: 6px;
  }

  .search-container {
    width: 380px;
    height: 56px;
    border-radius: 999px;
    background: rgba(255, 250, 244, 0.92);
    box-shadow: 0 10px 30px rgba(77, 43, 18, 0.08);
    display: flex;
    align-items: center;
    padding: 0 22px;
    gap: 14px;
    backdrop-filter: blur(12px);
  }

  .search-icon {
    font-size: 1.1rem;
    color: #9a7357;
  }

  .search-container input {
    width: 100%;
    border: none;
    outline: none;
    background: transparent;
    font-size: 1rem;
    color: #4a2b18;
  }

  .search-container input::placeholder {
    color: #9c7a63;
  }

  .topbar-actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .new-button {
    height: 56px;
    padding: 0 24px;
    border-radius: 999px;
    background: linear-gradient(135deg, #b86a1f, #9a5518);
    color: white;
    text-decoration: none;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 14px 30px rgba(155, 85, 29, 0.22);
  }

  .plus-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: white;
    color: #9a5518;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    font-weight: 900;
  }

  .account-link {
    text-decoration: none;
    color: #8b552b;
    font-size: 1rem;
    font-weight: 400;
  }

  .hero-card {
    max-width: 1280px;
    margin: 0 auto 30px;
    padding: 54px;
    border-radius: 38px;
    background: rgba(255, 250, 244, 0.82);
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 60px rgba(77, 43, 18, 0.1);
  }

  .eyebrow {
    margin: 0 0 14px;
    color: #a56a3d;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.82rem;
  }

  h1 {
    margin: 0;
    font-size: clamp(3rem, 7vw, 5.4rem);
    line-height: 0.95;
    letter-spacing: -3px;
    color: #4a2b18;
  }

  .headline-cookie {
    font-size: 0.72em;
  }

  .subtitle {
    margin: 24px 0 0;
    max-width: 760px;
    color: #6f5646;
    font-size: 1.2rem;
    line-height: 1.6;
  }

  .recipes-grid {
    max-width: 1280px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
  }

  .recipe-card {
    text-decoration: none;
    color: inherit;
    border-radius: 32px;
    padding: 28px;
    background: rgba(255, 250, 244, 0.88);
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 40px rgba(77, 43, 18, 0.08);
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
  }

  .recipe-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 28px 50px rgba(77, 43, 18, 0.14);
  }

  .recipe-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 22px;
  }

  .recipe-icon {
    width: 64px;
    height: 64px;
    border-radius: 22px;
    background: #fff0dd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
  }

  .difficulty {
    padding: 8px 12px;
    border-radius: 999px;
    background: #f6e1ca;
    color: #8a5a2f;
    font-size: 0.82rem;
    font-weight: 800;
  }

  .recipe-content h2 {
    margin: 0 0 14px;
    font-size: 1.7rem;
    color: #4a2b18;
  }

  .recipe-content p {
    margin: 0;
    color: #6f5646;
    line-height: 1.6;
  }

  .recipe-meta {
    margin-top: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #9a5518;
    font-weight: 700;
    font-size: 0.92rem;
  }

  .status-card {
    max-width: 700px;
    margin: 80px auto 0;
    padding: 34px;
    border-radius: 28px;
    text-align: center;
    background: rgba(255, 250, 244, 0.88);
    box-shadow: 0 20px 40px rgba(77, 43, 18, 0.08);
  }

  .status-card h2 {
    margin: 0 0 10px;
  }

  .status-card p {
    margin: 0;
    color: #6f5646;
  }

  .empty-icon {
    font-size: 3rem;
    margin-bottom: 14px;
  }

  @media (max-width: 980px) {
    .topbar {
      flex-direction: column;
      align-items: stretch;
      padding-top: 70px;
    }

    .search-container {
      width: 100%;
      box-sizing: border-box;
    }

    .topbar-actions {
      width: 100%;
      justify-content: space-between;
    }

    .hero-card {
      padding: 34px;
      border-radius: 28px;
    }

    h1 {
      letter-spacing: -2px;
    }
  }

  @media (max-width: 640px) {
    .recipes-page {
      padding: 18px;
    }

    .brand-link {
      position: static;
      display: inline-block;
      margin-bottom: 18px;
    }

    .topbar {
      padding-top: 0;
    }

    .topbar-actions {
      flex-direction: column;
      align-items: stretch;
    }

    .new-button {
      justify-content: center;
    }

    .account-link {
      text-align: center;
    }

    .hero-card {
      padding: 28px;
    }

    .recipes-grid {
      grid-template-columns: 1fr;
    }
  }
</style>