<script lang="ts">
  import { login } from "$lib/api";

  let username = $state("");
  let password = $state("");
  let error = $state("");

  async function handleLogin() {
    error = "";

    try {
      await login(username, password);
      window.location.href = "/recipes";
    } catch (err) {
      error = err instanceof Error ? err.message : "Login fehlgeschlagen.";
    }
  }
</script>

<main class="auth-page">
  <a href="/" class="brand-link">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="auth-card">
    <h1>Login</h1>
    <p>Melde dich an, um eigene Rezepte zu erstellen.</p>

    {#if error}
      <div class="error">{error}</div>
    {/if}

    <form
      onsubmit={(e) => {
        e.preventDefault();
        handleLogin();
      }}
    >
      <label for="username">Benutzername</label>
      <input id="username" bind:value={username} required />

      <label for="password">Passwort</label>
      <input id="password" type="password" bind:value={password} required />

      <button type="submit">Einloggen</button>
    </form>

    <p class="switch">
      Noch kein Konto?
      <a href="/register">Registrieren</a>
    </p>
  </section>
</main>

<style>
  .auth-page {
    min-height: 100vh;
    background: #fff7ec;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 32px;
    font-family: Arial, sans-serif;
  }

  .brand-link {
    position: fixed;
    top: 28px;
    left: 36px;
    text-decoration: none;
    color: #3b2416;
    font-size: 26px;
    font-weight: 800;
  }

  .auth-card {
    width: 100%;
    max-width: 420px;
    background: #ffffff;
    border-radius: 28px;
    padding: 38px;
    box-shadow: 0 18px 45px rgba(80, 45, 20, 0.14);
  }

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(-2px);
    margin-left: -3px;
    margin-right: -3px;
  }

  h1 {
    margin: 0;
    color: #3b2416;
    font-size: 38px;
  }

  p {
    color: #7a5a43;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 24px;
  }

  label {
    color: #3b2416;
    font-weight: 700;
  }

  input {
    border: 1px solid #ead8c3;
    border-radius: 16px;
    padding: 14px;
    font-size: 15px;
    outline: none;
    background: #fffaf4;
  }

  button {
    margin-top: 14px;
    border: none;
    border-radius: 999px;
    padding: 15px;
    background: #8b4a24;
    color: white;
    font-weight: 800;
    cursor: pointer;
  }

  button:hover {
    background: #6f3719;
  }

  .error {
    margin-top: 18px;
    padding: 12px;
    border-radius: 14px;
    background: #ffe6e6;
    color: #9b1c1c;
  }

  .switch {
    text-align: center;
    margin-top: 20px;
  }

  .switch a {
    color: #8b4a24;
    font-weight: 800;
  }
</style>