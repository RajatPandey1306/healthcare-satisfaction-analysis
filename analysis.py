"""
Healthcare Patient Satisfaction Analysis
Analyzing quarterly patient satisfaction scores against industry benchmarks
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for professional visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Patient Satisfaction Data - 2024
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
satisfaction_scores = [1.41, 4.25, 8.8, 5.17]
industry_target = 4.5

# Create DataFrame
df = pd.DataFrame({
    'Quarter': quarters,
    'Satisfaction Score': satisfaction_scores
})

# Calculate key metrics
average_score = np.mean(satisfaction_scores)
variance = np.var(satisfaction_scores)
std_dev = np.std(satisfaction_scores)
gap_from_target = average_score - industry_target
gap_percentage = (gap_from_target / industry_target) * 100

# Identify quarters meeting target
df['Meets Target'] = df['Satisfaction Score'] >= industry_target
meets_target_count = df['Meets Target'].sum()

# Calculate quarter-over-quarter change
df['QoQ Change'] = df['Satisfaction Score'].diff()
df['QoQ Change %'] = (df['Satisfaction Score'].pct_change() * 100).round(2)

print("=" * 70)
print("HEALTHCARE PATIENT SATISFACTION ANALYSIS - 2024")
print("=" * 70)
print("\nQUARTERLY PERFORMANCE DATA:")
print(df.to_string(index=False))

print("\n" + "=" * 70)
print("KEY METRICS SUMMARY")
print("=" * 70)
print(f"Average Satisfaction Score:  {average_score:.2f}")
print(f"Industry Target:              {industry_target:.2f}")
print(f"Gap from Target:              {gap_from_target:.2f} ({gap_percentage:+.1f}%)")
print(f"Standard Deviation:           {std_dev:.2f}")
print(f"Variance:                     {variance:.2f}")
print(f"Quarters Meeting Target:      {meets_target_count}/4")
print(f"\nHighest Score:                Q3 ({max(satisfaction_scores):.2f})")
print(f"Lowest Score:                 Q1 ({min(satisfaction_scores):.2f})")
print(f"Range:                        {max(satisfaction_scores) - min(satisfaction_scores):.2f}")

print("\n" + "=" * 70)
print("PERFORMANCE ANALYSIS BY QUARTER")
print("=" * 70)
for idx, row in df.iterrows():
    status = "✓ MEETS TARGET" if row['Meets Target'] else "✗ BELOW TARGET"
    print(f"\n{row['Quarter']}: {row['Satisfaction Score']:.2f} - {status}")
    if not pd.isna(row['QoQ Change']):
        direction = "↑" if row['QoQ Change'] > 0 else "↓"
        print(f"  Change: {direction} {row['QoQ Change %']:.1f}%")

print("\n" + "=" * 70)
print("INSIGHTS & TRENDS")
print("=" * 70)

# Q1 Analysis
print("\nQ1 CRITICAL ALERT:")
print(f"  • Score of {satisfaction_scores[0]:.2f} is {(industry_target - satisfaction_scores[0]):.2f} points below target")
print(f"  • This is the lowest performance in 2024")
print(f"  • {((industry_target - satisfaction_scores[0])/industry_target)*100:.1f}% below industry benchmark")

# Q2 Recovery
q1_to_q2_change = satisfaction_scores[1] - satisfaction_scores[0]
print(f"\nQ2 RECOVERY PHASE:")
print(f"  • Strong recovery: +{q1_to_q2_change:.2f} points ({(q1_to_q2_change/satisfaction_scores[0]*100):.1f}% improvement)")
print(f"  • Score of {satisfaction_scores[1]:.2f} approaches target range")

# Q3 Peak
print(f"\nQ3 PEAK PERFORMANCE:")
print(f"  • Exceptional score of {satisfaction_scores[2]:.2f} - highest in 2024")
print(f"  • Exceeds target by {satisfaction_scores[2] - industry_target:.2f} points ({((satisfaction_scores[2] - industry_target)/industry_target)*100:.1f}%)")
print(f"  • Demonstrates capability to exceed expectations")

# Q4 Decline
q3_to_q4_change = satisfaction_scores[3] - satisfaction_scores[2]
print(f"\nQ4 CONCERNING DECLINE:")
print(f"  • Significant drop: {q3_to_q4_change:.2f} points ({(q3_to_q4_change/satisfaction_scores[2]*100):.1f}% decline)")
print(f"  • Still above target at {satisfaction_scores[3]:.2f}, but trend is concerning")

print("\n" + "=" * 70)

# Create visualizations
print("\nGenerating visualizations...")

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 1. Trend Line Chart
ax1 = plt.subplot(2, 3, 1)
ax1.plot(quarters, satisfaction_scores, marker='o', linewidth=3, markersize=10, 
         color='#2E86AB', label='Actual Score')
ax1.axhline(y=industry_target, color='#A23B72', linestyle='--', linewidth=2, 
            label='Industry Target (4.5)')
ax1.fill_between(range(len(quarters)), satisfaction_scores, industry_target, 
                  where=(np.array(satisfaction_scores) >= industry_target),
                  alpha=0.3, color='green', label='Above Target')
ax1.fill_between(range(len(quarters)), satisfaction_scores, industry_target,
                  where=(np.array(satisfaction_scores) < industry_target),
                  alpha=0.3, color='red', label='Below Target')
ax1.set_ylabel('Satisfaction Score', fontweight='bold')
ax1.set_xlabel('Quarter', fontweight='bold')
ax1.set_title('Patient Satisfaction Trend - 2024', fontweight='bold', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 10)

# 2. Benchmark Comparison
ax2 = plt.subplot(2, 3, 2)
x_pos = np.arange(len(quarters))
bars = ax2.bar(x_pos, satisfaction_scores, color=['#D62828', '#F77F00', '#06A77D', '#06A77D'],
               edgecolor='black', linewidth=1.5, alpha=0.8)
ax2.axhline(y=industry_target, color='#A23B72', linestyle='--', linewidth=2, 
            label='Target (4.5)')
ax2.set_ylabel('Satisfaction Score', fontweight='bold')
ax2.set_xlabel('Quarter', fontweight='bold')
ax2.set_title('Quarterly Performance vs. Industry Target', fontweight='bold', fontsize=12)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(quarters)
ax2.legend()
ax2.set_ylim(0, 10)
# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, satisfaction_scores)):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.2f}',
            ha='center', va='bottom', fontweight='bold')

# 3. Gap Analysis
ax3 = plt.subplot(2, 3, 3)
gaps = [score - industry_target for score in satisfaction_scores]
colors = ['red' if gap < 0 else 'green' for gap in gaps]
bars = ax3.bar(quarters, gaps, color=colors, edgecolor='black', linewidth=1.5, alpha=0.7)
ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.set_ylabel('Gap from Target', fontweight='bold')
ax3.set_xlabel('Quarter', fontweight='bold')
ax3.set_title('Gap from Industry Target (4.5)', fontweight='bold', fontsize=12)
ax3.grid(True, alpha=0.3, axis='y')
# Add value labels
for bar, gap in zip(bars, gaps):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, height + (0.2 if height > 0 else -0.3),
            f'{gap:+.2f}', ha='center', va='bottom' if height > 0 else 'top', fontweight='bold')

# 4. QoQ Change
ax4 = plt.subplot(2, 3, 4)
qoq_changes = [0] + list(np.diff(satisfaction_scores))
colors_qoq = ['gray' if i == 0 else ('green' if change > 0 else 'red') for i, change in enumerate(qoq_changes)]
bars = ax4.bar(quarters, qoq_changes, color=colors_qoq, edgecolor='black', linewidth=1.5, alpha=0.7)
ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax4.set_ylabel('Change (Points)', fontweight='bold')
ax4.set_xlabel('Quarter', fontweight='bold')
ax4.set_title('Quarter-over-Quarter Change', fontweight='bold', fontsize=12)
ax4.grid(True, alpha=0.3, axis='y')

# 5. Distribution
ax5 = plt.subplot(2, 3, 5)
ax5.hist(satisfaction_scores, bins=5, color='#2E86AB', edgecolor='black', alpha=0.7)
ax5.axvline(average_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {average_score:.2f}')
ax5.axvline(industry_target, color='#A23B72', linestyle='--', linewidth=2, label=f'Target: {industry_target:.2f}')
ax5.set_ylabel('Frequency', fontweight='bold')
ax5.set_xlabel('Satisfaction Score', fontweight='bold')
ax5.set_title('Score Distribution', fontweight='bold', fontsize=12)
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# 6. Performance Status
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')
summary_text = f"""
PERFORMANCE SUMMARY

