<main class="auth-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="auth-card">
    <h1>Anmelden</h1>
    <p>Melde dich an, um deine Rezepte zu verwalten.</p>

    <form>
      <label for="username">Benutzername</label>
      <input id="username" type="text" placeholder="Benutzername eingeben" />

      <label for="password">Passwort</label>
      <input id="password" type="password" placeholder="Passwort eingeben" />

      <button type="submit" class="primary">Anmelden</button>
      <a href="/register" class="secondary">Registrieren</a>
    </form>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #fff7ed, #f3dfc8);
    color: #2b2118;
  }

  .auth-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 80px 24px 24px;
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
    gap: 0;
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

  .auth-card {
    width: 100%;
    max-width: 620px;
    background: #fffaf4;
    padding: 36px 44px;
    border-radius: 24px;
    box-shadow: 0 14px 35px rgba(92, 55, 25, 0.14);
  }

  h1 {
    font-size: 40px;
    margin: 0 0 16px;
    color: #3b2415;
  }

  p {
    font-size: 18px;
    color: #6d5140;
    margin: 0 0 26px;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  label {
    font-size: 20px;
    font-weight: 800;
  }

  input {
    height: 50px;
    border-radius: 12px;
    border: 1px solid #d8c3ad;
    padding: 0 16px;
    font-size: 18px;
  }

  .primary,
  .secondary {
    height: 54px;
    border-radius: 14px;
    font-size: 20px;
    font-weight: 800;
    margin-top: 18px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
  }

  .primary {
    background: #8b552b;
    color: white;
    border: none;
  }

  .secondary {
    background: #e8d8c2;
    color: #2b2118;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 4px;
  }
</style>