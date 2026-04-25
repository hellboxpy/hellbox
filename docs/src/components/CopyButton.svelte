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
    background-color: rgba(255, 255, 255, 1);
    border: none;
    border-radius: 4px;
    color: rgba(0, 0, 0, 0.8);
    cursor: pointer;
    transition:
      background 0.3s ease,
      color 0.3s ease;
    transform: rotate(-45deg);
  }

  button:hover {
    background: rgba(220, 220, 220, 1);
  }
</style>
