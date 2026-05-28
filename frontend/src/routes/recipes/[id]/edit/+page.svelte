<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { getRecipe, updateRecipe, deleteRecipe } from "$lib/api";

  const id = Number($page.params.id);

  let title = $state("");
  let description = $state("");
  let ingredients = $state("");
  let instructions = $state("");
  let time = $state("");
  let difficulty = $state("");
  let image_url = $state("");

  let loading = $state(true);
  let saving = $state(false);
  let error = $state("");
  let success = $state("");

  onMount(async () => {
    try {
      const recipe = await getRecipe(id);

      title = recipe.title ?? "";
      description = recipe.description ?? "";
      ingredients = recipe.ingredients ?? "";
      instructions = recipe.instructions ?? "";
      time = recipe.time ?? "";
      difficulty = recipe.difficulty ?? "";
      image_url = recipe.image_url ?? "";
    } catch (err) {
      error = "Das Rezept konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  });

  async function saveRecipe() {
    error = "";
    success = "";
    saving = true;

    try {
      await updateRecipe(id, {
        title,
        description,
        ingredients,
        instructions,
        time,
        difficulty,
        image_url
      });

      success = "Rezept wurde erfolgreich gespeichert.";
      setTimeout(() => goto(`/recipes/${id}`), 700);
    } catch (err) {
      error = "Das Rezept konnte nicht gespeichert werden.";
    } finally {
      saving = false;
    }
  }

  async function removeRecipe() {
    const confirmed = confirm("Möchtest du dieses Rezept wirklich löschen?");

    if (!confirmed) return;

    try {
      await deleteRecipe(id);
      goto("/recipes");
    } catch (err) {
      error = "Das Rezept konnte nicht gelöscht werden.";
    }
  }
</script>

<main class="edit-page">
  <a href="/" class="brand-link" aria-label="Zur Startseite">
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="form-card">
    <a href={`/recipes/${id}`} class="back-link">← Zurück zum Rezept</a>

    <h1>Rezept bearbeiten</h1>
    <p>Passe dein Rezept an oder lösche es dauerhaft.</p>

    {#if loading}
      <div class="state-box">Rezept wird geladen...</div>
    {:else}
      {#if error}
        <div class="error-box">{error}</div>
      {/if}

      {#if success}
        <div class="success-box">{success}</div>
      {/if}

      <form
        onsubmit={(event) => {
          event.preventDefault();
          saveRecipe();
        }}
      >
        <label for="title">Rezeptname</label>
        <input
          id="title"
          bind:value={title}
          type="text"
          placeholder="z. B. Schoko-Cookies"
          required
        />

        <label for="description">Beschreibung</label>
        <textarea
          id="description"
          bind:value={description}
          placeholder="Kurze Beschreibung"
        ></textarea>

        <label for="ingredients">Zutaten</label>
        <textarea
          id="ingredients"
          bind:value={ingredients}
          placeholder="Zutaten eingeben"
        ></textarea>

        <label for="instructions">Zubereitung</label>
        <textarea
          id="instructions"
          bind:value={instructions}
          placeholder="Zubereitungsschritte eingeben"
        ></textarea>

        <div class="form-grid">
          <div>
            <label for="time">Zubereitungszeit</label>
            <input
              id="time"
              bind:value={time}
              type="text"
              placeholder="z. B. 30 Minuten"
            />
          </div>

          <div>
            <label for="difficulty">Schwierigkeit</label>
            <input
              id="difficulty"
              bind:value={difficulty}
              type="text"
              placeholder="z. B. Einfach"
            />
          </div>
        </div>

        <label for="image_url">Bild-URL</label>
        <input
          id="image_url"
          bind:value={image_url}
          type="text"
          placeholder="https://..."
        />

        <div class="actions">
          <button type="button" class="delete-button" onclick={removeRecipe}>
            Löschen
          </button>

          <button type="submit" class="save-button" disabled={saving}>
            {saving ? "Speichern..." : "Änderungen speichern"}
          </button>
        </div>
      </form>
    {/if}
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background:
      radial-gradient(circle at top left, #ffe1b8 0, transparent 34%),
      linear-gradient(135deg, #fff7ec 0%, #f6d7aa 100%);
    color: #3d2415;
  }

  .edit-page {
    min-height: 100vh;
    padding: 110px 24px 40px;
    box-sizing: border-box;
  }

  .brand-link {
    position: fixed;
    top: 28px;
    left: 34px;
    z-index: 20;
    text-decoration: none;
    font-size: 2rem;
    font-weight: 900;
    color: #3d2415;
    letter-spacing: -1px;
  }

  .cookie-o {
    display: inline-block;
    margin: 0 -2px;
    font-size: 1.65rem;
    vertical-align: 2px;
  }

  .form-card {
    width: min(820px, 100%);
    margin: 0 auto;
    padding: 34px;
    border-radius: 32px;
    background: rgba(255, 255, 255, 0.78);
    box-shadow: 0 24px 70px rgba(77, 43, 18, 0.18);
    backdrop-filter: blur(12px);
  }

  .back-link {
    display: inline-block;
    margin-bottom: 18px;
    color: #8a5a2f;
    font-weight: 700;
    text-decoration: none;
  }

  h1 {
    margin: 0;
    font-size: clamp(2.2rem, 5vw, 4rem);
    letter-spacing: -2px;
  }

  p {
    margin: 12px 0 28px;
    color: #6f5646;
    font-size: 1.05rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  label {
    font-weight: 800;
    color: #4a2b18;
  }

  input,
  textarea {
    width: 100%;
    box-sizing: border-box;
    border: 2px solid #efd1ad;
    border-radius: 18px;
    padding: 14px 16px;
    font: inherit;
    background: #fffaf3;
    color: #3d2415;
    outline: none;
  }

  textarea {
    min-height: 105px;
    resize: vertical;
  }

  input:focus,
  textarea:focus {
    border-color: #c87a35;
    box-shadow: 0 0 0 4px rgba(200, 122, 53, 0.14);
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .actions {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    margin-top: 18px;
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 14px 22px;
    font-weight: 900;
    cursor: pointer;
  }

  button:hover {
    transform: translateY(-2px);
  }

  .save-button {
    background: #3d2415;
    color: white;
    box-shadow: 0 12px 26px rgba(61, 36, 21, 0.22);
  }

  .delete-button {
    background: #fff0ec;
    color: #b42318;
    border: 2px solid #ffd0c7;
  }

  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .state-box,
  .error-box,
  .success-box {
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 18px;
    font-weight: 700;
  }

  .state-box {
    background: #fff7ec;
  }

  .error-box {
    background: #fff0ec;
    color: #b42318;
  }

  .success-box {
    background: #ecfdf3;
    color: #027a48;
  }

  @media (max-width: 700px) {
    .edit-page {
      padding: 96px 16px 28px;
    }

    .brand-link {
      top: 20px;
      left: 20px;
      font-size: 1.55rem;
    }

    .form-card {
      padding: 24px;
      border-radius: 24px;
    }

    .form-grid {
      grid-template-columns: 1fr;
    }

    .actions {
      flex-direction: column;
    }
  }
</style>