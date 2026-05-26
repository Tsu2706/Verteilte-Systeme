<script lang="ts">
  const recipe = {
    title: "Schoko-Cookies",
    time: "25 Min.",
    difficulty: "Einfach",
    description: "Knusprige Cookies mit Schokostückchen.",
    ingredients: ["200g Mehl", "100g Butter", "80g Zucker", "1 Ei", "Schokostückchen"],
    steps: [
      "Alle Zutaten in eine Schüssel geben.",
      "Teig gut verrühren.",
      "Cookies formen und auf ein Backblech legen.",
      "Bei 180 Grad ca. 12 Minuten backen."
    ]
  };
</script>

<main class="detail-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="recipe-detail">
    <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>

    <h1>{recipe.title}</h1>
    <p class="description">{recipe.description}</p>

    <div class="meta">
      <span>⏱ {recipe.time}</span>
      <span>⭐ {recipe.difficulty}</span>
    </div>

    <h2>Zutaten</h2>
    <ul>
      {#each recipe.ingredients as ingredient}
        <li>{ingredient}</li>
      {/each}
    </ul>

    <h2>Zubereitung</h2>
    <ol>
      {#each recipe.steps as step}
        <li>{step}</li>
      {/each}
    </ol>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #fff7ed, #f3dfc8);
    color: #2b2118;
  }

  .detail-page {
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

  .recipe-detail {
    max-width: 850px;
    margin: 0 auto;
    background: #fffaf4;
    padding: 42px;
    border-radius: 28px;
    box-shadow: 0 16px 40px rgba(92, 55, 25, 0.12);
  }

  .back-link {
    color: #8b552b;
    font-weight: 800;
    text-decoration: none;
  }

  h1 {
    font-size: 46px;
    margin: 24px 0 12px;
    color: #3b2415;
  }

  .description {
    font-size: 20px;
    color: #6d5140;
    line-height: 1.5;
  }

  .meta {
    display: flex;
    gap: 14px;
    margin: 26px 0;
  }

  .meta span {
    background: #e8d8c2;
    color: #4a2c1a;
    padding: 10px 16px;
    border-radius: 999px;
    font-weight: 800;
  }

  h2 {
    margin-top: 30px;
    color: #4a2c1a;
  }

  li {
    margin-bottom: 10px;
    font-size: 18px;
    color: #5c4535;
  }
</style>