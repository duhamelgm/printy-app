<script lang="ts">
	import { goto } from '$app/navigation';
	import authorizedPost from '$lib/authorizedPost';
  import Button from '$lib/components/ui/button/button.svelte';

  let loading = $state(false);
  
  const handlePrintFortune = async () => {
    loading = true;
    try {
      const data = await authorizedPost('/v1/print/fortune');
      if (data.status === 'ok') {
				goto('/print/success');
			}
    } catch (error) {
      console.error(error);
    } finally {
      loading = false;
    }
  };
</script>

<Button onclick={handlePrintFortune} disabled={loading} {loading} size="lg" endIcon="Casino">Reveal Fortune</Button>