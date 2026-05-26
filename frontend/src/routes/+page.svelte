<script lang="ts">
  const benefits = [
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

  :global(a) {
    text-decoration: none;
  }

  .home {
    min-height: 100vh;
    padding: 48px 24px;
  }

  .hero {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.4fr 0.7fr;
    gap: 40px;
    align-items: stretch;
  }

  .content,
  .cookie-card,
  .benefit-card {
    background: #fffaf4;
    border-radius: 30px;
    box-shadow: 0 16px 40px rgba(92, 55, 25, 0.12);
  }

  .content {
    padding: 64px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .eyebrow {
    color: #a35b27;
    font-weight: 800;
    font-size: 22px;
    margin-bottom: 20px;
  }

  h1 {
    margin: 0;
    font-size: 72px;
    line-height: 0.95;
    color: #4a2c1a;
    letter-spacing: -2px;
  }

  .subtitle {
    margin-top: 28px;
    max-width: 650px;
    font-size: 22px;
    line-height: 1.7;
    color: #6d5140;
  }

  .actions {
    display: flex;
    gap: 20px;
    margin-top: 40px;
  }

  .primary,
  .secondary {
    width: 240px;
    height: 68px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 22px;
    transition: 0.2s ease;
    box-sizing: border-box;
  }

  .primary {
    background: #9b551d;
    color: white;
  }

  .primary:hover {
    transform: translateY(-2px);
  }

  .secondary {
    border: 3px solid #9b551d;
    color: #9b551d;
    background: transparent;
  }

  .secondary:hover {
    background: #fff1e5;
  }

  .cookie-card {
    padding: 48px;
    text-align: center;

    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .cookie {
    font-size: 90px;
    margin-bottom: 24px;
  }

  .cookie-card h2 {
    color: #4a2c1a;
    font-size: 42px;
    line-height: 1.1;
    margin-bottom: 20px;
  }

  .cookie-card p {
    color: #6d5140;
    line-height: 1.7;
    font-size: 22px;
  }

  .benefits {
    max-width: 1200px;
    margin: 36px auto 0;

    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }

  .benefit-card {
    padding: 28px;
    display: flex;
    gap: 18px;
    align-items: center;
    min-height: 110px;
  }

  .benefit-card span {
    background: #9b551d;
    color: white;

    min-width: 48px;
    height: 48px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-weight: 800;
    font-size: 22px;
  }

  .benefit-card p {
    margin: 0;
    color: #4a2c1a;
    font-weight: 700;
    font-size: 28px;
    line-height: 1.2;
  }

  @media (max-width: 950px) {
    .hero,
    .benefits {
      grid-template-columns: 1fr;
    }

    h1 {
      font-size: 52px;
    }

    .content {
      padding: 40px;
    }

    .actions {
      flex-direction: column;
    }

    .primary,
    .secondary {
      width: 100%;
    }
  }
</style>