<style>
	.neon-text-glow {
		text-shadow: 0 0 10px rgba(13, 204, 242, 0.5), 0 0 20px rgba(13, 204, 242, 0.3);
	}
</style>

<div class="relative flex h-screen w-full flex-col justify-between overflow-hidden bg-background-dark">
	<div class="absolute inset-0 pointer-events-none z-0">
		<div class="absolute inset-0 bg-synth-grid bg-[size:40px_40px] opacity-[0.15]"></div>
		<div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] opacity-40"></div>
		<div class="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-background-dark via-background-dark/90 to-transparent"></div>
	</div>

	<div class="relative z-10 w-full px-6 pt-12 pb-4 flex justify-between items-center">
		<a href="/" class="w-10 h-10 flex items-center justify-center rounded-full bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-colors">
			<span class="material-symbols-outlined text-white/70">close</span>
		</a>
		<div class="text-sm font-bold tracking-widest uppercase text-primary/60">Printy App</div>
		<div class="w-10"></div>
	</div>

	<div class="relative z-10 flex-1 flex flex-col items-center justify-center px-6 w-full max-w-md mx-auto">
		<div class="relative mb-8 group">
			<div class="absolute -inset-4 bg-gradient-to-tr from-primary to-neon-purple rounded-full blur-xl opacity-40 group-hover:opacity-60 transition-opacity duration-1000 animate-pulse"></div>
			<div class="relative flex items-center justify-center w-32 h-32 rounded-full bg-background-dark border-2 border-primary shadow-[0_0_30px_rgba(13,204,242,0.3)]">
				<span class="material-symbols-outlined text-6xl text-primary drop-shadow-[0_0_10px_rgba(13,204,242,0.8)]">
					check_circle
				</span>
			</div>
		</div>

		<div class="text-center space-y-4">
			<h1 class="text-white tracking-wide text-4xl font-bold leading-tight px-4 text-center neon-text-glow uppercase">
				Ticket<br/>Transmitted
			</h1>
			<p class="text-gray-300 text-lg font-normal leading-relaxed px-4 text-center max-w-xs mx-auto">
				Your request has been successfully beamed to the print server queue.
			</p>
		</div>
	</div>

	<div class="relative z-10 w-full px-6 pb-10 pt-4 flex flex-col gap-3 max-w-md mx-auto">
		<a href="/" class="w-full cursor-pointer flex items-center justify-center rounded-xl h-14 bg-[#1a2f33]/50 border border-white/10 text-white text-lg font-bold tracking-wide hover:bg-[#1a2f33] transition-colors active:scale-[0.98]">
			Done
        </a>
	</div>
</div>
