<script lang="ts">
  import { browser } from "$app/environment";
  import { getMe, getMyRecipes, logout, type Recipe, type User } from "$lib/api";

  let user = $state<User | null>(null);
  let recipes = $state<Recipe[]>([]);
  let loading = $state(true);
  let error = $state("");

  async function loadAccount() {
    loading = true;
    error = "";

    try {
      user = await getMe();
      recipes = await getMyRecipes();
    } catch (err) {
      error = err instanceof Error ? err.message : "Konto konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    logout();
  }

  $effect(() => {
    if (browser) {
      if (!localStorage.getItem("token")) {
        window.location.href = "/login";
        return;
      }

      loadAccount();
    }
  });
</script>

<main class="account-page">
  <a href="/" class="brand-link">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="account-card">
    <div class="top-row">
      <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>
      <button onclick={handleLogout}>Logout</button>
    </div>

    {#if loading}
      <p class="status">Konto wird geladen...</p>
    {:else if error}
      <p class="status error">{error}</p>
    {:else if user}
      <h1>Mein Konto</h1>

      <div class="user-box">
        <p><strong>Benutzername:</strong> {user.username}</p>
        <p><strong>E-Mail:</strong> {user.email}</p>
      </div>

      <div class="headline-row">
        <h2>Meine Rezepte</h2>
        <a href="/recipes/new" class="new-button">Neues Rezept</a>
      </div>

      {#if recipes.length === 0}
        <p class="status">Du hast noch keine Rezepte erstellt.</p>
      {:else}
        <div class="recipe-list">
          {#each recipes as recipe}
            <a href={`/recipes/${recipe.id}`} class="recipe-item">
              <div>
                <h3>{recipe.title}</h3>
                <p>{recipe.description || "Keine Beschreibung vorhanden."}</p>
              </div>

              <span>{recipe.is_public ? "Öffentlich" : "Privat"}</span>
            </a>
          {/each}
        </div>
      {/if}
    {/if}
  </section>
</main>

<style>
  .account-page {
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
    text-decoration: none;
    color: #3b2416;
    font-size: 26px;
    font-weight: 800;
  }

  .account-card {
    max-width: 860px;
    margin: 0 auto;
    background: white;
    border-radius: 30px;
    padding: 40px;
    box-shadow: 0 18px 45px rgba(80, 45, 20, 0.14);
  }

  .top-row,
  .headline-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }

  .back-link {
    text-decoration: none;
    color: #8b4a24;
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

  button,
  .new-button {
    border: none;
    border-radius: 999px;
    padding: 12px 18px;
    background: #8b4a24;
    color: white;
    font-weight: 800;
    cursor: pointer;
    text-decoration: none;
  }

  h1 {
    margin: 34px 0 18px;
    font-size: 42px;
  }

  h2 {
    margin: 0;
    font-size: 28px;
  }

  .user-box {
    background: #fff7ec;
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 34px;
  }

  .user-box p {
    margin: 8px 0;
    color: #7a5a43;
  }

  .recipe-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-top: 22px;
  }

  .recipe-item {
    display: flex;
    justify-content: space-between;
    gap: 18px;
    align-items: center;
    padding: 20px;
    border-radius: 20px;
    background: #fffaf4;
    text-decoration: none;
    color: inherit;
    border: 1px solid #f0dfcd;
  }

  .recipe-item h3 {
    margin: 0 0 6px;
    font-size: 21px;
  }

  .recipe-item p {
    margin: 0;
    color: #7a5a43;
  }

  .recipe-item span {
    background: #f2ddc7;
    color: #6f3719;
    border-radius: 999px;
    padding: 8px 12px;
    font-weight: 800;
    white-space: nowrap;
    font-size: 13px;
  }

  .status {
    margin-top: 28px;
    color: #7a5a43;
  }

  .status.error {
    color: #9b1c1c;
  }

  @media (max-width: 700px) {
    .account-card {
      padding: 28px;
    }

    .top-row,
    .headline-row,
    .recipe-item {
      flex-direction: column;
      align-items: flex-start;
    }

    h1 {
      font-size: 34px;
    }
  }
</style>