<script lang="ts">
  import { createRecipe } from "$lib/api";

  let title = $state("");
  let description = $state("");
  let ingredients = $state("");
  let steps = $state("");
  let time = $state("");
  let difficulty = $state("");
  let isPublic = $state(true);

  let saving = $state(false);
  let error = $state("");

  async function saveRecipe(event: SubmitEvent) {
    event.preventDefault();

    error = "";
    saving = true;

    try {
      await createRecipe({
        title,
        description,
        ingredients: ingredients
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        steps: steps
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        time,
        difficulty,
        is_public: isPublic
      });

      window.location.href = "/recipes";
    } catch (err) {
      error = "Rezept konnte nicht gespeichert werden.";
      console.error(err);
    } finally {
      saving = false;
    }
  }
</script>

<main class="new-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="form-card">
    <a href="/recipes" class="back-link">
      ← Zurück zu den Rezepten
    </a>

    <h1>Neues Rezept</h1>

    <p class="subtitle">
      Erstelle ein neues Lieblingsrezept für SmartCookies.
    </p>

    <form onsubmit={saveRecipe}>
      <div class="field">
        <label for="title">Rezeptname</label>
        <input
          id="title"
          bind:value={title}
          type="text"
          placeholder="z. B. Pasta Carbonara"
          required
        />
      </div>

      <div class="field">
        <label for="description">Beschreibung</label>
        <textarea
          id="description"
          bind:value={description}
          placeholder="Kurze Beschreibung des Rezepts"
        ></textarea>
      </div>

      <div class="double-grid">
        <div class="field">
          <label for="time">Zubereitungszeit</label>
          <input
            id="time"
            bind:value={time}
            type="text"
            placeholder="z. B. 30 Minuten"
          />
        </div>

        <div class="field">
          <label for="difficulty">Schwierigkeit</label>
          <select id="difficulty" bind:value={difficulty}>
            <option value="">Auswählen</option>
            <option value="Einfach">Einfach</option>
            <option value="Mittel">Mittel</option>
            <option value="Schwer">Schwer</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label for="ingredients">Zutaten</label>
        <textarea
          id="ingredients"
          bind:value={ingredients}
          placeholder="Jede Zutat in eine neue Zeile schreiben"
          required
        ></textarea>
      </div>

      <div class="field">
        <label for="steps">Zubereitung</label>
        <textarea
          id="steps"
          bind:value={steps}
          placeholder="Jeden Schritt in eine neue Zeile schreiben"
          required
        ></textarea>
      </div>

      <label class="checkbox-row">
        <input type="checkbox" bind:checked={isPublic} />
        Öffentlich sichtbar
      </label>

      {#if error}
        <div class="error-box">
          {error}
        </div>
      {/if}

      <button type="submit" disabled={saving}>
        {#if saving}
          Rezept wird gespeichert...
        {:else}
          Rezept speichern 🍪
        {/if}
      </button>
    </form>
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

  .new-page {
    min-height: 100vh;
    padding: 90px 24px 40px;
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
    max-width: 900px;
    margin: 0 auto;
    background: #fffaf4;
    border-radius: 30px;
    padding: 42px;
    box-shadow: 0 12px 30px rgba(92, 55, 25, 0.12);
  }

  .back-link {
    display: inline-block;
    margin-bottom: 28px;
    color: #9b551d;
    text-decoration: none;
    font-weight: 800;
  }

  h1 {
    margin: 0;
    font-size: 52px;
    color: #4a2c1a;
  }

  .subtitle {
    margin: 18px 0 34px;
    color: #6d5140;
    font-size: 18px;
    line-height: 1.5;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .field label {
    font-weight: 800;
    color: #4a2c1a;
  }

  input,
  textarea,
  select {
    border: none;
    outline: none;
    background: #fff0dd;
    border-radius: 18px;
    padding: 16px 18px;
    font-size: 16px;
    color: #4a2c1a;
    box-sizing: border-box;
  }

  textarea {
    min-height: 140px;
    resize: vertical;
  }

  .double-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }

  .checkbox-row {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    color: #6d5140;
  }

  .checkbox-row input {
    width: 18px;
    height: 18px;
  }

  button {
    height: 56px;
    border: none;
    border-radius: 999px;
    background: #9b551d;
    color: white;
    font-size: 18px;
    font-weight: 800;
    cursor: pointer;
    transition: transform 0.2s ease;
  }

  button:hover {
    transform: translateY(-2px);
  }

  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .error-box {
    background: #ffe4e1;
    color: #b42318;
    padding: 16px 18px;
    border-radius: 18px;
    font-weight: 700;
  }

  @media (max-width: 750px) {
    .brand-link {
      position: static;
      margin-bottom: 20px;
    }

    .new-page {
      padding-top: 24px;
    }

    .form-card {
      padding: 28px;
    }

    .double-grid {
      grid-template-columns: 1fr;
    }

    h1 {
      font-size: 40px;
    }
  }
</style>