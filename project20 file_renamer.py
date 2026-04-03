import os

while True:

    def list_files(directory, extension=None):
        """Lists files in the directory, optionally filtered by extension."""
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            if extension:
                if not extension.startswith('.'):
                    extension = '.' + extension
                files = [f for f in files if f.endswith(extension)]
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def rename_files(directory, files, mode, **kwargs):
        """Generates a mapping of old filenames to new filenames based on the chosen mode."""
        renamed_map = {}
        for i, filename in enumerate(files):
            name, ext = os.path.splitext(filename)
            new_name = name

            if mode == 'prefix':
                new_name = kwargs.get('prefix', '') + name
            elif mode == 'suffix':
                new_name = name + kwargs.get('suffix', '')
            elif mode == 'replace':
                new_name = name.replace(kwargs.get('old', ''), kwargs.get('new', ''))
            elif mode == 'sequential':
                prefix = kwargs.get('prefix', '')
                new_name = f"{prefix}{i + 1}"
            elif mode == 'extension':
                new_ext = kwargs.get('new_ext', ext)
                if not new_ext.startswith('.'):
                    new_ext = '.' + new_ext
                ext = new_ext

            new_filename = new_name + ext
            if new_filename != filename and os.path.exists(os.path.join(directory, new_filename)):
                print(f"Warning: {new_filename} already exists. Skipping {filename}.")
                continue
                
            renamed_map[filename] = new_filename

        return renamed_map

    def main():
        print("\n" + "="*30)
        print("   PYTHON FILE RENAMER Tool")
        print("="*30)
        
        directory = input("\nEnter the directory path (default: current directory '.'): ").strip() or "."
        
        if not os.path.isdir(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            return

        extension = input("Filter by extension (e.g., .txt) or press Enter for all: ").strip()
        files = list_files(directory, extension)

        if not files:
            print("\nNo files found matching the criteria.")
            return

        print(f"\nFound {len(files)} files:")
        for f in files:
            print(f"  - {f}")

        print("\nChoose rename mode:")
        print("1. Add Prefix")
        print("2. Add Suffix")
        print("3. Replace Text")
        print("4. Sequential Numbering")
        print("5. Change Extension")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-5): ").strip()

        if choice == '0':
            print("Exiting.")
            return

        renamed_map = {}
        if choice == '1':
            prefix = input("Enter prefix: ")
            renamed_map = rename_files(directory, files, 'prefix', prefix=prefix)
        elif choice == '2':
            suffix = input("Enter suffix: ")
            renamed_map = rename_files(directory, files, 'suffix', suffix=suffix)
        elif choice == '3':
            old = input("Enter text to replace: ")
            new = input("Enter new text: ")
            renamed_map = rename_files(directory, files, 'replace', old=old, new=new)
        elif choice == '4':
            prefix = input("Enter prefix for numbering (optional): ")
            renamed_map = rename_files(directory, files, 'sequential', prefix=prefix)
        elif choice == '5':
            new_ext = input("Enter new extension (e.g., .png): ")
            renamed_map = rename_files(directory, files, 'extension', new_ext=new_ext)
        else:
            print("Invalid choice.")
            return

        if not renamed_map:
            print("No changes to apply.")
            return

        print("\nPreview of changes:")
        for old, new in renamed_map.items():
            if old != new:
                print(f"  {old} -> {new}")
            else:
                print(f"  {old} (no change)")

        confirm = input("\nDo you want to apply these changes? (y/n): ").strip().lower()
        if confirm == 'y':
            success_count = 0
            for old, new in renamed_map.items():
                if old == new:
                    continue
                try:
                    os.rename(os.path.join(directory, old), os.path.join(directory, new))
                    success_count += 1
                except Exception as e:
                    print(f"Error renaming {old}: {e}")
            print(f"\nSuccessfully renamed {success_count} files!")
        else:
            print("Changes discarded.")

    if __name__ == "__main__":
        main()