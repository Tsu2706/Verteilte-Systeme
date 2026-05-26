<script lang="ts">
  let { children } = $props();
</script>

<nav>
  <a href="/">SmartCookies</a>
  <a href="/recipes">Rezepte</a>
  <a href="/login">Login</a>
</nav>

{@render children()}
