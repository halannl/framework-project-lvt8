import random
import os
import sys
import argparse
from datetime import datetime

# Pack definitions - optimized for Suno prompt precedence
PACK_START = {
    "A": "Sunset Melodic House, 122-124 BPM",
    "B": "Progressive House, Chill Progressive, 120-124 BPM",
    "C": "Deep House, 120-122 BPM",
    "D": "Organic House, Progressive House, 118-122 BPM"
}

PACK_SPINE = {
    "A": "deep melodic vibes, emotional instrumental electronic, slow build arrangement, clean modern EDM production, spacious reverb, Ibiza sunset energy",
    "B": "melodic progressive EDM, slow build ups, sunset festival vibes, instrumental focus, clean modern mix",
    "C": "sunset electronic, hypnotic grooves, smooth percussion, subtle melodic hooks, sunset rooftop vibe",
    "D": "atmospheric progressive, warm organic textures, deep melodic bassline, flowing rhythms, sunset horizon vibe, modern progressive sound"
}

def get_base_path():
    """Get the base path for resource files (handles PyInstaller bundling)."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def load_options(filename):
    """Load options from a text file, one per line."""
    filepath = os.path.join(get_base_path(), "styles 2.0", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def load_harmonic_carriers(pack):
    """Load harmonic carriers filtered by pack compatibility."""
    filepath = os.path.join(get_base_path(), "styles 2.0", "harmonic_carrier.txt")
    carriers = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "|" in line:
                carrier, packs = line.split("|")
                if pack in packs:
                    carriers.append(carrier.strip())
            else:
                carriers.append(line)
    return carriers

def load_sub_genres(pack):
    """Load sub-genres for the selected pack."""
    filepath = os.path.join(get_base_path(), "styles 2.0", "sub_genre.txt")
    sub_genres = []
    pack_key = f"[PACK_{pack}]"
    in_section = False
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == pack_key:
                in_section = True
                continue
            if line.startswith("["):
                in_section = False
            if in_section and line:
                sub_genres.append(line)
    return sub_genres


def generate_prompts(pack):
    """Generate 12 unique Suno AI prompts for the selected pack."""
    pack_start = PACK_START[pack]
    pack_spine = PACK_SPINE[pack]
    
    # Load all option lists
    emotion_limiters = load_options("emotion_limiter.txt")
    visual_scenes = load_options("emotion_visual_scene.txt")
    emotion_cores = load_options("emotion_core.txt")
    arrangement_hints = load_options("arrangement_arc.txt")
    instrument_hints = load_options("instrument_hint.txt")
    harmonic_carriers = load_harmonic_carriers(pack)
    sub_genres = load_sub_genres(pack)
    
    prompts = []
    used_lines = set()
    used_combinations = set()
    used_carriers = {}
    used_instruments = set()
    
    attempts = 0
    max_attempts = 1000
    
    while len(prompts) < 12 and attempts < max_attempts:
        attempts += 1
        
        # Random picks
        emotion_limiter = random.choice(emotion_limiters)
        visual_scene = random.choice(visual_scenes)
        emotion_1 = random.choice(emotion_cores)
        emotion_2 = random.choice([e for e in emotion_cores if e != emotion_1])
        arrangement_hint = random.choice(arrangement_hints)
        
        # Pick harmonic carrier (max 2 uses per carrier type)
        available_carriers = [c for c in harmonic_carriers if used_carriers.get(c, 0) < 2]
        if not available_carriers:
            available_carriers = harmonic_carriers
        harmonic_carrier = random.choice(available_carriers)
        
        # Pick secondary instrument (no repeats)
        available_instruments = [i for i in instrument_hints if i not in used_instruments]
        if not available_instruments:
            available_instruments = instrument_hints
        instrument_hint = random.choice(available_instruments)
        
        # Pick sub-genre
        sub_genre = random.choice(sub_genres)
        
        # Build the prompt line with new structure
        # "[PACK_START], harmonic bed [HARMONIC_CARRIER], secondary instrument [SECONDARY_INSTRUMENT], [SUB_GENRE], [limiter] [visual scene], [emotion1] [emotion2] [arrangement arc], extended drop, long ending, [PACK_SPINE]"
        prompt = f"{pack_start}, harmonic bed {harmonic_carrier}, secondary instrument {instrument_hint}, {sub_genre}, {emotion_limiter} {visual_scene}, {emotion_1} {emotion_2} {arrangement_hint}, extended drop, long ending, {pack_spine}"
        
        # Check uniqueness
        combination = (visual_scene, emotion_1, emotion_2, harmonic_carrier)
        
        if prompt not in used_lines and combination not in used_combinations:
            used_lines.add(prompt)
            used_combinations.add(combination)
            used_carriers[harmonic_carrier] = used_carriers.get(harmonic_carrier, 0) + 1
            used_instruments.add(instrument_hint)
            prompts.append(prompt)
    
    return prompts

def save_prompts(prompts, pack, output_path=None):
    """Save prompts to the specified path or a timestamped file in the default directory."""
    if output_path:
        filepath = output_path
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if getattr(sys, 'frozen', False):
            output_dir = os.path.dirname(sys.executable)
        else:
            output_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"suno_prompts_pack{pack}_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        for i, prompt in enumerate(prompts, 1):
            f.write(f"{prompt}\n")
    
    return filepath

def run_gui():
    """Launch the tkinter GUI (default mode)."""
    import tkinter as tk
    from tkinter import ttk, messagebox

    class App:
        def __init__(self, root):
            self.root = root
            self.root.title("Suno AI Prompt Generator")
            self.root.geometry("400x200")
            self.root.resizable(False, False)
            self.root.eval('tk::PlaceWindow . center')

            main_frame = ttk.Frame(root, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)

            title_label = ttk.Label(main_frame, text="Suno AI Prompt Generator", font=("Segoe UI", 14, "bold"))
            title_label.pack(pady=(0, 20))

            pack_frame = ttk.Frame(main_frame)
            pack_frame.pack(pady=10)

            pack_label = ttk.Label(pack_frame, text="Select Pack:", font=("Segoe UI", 10))
            pack_label.pack(side=tk.LEFT, padx=(0, 10))

            self.pack_var = tk.StringVar(value="A")
            pack_combo = ttk.Combobox(pack_frame, textvariable=self.pack_var, values=["A", "B", "C", "D"], state="readonly", width=5)
            pack_combo.pack(side=tk.LEFT)

            generate_btn = ttk.Button(main_frame, text="Generate 12 Prompts", command=self.generate)
            generate_btn.pack(pady=20)

            self.status_label = ttk.Label(main_frame, text="", font=("Segoe UI", 9))
            self.status_label.pack()

        def generate(self):
            try:
                pack = self.pack_var.get()
                prompts = generate_prompts(pack)
                filepath = save_prompts(prompts, pack)
                self.status_label.config(text=f"Saved to: {os.path.basename(filepath)}")
                messagebox.showinfo("Success", f"Generated 12 prompts!\n\nSaved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    root = tk.Tk()
    App(root)
    root.mainloop()


def run_cli(pack, output_path=None):
    """Run in headless CLI mode."""
    pack = pack.upper()
    if pack not in PACK_START:
        print(f"Error: Invalid pack '{pack}'. Must be one of: A, B, C, D")
        sys.exit(1)
    prompts = generate_prompts(pack)
    filepath = save_prompts(prompts, pack, output_path)
    print(f"Generated 12 prompts for Pack {pack}")
    print(f"Saved to: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Suno AI Prompt Generator")
    parser.add_argument("--pack", type=str, choices=["A", "B", "C", "D", "a", "b", "c", "d"],
                        help="Pack letter (A/B/C/D). If provided, runs in headless CLI mode.")
    parser.add_argument("--output", type=str,
                        help="Output file path. If omitted, saves to a timestamped file in the script directory.")
    args = parser.parse_args()

    if args.pack:
        run_cli(args.pack, args.output)
    else:
        run_gui()


if __name__ == "__main__":
    main()
