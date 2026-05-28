<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { getMe, getMyRecipes, logout } from "$lib/api";

  let user = $state<any>(null);
  let recipes = $state<any[]>([]);
  let loading = $state(true);
  let error = $state("");

  onMount(async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      goto("/login");
      return;
    }

    try {
      user = await getMe();
      recipes = await getMyRecipes();
    } catch (err) {
      error = "Dein Konto konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  });

  function handleLogout() {
    logout();
  }
</script>

<main class="account-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="account-card">
    <div class="top-bar">
      <div>
        <p class="eyebrow">Mein Konto</p>
        <h1>Dein SmartCookies Profil</h1>
      </div>

      <button class="logout-button" onclick={handleLogout}>
        Ausloggen
      </button>
    </div>

    {#if loading}
      <div class="state-box">Konto wird geladen...</div>
    {:else}
      {#if error}
        <div class="error-box">{error}</div>
      {/if}

      {#if user}
        <div class="user-card">
          <div class="avatar">
            {user.username?.charAt(0).toUpperCase()}
          </div>

          <div>
            <h2>{user.username}</h2>
            <p>{user.email}</p>
          </div>
        </div>
      {/if}

      <div class="recipes-header">
        <h2>Meine Rezepte</h2>

        <a href="/recipes/new" class="new-button">
          + Neues Rezept
        </a>
      </div>

      {#if recipes.length === 0}
        <div class="empty-box">
          Du hast noch keine Rezepte erstellt.
        </div>
      {:else}
        <div class="recipes-grid">
          {#each recipes as recipe}
            <a class="recipe-card" href={`/recipes/${recipe.id}`}>
              <div class="recipe-content">
                <div class="recipe-top">
                  <h3>{recipe.title}</h3>

                  {#if recipe.difficulty}
                    <span class="badge">{recipe.difficulty}</span>
                  {/if}
                </div>

                <p>{recipe.description || "Keine Beschreibung vorhanden."}</p>

                <div class="recipe-meta">
                  {#if recipe.time}
                    <span>⏱ {recipe.time}</span>
                  {/if}

                  <span>→ Rezept öffnen</span>
                </div>
              </div>
            </a>
          {/each}
        </div>
      {/if}
    {/if}
  </section>
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

  .account-page {
    min-height: 100vh;
    padding: 110px 24px 40px;
    box-sizing: border-box;
  }

  .brand-link {
    position: fixed;
    top: 28px;
    left: 34px;
    z-index: 20;
    text-decoration: none;
    font-size: 2rem;
    font-weight: 900;
    color: #3d2415;
    letter-spacing: -1px;
  }

  .cookie-o {
    display: inline-block;
    margin: 0 -2px;
    font-size: 1.65rem;
    vertical-align: 2px;
  }

  .account-card {
    width: min(1100px, 100%);
    margin: 0 auto;
    padding: 34px;
    border-radius: 32px;
    background: rgba(255, 255, 255, 0.78);
    box-shadow: 0 24px 70px rgba(77, 43, 18, 0.18);
    backdrop-filter: blur(12px);
  }

  .top-bar {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    align-items: center;
    margin-bottom: 30px;
  }

  .eyebrow {
    margin: 0 0 10px;
    color: #a56a3d;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.8rem;
  }

  h1 {
    margin: 0;
    font-size: clamp(2.2rem, 5vw, 4rem);
    letter-spacing: -2px;
  }

  .logout-button {
    border: none;
    border-radius: 999px;
    padding: 14px 22px;
    background: #3d2415;
    color: white;
    font-weight: 900;
    cursor: pointer;
    box-shadow: 0 12px 26px rgba(61, 36, 21, 0.22);
  }

  .user-card {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 22px;
    border-radius: 24px;
    background: #fff8ef;
    margin-bottom: 34px;
  }

  .avatar {
    width: 74px;
    height: 74px;
    border-radius: 50%;
    background: #3d2415;
    color: white;
    display: grid;
    place-items: center;
    font-size: 2rem;
    font-weight: 900;
  }

  .user-card h2 {
    margin: 0 0 6px;
    font-size: 1.5rem;
  }

  .user-card p {
    margin: 0;
    color: #6f5646;
  }

  .recipes-header {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    align-items: center;
    margin-bottom: 22px;
  }

  .recipes-header h2 {
    margin: 0;
    font-size: 2rem;
  }

  .new-button {
    text-decoration: none;
    background: #3d2415;
    color: white;
    padding: 14px 22px;
    border-radius: 999px;
    font-weight: 900;
  }

  .recipes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 22px;
  }

  .recipe-card {
    text-decoration: none;
    color: inherit;
    border-radius: 26px;
    overflow: hidden;
    background: #fffaf3;
    border: 2px solid #f2d7b8;
  }

  .recipe-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(61, 36, 21, 0.12);
  }

  .recipe-content {
    padding: 22px;
  }

  .recipe-top {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    align-items: flex-start;
    margin-bottom: 12px;
  }

  .recipe-top h3 {
    margin: 0;
    font-size: 1.3rem;
  }

  .badge {
    background: #f5e1ca;
    color: #8a5a2f;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 800;
    white-space: nowrap;
  }

  .recipe-card p {
    color: #6f5646;
    line-height: 1.5;
    margin-bottom: 20px;
  }

  .recipe-meta {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    color: #8a5a2f;
    font-weight: 700;
    font-size: 0.92rem;
  }

  .state-box,
  .error-box,
  .empty-box {
    border-radius: 18px;
    padding: 16px;
    font-weight: 700;
  }

  .state-box,
  .empty-box {
    background: #fff7ec;
  }

  .error-box {
    background: #fff0ec;
    color: #b42318;
  }

  @media (max-width: 700px) {
    .account-page {
      padding: 96px 16px 28px;
    }

    .brand-link {
      top: 20px;
      left: 20px;
      font-size: 1.55rem;
    }

    .account-card {
      padding: 24px;
      border-radius: 24px;
    }

    .top-bar,
    .recipes-header,
    .recipe-top,
    .recipe-meta {
      flex-direction: column;
      align-items: flex-start;
    }

    .logout-button,
    .new-button {
      width: 100%;
      text-align: center;
      box-sizing: border-box;
    }
  }
</style>