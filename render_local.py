import os
import subprocess
import bpy

proj_dir = os.path.dirname(os.path.abspath(__file__))
blend_file = os.path.join(proj_dir, "zack_animation.blend")
output_dir = os.path.join(proj_dir, "output")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

bpy.ops.wm.open_mainfile(filepath=blend_file)
scene = bpy.context.scene

scene.cycles.samples = 10
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

print("=" * 60)
print("LOCAL BATCH RENDERER — ZACK D. FILMS STYLE")
print("=" * 60)

# Check which frames need rendering (1 to 300)
missing_frames = []
for f in range(1, 301):
    frame_file = os.path.join(output_dir, f"frame_{f:04d}.png")
    if not os.path.exists(frame_file):
        missing_frames.append(f)

print(f"Total frames: 300 | Already rendered: {300 - len(missing_frames)} | Remaining: {len(missing_frames)}")

# Render next batch of frames
batch_to_render = missing_frames[:5]

for f in batch_to_render:
    frame_path = os.path.join(output_dir, f"frame_{f:04d}.png")
    scene.frame_set(f)
    scene.render.filepath = frame_path
    print(f"[Render] Processing Frame {f}/300 ...")
    bpy.ops.render.render(write_still=True)
    print(f"[Done] Frame {f} saved: {frame_path}")

print("Batch rendering completed.")

# Automatically encode existing frames into a playable preview video
existing = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".png")])
if len(existing) >= 2:
    print(f"Assembling {len(existing)} rendered frames into MP4 video with FFmpeg...")
    mp4_out = os.path.join(proj_dir, "zack_animation_preview.mp4")
    list_file = os.path.join(proj_dir, "frames_list.txt")
    with open(list_file, "w") as fp:
        for p in existing:
            clean_p = p.replace("\\", "/")
            fp.write("file '" + clean_p + "'\n")
            fp.write("duration 0.033333\n")
        last_p = existing[-1].replace("\\", "/")
        fp.write("file '" + last_p + "'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        mp4_out
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Preview video generated successfully: {mp4_out}")
    else:
        print("FFmpeg encoding notice:", res.stderr[-200:] if res.stderr else "None")
