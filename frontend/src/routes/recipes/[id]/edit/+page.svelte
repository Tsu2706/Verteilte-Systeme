<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";
  import { getRecipe, updateRecipe, type Recipe } from "$lib/api";

  let recipe = $state<Recipe | null>(null);
  let title = $state("");
  let description = $state("");
  let time = $state("");
  let difficulty = $state("");
  let ingredientsText = $state("");
  let stepsText = $state("");
  let isPublic = $state(true);
  let loading = $state(true);
  let error = $state("");

  function arrayToLines(values: string[] | undefined) {
    return values?.join("\n") ?? "";
  }

  function linesToArray(value: string) {
    return value
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
  }

  async function loadRecipe() {
    loading = true;
    error = "";

    try {
      const id = Number($page.params.id);
      recipe = await getRecipe(id);

      title = recipe.title;
      description = recipe.description ?? "";
      time = recipe.time ?? "";
      difficulty = recipe.difficulty ?? "";
      ingredientsText = arrayToLines(recipe.ingredients);
      stepsText = arrayToLines(recipe.steps);
      isPublic = recipe.is_public;
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  async function handleSubmit() {
    if (!recipe) return;

    error = "";

    try {
      await updateRecipe(recipe.id, {
        title,
        description,
        time,
        difficulty,
        ingredients: linesToArray(ingredientsText),
        steps: linesToArray(stepsText),
        is_public: isPublic
      });

      window.location.href = `/recipes/${recipe.id}`;
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht gespeichert werden.";
    }
  }

  $effect(() => {
    if (browser) {
      if (!localStorage.getItem("token")) {
        window.location.href = "/login";
        return;
      }

      loadRecipe();
    }
  });
</script>

<main class="edit-page">
  <a href="/" class="brand-link">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="form-card">
    <a href={recipe ? `/recipes/${recipe.id}` : "/recipes"} class="back-link">
      ← Zurück
    </a>

    <h1>Rezept bearbeiten</h1>
    <p>Bearbeite dein bestehendes Rezept oder passe einzelne Angaben an.</p>

    {#if loading}
      <p class="status">Rezept wird geladen...</p>
    {:else if error}
      <div class="error">{error}</div>
    {:else}
      <form
        onsubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
      >
        <label for="title">Rezeptname</label>
        <input id="title" bind:value={title} required />

        <label for="description">Beschreibung</label>
        <textarea id="description" bind:value={description}></textarea>

        <div class="row">
          <div>
            <label for="time">Zubereitungszeit</label>
            <input id="time" bind:value={time} />
          </div>

          <div>
            <label for="difficulty">Schwierigkeit</label>
            <input id="difficulty" bind:value={difficulty} />
          </div>
        </div>

        <label for="ingredients">Zutaten</label>
        <textarea id="ingredients" bind:value={ingredientsText} required></textarea>

        <label for="steps">Zubereitungsschritte</label>
        <textarea id="steps" bind:value={stepsText} required></textarea>

        <label class="checkbox">
          <input type="checkbox" bind:checked={isPublic} />
          Rezept öffentlich anzeigen
        </label>

        <button type="submit">Änderungen speichern</button>
      </form>
    {/if}
  </section>
</main>

<style>
  .edit-page {
    min-height: 100vh;
    background: #fff7ec;
    padding: 100px 28px 40px;
    font-family: Arial, sans-serif;
    color: #3b2416;
  }

  .brand-link {
    position: absolute;
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

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(-2px);
    margin-left: -3px;
    margin-right: -3px;
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

  .error {
    margin-top: 18px;
    padding: 12px;
    border-radius: 14px;
    background: #ffe6e6;
    color: #9b1c1c;
  }

  .status {
    margin-top: 28px;
    color: #7a5a43;
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