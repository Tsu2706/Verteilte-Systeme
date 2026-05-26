<main class="new-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="form-card">
    <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>

    <h1>Neues Rezept</h1>
    <p>Erstelle ein neues Rezept für SmartCookies.</p>

    <form>
      <label for="title">Rezeptname</label>
      <input id="title" type="text" placeholder="z. B. Schoko-Cookies" />

      <label for="description">Beschreibung</label>
      <textarea id="description" placeholder="Kurze Beschreibung des Rezepts"></textarea>

      <label for="time">Zubereitungszeit</label>
      <input id="time" type="text" placeholder="z. B. 25 Min." />

      <label for="ingredients">Zutaten</label>
      <textarea id="ingredients" placeholder="Zutaten eingeben"></textarea>

      <label for="steps">Zubereitung</label>
      <textarea id="steps" placeholder="Zubereitungsschritte eingeben"></textarea>

      <button type="submit">Rezept speichern</button>
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

  .new-page {
    min-height: 100vh;
    padding: 90px 24px 48px;
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

  .form-card {
    max-width: 760px;
    margin: 0 auto;
    background: #fffaf4;
    padding: 38px 44px;
    border-radius: 28px;
    box-shadow: 0 16px 40px rgba(92, 55, 25, 0.12);
  }

  .back-link {
    color: #8b552b;
    font-weight: 800;
    text-decoration: none;
  }

  h1 {
    font-size: 42px;
    margin: 24px 0 10px;
    color: #3b2415;
  }

  p {
    font-size: 18px;
    color: #6d5140;
    margin-bottom: 28px;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  label {
    font-size: 19px;
    font-weight: 800;
    color: #3b2415;
  }

  input,
  textarea {
    border-radius: 12px;
    border: 1px solid #d8c3ad;
    padding: 14px 16px;
    font-size: 17px;
    font-family: Arial, sans-serif;
    background: white;
  }

  input {
    height: 48px;
    box-sizing: border-box;
  }

  textarea {
    min-height: 80px;
    resize: vertical;
  }

  button {
    height: 54px;
    border-radius: 14px;
    font-size: 20px;
    font-weight: 800;
    margin-top: 18px;
    cursor: pointer;
    background: #8b552b;
    color: white;
    border: none;
  }
</style>