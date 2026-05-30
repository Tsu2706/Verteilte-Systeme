<script lang="ts">
  import { browser } from "$app/environment";
  import { createRecipe, getTags, getMe, createTag, deleteTag, type Tag, type User } from "$lib/api";

  let title = $state("");
  let description = $state("");
  let time = $state("");
  let difficulty = $state("");
  let ingredientsText = $state("");
  let stepsText = $state("");
  let isPublic = $state(true);

  let currentUser = $state<User | null>(null);

  let tags = $state<Tag[]>([]);
  let selectedTagIds = $state<number[]>([]);
  let newTagName = $state("");

  let error = $state("");
  let success = $state("");

  $effect(() => {
    if (browser) {
      if (!localStorage.getItem("token")) {
        window.location.href = "/login";
        return;
      }

      loadTags();
    }
  });

  async function loadTags() {
    try {
      currentUser = await getMe();
      tags = await getTags();
    } catch {
      tags = [];
    }
  }

  function linesToArray(value: string) {
    return value
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
  }

  function toggleTag(tagId: number) {
    if (selectedTagIds.includes(tagId)) {
      selectedTagIds = selectedTagIds.filter((id) => id !== tagId);
    } else {
      selectedTagIds = [...selectedTagIds, tagId];
    }
  }

  async function handleCreateTag() {
    error = "";

    if (!newTagName.trim()) return;

    try {
      const tag = await createTag(newTagName.trim());
      tags = [...tags, tag];
      selectedTagIds = [...selectedTagIds, tag.id];
      newTagName = "";
    } catch (err) {
      error = err instanceof Error ? err.message : "Tag konnte nicht erstellt werden.";
    }
  }

  async function handleDeleteTag(tagId: number) {
    error = "";

    const confirmed = confirm("Möchtest du diesen Tag wirklich löschen?");
    if (!confirmed) return;

    try {
      await deleteTag(tagId);
      tags = tags.filter((tag) => tag.id !== tagId);
      selectedTagIds = selectedTagIds.filter((id) => id !== tagId);
    } catch (err) {
      error = err instanceof Error ? err.message : "Tag konnte nicht gelöscht werden.";
    }
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
        tag_ids: selectedTagIds
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
    SmartC<span class="cookie-o">🍪</span><span class="cookie-o">🍪</span>kies
  </a>

  <section class="form-card">
    <a href="/recipes" class="back-link">← Zurück zu den Rezepten</a>

    <h1>Neues Rezept</h1>
    <p>Erstelle ein neues Rezept und ordne passende Tags/Kategorien zu.</p>

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

      <section class="tag-section">
        <p class="section-label">Tags / Kategorien</p>

        {#if tags.length > 0}
          <div class="tag-list">
            {#each tags as tag}
              <div class="tag-item">
                <button
                  type="button"
                  class:active={selectedTagIds.includes(tag.id)}
                  onclick={() => toggleTag(tag.id)}
                >
                  {tag.name}
                </button>
                {#if currentUser && tag.creator_id === currentUser.id}
                <button
                  type="button"
                  class="tag-delete-button"
                  onclick={() => handleDeleteTag(tag.id)}
                  aria-label={`Tag ${tag.name} löschen`}
                >
                  ×
                </button>
                {/if}
              </div>
            {/each}
          </div>
        {:else}
          <p class="small-info">Noch keine Tags vorhanden.</p>
        {/if}

        <div class="new-tag-row">
          <input
            bind:value={newTagName}
            placeholder="Neuen Tag erstellen, z. B. Vegan"
          />

          <button type="button" class="tag-create-button" onclick={handleCreateTag}>
            Tag hinzufügen
          </button>
        </div>
      </section>

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

      <button type="submit" class="submit-button">Rezept speichern</button>
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

  label,
  .section-label {
    font-weight: 800;
    color: #3b2416;
  }

  .section-label {
    margin: 0;
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

  .tag-section {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 20px;
    border-radius: 22px;
    background: #fff7ec;
    border: 1px solid #f0dfcd;
  }

  .tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .tag-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .tag-item > button:first-child {
    border: 1px solid #ead8c3;
    border-radius: 999px;
    background: #fffaf4;
    color: #7a5a43;
    padding: 9px 14px;
    cursor: pointer;
    font-weight: 700;
  }

  .tag-item > button:first-child.active {
    background: #8b4a24;
    color: white;
    border-color: #8b4a24;
  }

  .tag-delete-button {
    border: none;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #ffe6e6;
    color: #9b1c1c;
    font-weight: 900;
    cursor: pointer;
  }

  .new-tag-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    margin-top: 4px;
  }

  .tag-create-button {
    border: none;
    border-radius: 999px;
    padding: 0 16px;
    background: #f2ddc7;
    color: #6f3719;
    font-weight: 800;
    cursor: pointer;
  }

  .small-info {
    margin: 0;
    color: #7a5a43;
    font-size: 14px;
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

  .submit-button {
    margin-top: 16px;
    border: none;
    border-radius: 999px;
    padding: 15px;
    background: #8b4a24;
    color: white;
    font-weight: 800;
    cursor: pointer;
  }

  .submit-button:hover {
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
    .row,
    .new-tag-row {
      grid-template-columns: 1fr;
    }

    .tag-create-button {
      padding: 13px 16px;
    }

    .form-card {
      padding: 28px;
    }

    h1 {
      font-size: 34px;
    }
  }
</style>