import os
import subprocess
import json
import re

def get_git_changes():
    """Get list of changed files in the database directory."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain', 'database/kanachu/v3/database/'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError:
        return []

def extract_route_ids(changes):
    """Extract unique route IDs from git changes."""
    route_ids = set()
    # Pattern to match database/kanachu/v3/database/{route_id}/...
    pattern = re.compile(r'database/kanachu/v3/database/(\d{10})/')
    for line in changes:
        # line format: "XY path/to/file"
        path = line[3:]
        match = pattern.search(path)
        if match:
            route_ids.add(match.group(1))
    return sorted(list(route_ids))

def get_route_info(route_id):
    """Read route.json and extract basic info."""
    route_json_path = f"database/kanachu/v3/database/{route_id}/route.json"
    if not os.path.exists(route_json_path):
        return None
    
    try:
        with open(route_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        system = data.get("system", "不明")
        busstops = data.get("busstops", [])
        
        start_stop = busstops[0].get("name", "不明") if busstops else "不明"
        end_stop = busstops[-1].get("name", "不明") if len(busstops) > 1 else "不明"
        route_url = data.get("route_url", "")
        
        return {
            "id": route_id,
            "system": system,
            "section": f"{start_stop} ➔ {end_stop}",
            "url": route_url
        }
    except Exception:
        return None

def main():
    changes = get_git_changes()
    route_ids = extract_route_ids(changes)
    
    if not route_ids:
        print("### 🕒 更新された路線はありません")
        return

    print(f"### 🚌 更新された路線一覧 (全 {len(route_ids)} 路線)")
    print("")
    print("| 路線ID | 系統 | 区間 | 詳細 |")
    print("| :--- | :--- | :--- | :--- |")
    
    for rid in route_ids:
        info = get_route_info(rid)
        if info:
            url_link = f"[リンク]({info['url']})" if info['url'] else "-"
            print(f"| `{info['id']}` | {info['system']} | {info['section']} | {url_link} |")

if __name__ == "__main__":
    main()
