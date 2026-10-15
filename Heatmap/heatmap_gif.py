import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

# Add ImageClip and concatenate_videoclips to your existing imports
from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips

# 1. Generate Synthetic Daily Data
dates = pd.date_range(start='2026-01-01', end='2026-12-31')
data = np.random.randint(10, 100, size=len(dates))
df = pd.DataFrame({'Date': dates, 'Value': data})

# Extract calendar layout features
df['DayOfWeek'] = df['Date'].dt.dayofweek  # 0=Monday, 6=Sunday
df['Week'] = df['Date'].dt.isocalendar().week

# 2. Establish Fixed Grid Dimensions
# This prevents the axis from shifting or jumping as new weeks are added
week_min, week_max = df['Week'].min(), df['Week'].max()
all_weeks = range(week_min, week_max + 1)
all_days = range(7)

# Pre-configure the figure for high-quality video output
fig, ax = plt.subplots(figsize=(14, 4), dpi=150)
plt.subplots_adjust(left=0.05, right=0.98, top=0.85, bottom=0.15)

fps = 30
duration = 12  # Video length in seconds
total_frames = int(duration * fps)

# 3. Define the Frame Generation Function
def make_frame(t):
    current_frame = int(t * fps)
    
    # Map current frame to the corresponding day of the year
    day_idx = int((current_frame / total_frames) * len(df))
    if day_idx >= len(df):
        day_idx = len(df) - 1
        
    # Slice data up to the current animation frame
    df_current = df.iloc[:day_idx + 1]
    
    # Pivot into Calendar Grid
    pivot = df_current.pivot(index='DayOfWeek', columns='Week', values='Value')
    
    # Reindex forces the DataFrame to keep the full 52-week x 7-day structure
    pivot = pivot.reindex(index=all_days, columns=all_weeks)
    
    ax.clear()
    
    # Plot Seaborn Heatmap
    # vmin and vmax MUST be locked so colors don't recalibrate mid-animation
    sns.heatmap(pivot, cmap='coolwarm', ax=ax, cbar=False, 
                vmin=10, vmax=100, linewidths=.5, linecolor='white')
    
    current_date_str = df.iloc[day_idx]['Date'].strftime('%B %d, %Y')
    ax.set_title(f"Year-to-Date Volume: {current_date_str}", fontsize=16, pad=15)
    
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=0)
    ax.set_xlabel('Week of the Year')
    ax.set_ylabel('')
    
    # Convert the matplotlib canvas to a numpy array for moviepy
    return mplfig_to_npimage(fig)

# # 4. Render and Export
# print("Rendering video...")
# animation = VideoClip(make_frame, duration=duration)
# animation.write_videofile("calendar_heatmap_build.mp4", fps=fps, codec='libx264')

# 4. Render and Export with Freeze Frame
print("Generating animation sequence...")
main_clip = VideoClip(make_frame, duration=duration)

print("Generating 5-second freeze frame...")
# Grab a frame from the very end of the main clip
# We subtract a tiny fraction (0.1) to safely guarantee we hit a valid frame
last_frame_array = main_clip.get_frame(duration - 0.1)

# Convert that single frame array into a 5-second static clip
# Convert to 5-second clip and chain the fadeout method
# The '1' represents the duration of the fade in seconds
freeze_clip = (ImageClip(last_frame_array)
               .set_duration(5)
               .fadeout(1)) 

print("Concatenating and rendering final video...")
# Stitch the animated clip and the static clip together
final_video = concatenate_videoclips([main_clip, freeze_clip])

# Write the final 17-second video (12s animation + 5s hold with 1s fade)
final_video.write_videofile("calendar_heatmap_build.mp4", fps=fps, codec='libx264')