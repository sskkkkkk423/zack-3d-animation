# 3D Zack D. Films Animation Project

This project contains the complete 3D scene, local automated renderer, and cloud GPU rendering configurations.

---

## Project Structure

* `zack_animation.blend`: Master Blender 3.1.2 scene with character, lighting, and camera keyframes.
* `output/`: Folder containing all rendered `.png` frames.
* `render_local.py`: Automated local batch rendering script with resume capability and FFmpeg video compiler.
* `.github/workflows/render_matrix.yml`: GitHub Actions parallel workflow splitting 300 frames across 6 concurrent runner jobs.
* `Zack_GPU_Renderer.ipynb`: Google Colab 1-click GPU rendering notebook (renders in ~3 minutes on a free NVIDIA T4 GPU).

---

## 1. Running Locally
Run the batch renderer anytime:
```powershell
& "C:\Users\This PC\Downloads\blender-3.1.2-windows-x64\blender.exe" -b -P render_local.py
```
It skips already rendered frames, renders the next batch, and compiles existing frames into `zack_animation_preview.mp4`.

---

## 2. Running on GitHub Actions (Parallel Matrix)
1. Initialize git and push this folder to your GitHub repo:
   ```powershell
   git init
   git add .
   git commit -m "Initial 3D animation project"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USER>/<YOUR_REPO>.git
   git push -u origin main
   ```
2. In GitHub, go to **Actions** &rarr; select **Parallel 3D Render** &rarr; click **Run workflow**.

---

## 3. Running on Google Colab (Free NVIDIA T4 GPU — 3 Minutes)
1. Open [Google Colab](https://colab.research.google.com/).
2. Select **Upload** and upload `Zack_GPU_Renderer.ipynb`.
3. Set runtime to **T4 GPU** and run all cells.
