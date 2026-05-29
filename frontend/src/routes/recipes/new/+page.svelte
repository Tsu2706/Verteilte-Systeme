<script lang="ts">
  import { browser } from "$app/environment";
  import { createRecipe } from "$lib/api";

  let title = $state("");
  let description = $state("");
  let time = $state("");
  let difficulty = $state("");
  let ingredientsText = $state("");
  let stepsText = $state("");
  let isPublic = $state(true);
  let error = $state("");
  let success = $state("");

  $effect(() => {
    if (browser && !localStorage.getItem("token")) {
      window.location.href = "/login";
    }
  });

  function linesToArray(value: string) {
    return value
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
  }

  async function handleSubmit() {
    error = "";
    success = "";

    try {
      const recipe = await createRecipe({
        title,
        description,
        time,
        difficulty,
        ingredients: linesToArray(ingredientsText),
        steps: linesToArray(stepsText),
        is_public: isPublic,
        tag_ids: []
      });

      success = "Rezept wurde erfolgreich gespeichert.";
      window.location.href = `/recipes/${recipe.id}`;
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht gespeichert werden.";
    }
  }
</script>

<main class="new-page">
  <a href="/" class="brand-link">
    SmartC<span>🍪</span><span>🍪</span>kies
  </a>

  <section class="form-card">
    <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>

    <h1>Neues Rezept</h1>
    <p>Erstelle ein neues Rezept für SmartCookies.</p>

    {#if error}
      <div class="error">{error}</div>
    {/if}

    {#if success}
      <div class="success">{success}</div>
    {/if}

    <form
      onsubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <label for="title">Rezeptname</label>
      <input id="title" bind:value={title} placeholder="z. B. Schoko-Cookies" required />

      <label for="description">Beschreibung</label>
      <textarea
        id="description"
        bind:value={description}
        placeholder="Kurze Beschreibung des Rezepts"
      ></textarea>

      <div class="row">
        <div>
          <label for="time">Zubereitungszeit</label>
          <input id="time" bind:value={time} placeholder="z. B. 30 Minuten" />
        </div>

        <div>
          <label for="difficulty">Schwierigkeit</label>
          <input id="difficulty" bind:value={difficulty} placeholder="z. B. Einfach" />
        </div>
      </div>

      <label for="ingredients">Zutaten</label>
      <textarea
        id="ingredients"
        bind:value={ingredientsText}
        placeholder="Jede Zutat in eine neue Zeile schreiben"
        required
      ></textarea>

      <label for="steps">Zubereitungsschritte</label>
      <textarea
        id="steps"
        bind:value={stepsText}
        placeholder="Jeden Schritt in eine neue Zeile schreiben"
        required
      ></textarea>

      <label class="checkbox">
        <input type="checkbox" bind:checked={isPublic} />
        Rezept öffentlich anzeigen
      </label>

      <button type="submit">Rezept speichern</button>
    </form>
  </section>
</main>

<style>
  .new-page {
    min-height: 100vh;
    background: #fff7ec;
    padding: 100px 28px 40px;
    font-family: Arial, sans-serif;
    color: #3b2416;
  }

  .brand-link {
    position: fixed;
    top: 28px;
    left: 36px;
    z-index: 10;
    text-decoration: none;
    color: #3b2416;
    font-size: 26px;
    font-weight: 800;
  }

  .form-card {
    max-width: 760px;
    margin: 0 auto;
    background: white;
    border-radius: 28px;
    padding: 38px;
    box-shadow: 0 18px 45px rgba(80, 45, 20, 0.14);
  }

  .back-link {
    text-decoration: none;
    color: #8b4a24;
    font-weight: 800;
  }

  h1 {
    margin: 26px 0 8px;
    font-size: 42px;
  }

  p {
    color: #7a5a43;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 13px;
    margin-top: 28px;
  }

  label {
    font-weight: 800;
  }

  input,
  textarea {
    border: 1px solid #ead8c3;
    border-radius: 16px;
    padding: 14px;
    font-size: 15px;
    outline: none;
    background: #fffaf4;
    font-family: inherit;
  }

  textarea {
    min-height: 110px;
    resize: vertical;
  }

  .row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }

  .row div {
    display: flex;
    flex-direction: column;
    gap: 13px;
  }

  .checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #7a5a43;
  }

  .checkbox input {
    width: 18px;
    height: 18px;
  }

  button {
    margin-top: 16px;
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

  .error,
  .success {
    margin-top: 18px;
    padding: 12px;
    border-radius: 14px;
  }

  .error {
    background: #ffe6e6;
    color: #9b1c1c;
  }

  .success {
    background: #e7f8ec;
    color: #19743a;
  }

  @media (max-width: 700px) {
    .row {
      grid-template-columns: 1fr;
    }

    .form-card {
      padding: 28px;
    }

    h1 {
      font-size: 34px;
    }
  }
</style>