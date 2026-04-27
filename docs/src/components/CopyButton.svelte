<script>
  import { Copy, Check } from "lucide-svelte";

  let { text } = $props();
  let copied = $state(false);

  async function handleClick() {
    await navigator.clipboard.writeText(text);
    copied = true;
    setTimeout(() => (copied = false), 2500);
  }
</script>

<button
  onclick={handleClick}
  aria-label={copied ? "Copied!" : "Copy to clipboard"}
>
  {#if copied}
    <Check size={18} strokeWidth={2} />
  {:else}
    <Copy size={18} strokeWidth={2} />
  {/if}
</button>

<style>
  button {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    padding: 0.6rem;
    background-color: var(--color-button-bg);
    border: 1px solid;
    border-color:
      var(--color-emboss-highlight)
      var(--color-emboss-shadow)
      var(--color-emboss-shadow)
      var(--color-emboss-highlight);
    border-radius: 1px;
    color: var(--color-text-muted);
    cursor: pointer;
    transition:
      background 0.3s ease,
      color 0.3s ease,
      border-color 0.3s ease;
  }

  button:active {
    background: var(--color-button-active-bg);
    border-color:
      var(--color-emboss-shadow)
      var(--color-emboss-highlight)
      var(--color-emboss-highlight)
      var(--color-emboss-shadow);
    transition: none;
  }
</style>
