<script lang="ts">
  const benefits = [
    "Lieblingsgerichte übersichtlich verwalten",
    "Schnell zur Rezeptübersicht wechseln"
  ];

  const tips = [
    "Pasta-Wasser immer salzen, bevor die Nudeln hineinkommen.",
    "Messer regelmäßig schärfen – das macht Kochen schneller und sicherer.",
    "Kräuter erst am Ende dazugeben, damit sie frisch schmecken.",
    "Pfanne immer gut vorheizen, bevor du etwas anbrätst.",
    "Rezepte vor dem Kochen einmal komplett durchlesen.",
    "Zutaten vorher bereitstellen – das spart Stress beim Kochen.",
    "Reste direkt luftdicht verpacken, damit sie länger frisch bleiben."
  ];

  const today = new Date();
  const dayIndex = today.getDay();
  const tipOfTheDay = tips[dayIndex];
</script>

<main class="home">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="hero">
    <div class="left-column">
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

      <section class="benefits">
        {#each benefits as benefit}
          <div class="benefit-card">
            <span>✓</span>
            <p>{benefit}</p>
          </div>
        {/each}
      </section>

      <div class="daily-tip">
        <span>💡</span>
        <div>
          <strong>Tipp des Tages</strong>
          <p>{tipOfTheDay}</p>
        </div>
      </div>
    </div>

    <div class="cookie-card">
      <img src="/images/portrait.png" alt="SmartCookies Team" class="team-image" />

      <h2>Smart geplant. Einfach gekocht.</h2>
      <p>Mit SmartCookies findest du schneller das passende Rezept für deinen Tag.</p>
    </div>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #fff7ed, #f3dfc8);
    color: #3b2415;
    overflow: auto;
  }

  .home {
    height: 100vh;
    padding: 72px 24px 24px;
    box-sizing: border-box;
  }

  .brand-link {
    position: absolute;
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
    height: 100%;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.4fr 0.7fr;
    gap: 28px;
    align-items: stretch;
  }

  .left-column {
    display: grid;
    grid-template-rows: 1fr auto auto;
    gap: 18px;
    min-height: 0;
  }

  .content,
  .cookie-card,
  .benefit-card,
  .daily-tip {
    background: #fffaf4;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.12);
  }

  .content {
    border-radius: 26px;
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
    margin-top: 42px;
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
    border-radius: 26px;
    padding: 32px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .team-image {
    width: 100%;
    max-width: 420px;
    height: auto;
    object-fit: contain;
    margin: 0 auto 32px;
    border-radius: 28px;
    filter: drop-shadow(0 18px 28px rgba(59, 36, 20, 0.18));
  }

  .cookie-card h2 {
    color: #8b552b;
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
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin: 0;
  }

  .benefit-card {
    border-radius: 22px;
    padding: 16px 18px;
    display: flex;
    gap: 12px;
    align-items: center;
    min-height: 58px;
  }

  .benefit-card span {
    background: #9b551d;
    color: white;
    min-width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 16px;
  }

  .benefit-card p {
    margin: 0;
    color: #4a2c1a;
    font-weight: 800;
    font-size: 16px;
    line-height: 1.2;
  }

  .daily-tip {
    border-radius: 26px;
    padding: 22px 28px;
    display: flex;
    align-items: center;
    gap: 18px;
  }

  .daily-tip span {
    min-width: 46px;
    height: 46px;
    border-radius: 50%;
    background: #9b551d;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
  }

  .daily-tip strong {
    color: #8b552b;
    font-size: 20px;
  }

  .daily-tip p {
    margin: 5px 0 0;
    color: #6d5140;
    font-size: 17px;
    line-height: 1.4;
  }

  @media (max-width: 950px) {
    .home {
      height: auto;
      min-height: 100vh;
    }

    .hero {
      height: auto;
      grid-template-columns: 1fr;
    }

    .left-column {
      grid-template-rows: auto auto auto;
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

    .benefits {
      grid-template-columns: 1fr;
    }
  }
</style>