import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
import time
import random

warnings.filterwarnings('ignore')

# ============================================================================
# 1. KONFIGURASI APLIKASI STREAMLIT
# ============================================================================
st.set_page_config(
    page_title="Simulasi Monte Carlo - Pembangunan Gedung FITE",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling dengan Animasi
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        font-weight: bold;
    }
    .info-box {
        background-color: #F0F8FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stage-card {
        background-color: #F8FAFC;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 4px solid #10B981;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* ANIMASI BALON */
    @keyframes float-balloon {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    @keyframes sway-balloon {
        0%, 100% { margin-left: 0; }
        50% { margin-left: 50px; }
    }
    .balloon {
        position: fixed;
        font-size: 3rem;
        animation: float-balloon 8s linear infinite, sway-balloon 3s ease-in-out infinite;
        z-index: 9999;
        pointer-events: none;
    }
    
    /* ANIMASI PESAWAT */
    @keyframes fly-plane {
        0% { transform: translateX(-100vw) translateY(20vh) rotate(5deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateX(100vw) translateY(30vh) rotate(-5deg); opacity: 0; }
    }
    .plane {
        position: fixed;
        font-size: 4rem;
        animation: fly-plane 6s linear infinite;
        z-index: 9998;
        pointer-events: none;
    }
    
    /* ANIMASI SUPERMAN */
    @keyframes fly-superman {
        0% { transform: translate(-100vw, 50vh) scale(0.5); opacity: 0; }
        20% { opacity: 1; transform: translate(-50vw, 40vh) scale(1); }
        50% { transform: translate(0vw, 30vh) scale(1.2); }
        80% { transform: translate(50vw, 40vh) scale(1); }
        100% { transform: translate(100vw, 50vh) scale(0.5); opacity: 0; }
    }
    .superman {
        position: fixed;
        font-size: 5rem;
        animation: fly-superman 5s ease-in-out infinite;
        z-index: 9997;
        pointer-events: none;
        filter: drop-shadow(0 0 10px blue);
    }
    
    /* ANIMASI BATMAN & JOKER */
    @keyframes chase-batman {
        0% { transform: translateX(-100vw); opacity: 0; }
        10% { opacity: 1; }
        45% { transform: translateX(40vw); }
        50% { transform: translateX(45vw); }
        55% { transform: translateX(40vw); }
        90% { opacity: 1; }
        100% { transform: translateX(100vw); opacity: 0; }
    }
    @keyframes chase-joker {
        0% { transform: translateX(-100vw); opacity: 0; }
        10% { opacity: 1; }
        40% { transform: translateX(35vw); }
        45% { transform: translateX(40vw); }
        50% { transform: translateX(35vw); }
        90% { opacity: 1; }
        100% { transform: translateX(100vw); opacity: 0; }
    }
    .batman {
        position: fixed;
        font-size: 4.5rem;
        animation: chase-batman 7s linear infinite;
        z-index: 9996;
        pointer-events: none;
        top: 60vh;
    }
    .joker {
        position: fixed;
        font-size: 4.5rem;
        animation: chase-joker 7s linear infinite;
        z-index: 9995;
        pointer-events: none;
        top: 60vh;
        margin-left: 150px;
    }
    
    /* JUMPSCARE MODAL */
    @keyframes scare-flash {
        0%, 100% { background-color: transparent; }
        50% { background-color: red; }
    }
    @keyframes scare-shake {
        0%, 100% { transform: translate(0, 0); }
        25% { transform: translate(-10px, 10px); }
        50% { transform: translate(10px, -10px); }
        75% { transform: translate(-10px, -10px); }
    }
    .jumpscare-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: radial-gradient(circle, red 0%, black 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        animation: scare-flash 0.5s ease-in-out;
    }
    .jumpscare-face {
        font-size: 15rem;
        animation: scare-shake 0.3s ease-in-out infinite;
        filter: drop-shadow(0 0 30px red);
    }
    .jumpscare-text {
        position: absolute;
        bottom: 20%;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 0 0 20px red;
        animation: scare-shake 0.2s ease-in-out infinite;
    }
    
    /* PROGRESS BAR ANIMATION */
    @keyframes pulse-progress {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .progress-container {
        animation: pulse-progress 1s ease-in-out infinite;
    }
    
    /* HIDE ANIMATIONS BY DEFAULT */
    .animation-container {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9990;
    }
    .animation-container.active {
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. KELAS PEMODELAN SISTEM - KONSTRUKSI GEDUNG FITE
# ============================================================================
class ConstructionStage:
    """Kelas untuk memodelkan tahapan konstruksi gedung dengan faktor risiko"""
    
    def __init__(self, name, base_params, risk_factors=None, dependencies=None):
        self.name = name
        self.optimistic = float(base_params['optimistic'])
        self.most_likely = float(base_params['most_likely'])
        self.pessimistic = float(base_params['pessimistic'])
        self.risk_factors = risk_factors or {}
        self.dependencies = dependencies or []
        
    def sample_duration(self, n_simulations, risk_multiplier=1.0):
        """Sampling durasi dengan mempertimbangkan distribusi dan faktor risiko"""
        # Distribusi triangular untuk estimasi tiga titik
        base_duration = np.random.triangular(
            self.optimistic,
            self.most_likely,
            self.pessimistic,
            n_simulations
        )
        
        # Aplikasi faktor risiko
        for risk_name, risk_params in self.risk_factors.items():
            if risk_params['type'] == 'discrete':
                probability = float(risk_params['probability'])
                impact = float(risk_params['impact'])
                
                risk_occurs = np.random.random(n_simulations) < probability
                
                base_duration = np.where(
                    risk_occurs,
                    base_duration * (1 + impact),
                    base_duration
                )
                
            elif risk_params['type'] == 'continuous':
                mean = float(risk_params['mean'])
                std = float(risk_params['std'])
                
                productivity_factor = np.random.normal(mean, std, n_simulations)
                base_duration = base_duration / np.clip(productivity_factor, 0.5, 1.5)
        
        return base_duration * risk_multiplier


class MonteCarloConstructionSimulation:
    """Kelas untuk menjalankan simulasi Monte Carlo proyek konstruksi"""
    
    def __init__(self, stages_config, num_simulations=10000):
        self.stages_config = stages_config
        self.num_simulations = num_simulations
        self.stages = {}
        self.simulation_results = None
        self.initialize_stages()
        
    def initialize_stages(self):
        """Inisialisasi objek tahapan dari konfigurasi"""
        for stage_name, config in self.stages_config.items():
            self.stages[stage_name] = ConstructionStage(
                name=stage_name,
                base_params=config['base_params'],
                risk_factors=config.get('risk_factors', {}),
                dependencies=config.get('dependencies', [])
            )
    
    def run_simulation(self):
        """Menjalankan simulasi Monte Carlo lengkap"""
        results = pd.DataFrame(index=range(self.num_simulations))
        
        # Simulasi durasi per tahapan
        for stage_name, stage in self.stages.items():
            results[stage_name] = stage.sample_duration(self.num_simulations)
        
        # Simulasi ketergantungan antar tahapan
        start_times = pd.DataFrame(index=range(self.num_simulations))
        end_times = pd.DataFrame(index=range(self.num_simulations))
        
        for stage_name in self.stages.keys():
            deps = self.stages[stage_name].dependencies
            
            if not deps:
                start_times[stage_name] = 0
            else:
                start_times[stage_name] = end_times[deps].max(axis=1)
            
            end_times[stage_name] = start_times[stage_name] + results[stage_name]
        
        # Hitung durasi total proyek
        results['Total_Duration'] = end_times.max(axis=1)
        
        # Simpan juga waktu selesai per tahapan
        for stage_name in self.stages.keys():
            results[f'{stage_name}_Finish'] = end_times[stage_name]
            results[f'{stage_name}_Start'] = start_times[stage_name]
        
        self.simulation_results = results
        return results
    
    def calculate_critical_path_probability(self):
        """Menghitung probabilitas setiap tahapan berada di critical path"""
        if self.simulation_results is None:
            raise ValueError("Run simulation first")
        
        critical_path_probs = {}
        total_duration = self.simulation_results['Total_Duration']
        
        for stage_name in self.stages.keys():
            stage_finish = self.simulation_results[f'{stage_name}_Finish']
            correlation = self.simulation_results[stage_name].corr(total_duration)
            
            is_critical = (stage_finish + 0.1) >= total_duration
            prob_critical = np.mean(is_critical)
            
            critical_path_probs[stage_name] = {
                'probability': prob_critical,
                'correlation': correlation,
                'avg_duration': self.simulation_results[stage_name].mean()
            }
        
        return pd.DataFrame(critical_path_probs).T
    
    def analyze_risk_contribution(self):
        """Analisis kontribusi risiko terhadap variabilitas total durasi"""
        if self.simulation_results is None:
            raise ValueError("Run simulation first")
        
        total_var = self.simulation_results['Total_Duration'].var()
        contributions = {}
        
        for stage_name in self.stages.keys():
            stage_var = self.simulation_results[stage_name].var()
            stage_covar = self.simulation_results[stage_name].cov(
                self.simulation_results['Total_Duration']
            )
            
            contribution = (stage_covar / total_var) * 100
            
            contributions[stage_name] = {
                'variance': stage_var,
                'contribution_percent': contribution,
                'std_dev': np.sqrt(stage_var)
            }
        
        return pd.DataFrame(contributions).T


# ============================================================================
# 3. FUNGSI VISUALISASI PLOTLY
# ============================================================================
def create_distribution_plot(results):
    """Membuat plot distribusi durasi total proyek"""
    total_duration = results['Total_Duration']
    mean_duration = total_duration.mean()
    median_duration = np.median(total_duration)
    
    fig = go.Figure()
    
    # Histogram
    fig.add_trace(go.Histogram(
        x=total_duration,
        nbinsx=50,
        name='Distribusi Durasi',
        marker_color='skyblue',
        opacity=0.7,
        histnorm='probability density'
    ))
    
    # Garis mean dan median
    fig.add_vline(x=mean_duration, line_dash="dash", line_color="red",
                  annotation_text=f"Mean: {mean_duration:.1f} bulan")
    fig.add_vline(x=median_duration, line_dash="dash", line_color="green",
                  annotation_text=f"Median: {median_duration:.1f} bulan")
    
    # Confidence intervals
    ci_80 = np.percentile(total_duration, [10, 90])
    ci_95 = np.percentile(total_duration, [2.5, 97.5])
    
    fig.add_vrect(x0=ci_80[0], x1=ci_80[1], fillcolor="yellow", opacity=0.2,
                  annotation_text="80% CI", line_width=0)
    fig.add_vrect(x0=ci_95[0], x1=ci_95[1], fillcolor="orange", opacity=0.1,
                  annotation_text="95% CI", line_width=0)
    
    fig.update_layout(
        title='📊 Distribusi Durasi Total Proyek',
        xaxis_title='Durasi Total Proyek (Bulan)',
        yaxis_title='Densitas Probabilitas',
        showlegend=True,
        height=500,
        template='plotly_white'
    )
    
    return fig, {
        'mean': mean_duration,
        'median': median_duration,
        'std': total_duration.std(),
        'min': total_duration.min(),
        'max': total_duration.max(),
        'ci_80': ci_80,
        'ci_95': ci_95
    }


def create_completion_probability_plot(results):
    """Membuat plot probabilitas penyelesaian proyek"""
    deadlines = np.arange(12, 30, 1)  # 12-30 bulan
    completion_probs = []
    
    for deadline in deadlines:
        prob = np.mean(results['Total_Duration'] <= deadline)
        completion_probs.append(prob)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=deadlines,
        y=completion_probs,
        mode='lines',
        name='Probabilitas Selesai',
        line=dict(color='darkblue', width=3),
        fill='tozeroy',
        fillcolor='rgba(173, 216, 230, 0.3)'
    ))
    
    # Garis referensi probabilitas
    fig.add_hline(y=0.5, line_dash="dash", line_color="red",
                  annotation_text="50%", annotation_position="right")
    fig.add_hline(y=0.8, line_dash="dash", line_color="green",
                  annotation_text="80%", annotation_position="right")
    fig.add_hline(y=0.95, line_dash="dash", line_color="blue",
                  annotation_text="95%", annotation_position="right")
    
    # Tandai deadline penting
    key_deadlines = [16, 20, 24]
    for dl in key_deadlines:
        idx = np.where(deadlines == dl)[0]
        if len(idx) > 0:
            prob = completion_probs[idx[0]]
            fig.add_trace(go.Scatter(
                x=[dl], y=[prob],
                mode='markers+text',
                marker=dict(size=15, color='red'),
                text=[f'{prob:.1%}'],
                textposition="top center",
                showlegend=False
            ))
    
    fig.update_layout(
        title='🎯 Kurva Probabilitas Penyelesaian Proyek',
        xaxis_title='Deadline (Bulan)',
        yaxis_title='Probabilitas Selesai Tepat Waktu',
        yaxis_range=[-0.05, 1.05],
        xaxis_range=[12, 30],
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_critical_path_plot(critical_analysis):
    """Membuat plot analisis critical path"""
    critical_analysis = critical_analysis.sort_values('probability', ascending=True)
    
    colors = ['red' if prob > 0.7 else 'lightcoral' for prob in critical_analysis['probability']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=[stage.replace('_', ' ') for stage in critical_analysis.index],
        x=critical_analysis['probability'],
        orientation='h',
        marker_color=colors,
        text=[f'{prob:.1%}' for prob in critical_analysis['probability']],
        textposition='auto'
    ))
    
    fig.add_vline(x=0.5, line_dash="dot", line_color="gray")
    fig.add_vline(x=0.7, line_dash="dot", line_color="orange")
    
    fig.update_layout(
        title='🔍 Analisis Critical Path per Tahapan',
        xaxis_title='Probabilitas Menjadi Critical Path',
        xaxis_range=[0, 1.0],
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_stage_boxplot(results, stages):
    """Membuat boxplot distribusi durasi per tahapan"""
    stage_names = list(stages.keys())
    
    fig = go.Figure()
    
    for i, stage_name in enumerate(stage_names):
        data = results[stage_name]
        
        fig.add_trace(go.Box(
            y=data,
            name=stage_name.replace('_', '\n'),
            boxmean='sd',
            marker_color=px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)],
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8
        ))
    
    fig.update_layout(
        title='📦 Distribusi Durasi per Tahapan',
        yaxis_title='Durasi (Bulan)',
        height=500,
        showlegend=False,
        template='plotly_white'
    )
    
    return fig


def create_risk_contribution_plot(risk_contrib):
    """Membuat plot kontribusi risiko per tahapan"""
    risk_contrib = risk_contrib.sort_values('contribution_percent', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[name.replace('_', '\n') for name in risk_contrib.index],
        y=risk_contrib['contribution_percent'],
        marker_color=px.colors.qualitative.Set3,
        text=[f'{contrib:.1f}%' for contrib in risk_contrib['contribution_percent']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='⚠️ Kontribusi Risiko per Tahapan',
        yaxis_title='Kontribusi terhadap Variabilitas (%)',
        height=400,
        template='plotly_white'
    )
    
    return fig


def create_correlation_heatmap(results, stages):
    """Membuat heatmap korelasi antar tahapan"""
    correlation_matrix = results[list(stages.keys())].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=[name.replace('_', '\n') for name in correlation_matrix.columns],
        y=[name.replace('_', '\n') for name in correlation_matrix.index],
        colorscale='RdBu',
        zmid=0,
        text=np.round(correlation_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='📊 Matriks Korelasi Antar Tahapan',
        height=500,
        template='plotly_white'
    )
    
    return fig


# ============================================================================
# 4. KOMPONEN ANIMASI
# ============================================================================
def create_animation_container():
    """Membuat container untuk animasi"""
    return """
    <div class="animation-container" id="animationContainer">
        <div class="balloon" style="left: 10%; animation-delay: 0s;">🎈</div>
        <div class="balloon" style="left: 20%; animation-delay: 1s;">🎈</div>
        <div class="balloon" style="left: 30%; animation-delay: 2s;">🎈</div>
        <div class="balloon" style="left: 40%; animation-delay: 0.5s;">🎈</div>
        <div class="balloon" style="left: 50%; animation-delay: 1.5s;">🎈</div>
        <div class="balloon" style="left: 60%; animation-delay: 2.5s;">🎈</div>
        <div class="balloon" style="left: 70%; animation-delay: 0.8s;">🎈</div>
        <div class="balloon" style="left: 80%; animation-delay: 1.8s;">🎈</div>
        <div class="balloon" style="left: 90%; animation-delay: 2.2s;">🎈</div>
        
        <div class="plane">✈️</div>
        
        <div class="superman">🦸</div>
        
        <div class="batman">🦇</div>
        <div class="joker">🤡</div>
    </div>
    """


def create_jumpscare_modal():
    """Membuat modal jumpscare"""
    funny_faces = ['🤪', '😜', '🤡', '👻', '😱', '🤯']
    face = random.choice(funny_faces)
    
    return f"""
    <div class="jumpscare-overlay" id="jumpscareModal" style="display: none;">
        <div class="jumpscare-face">{face}</div>
        <div class="jumpscare-text">🎉 SIMULASI SELESAI! 🎉</div>
    </div>
    
    <script>
        function showJumpscare() {{
            const modal = document.getElementById('jumpscareModal');
            modal.style.display = 'flex';
            setTimeout(() => {{
                modal.style.display = 'none';
            }}, 1500);
        }}
        
        function showAnimations() {{
            const container = document.getElementById('animationContainer');
            if (container) {{
                container.classList.add('active');
                setTimeout(() => {{
                    container.classList.remove('active');
                }}, 8000);
            }}
        }}
    </script>
    """


# ============================================================================
# 5. KONFIGURASI TAHAPAN PROYEK FITE
# ============================================================================
def get_fite_construction_config():
    """Konfigurasi tahapan pembangunan gedung FITE"""
    return {
        "Persiapan_Lahan": {
            "base_params": {"optimistic": 1.0, "most_likely": 2.0, "pessimistic": 3.0},
            "risk_factors": {
                "kondisi_tanah": {
                    "type": "discrete",
                    "probability": 0.3,
                    "impact": 0.4
                },
                "izin_pembangunan": {
                    "type": "discrete",
                    "probability": 0.2,
                    "impact": 0.3
                }
            }
        },
        "Pondasi_Dasar": {
            "base_params": {"optimistic": 2.0, "most_likely": 3.0, "pessimistic": 5.0},
            "risk_factors": {
                "cuaca_buruk": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.3
                },
                "keterlambatan_material": {
                    "type": "discrete",
                    "probability": 0.25,
                    "impact": 0.2
                }
            },
            "dependencies": ["Persiapan_Lahan"]
        },
        "Struktur_Lantai_1_2": {
            "base_params": {"optimistic": 3.0, "most_likely": 4.0, "pessimistic": 6.0},
            "risk_factors": {
                "produktivitas_pekerja": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.25
                },
                "ketersediaan_alat_berat": {
                    "type": "discrete",
                    "probability": 0.15,
                    "impact": 0.3
                }
            },
            "dependencies": ["Pondasi_Dasar"]
        },
        "Struktur_Lantai_3_4": {
            "base_params": {"optimistic": 3.0, "most_likely": 4.0, "pessimistic": 6.0},
            "risk_factors": {
                "produktivitas_pekerja": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.25
                },
                "cuaca_buruk": {
                    "type": "discrete",
                    "probability": 0.2,
                    "impact": 0.25
                }
            },
            "dependencies": ["Struktur_Lantai_1_2"]
        },
        "Struktur_Lantai_5": {
            "base_params": {"optimistic": 2.0, "most_likely": 3.0, "pessimistic": 5.0},
            "risk_factors": {
                "keselamatan_kerja": {
                    "type": "discrete",
                    "probability": 0.1,
                    "impact": 0.4
                },
                "produktivitas_pekerja": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.25
                }
            },
            "dependencies": ["Struktur_Lantai_3_4"]
        },
        "Instalasi_Listrik_Dan_Air": {
            "base_params": {"optimistic": 2.0, "most_likely": 3.0, "pessimistic": 5.0},
            "risk_factors": {
                "perubahan_desain": {
                    "type": "discrete",
                    "probability": 0.3,
                    "impact": 0.35
                },
                "ketersediaan_teknisi": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.2
                }
            },
            "dependencies": ["Struktur_Lantai_5"]
        },
        "Pembangunan_Laboratorium": {
            "base_params": {"optimistic": 3.0, "most_likely": 5.0, "pessimistic": 8.0},
            "risk_factors": {
                "peralatan_khusus": {
                    "type": "discrete",
                    "probability": 0.35,
                    "impact": 0.4
                },
                "spesifikasi_teknis": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.3
                },
                "impor_peralatan": {
                    "type": "discrete",
                    "probability": 0.2,
                    "impact": 0.5
                }
            },
            "dependencies": ["Instalasi_Listrik_Dan_Air"]
        },
        "Finishing_Dan_Interior": {
            "base_params": {"optimistic": 2.0, "most_likely": 3.0, "pessimistic": 5.0},
            "risk_factors": {
                "kualitas_material": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.2
                },
                "perubahan_desain_interior": {
                    "type": "discrete",
                    "probability": 0.25,
                    "impact": 0.3
                }
            },
            "dependencies": ["Pembangunan_Laboratorium"]
        },
        "Pengujian_Sistem": {
            "base_params": {"optimistic": 1.0, "most_likely": 2.0, "pessimistic": 3.0},
            "risk_factors": {
                "bug_sistem": {
                    "type": "discrete",
                    "probability": 0.3,
                    "impact": 0.5
                },
                "ketersediaan_penguji": {
                    "type": "continuous",
                    "mean": 1.0,
                    "std": 0.25
                }
            },
            "dependencies": ["Finishing_Dan_Interior"]
        },
        "Serah_Terima": {
            "base_params": {"optimistic": 0.5, "most_likely": 1.0, "pessimistic": 2.0},
            "risk_factors": {
                "dokumentasi": {
                    "type": "discrete",
                    "probability": 0.2,
                    "impact": 0.4
                }
            },
            "dependencies": ["Pengujian_Sistem"]
        }
    }


