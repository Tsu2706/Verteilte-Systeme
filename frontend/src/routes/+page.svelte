<script lang="ts">
  const benefits = [
    "Lieblingsgerichte übersichtlich verwalten",
    "Schnell zur Rezeptübersicht wechseln"
  ];
</script>

<main class="home">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="hero">
    <div class="content">
      <p class="eyebrow">Deine smarte Rezept-App</p>

      <h1>
        SmartC<span class="headline-cookie">🍪</span><span class="headline-cookie">🍪</span>kies
      </h1>

      <p class="subtitle">
        Speichere deine Lieblingsrezepte, entdecke neue Kochideen und behalte
        alles übersichtlich an einem Ort.
      </p>

      <div class="actions">
        <a href="/recipes" class="primary">Rezepte ansehen</a>
        <a href="/login" class="secondary">Einloggen</a>
      </div>
    </div>

    <div class="cookie-card">
      <div class="cookie">🍪</div>
      <h2>Smart geplant. Einfach gekocht.</h2>
      <p>Mit SmartCookies findest du schneller das passende Rezept für deinen Tag.</p>
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
    overflow: hidden;
  }

  .home {
    height: 100vh;
    padding: 72px 24px 24px;
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

  .hero {
    max-width: 1180px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.4fr 0.7fr;
    gap: 28px;
    align-items: stretch;
  }

  .content,
  .cookie-card,
  .benefit-card {
    background: #fffaf4;
    border-radius: 26px;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.12);
  }

  .content {
    padding: 42px 50px;
  }

  .eyebrow {
    color: #a35b27;
    font-weight: 800;
    font-size: 18px;
    margin: 0 0 14px;
  }

  h1 {
    margin: 0;
    font-size: 56px;
    line-height: 0.95;
    color: #4a2c1a;
    letter-spacing: -2px;
  }

  .headline-cookie {
    font-size: 0.62em;
    display: inline-block;
    transform: translateY(-4px);
    margin-left: -5px;
    margin-right: -5px;
  }

  .subtitle {
    margin: 22px 0 0;
    max-width: 650px;
    font-size: 18px;
    line-height: 1.5;
    color: #6d5140;
  }

  .actions {
    display: flex;
    gap: 16px;
    margin-top: 28px;
  }

  .primary,
  .secondary {
    width: 210px;
    height: 54px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
    text-decoration: none;
    box-sizing: border-box;
  }

  .primary {
    background: #9b551d;
    color: white;
  }

  .secondary {
    border: 3px solid #9b551d;
    color: #9b551d;
  }

  .cookie-card {
    padding: 32px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .cookie {
    font-size: 62px;
    margin-bottom: 16px;
  }

  .cookie-card h2 {
    color: #4a2c1a;
    font-size: 30px;
    line-height: 1.1;
    margin: 0 0 14px;
  }

  .cookie-card p {
    color: #6d5140;
    line-height: 1.5;
    font-size: 17px;
    margin: 0;
  }

  .benefits {
    max-width: 1180px;
    margin: 24px auto 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
  }

  .benefit-card {
    padding: 20px 24px;
    display: flex;
    gap: 14px;
    align-items: center;
    min-height: 76px;
  }

  .benefit-card span {
    background: #9b551d;
    color: white;
    min-width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
  }

  .benefit-card p {
    margin: 0;
    color: #4a2c1a;
    font-weight: 700;
    font-size: 20px;
    line-height: 1.2;
  }

  @media (max-width: 950px) {
    :global(body) {
      overflow: auto;
    }

    .home {
      height: auto;
      min-height: 100vh;
    }

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