<script lang="ts">
  let username = "";
  let password = "";
  let message = "";

  function login() {
    if (!username || !password) {
      message = "Bitte Benutzername und Passwort eingeben.";
      return;
    }

    message = `Login für ${username} wurde ausgeführt.`;
  }

  function register() {
    if (!username || !password) {
      message = "Bitte Benutzername und Passwort eingeben.";
      return;
    }

    message = `Registrierung für ${username} wurde ausgeführt.`;
  }
</script>

<main class="login-page">
  <section class="login-card">
    <h1>Kochbuch App</h1>
    <p>Melde dich an oder registriere dich, um Rezepte hochzuladen und zu bewerten.</p>

    <label for="username">Benutzername</label>
    <input
      id="username"
      type="text"
      bind:value={username}
      placeholder="Benutzername eingeben"
    />

    <label for="password">Passwort</label>
    <input
      id="password"
      type="password"
      bind:value={password}
      placeholder="Passwort eingeben"
    />

    <div class="button-row">
      <button on:click={login}>Anmelden</button>
      <button class="secondary" on:click={register}>Registrieren</button>
    </div>

    {#if message}
      <p class="message">{message}</p>
    {/if}
  </section>
</main>

<style>
  .login-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f6f1e8;
    font-family: Arial, sans-serif;
  }

  .login-card {
    width: 100%;
    max-width: 420px;
    padding: 32px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
  }

  h1 {
    margin: 0 0 10px;
    color: #2f241d;
  }

  p {
    color: #6b5e54;
    margin-bottom: 24px;
  }

  label {
    display: block;
    margin: 14px 0 6px;
    font-weight: bold;
    color: #2f241d;
  }

  input {
    width: 100%;
    padding: 12px;
    border: 1px solid #d4c7b8;
    border-radius: 10px;
    font-size: 16px;
  }

  .button-row {
    display: flex;
    gap: 12px;
    margin-top: 22px;
  }

  button {
    flex: 1;
    padding: 12px;
    border: none;
    border-radius: 10px;
    background: #7a4f2a;
    color: white;
    font-weight: bold;
    cursor: pointer;
  }

  button:hover {
    background: #5f3d20;
  }

  .secondary {
    background: #e7d8c6;
    color: #2f241d;
  }

  .secondary:hover {
    background: #d6c1a7;
  }

  .message {
    margin-top: 18px;
    color: #2f241d;
    font-weight: bold;
  }
</style>