# ============================================================================
# 6. FUNGSI UTAMA STREAMLIT
# ============================================================================
def main():
    # Header aplikasi
    st.markdown('<h1 class="main-header">🏗️ Simulasi Monte Carlo - Pembangunan Gedung FITE</h1>', 
                unsafe_allow_html=True)
    
    # Deskripsi
    st.markdown("""
    <div class="info-box">
    <b>📋 Deskripsi Proyek:</b> Pembangunan gedung Fakultas Informatika & Teknik Elektro (FITE) 
    5 lantai dengan fasilitas lengkap termasuk ruang kelas, laboratorium komputer, laboratorium elektro, 
    laboratorium mobile, laboratorium VR/AR, laboratorium game, ruang dosen, toilet, dan ruang serbaguna.
    <br><br>
    <b>🎯 Tujuan Simulasi:</b> Memodelkan ketidakpastian durasi konstruksi dan menghasilkan estimasi 
    waktu penyelesaian yang lebih akurat dengan mempertimbangkan berbagai faktor risiko.
    </div>
    """, unsafe_allow_html=True)
    
    # Tambahkan komponen animasi
    st.markdown(create_animation_container(), unsafe_allow_html=True)
    st.markdown(create_jumpscare_modal(), unsafe_allow_html=True)
    
    # Sidebar untuk konfigurasi
    st.sidebar.markdown('<h2>⚙️ Konfigurasi Simulasi</h2>', unsafe_allow_html=True)
    
    # Slider untuk jumlah simulasi - SEMUA INT (konsisten)
    num_simulations = int(st.sidebar.slider(
        'Jumlah Iterasi Simulasi:',
        min_value=5000,
        max_value=50000,
        value=20000,
        step=5000,
        help='Semakin banyak iterasi, semakin akurat hasilnya tetapi lebih lama waktu prosesnya'
    ))
    
    # Konfigurasi seed untuk reproducibility
    np.random.seed(42)
    
    st.sidebar.markdown('<h3>📋 Konfigurasi Tahapan Proyek</h3>', unsafe_allow_html=True)
    
    # Konfigurasi default
    default_config = get_fite_construction_config()
    
    # Menampilkan konfigurasi tahapan di sidebar - DIPERBAIKI: SEMUA FLOAT (konsisten)
    for stage_name, config in default_config.items():
        with st.sidebar.expander(f"⚙️ {stage_name.replace('_', ' ')}", expanded=False):
            # SEMUA PARAMETER HARUS FLOAT (konsisten) - INI PERBAIKAN ERROR
            optimistic = float(st.number_input(
                f"Optimistic (bulan)",
                min_value=0.5,      # float
                max_value=20.0,     # float
                value=float(config['base_params']['optimistic']),  # float
                step=0.5,           # float
                key=f"opt_{stage_name}"
            ))
            
            most_likely = float(st.number_input(
                f"Most Likely (bulan)",
                min_value=0.5,      # float
                max_value=20.0,     # float
                value=float(config['base_params']['most_likely']),  # float
                step=0.5,           # float
                key=f"ml_{stage_name}"
            ))
            
            pessimistic = float(st.number_input(
                f"Pessimistic (bulan)",
                min_value=0.5,      # float
                max_value=20.0,     # float
                value=float(config['base_params']['pessimistic']),  # float
                step=0.5,           # float
                key=f"pes_{stage_name}"
            ))
            
            # Update config dengan tipe float
            default_config[stage_name]['base_params'] = {
                'optimistic': optimistic,
                'most_likely': most_likely,
                'pessimistic': pessimistic
            }
    
    # Tombol untuk menjalankan
    run_simulation = st.sidebar.button("🚀 JALANKAN SIMULASI", type="primary", use_container_width=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-size: 0.8rem; color: #666;">
    <b>Keterangan:</b><br>
    • Optimistic: Estimasi terbaik (tanpa hambatan)<br>
    • Most Likely: Estimasi realistis (kondisi normal)<br>
    • Pessimistic: Estimasi terburuk (banyak hambatan)<br>
    • CI: Confidence Interval (Tingkat Kepercayaan)
    </div>
    """, unsafe_allow_html=True)
    
    # Inisialisasi session state
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None
    if 'simulator' not in st.session_state:
        st.session_state.simulator = None
    if 'simulation_complete' not in st.session_state:
        st.session_state.simulation_complete = False
    
    # Jalankan simulasi ketika tombol ditekan
    if run_simulation:
        # Tampilkan progress bar dengan animasi
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        # Tampilkan animasi
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3>🎬 Animasi Dimulai...</h3>
            <p>🎈 🎈 🎈</p>
            <p>✈️ Pesawat sedang terbang...</p>
            <p>🦸 Superman sedang patroli...</p>
            <p>🦇 Batman mengejar Joker...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Script untuk menjalankan animasi
        st.markdown("""
        <script>
            showAnimations();
        </script>
        """, unsafe_allow_html=True)
        
        with st.spinner('🏗️ Menjalankan simulasi Monte Carlo... Harap tunggu...'):
            # Simulasi progress
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
                status_text.text(f'Proses simulasi: {i + 1}%')
            
            # Inisialisasi simulator
            simulator = MonteCarloConstructionSimulation(
                stages_config=default_config,
                num_simulations=num_simulations
            )
            
            # Jalankan simulasi
            results = simulator.run_simulation()
            
            # Simpan ke session state
            st.session_state.simulation_results = results
            st.session_state.simulator = simulator
            st.session_state.simulation_complete = True
            
            st.sidebar.success(f'✅ Simulasi selesai! {num_simulations:,} iterasi berhasil dijalankan.')
            
            # Trigger jumpscare
            st.markdown("""
            <script>
                setTimeout(() => {
                    showJumpscare();
                }, 500);
            </script>
            """, unsafe_allow_html=True)
    
    # Tampilkan hasil jika simulasi sudah dijalankan
    if st.session_state.simulation_results is not None:
        results = st.session_state.simulation_results
        simulator = st.session_state.simulator
        
        # ====================================================================
        # BAGIAN 1: STATISTIK UTAMA
        # ====================================================================
        st.markdown('<h2 class="sub-header">📈 Statistik Utama Proyek</h2>', unsafe_allow_html=True)
        
        # Metrik utama
        total_duration = results['Total_Duration']
        mean_duration = total_duration.mean()
        median_duration = np.median(total_duration)
        ci_80 = np.percentile(total_duration, [10, 90])
        ci_95 = np.percentile(total_duration, [2.5, 97.5])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{mean_duration:.1f}</h3>
                <p>Rata-rata Durasi (Bulan)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{median_duration:.1f}</h3>
                <p>Median Durasi (Bulan)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{ci_80[0]:.1f} - {ci_80[1]:.1f}</h3>
                <p>80% Confidence Interval</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{ci_95[0]:.1f} - {ci_95[1]:.1f}</h3>
                <p>95% Confidence Interval</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ====================================================================
        # BAGIAN 2: VISUALISASI UTAMA
        # ====================================================================
        st.markdown('<h2 class="sub-header">📊 Visualisasi Hasil Simulasi</h2>', unsafe_allow_html=True)
        
        # Tab untuk visualisasi
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Distribusi Durasi", 
            "🎯 Probabilitas Penyelesaian", 
            "🔍 Analisis Tahapan", 
            "📊 Analisis Risiko"
        ])
        
        with tab1:
            # Plot distribusi durasi
            fig_dist, stats = create_distribution_plot(results)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Tampilkan statistik detail
            with st.expander("📋 Detail Statistik Distribusi"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Statistik Deskriptif:**")
                    st.write(f"- Rata-rata: {stats['mean']:.1f} bulan")
                    st.write(f"- Median: {stats['median']:.1f} bulan")
                    st.write(f"- Standar Deviasi: {stats['std']:.1f} bulan")
                    st.write(f"- Minimum: {stats['min']:.1f} bulan")
                    st.write(f"- Maximum: {stats['max']:.1f} bulan")
                
                with col2:
                    st.write("**Confidence Intervals:**")
                    st.write(f"- 80% CI: [{stats['ci_80'][0]:.1f}, {stats['ci_80'][1]:.1f}] bulan")
                    st.write(f"- 95% CI: [{stats['ci_95'][0]:.1f}, {stats['ci_95'][1]:.1f}] bulan")
        
        with tab2:
            # Plot probabilitas penyelesaian
            fig_prob = create_completion_probability_plot(results)
            st.plotly_chart(fig_prob, use_container_width=True)
            
            # Analisis probabilitas deadline
            with st.expander("📅 Analisis Probabilitas Deadline"):
                deadlines = [16, 18, 20, 22, 24]
                cols = st.columns(len(deadlines))
                
                for i, deadline in enumerate(deadlines):
                    prob_on_time = np.mean(total_duration <= deadline)
                    prob_late = 1 - prob_on_time
                    
                    with cols[i]:
                        st.metric(
                            label=f"Deadline {deadline} bulan",
                            value=f"{prob_on_time:.1%}",
                            delta=f"{prob_late:.1%} terlambat" if prob_late > 0 else "Tepat waktu",
                            delta_color="inverse"
                        )
        
        with tab3:
            # Plot critical path dan boxplot
            col1, col2 = st.columns(2)
            
            with col1:
                # Critical path analysis
                critical_analysis = simulator.calculate_critical_path_probability()
                fig_critical = create_critical_path_plot(critical_analysis)
                st.plotly_chart(fig_critical, use_container_width=True)
            
            with col2:
                # Boxplot durasi per tahapan
                fig_boxplot = create_stage_boxplot(results, simulator.stages)
                st.plotly_chart(fig_boxplot, use_container_width=True)
            
            # Detail tahapan kritis
            with st.expander("🔍 Detail Analisis Critical Path"):
                critical_df = critical_analysis.sort_values('probability', ascending=False)
                st.dataframe(critical_df, use_container_width=True)
        
        with tab4:
            # Analisis risiko
            col1, col2 = st.columns(2)
            
            with col1:
                # Kontribusi risiko
                risk_contrib = simulator.analyze_risk_contribution()
                fig_risk = create_risk_contribution_plot(risk_contrib)
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with col2:
                # Heatmap korelasi
                fig_corr = create_correlation_heatmap(results, simulator.stages)
                st.plotly_chart(fig_corr, use_container_width=True)
            
            # Detail analisis risiko
            with st.expander("📋 Detail Analisis Kontribusi Risiko"):
                st.dataframe(risk_contrib, use_container_width=True)
        
        # ====================================================================
        # BAGIAN 3: ANALISIS STATISTIK LENGKAP
        # ====================================================================
        st.markdown('<h2 class="sub-header">📋 Analisis Statistik Lengkap</h2>', unsafe_allow_html=True)
        
        with st.expander("📊 Tabel Data Simulasi", expanded=False):
            st.dataframe(results.head(100), use_container_width=True)
        
        # Statistik per tahapan
        st.markdown("**Statistik Durasi per Tahapan:**")
        stage_stats = pd.DataFrame()
        for stage_name in simulator.stages.keys():
            stage_data = results[stage_name]
            stage_stats[stage_name] = [
                stage_data.mean(),
                stage_data.std(),
                np.percentile(stage_data, 25),
                np.percentile(stage_data, 50),
                np.percentile(stage_data, 75)
            ]
        
        stage_stats.index = ['Mean', 'Std Dev', 'Q1', 'Median', 'Q3']
        st.dataframe(stage_stats.T, use_container_width=True)
        
        # ====================================================================
        # BAGIAN 4: ANALISIS DEADLINE DAN REKOMENDASI
        # ====================================================================
        st.markdown('<h2 class="sub-header">🎯 Analisis Deadline & Rekomendasi</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input deadline target - SEMUA INT (konsisten)
            target_deadline = int(st.number_input(
                "Masukkan deadline target (bulan):",
                min_value=12,
                max_value=36,
                value=20,
                step=1
            ))
            
            # Hitung probabilitas untuk deadline target
            prob_target = np.mean(total_duration <= target_deadline)
            days_at_risk = max(0, np.percentile(total_duration, 95) - target_deadline)
            
            st.metric(
                label=f"Probabilitas selesai dalam {target_deadline} bulan",
                value=f"{prob_target:.1%}",
                delta=f"Potensi keterlambatan: {days_at_risk:.1f} bulan" if days_at_risk > 0 else "Tepat waktu",
                delta_color="inverse"
            )
        
        with col2:
            # Rekomendasi buffer
            safety_buffer = np.percentile(total_duration, 80) - mean_duration
            contingency_reserve = np.percentile(total_duration, 95) - mean_duration
            
            st.markdown(f"""
            <div class="info-box">
                <h4>🏗️ Rekomendasi Manajemen Risiko:</h4>
                • <b>Safety Buffer</b> (untuk 80% confidence): <b>{safety_buffer:.1f} bulan</b><br>
                • <b>Contingency Reserve</b> (untuk 95% confidence): <b>{contingency_reserve:.1f} bulan</b><br><br>
                • <b>Estimasi jadwal yang direkomendasikan:</b><br>
                    {mean_duration:.1f} + {safety_buffer:.1f} = <b>{mean_duration + safety_buffer:.1f} bulan</b>
            </div>
            """, unsafe_allow_html=True)
        
        # ====================================================================
        # BAGIAN 5: INFORMASI TEKNIS
        # ====================================================================
        with st.expander("ℹ️ Informasi Teknis Simulasi", expanded=False):
            st.write(f"**Parameter Simulasi:**")
            st.write(f"- Jumlah iterasi: {num_simulations:,}")
            st.write(f"- Jumlah tahapan: {len(simulator.stages)}")
            st.write(f"- Seed acak: 42 (untuk hasil yang dapat direproduksi)")
            
            st.write(f"\n**Konfigurasi Tahapan:**")
            for stage_name, config in default_config.items():
                base = config['base_params']
                st.markdown(f"""
                <div class="stage-card">
                    <b>{stage_name.replace('_', ' ')}</b><br>
                    • Optimistic: {base['optimistic']} bulan<br>
                    • Most Likely: {base['most_likely']} bulan<br>
                    • Pessimistic: {base['pessimistic']} bulan
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Tampilkan instruksi jika simulasi belum dijalankan
        st.markdown("""
        <div style="text-align: center; padding: 4rem; background-color: #f8f9fa; border-radius: 10px;">
            <h3>🚀 Siap untuk memulai simulasi?</h3>
            <p>Atur parameter di sidebar kiri, lalu klik tombol <b>"🚀 JALANKAN SIMULASI"</b> untuk memulai analisis.</p>
            <p>📊 Hasil simulasi akan ditampilkan di sini setelah proses selesai.</p>
            <p>🎉 Jangan lupa tunggu animasi dan kejutan spesial!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tampilkan preview konfigurasi
        st.markdown('<h2 class="sub-header">📋 Preview Konfigurasi Tahapan</h2>', unsafe_allow_html=True)
        
        for stage_name, config in default_config.items():
            base = config['base_params']
            st.markdown(f"""
            <div class="stage-card">
                <b>{stage_name.replace('_', ' ')}</b> | 
                Optimistic: {base['optimistic']} bulan | 
                Most Likely: {base['most_likely']} bulan | 
                Pessimistic: {base['pessimistic']} bulan
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><b>Simulasi Monte Carlo untuk Estimasi Waktu Pembangunan Gedung FITE</b></p>
    <p>⚠️ Hasil simulasi ini merupakan estimasi probabilistik dan bukan prediksi pasti.</p>
    <p>📚 Modul Praktikum 5 - Pemodelan dan Simulasi (MODSIM) 2026</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 7. JALANKAN APLIKASI
# ============================================================================
if __name__ == "__main__":
    main()