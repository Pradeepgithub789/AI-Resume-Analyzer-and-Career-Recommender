import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from typing import Dict, List

# Set seaborn design style
sns.set_theme(style="dark")
plt.rcParams.update({
    'figure.facecolor': '#111216',
    'axes.facecolor': '#111216',
    'text.color': '#F4F5F7',
    'axes.labelcolor': '#8B949E',
    'xtick.color': '#8B949E',
    'ytick.color': '#8B949E',
    'font.family': 'sans-serif',
    'axes.edgecolor': '#21262D',
    'grid.color': '#21262D',
})

def render_premium_card(title: str, content: str, subtitle: str = "", color_theme: str = "indigo") -> str:
    """
    Generate premium glassmorphism styled HTML for Streamlit metrics.
    Themes: 'indigo', 'emerald', 'amber', 'rose', 'cyan'
    """
    themes = {
        "indigo": {
            "border": "rgba(99, 102, 241, 0.4)",
            "bg": "rgba(99, 102, 241, 0.05)",
            "glow": "rgba(99, 102, 241, 0.15)",
            "text": "#818CF8"
        },
        "emerald": {
            "border": "rgba(16, 185, 129, 0.4)",
            "bg": "rgba(16, 185, 129, 0.05)",
            "glow": "rgba(16, 185, 129, 0.15)",
            "text": "#34D399"
        },
        "amber": {
            "border": "rgba(245, 158, 11, 0.4)",
            "bg": "rgba(245, 158, 11, 0.05)",
            "glow": "rgba(245, 158, 11, 0.15)",
            "text": "#FBBF24"
        },
        "rose": {
            "border": "rgba(244, 63, 94, 0.4)",
            "bg": "rgba(244, 63, 94, 0.05)",
            "glow": "rgba(244, 63, 94, 0.15)",
            "text": "#FB7185"
        },
        "cyan": {
            "border": "rgba(6, 182, 212, 0.4)",
            "bg": "rgba(6, 182, 212, 0.05)",
            "glow": "rgba(6, 182, 212, 0.15)",
            "text": "#22D3EE"
        }
    }
    
    t = themes.get(color_theme, themes["indigo"])
    
    card_html = f"""
    <div style="
        background: {t['bg']};
        border: 1px solid {t['border']};
        box-shadow: 0 8px 32px 0 {t['glow']};
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 0.85rem; font-weight: 500; color: #8B949E; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">
            {title}
        </div>
        <div style="font-size: 2.2rem; font-weight: 700; color: {t['text']}; margin-bottom: 4px; line-height: 1.2;">
            {content}
        </div>
        <div style="font-size: 0.8rem; color: #8B949E;">
            {subtitle}
        </div>
    </div>
    """
    return card_html

def plot_skill_distribution(skills_by_category: Dict[str, List[str]]):
    """
    Create a highly styled horizontal bar chart of skills per category.
    """
    categories = list(skills_by_category.keys())
    counts = [len(skills) for skills in skills_by_category.values()]
    
    # Sort together
    sorted_data = sorted(zip(categories, counts), key=lambda x: x[1])
    categories, counts = zip(*sorted_data)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Beautiful purple-indigo gradient colors
    colors = sns.color_palette("viridis", len(categories))
    
    bars = ax.barh(categories, counts, color=colors, height=0.65, edgecolor='#111216', linewidth=1)
    
    # Grid styling
    ax.grid(axis='x', linestyle='--', alpha=0.15, color='#8B949E')
    ax.set_axisbelow(True)
    
    # Spine cleanups
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#21262D')
    ax.spines['bottom'].set_color('#21262D')
    
    # Labels
    ax.set_xlabel('Number of Extracted Skills', fontsize=10, labelpad=10)
    ax.set_title('Extracted Skill Distribution By Category', fontsize=12, pad=15, fontweight='bold', color='#F4F5F7')
    
    # Value labels inside/outside bars
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(
                width + 0.15, 
                bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', 
                ha='left', 
                va='center', 
                fontsize=9, 
                fontweight='bold', 
                color='#F4F5F7'
            )
            
    plt.tight_layout()
    return fig

def render_radial_gauge(percentage: float, title: str, subtitle: str = "") -> str:
    """
    Draw a dynamic, responsive pure-CSS circular progress gauge with premium UI gradients.
    """
    # Choose color based on percentage
    if percentage >= 80:
        color = "#10B981" # Emerald
        bg_glow = "rgba(16, 185, 129, 0.1)"
    elif percentage >= 60:
        color = "#3B82F6" # Blue
        bg_glow = "rgba(59, 130, 246, 0.1)"
    elif percentage >= 40:
        color = "#F59E0B" # Amber
        bg_glow = "rgba(245, 158, 11, 0.1)"
    else:
        color = "#EF4444" # Red
        bg_glow = "rgba(239, 68, 68, 0.1)"
        
    gauge_html = f"""
    <div style="
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 {bg_glow};
        border-radius: 16px;
        padding: 30px;
        margin: 15px 0;
    ">
        <h4 style="color: #8B949E; margin: 0 0 20px 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">{title}</h4>
        
        <!-- SVG Gauge -->
        <svg width="180" height="180" viewBox="0 0 180 180" style="transform: rotate(-90deg);">
            <!-- Background circle -->
            <circle cx="90" cy="90" r="70" stroke="rgba(255, 255, 255, 0.05)" stroke-width="12" fill="transparent" />
            <!-- Active indicator -->
            <circle cx="90" cy="90" r="70" 
                stroke="{color}" 
                stroke-width="12" 
                fill="transparent" 
                stroke-dasharray="439.8" 
                stroke-dashoffset="{439.8 - (439.8 * percentage / 100)}"
                stroke-linecap="round"
                style="transition: stroke-dashoffset 1s ease-out;"
            />
        </svg>
        
        <!-- Percentage display overlapping -->
        <div style="
            position: absolute; 
            margin-top: 25px; 
            font-size: 2.2rem; 
            font-weight: 800; 
            color: #F4F5F7;
        ">
            {percentage}%
        </div>
        
        <div style="margin-top: 15px; font-size: 0.85rem; font-weight: 500; color: #8B949E; text-align: center;">
            {subtitle}
        </div>
    </div>
    """
    return gauge_html

def inject_premium_css():
    """
    Inject custom styles into the Streamlit app to hide default layout issues,
    beautify cards, and set high-end margins.
    """
    st.markdown("""
        <style>
            /* Custom CSS injection for glowing buttons and hover transitions */
            div.stButton > button {
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 24px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease-out !important;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
            }
            div.stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
                background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
            }
            
            /* Metric overrides */
            [data-testid="stMetricValue"] {
                font-size: 2.2rem !important;
                font-weight: 700 !important;
                color: #6366F1 !important;
            }
            
            /* Sidebar beauty */
            section[data-testid="stSidebar"] {
                background-color: #0d0e12 !important;
                border-right: 1px solid #21262D !important;
            }
            
            /* Card panels */
            div[data-testid="stExpander"] {
                background-color: rgba(255, 255, 255, 0.02) !important;
                border: 1px solid #21262D !important;
                border-radius: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)
