import os
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
DIRECTORIES = {
    "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "Videos": os.path.join(os.path.expanduser("~"), "Videos"),
}

TARGET_DIRS = {
    "Images": os.path.join(os.path.expanduser("~"), "Pictures"),
    "Videos": os.path.join(os.path.expanduser("~"), "Videos"),
    "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "Music": os.path.join(os.path.expanduser("~"), "Music"),
}

EXTENSIONS = {
    "Images": {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.heic'},
    "Videos": {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.m4v'},
    "Documents": {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.rtf', '.odt'},
    "Music": {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'}
}

IGNORED_FILES = {'desktop.ini', 'thumbs.db', '.ds_store', '.localized'}
IGNORED_EXTENSIONS = {'.tmp', '.crdownload', '.part', '.ini', '.db'}

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cleanup_history.json")

def get_category(extension):
    """Returns the category for a given file extension."""
    ext = extension.lower()
    for category, exts in EXTENSIONS.items():
        if ext in exts:
            return category
    return None

def get_unique_filename(directory, filename):
    """Generates a unique filename if the file already exists."""
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{name}({counter}){ext}"
        counter += 1
    return new_filename

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def organize_files():
    """Organizes files from source directories to target directories."""
    history = load_history()
    current_batch = {
        "timestamp": datetime.now().isoformat(),
        "moves": []
    }
    
    moved_count = 0
    
    print("Iniciando organização...")

    for source_name, source_path in DIRECTORIES.items():
        if not os.path.exists(source_path):
            print(f"Aviso: Pasta {source_name} não encontrada em {source_path}")
            continue

        print(f"Verificando {source_name}...")
        
        # List only files, not directories
        try:
            items = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
        except PermissionError:
            print(f"Erro de permissão ao acessar {source_path}")
            continue

        for filename in items:
            # Skip system and hidden files
            if filename.lower() in IGNORED_FILES or filename.startswith('.'):
                continue
                
            file_path = os.path.join(source_path, filename)
            _, ext = os.path.splitext(filename)
            
            if ext.lower() in IGNORED_EXTENSIONS:
                continue
            
            category = get_category(ext)
            
            if category:
                target_dir = TARGET_DIRS[category]
                
                # Skip if source and target are the same (e.g. Videos -> Videos)
                if os.path.abspath(source_path) == os.path.abspath(target_dir):
                    continue

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                new_filename = get_unique_filename(target_dir, filename)
                target_path = os.path.join(target_dir, new_filename)

                try:
                    shutil.move(file_path, target_path)
                    print(f"Movido: {filename} -> {category}")
                    
                    current_batch["moves"].append({
                        "original_path": file_path,
                        "new_path": target_path
                    })
                    moved_count += 1
                except Exception as e:
                    print(f"Erro ao mover {filename}: {e}")

    if moved_count > 0:
        history.append(current_batch)
        save_history(history)
        print(f"\nSucesso! {moved_count} arquivos organizados.")
    else:
        print("\nNenhum arquivo precisou ser movido.")

def undo_last_run():
    """Reverts the last organization batch."""
    history = load_history()
    
    if not history:
        print("Nenhum histórico de organização encontrado para desfazer.")
        return

    last_batch = history.pop()
    moves = last_batch.get("moves", [])
    
    print(f"Desfazendo organização de {last_batch['timestamp']}...")
    
    restored_count = 0
    
    # Process in reverse order to handle potential renaming logic correctly if needed
    for move in reversed(moves):
        original_path = move["original_path"]
        current_path = move["new_path"]
        
        if os.path.exists(current_path):
            # Ensure original directory exists
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            
            try:
                # Check if original path is occupied now
                if os.path.exists(original_path):
                    print(f"Aviso: O local original já está ocupado: {original_path}. Pulando restauração deste arquivo.")
                    continue
                
                shutil.move(current_path, original_path)
                print(f"Restaurado: {os.path.basename(current_path)} -> {os.path.dirname(original_path)}")
                restored_count += 1
            except Exception as e:
                print(f"Erro ao restaurar {current_path}: {e}")
        else:
            print(f"Arquivo não encontrado para restaurar: {current_path}")

    save_history(history)
    print(f"\nDesfazer concluído. {restored_count} arquivos restaurados.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Faxineiro IA - Organizador de Arquivos")
    parser.add_argument("--undo", action="store_true", help="Desfazer a última organização")
    
    args = parser.parse_args()
    
    if args.undo:
        undo_last_run()
    else:
        organize_files()
