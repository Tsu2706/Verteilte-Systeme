<script lang="ts">
  import { browser } from "$app/environment";
  import { page } from "$app/stores";
  import {
    getRecipe,
    updateRecipe,
    getMe,
    getTags,
    type Recipe,
    type User,
    type Tag
  } from "$lib/api";

  let recipe = $state<Recipe | null>(null);
  let currentUser = $state<User | null>(null);
  let tags = $state<Tag[]>([]);

  let title = $state("");
  let description = $state("");
  let ingredientsText = $state("");
  let stepsText = $state("");
  let time = $state("");
  let difficulty = $state("");
  let isPublic = $state(true);
  let selectedTagIds = $state<number[]>([]);

  let loading = $state(true);
  let saving = $state(false);
  let error = $state("");
  let success = $state("");

  async function loadData() {
    loading = true;
    error = "";

    try {
      currentUser = await getMe();

      const id = Number($page.params.id);
      recipe = await getRecipe(id);

      if (recipe.user_id !== currentUser.id) {
        error = "Du darfst nur deine eigenen Rezepte bearbeiten.";
        return;
      }

      tags = await getTags();

      title = recipe.title;
      description = recipe.description ?? "";
      ingredientsText = recipe.ingredients?.join("\n") ?? "";
      stepsText = recipe.steps?.join("\n") ?? "";
      time = recipe.time ?? "";
      difficulty = recipe.difficulty ?? "";
      isPublic = recipe.is_public;
      selectedTagIds = recipe.tags?.map((tag) => tag.id) ?? [];
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht geladen werden.";
    } finally {
      loading = false;
    }
  }

  function toggleTag(tagId: number) {
    if (selectedTagIds.includes(tagId)) {
      selectedTagIds = selectedTagIds.filter((id) => id !== tagId);
    } else {
      selectedTagIds = [...selectedTagIds, tagId];
    }
  }

  async function handleSubmit() {
    if (!recipe) return;

    saving = true;
    error = "";
    success = "";

    try {
      await updateRecipe(recipe.id, {
        title,
        description,
        ingredients: ingredientsText
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        steps: stepsText
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        time,
        difficulty,
        is_public: isPublic,
        tag_ids: selectedTagIds
      });

      success = "Rezept wurde gespeichert.";
      window.location.href = `/recipes/${recipe.id}`;
    } catch (err) {
      error = err instanceof Error ? err.message : "Rezept konnte nicht gespeichert werden.";
    } finally {
      saving = false;
    }
  }

  $effect(() => {
    if (browser) {
      loadData();
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
    <p>Hier kannst du nur deine eigenen Rezepte ändern.</p>

    {#if loading}
      <p class="status">Rezept wird geladen...</p>
    {:else if error}
      <p class="status error">{error}</p>
    {:else if recipe}
      <form onsubmit={(event) => { event.preventDefault(); handleSubmit(); }}>
        <label for="title">Rezeptname</label>
        <input id="title" bind:value={title} required />

        <label for="description">Beschreibung</label>
        <textarea id="description" bind:value={description}></textarea>

        <label for="time">Zubereitungszeit</label>
        <input id="time" bind:value={time} placeholder="z. B. 30 Minuten" />

        <label for="difficulty">Schwierigkeit</label>
        <select id="difficulty" bind:value={difficulty}>
          <option value="">Bitte auswählen</option>
          <option value="Einfach">Einfach</option>
          <option value="Mittel">Mittel</option>
          <option value="Schwer">Schwer</option>
        </select>

        <label for="ingredients">Zutaten</label>
        <textarea
          id="ingredients"
          bind:value={ingredientsText}
          placeholder="Eine Zutat pro Zeile"
          required
        ></textarea>

        <label for="steps">Zubereitungsschritte</label>
        <textarea
          id="steps"
          bind:value={stepsText}
          placeholder="Ein Schritt pro Zeile"
          required
        ></textarea>

        <div class="visibility-row">
          <input id="isPublic" type="checkbox" bind:checked={isPublic} />
          <label for="isPublic">Rezept öffentlich sichtbar machen</label>
        </div>

        {#if tags.length > 0}
          <div class="tag-section">
            <p>Tags</p>

            <div class="tag-list">
              {#each tags as tag}
                <button
                  type="button"
                  class:active={selectedTagIds.includes(tag.id)}
                  onclick={() => toggleTag(tag.id)}
                >
                  {tag.name}
                </button>
              {/each}
            </div>
          </div>
        {/if}

        {#if success}
          <p class="status success">{success}</p>
        {/if}

        {#if error}
          <p class="status error">{error}</p>
        {/if}

        <button type="submit" class="save-button" disabled={saving}>
          {saving ? "Wird gespeichert..." : "Speichern"}
        </button>
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

  .cookie-o {
    font-size: 0.72em;
    line-height: 1;
    display: inline-flex;
    transform: translateY(-2px);
    margin-left: -3px;
    margin-right: -3px;
  }

  .form-card {
    max-width: 820px;
    margin: 0 auto;
    background: white;
    border-radius: 30px;
    padding: 40px;
    box-shadow: 0 18px 45px rgba(80, 45, 20, 0.14);
  }

  .back-link {
    text-decoration: none;
    color: #8b4a24;
    font-weight: 800;
  }

  h1 {
    margin: 28px 0 8px;
    font-size: 42px;
  }

  p {
    color: #7a5a43;
  }

  form {
    display: grid;
    gap: 14px;
    margin-top: 30px;
  }

  label {
    font-weight: 800;
    color: #5a331f;
  }

  input,
  textarea,
  select {
    border: 1px solid #ead6c2;
    border-radius: 16px;
    padding: 14px 16px;
    font-size: 16px;
    font-family: inherit;
    background: #fffaf5;
    color: #3b2416;
  }

  textarea {
    min-height: 110px;
    resize: vertical;
  }

  .visibility-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
  }

  .visibility-row input {
    width: 18px;
    height: 18px;
  }

  .tag-section {
    margin-top: 12px;
  }

  .tag-section p {
    margin-bottom: 10px;
    font-weight: 800;
    color: #5a331f;
  }

  .tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .tag-list button {
    border: 1px solid #ead6c2;
    background: #fffaf5;
    color: #8b4a24;
    border-radius: 999px;
    padding: 9px 14px;
    font-weight: 800;
    cursor: pointer;
  }

  .tag-list button.active {
    background: #8b4a24;
    color: white;
    border-color: #8b4a24;
  }

  .save-button {
    margin-top: 18px;
    border: none;
    border-radius: 999px;
    padding: 15px 22px;
    background: #8b4a24;
    color: white;
    font-weight: 900;
    font-size: 16px;
    cursor: pointer;
  }

  .save-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .status {
    margin-top: 18px;
    color: #7a5a43;
    font-weight: 700;
  }

  .status.error {
    color: #9b1c1c;
  }

  .status.success {
    color: #2f7d32;
  }

  @media (max-width: 700px) {
    .form-card {
      padding: 28px;
    }

    h1 {
      font-size: 34px;
    }
  }
</style>