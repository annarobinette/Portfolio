# visualisation_functions.py
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(df):
    # Set up the figure
    sns.set_theme(style="white")
    fig = plt.figure(figsize=(15, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.3)
    
    # Download count visualization
    ax1 = fig.add_subplot(gs[0])
    
    # Create bins on a log scale for better distribution visibility
    download_data = df['download_count']
    bins = np.logspace(np.log10(max(1, download_data.min())), 
                      np.log10(download_data.max()), 
                      50)
    
    # Plot histogram with log scale
    ax1.hist(download_data, bins=bins, alpha=0.6, color='#4e79a7')
    ax1.set_xscale('log')
    
    # Add vertical lines for mean and median
    median = df['download_count'].median()
    mean = df['download_count'].mean()
    ymin, ymax = ax1.get_ylim()
    
    ax1.vlines(median, ymin, ymax*0.9, colors='#e15759', linestyles='--', 
               label=f'Median: {median:.0f}')
    ax1.vlines(mean, ymin, ymax*0.9, colors='#59a14f', linestyles='--', 
               label=f'Mean: {mean:.0f}')
    
    # Customize axes
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.set_title('Download Count Distribution (Log Scale)', pad=20, fontsize=11)
    ax1.set_xlabel('Number of Downloads', fontsize=10)
    ax1.set_ylabel('Number of Books', fontsize=10)
    ax1.legend(frameon=False)
    
    # Language distribution
    ax2 = fig.add_subplot(gs[1])
    
    # Calculate language percentages
    languages = df['languages'].str.split('; ').explode()
    lang_counts = languages.value_counts()
    lang_percentages = (lang_counts / lang_counts.sum() * 100).head(8)
    
    # Create horizontal bars
    bars = ax2.barh(
        range(len(lang_percentages)),
        lang_percentages,
        color='#4e79a7',
        alpha=0.6,
        height=0.6
    )
    
    # Remove spines
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Add percentage labels
    for i, (bar, percentage) in enumerate(zip(bars, lang_percentages)):
        ax2.text(
            percentage + 0.3,
            i,
            f'{percentage:.1f}%',
            va='center',
            fontsize=9,
            color='#404040'
        )
    
    # Customize axes
    ax2.set_title('Language Distribution', pad=20, fontsize=11)
    ax2.set_xlabel('Percentage of Collection', fontsize=10)
    ax2.set_yticks(range(len(lang_percentages)))
    ax2.set_yticklabels([lang.upper() for lang in lang_percentages.index], fontsize=9)
    ax2.grid(False)
    
    plt.tight_layout()
    return fig

# Show figures
fig = create_visualizations(df)
plt.show()