Average Score:           {average_score:.2f}
Target Score:            {industry_target:.2f}
Gap:                     {gap_from_target:+.2f} ({gap_percentage:+.1f}%)

Quarters Above Target:   {meets_target_count}/4
Performance Std Dev:     {std_dev:.2f}

Highest:                 Q3 ({max(satisfaction_scores):.2f})
Lowest:                  Q1 ({min(satisfaction_scores):.2f})

Status: {'✓ EXCEEDS TARGET' if average_score >= industry_target else '✗ BELOW TARGET'}
"""
ax6.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
        verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Healthcare Patient Satisfaction Analysis - 2024', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()

# Save visualization
output_path = Path('visualizations')
output_path.mkdir(exist_ok=True)
plt.savefig(output_path / 'patient_satisfaction_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Main visualization saved: visualizations/patient_satisfaction_analysis.png")

# Create additional detailed charts
fig2, ((ax7, ax8), (ax9, ax10)) = plt.subplots(2, 2, figsize=(14, 10))

# Performance by Quarter (Gauge-like)
ax7.barh(['Q1', 'Q2', 'Q3', 'Q4'], satisfaction_scores, 
         color=['#D62828', '#F77F00', '#06A77D', '#06A77D'], alpha=0.8, edgecolor='black', linewidth=1.5)
ax7.axvline(industry_target, color='#A23B72', linestyle='--', linewidth=2, label='Target')
ax7.set_xlabel('Satisfaction Score', fontweight='bold')
ax7.set_title('Performance by Quarter (Horizontal)', fontweight='bold')
ax7.legend()
ax7.set_xlim(0, 10)
for i, v in enumerate(satisfaction_scores):
    ax7.text(v + 0.2, i, f'{v:.2f}', va='center', fontweight='bold')

# Cumulative Score
ax8.plot(quarters, np.cumsum(satisfaction_scores), marker='o', linewidth=3, 
         markersize=10, color='#2E86AB')
ax8.fill_between(range(len(quarters)), np.cumsum(satisfaction_scores), alpha=0.3, color='#2E86AB')
ax8.set_ylabel('Cumulative Score', fontweight='bold')
ax8.set_xlabel('Quarter', fontweight='bold')
ax8.set_title('Cumulative Patient Satisfaction', fontweight='bold')
ax8.grid(True, alpha=0.3)

# Target Achievement Rate
target_achievement = [(score / industry_target) * 100 for score in satisfaction_scores]
colors_achievement = ['red' if x < 100 else 'green' for x in target_achievement]
bars = ax9.bar(quarters, target_achievement, color=colors_achievement, 
               edgecolor='black', linewidth=1.5, alpha=0.7)
ax9.axhline(100, color='black', linestyle='-', linewidth=2, label='100% (Target)')
ax9.set_ylabel('Achievement Rate (%)', fontweight='bold')
ax9.set_xlabel('Quarter', fontweight='bold')
ax9.set_title('Target Achievement Rate', fontweight='bold')
ax9.legend()
ax9.grid(True, alpha=0.3, axis='y')
for bar, rate in zip(bars, target_achievement):
    ax9.text(bar.get_x() + bar.get_width()/2, rate + 2, f'{rate:.1f}%',
            ha='center', va='bottom', fontweight='bold')

# Statistical Summary Box Plot
ax10.boxplot(satisfaction_scores, labels=['2024 Data'], patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5))
ax10.axhline(industry_target, color='#A23B72', linestyle='--', linewidth=2, label='Target')
ax10.set_ylabel('Satisfaction Score', fontweight='bold')
ax10.set_title('Distribution Statistics', fontweight='bold')
ax10.legend()
ax10.set_ylim(0, 10)
ax10.grid(True, alpha=0.3, axis='y')

plt.suptitle('Detailed Performance Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(output_path / 'detailed_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Detailed analysis saved: visualizations/detailed_analysis.png")

plt.close('all')

# Export data to CSV
df.to_csv('quarterly_satisfaction_data.csv', index=False)
print(f"✓ Data exported: quarterly_satisfaction_data.csv")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
