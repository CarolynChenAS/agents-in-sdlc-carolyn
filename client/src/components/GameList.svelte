<script lang="ts">
    import { onMount } from "svelte";

    interface Game {
        id: number;
        title: string;
        description: string;
        publisher_name?: string;
        category_name?: string;
    }

    export let games: Game[] = [];
    let loading = true;
    let error: string | null = null;

    const fetchGames = async () => {
        loading = true;
        try {
            const response = await fetch('/api/games');
            if(response.ok) {
                games = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    onMount(() => {
        fetchGames();
    });
</script>

<div>
    <h2 class="text-2xl font-semibold mb-6 text-white tracking-wide">Featured Games</h2>
    
    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/70 backdrop-blur-sm rounded-lg overflow-hidden shadow-xl border border-slate-700/60">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-5 bg-slate-700/80 rounded w-3/4 mb-3"></div>
                            <div class="h-3 bg-slate-700/60 rounded w-full mb-2"></div>
                            <div class="h-3 bg-slate-700/60 rounded w-5/6 mb-2"></div>
                            <div class="h-3 bg-slate-700/60 rounded w-4/5 mb-4"></div>
                            <div class="flex gap-2 mb-4">
                                <div class="h-6 bg-slate-700/60 rounded-md w-16"></div>
                                <div class="h-6 bg-slate-700/60 rounded-md w-20"></div>
                            </div>
                            <div class="h-4 bg-slate-700/80 rounded w-24"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/70 backdrop-blur-sm rounded-lg border border-slate-700/60 shadow-xl">
            <p class="text-red-400 font-medium">{error}</p>
        </div>
    {:else if games.length === 0}
        <!-- no games found -->
        <div class="text-center py-12 bg-slate-800/70 backdrop-blur-sm rounded-lg border border-slate-700/60 shadow-xl">
            <p class="text-slate-300 font-medium">No games available at the moment.</p>
        </div>
    {:else}
        <!-- game list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="games-grid">
            {#each games as game (game.id)}
                <div 
                    class="group bg-slate-800/70 backdrop-blur-sm rounded-lg overflow-hidden shadow-xl border border-slate-700/60 hover:border-slate-600/80 hover:shadow-2xl hover:shadow-blue-500/5 transition-all duration-300 hover:translate-y-[-2px]"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-br from-slate-700/20 to-slate-800/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-lg font-semibold text-white mb-3 group-hover:text-blue-300 transition-colors line-clamp-1" data-testid="game-title">{game.title}</h3>
                            
                            <p class="text-slate-300 mb-4 text-sm leading-relaxed line-clamp-3" data-testid="game-description">{game.description}</p>
                            
                            {#if game.category_name || game.publisher_name}
                                <div class="flex gap-2 mb-4">
                                    {#if game.category_name}
                                        <span class="text-xs font-medium px-2 py-1 rounded-md bg-blue-900/40 text-blue-300 border border-blue-800/30" data-testid="game-category">
                                            {game.category_name}
                                        </span>
                                    {/if}
                                    {#if game.publisher_name}
                                        <span class="text-xs font-medium px-2 py-1 rounded-md bg-purple-900/40 text-purple-300 border border-purple-800/30" data-testid="game-publisher">
                                            {game.publisher_name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <a 
                                href={`/game/${game.id}`}
                                class="inline-flex items-center text-sm text-blue-400 hover:text-blue-300 font-medium transition-colors duration-200 group-hover:translate-x-1 transform"
                            >
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2 transform transition-transform duration-300 group-hover:translate-x-1" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>