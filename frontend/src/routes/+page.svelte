<script lang="ts">
  const benefits = [
    "Rezepte speichern und wiederfinden",
    "Lieblingsgerichte übersichtlich verwalten",
    "Schnell zur Rezeptübersicht wechseln"
  ];
</script>

<main class="home">
  <section class="hero">
    <div class="content">
      <p class="eyebrow">🍪 SmartCookies</p>

      <h1>Deine smarte Rezeptverwaltung</h1>

      <p class="subtitle">
        Speichere deine Lieblingsrezepte, entdecke neue Kochideen und behalte
        alles an einem Ort im Blick.
      </p>

      <div class="actions">
        <a href="/recipes" class="primary">Rezepte ansehen</a>
        <a href="/login" class="secondary">Einloggen</a>
      </div>
    </div>

    <div class="cookie-card">
      <div class="cookie">🍪</div>
      <h2>Smart geplant. Einfach gekocht.</h2>
      <p>
        Mit SmartCookies findest du schneller das passende Rezept für deinen Tag.
      </p>
    </div>
  </section>

  <section class="benefits">
    {#each benefits as benefit}
      <div class="benefit-card">
        <span>✓</span>
        <p>{benefit}</p>
      </div>
    {/each}
  </section>
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
    padding: 48px 24px;
  }

  .hero {
    max-width: 1100px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.3fr 0.7fr;
    gap: 32px;
    align-items: center;
  }

  .content,
  .cookie-card,
  .benefit-card {
    background: #fffaf4;
    border-radius: 28px;
    box-shadow: 0 16px 40px rgba(92, 55, 25, 0.14);
  }

  .content {
    padding: 56px;
  }

  .eyebrow {
    color: #a35b27;
    font-weight: 800;
    font-size: 20px;
    margin-bottom: 16px;
  }

  h1 {
    margin: 0;
    font-size: 52px;
    line-height: 1.05;
    color: #4a2c1a;
  }

  .subtitle {
    margin-top: 22px;
    max-width: 620px;
    font-size: 18px;
    line-height: 1.6;
    color: #6d5140;
  }

  .actions {
    display: flex;
    gap: 16px;
    margin-top: 34px;
  }

  .primary,
  .secondary {
    padding: 14px 24px;
    border-radius: 999px;
    text-decoration: none;
    font-weight: 800;
  }

  .primary {
    background: #8b4513;
    color: white;
  }

  .secondary {
    border: 2px solid #8b4513;
    color: #8b4513;
  }

  .cookie-card {
    padding: 36px;
    text-align: center;
  }

  .cookie {
    font-size: 76px;
    margin-bottom: 20px;
  }

  .cookie-card h2 {
    color: #4a2c1a;
    margin-bottom: 12px;
  }

  .cookie-card p {
    color: #6d5140;
    line-height: 1.5;
  }

  .benefits {
    max-width: 1100px;
    margin: 32px auto 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }

  .benefit-card {
    padding: 24px;
    display: flex;
    gap: 14px;
    align-items: center;
  }

  .benefit-card span {
    background: #8b4513;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-weight: 800;
  }

  .benefit-card p {
    margin: 0;
    color: #4a2c1a;
    font-weight: 700;
  }

  @media (max-width: 850px) {
    .hero,
    .benefits {
      grid-template-columns: 1fr;
    }

    .content {
      padding: 36px;
    }

    h1 {
      font-size: 38px;
    }

    .actions {
      flex-direction: column;
    }
  }
</style>