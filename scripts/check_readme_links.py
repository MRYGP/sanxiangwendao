import os
import re
import urllib.parse
from pathlib import Path

def find_readme_files(root_dir):
    readme_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and node_modules, etc.
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for file in files:
            if file.lower() == 'readme.md':
                readme_files.append(os.path.join(root, file))
    return readme_files

def check_link(file_path, link, root_dir):
    # Ignore external links
    if link.startswith('http://') or link.startswith('https://') or link.startswith('mailto:'):
        return None

    # Ignore anchor only links
    if link.startswith('#'):
        return None

    # Split anchor if present
    path_part = link.split('#')[0]
    
    if not path_part:
        return None

    # Decode URL (e.g., %20 to space)
    path_part = urllib.parse.unquote(path_part)

    # Determine absolute path of the target
    file_dir = os.path.dirname(file_path)
    
    if os.path.isabs(path_part):
        # If it looks like absolute path, treat relative to system root? 
        # Usually in markdown / means root of repo, but os.path.isabs checks for drive letter on windows or / on unix.
        # In markdown context, usually relative paths are used. 
        # If it starts with /, treat as relative to project root.
        if path_part.startswith('/'):
             target_path = os.path.join(root_dir, path_part.lstrip('/'))
        else:
             target_path = os.path.abspath(path_part) # Unlikely intended
    else:
        target_path = os.path.join(file_dir, path_part)

    target_path = os.path.normpath(target_path)

    if not os.path.exists(target_path):
        return f"File not found: {path_part}"
    
    return None

def scan_file(file_path, root_dir):
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex for markdown links: [text](url) and images ![alt](url)
        # Simplified regex, might miss some edge cases but good enough for general check
        # Capture the URL part
        link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
        
        for match in link_pattern.finditer(content):
            link = match.group(1)
            # Remove title part if present: "url" "title"
            if '"' in link:
                link = link.split('"')[0].strip()
            elif "'" in link:
                link = link.split("'")[0].strip()
            
            # Remove parenthesis that might be matched if regex is greedy inside ()
            # The simple regex above \((.*?)\) is non-greedy, so it should be fine mostly.
            # But standard markdown allows parenthesis in URL if balanced or escaped.
            
            error = check_link(file_path, link, root_dir)
            if error:
                # Find line number (rough estimate)
                line_num = content[:match.start()].count('\n') + 1
                errors.append({'line': line_num, 'link': link, 'error': error})
                
    except Exception as e:
        errors.append({'line': 0, 'link': 'N/A', 'error': f"Error reading file: {str(e)}"})
        
    return errors

def main():
    root_dir = os.getcwd()
    print(f"Scanning for README.md files in {root_dir}...")
    
    readme_files = find_readme_files(root_dir)
    print(f"Found {len(readme_files)} README files.")
    
    total_errors = 0
    
    for readme in readme_files:
        rel_path = os.path.relpath(readme, root_dir)
        errors = scan_file(readme, root_dir)
        
        if errors:
            print(f"\nIssues in {rel_path}:")
            for err in errors:
                print(f"  Line {err['line']}: {err['link']} -> {err['error']}")
                total_errors += 1

    if total_errors == 0:
        print("\nNo broken links found!")
    else:
        print(f"\nFound {total_errors} broken links.")

if __name__ == "__main__":
    main()
