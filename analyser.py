import os
from collections import Counter
from datetime import datetime
import math

# Configuration
DIRECTORIES = {
    "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "Pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "Videos": os.path.join(os.path.expanduser("~"), "Videos"),
    "Music": os.path.join(os.path.expanduser("~"), "Music"),
}

def analyze_directory(path, name):
    if not os.path.exists(path):
        return None

    stats = {
        "total_files": 0,
        "total_folders": 0,
        "loose_files": 0,
        "extensions": Counter(),
        "depth_distribution": Counter(),
        "naming_patterns": Counter(),
        "old_files": 0, # > 6 months
    }

    six_months_ago = datetime.now().timestamp() - (6 * 30 * 24 * 60 * 60)

    # Walk through directory
    for root, dirs, files in os.walk(path):
        # Calculate depth relative to root
        rel_path = os.path.relpath(root, path)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
        
        stats["total_folders"] += len(dirs)
        stats["depth_distribution"][depth] += len(files)
        
        if depth == 0:
            stats["loose_files"] += len(files)

        for file in files:
            stats["total_files"] += 1
            _, ext = os.path.splitext(file)
            stats["extensions"][ext.lower()] += 1
            
            # Age check
            try:
                file_path = os.path.join(root, file)
                mtime = os.path.getmtime(file_path)
                if mtime < six_months_ago:
                    stats["old_files"] += 1
            except:
                pass

            # Naming pattern check
            if file.startswith("IMG_") or file.startswith("DSC_"):
                stats["naming_patterns"]["Camera Default"] += 1
            elif file.startswith("Screenshot_"):
                stats["naming_patterns"]["Screenshot"] += 1
            elif " (1)" in file or " Copy" in file:
                stats["naming_patterns"]["Duplicate/Copy"] += 1
            elif file[0].isdigit() and "-" in file: # e.g. 2023-11...
                stats["naming_patterns"]["Dated"] += 1

    return stats

def calculate_score(stats_map):
    score = 100
    penalties = []

    # 1. Clutter Penalty (Desktop & Downloads)
    for folder in ["Desktop", "Downloads"]:
        if folder in stats_map and stats_map[folder]:
            loose = stats_map[folder]["loose_files"]
            if loose > 20:
                penalty = min(30, loose // 2)
                score -= penalty
                penalties.append(f"Bagunça no {folder}: -{penalty} pts ({loose} arquivos soltos)")

    # 2. Hierarchy Penalty
    total_depth_issues = 0
    for folder, stats in stats_map.items():
        if not stats: continue
        # Too deep (> 5 levels)
        deep_files = sum(count for depth, count in stats["depth_distribution"].items() if depth > 5)
        if deep_files > 0:
            total_depth_issues += 1
    
    if total_depth_issues > 0:
        score -= 10
        penalties.append(f"Labirinto de Pastas: -10 pts (Arquivos muito profundos encontrados)")

    # 3. Naming Consistency
    total_default_names = 0
    for folder, stats in stats_map.items():
        if not stats: continue
        total_default_names += stats["naming_patterns"]["Camera Default"]
        total_default_names += stats["naming_patterns"]["Screenshot"]
        total_default_names += stats["naming_patterns"]["Duplicate/Copy"]

    if total_default_names > 50:
        score -= 15
        penalties.append(f"Nomes Genéricos: -15 pts ({total_default_names} arquivos como IMG_..., Screenshot_...)")

    # 4. Old Files
    total_old = sum(s["old_files"] for s in stats_map.values() if s)
    if total_old > 100:
        score -= 5
        penalties.append(f"Arquivo Morto: -5 pts ({total_old} arquivos não modificados há 6 meses)")

    return max(0, score), penalties

def print_report():
    print("--- RELATÓRIO DE ORGANIZAÇÃO FAXINEIRO IA ---\n")
    
    stats_map = {}
    for name, path in DIRECTORIES.items():
        print(f"Analisando {name}...")
        stats_map[name] = analyze_directory(path, name)

    score, penalties = calculate_score(stats_map)

    print(f"\n\nNOTA FINAL: {score}/100")
    
    if score == 100:
        print("Status: PERFEITO! 🌟")
    elif score >= 80:
        print("Status: Muito Bom! ✅")
    elif score >= 60:
        print("Status: Aceitável ⚠️")
    else:
        print("Status: Caos Total 🚨")

    print("\n--- ONDE PERDEU PONTOS ---")
    for p in penalties:
        print(f"❌ {p}")

    print("\n--- ANÁLISE DE HIERARQUIA ---")
    for name, stats in stats_map.items():
        if not stats: continue
        max_depth = max(stats["depth_distribution"].keys()) if stats["depth_distribution"] else 0
        print(f"\n📂 {name}:")
        print(f"   - Profundidade Máxima: {max_depth} níveis")
        print(f"   - Arquivos Soltos (Raiz): {stats['loose_files']}")
        
        # Structure Hint
        if stats["naming_patterns"]["Dated"] > 10:
            print("   - Padrão Detectado: Organização por Data 📅")
        elif stats["total_folders"] > stats["total_files"] / 5 and stats["total_files"] > 20:
             print("   - Padrão Detectado: Muitas subpastas (Possível excesso de categorias) 📂")

    print("\n--- DICAS DO FAXINEIRO ---")
    if score < 100:
        if any("Bagunça" in p for p in penalties):
            print("💡 Dica: Rode o 'cleaner.py' para limpar Desktop e Downloads.")
        if any("Nomes Genéricos" in p for p in penalties):
            print("💡 Dica: Use o 'renamer.py' (em breve) para organizar fotos por data.")
        if any("Labirinto" in p for p in penalties):
            print("💡 Dica: Tente achatar sua estrutura. Mais de 3 níveis de pasta geralmente é desnecessário.")
    else:
        print("💡 Dica: Continue assim! Seu sistema é sólido.")

if __name__ == "__main__":
    print_report()
    input("\nPressione Enter para sair...")
