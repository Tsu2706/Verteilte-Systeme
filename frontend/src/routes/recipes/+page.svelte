<script lang="ts">
  import { onMount } from "svelte";
  import { getRecipes } from "$lib/api";

  type Recipe = {
    id: number;
    title: string;
    description?: string;
    ingredients?: string;
    instructions?: string;
    cooking_time?: number;
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

<main class="recipes-page">
  <header class="topbar">
    <a href="/" class="brand-link" aria-label="Zur Startseite">
      SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
    </a>

    <a href="/recipes/new" class="new-button">
      <span class="plus">+</span>
      <span>Neues Lieblingsrezept hinzufügen</span>
    </a>
  </header>

  <section class="hero">
    <p class="eyebrow">Deine Sammlung</p>

    <h1>
      Lieblingsrezepte
      <span class="headline-cookie">🍪</span>
    </h1>

    <p class="subtitle">
      Hier findest du alle gespeicherten Rezepte übersichtlich an einem Ort.
      Klicke auf ein Rezept, um die Details zu öffnen.
    </p>
  </section>

  {#if loading}
    <section class="state-card">
      <p>Rezepte werden geladen...</p>
    </section>
  {:else if error}
    <section class="state-card error">
      <p>{error}</p>
    </section>
  {:else if recipes.length === 0}
    <section class="empty-state">
      <div class="empty-cookie">🍪</div>
      <h2>Noch keine Rezepte vorhanden</h2>
      <p>Füge dein erstes Lieblingsrezept hinzu und starte deine Sammlung.</p>

      <a href="/recipes/new" class="empty-button">
        <span>+</span>
        Neues Lieblingsrezept hinzufügen
      </a>
    </section>
  {:else}
    <section class="recipes-grid" aria-label="Rezeptübersicht">
      {#each recipes as recipe}
        <a href={`/recipes/${recipe.id}`} class="recipe-card">
          <div class="card-icon">🍪</div>

          <div class="card-content">
            <h2>{recipe.title}</h2>

            {#if recipe.description}
              <p>{recipe.description}</p>
            {:else}
              <p>Öffne das Rezept, um Zutaten und Zubereitung anzusehen.</p>
            {/if}

            <div class="card-footer">
              {#if recipe.cooking_time}
                <span>{recipe.cooking_time} Min.</span>
              {:else}
                <span>Rezeptdetails ansehen</span>
              {/if}

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
    font-family:
      Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
      "Segoe UI", sans-serif;
    background:
      radial-gradient(circle at top left, rgba(255, 216, 155, 0.45), transparent 30%),
      linear-gradient(135deg, #fff7ed 0%, #fff1df 45%, #fbe7d0 100%);
    color: #3f2a1d;
  }

  .recipes-page {
    min-height: 100vh;
    padding: 2rem;
  }

  .topbar {
    max-width: 1180px;
    margin: 0 auto 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
  }

  .brand-link {
    text-decoration: none;
    color: #4b2e1f;
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 900;
    letter-spacing: -0.05em;
  }

  .cookie-o,
  .headline-cookie {
    display: inline-block;
    transform: translateY(0.08em);
  }

  .new-button,
  .empty-button {
    display: inline-flex;
    align-items: center;
    gap: 0.7rem;
    border: none;
    border-radius: 999px;
    padding: 0.9rem 1.3rem;
    background: #8b4a24;
    color: #fffaf3;
    text-decoration: none;
    font-weight: 800;
    box-shadow: 0 14px 30px rgba(139, 74, 36, 0.25);
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease,
      background 0.2s ease;
  }

  .new-button:hover,
  .empty-button:hover {
    transform: translateY(-2px);
    background: #6f381b;
    box-shadow: 0 18px 40px rgba(139, 74, 36, 0.32);
  }

  .plus {
    width: 1.6rem;
    height: 1.6rem;
    display: inline-grid;
    place-items: center;
    border-radius: 50%;
    background: #fff2dc;
    color: #8b4a24;
    font-size: 1.2rem;
    font-weight: 900;
  }

  .hero {
    max-width: 900px;
    margin: 0 auto 3rem;
    text-align: center;
  }

  .eyebrow {
    margin: 0 0 0.8rem;
    color: #a7652c;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.8rem;
  }

  h1 {
    margin: 0;
    font-size: clamp(2.6rem, 7vw, 5.2rem);
    line-height: 0.95;
    letter-spacing: -0.08em;
    color: #3f2415;
  }

  .subtitle {
    max-width: 640px;
    margin: 1.4rem auto 0;
    color: #7b5a42;
    font-size: 1.1rem;
    line-height: 1.7;
  }

  .recipes-grid {
    max-width: 1180px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.4rem;
  }

  .recipe-card {
    min-height: 230px;
    padding: 1.4rem;
    border-radius: 2rem;
    background: rgba(255, 250, 243, 0.82);
    border: 1px solid rgba(139, 74, 36, 0.13);
    text-decoration: none;
    color: inherit;
    box-shadow: 0 18px 45px rgba(91, 56, 31, 0.12);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease,
      border-color 0.2s ease;
  }

  .recipe-card:hover {
    transform: translateY(-6px);
    border-color: rgba(139, 74, 36, 0.35);
    box-shadow: 0 24px 60px rgba(91, 56, 31, 0.18);
  }

  .card-icon {
    width: 3.2rem;
    height: 3.2rem;
    display: grid;
    place-items: center;
    border-radius: 1.1rem;
    background: #fff0d8;
    font-size: 1.7rem;
    margin-bottom: 1.2rem;
  }

  .card-content h2 {
    margin: 0 0 0.7rem;
    font-size: 1.35rem;
    color: #432513;
  }

  .card-content p {
    margin: 0;
    color: #7b5a42;
    line-height: 1.6;
  }

  .card-footer {
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #9a5926;
    font-weight: 800;
  }

  .arrow {
    font-size: 1.5rem;
  }

  .state-card,
  .empty-state {
    max-width: 680px;
    margin: 0 auto;
    padding: 2rem;
    border-radius: 2rem;
    background: rgba(255, 250, 243, 0.86);
    border: 1px solid rgba(139, 74, 36, 0.13);
    box-shadow: 0 18px 45px rgba(91, 56, 31, 0.12);
    text-align: center;
  }

  .state-card p,
  .empty-state p {
    color: #7b5a42;
  }

  .error p {
    color: #9b1c1c;
    font-weight: 700;
  }

  .empty-cookie {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .empty-state h2 {
    margin: 0 0 0.7rem;
    color: #432513;
  }

  .empty-button {
    margin-top: 1.3rem;
  }

  @media (max-width: 720px) {
    .recipes-page {
      padding: 1.2rem;
    }

    .topbar {
      align-items: flex-start;
      flex-direction: column;
      margin-bottom: 2.4rem;
    }

    .new-button {
      width: 100%;
      justify-content: center;
    }
  }
</style>