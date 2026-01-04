import os
import sys
import json
import shutil
import zipfile
import hashlib
import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Setup project root for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, PROJECT_ROOT)

from script.common.hash import hash_file  # noqa: E402

def create_deterministic_zip(source_dir, zip_path):
    """Create a zip file with sorted files and fixed timestamps for reproducibility."""
    # Use a fixed date for all files inside the zip: 2025-01-01 00:00:00
    fixed_time = (2025, 1, 1, 0, 0, 0)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the route directory and add files to zip in sorted order
        for root, dirs, files in os.walk(source_dir):
            dirs.sort()  # Sort directories for consistent walking
            for file in sorted(files):
                file_path = os.path.join(root, file)
                
                # Create ZipInfo with fixed timestamp
                zinfo = zipfile.ZipInfo(file)
                zinfo.date_time = fixed_time
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                
                with open(file_path, 'rb') as f:
                    zipf.writestr(zinfo, f.read())

def main():
    logger.info("Starting V3 release artifact generation...")

    # Define paths
    base_dir = os.path.join(PROJECT_ROOT, "database/kanachu/v3/database")
    release_dir = os.path.join(PROJECT_ROOT, "release/kanachu/v3")
    
    # Ensure release directory exists
    os.makedirs(release_dir, exist_ok=True)

    # 1. Copy busstops.json and calculate hash
    busstops_src = os.path.join(base_dir, "busstops.json")
    busstops_dst = os.path.join(release_dir, "busstops.json")
    
    if not os.path.exists(busstops_src):
        logger.error(f"busstops.json not found at {busstops_src}")
        sys.exit(1)
        
    shutil.copy2(busstops_src, busstops_dst)
    busstops_hash = hash_file(busstops_dst)
    logger.info(f"Copied busstops.json. Hash: {busstops_hash}")

    # 2. Process routes
    route_ids_path = os.path.join(base_dir, "route_ids.json")
    if not os.path.exists(route_ids_path):
        logger.error(f"route_ids.json not found at {route_ids_path}")
        sys.exit(1)

    with open(route_ids_path, 'r', encoding='utf-8') as f:
        route_ids = json.load(f)

    routes_metadata = []
    
    for route_id in route_ids:
        route_dir = os.path.join(base_dir, route_id)
        if not os.path.isdir(route_dir):
            logger.warning(f"Route directory not found for ID: {route_id}, skipping.")
            continue

        # Create zip file for the route (deterministic)
        zip_filename = f"{route_id}.zip"
        zip_path = os.path.join(release_dir, zip_filename)
        
        create_deterministic_zip(route_dir, zip_path)
        
        # Calculate hash of the zip file
        zip_hash = hash_file(zip_path)
        
        # Get busstops list from route.json for metadata
        route_json_path = os.path.join(route_dir, "route.json")
        busstop_ids = []
        if os.path.exists(route_json_path):
            try:
                with open(route_json_path, 'r', encoding='utf-8') as rf:
                    route_data = json.load(rf)
                    # route.json structure: { "busstops": [ { "id": "..." }, ... ] }
                    if "busstops" in route_data:
                        busstop_ids = [b.get("id") for b in route_data["busstops"] if "id" in b]
            except Exception as e:
                logger.warning(f"Failed to read route.json for {route_id}: {e}")

        routes_metadata.append({
            "id": route_id,
            "hash": zip_hash,
            "busstops": busstop_ids
        })
        logger.info(f"Created {zip_filename}. Hash: {zip_hash}")

    # 3. Create info.json
    # Calculate dataset hash (hash of all route hashes + busstop hash)
    combined_hash_input = busstops_hash + "".join([r["hash"] for r in routes_metadata])
    dataset_hash = hashlib.sha256(combined_hash_input.encode()).hexdigest()
    
    # Check existing info.json to see if anything changed
    info_path = os.path.join(release_dir, "info.json")
    existing_info = {}
    if os.path.exists(info_path):
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                existing_info = json.load(f)
        except Exception:
            pass

    updated_at = datetime.date.today().isoformat()
    # If the hash is the same as before, keep the old updated_at to avoid unnecessary changes
    if existing_info.get("hash") == dataset_hash:
        logger.info("No changes detected in dataset hash. Preserving old updated_at.")
        updated_at = existing_info.get("updated_at", updated_at)

    info_data = {
        "updated_at": updated_at,
        "hash": dataset_hash,
        "busstops": {
            "hash": busstops_hash
        },
        "routes": routes_metadata
    }

    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(info_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Created info.json. Dataset Hash: {dataset_hash}")
    logger.info("Release artifact generation completed.")


if __name__ == "__main__":
    main()
