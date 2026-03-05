"""One-time script to update artwork image_url fields in the database."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DB_URL", os.environ.get("DB_URL", ""))

from db import init_db, SessionLocal
from models import Artwork

# Artwork title -> image URL mapping (Art Institute of Chicago open collection + Wikimedia)
IMAGE_MAP = {
    'Composition in Red, Blue and Yellow': 'https://www.artic.edu/iiif/2/3182d5ce-6518-400d-2df4-60d3ecfcfd44/full/600,/0/default.jpg',
    'Untitled (Ocean Park Series)': 'https://www.artic.edu/iiif/2/d8ec86ef-8261-e933-857d-b21c7256bac2/full/600,/0/default.jpg',
    'Red Balloon over Paris': 'https://www.artic.edu/iiif/2/c8024369-fa0a-6438-0072-f9b9929a800b/full/600,/0/default.jpg',
    'Rhein II': 'https://www.artic.edu/iiif/2/41d9b65a-6649-28e6-19d9-c16ef27df8f1/full/600,/0/default.jpg',
    'Girl with Balloon': 'https://www.artic.edu/iiif/2/97cb5c4b-cce5-c4d8-f303-613ce92832c7/full/600,/0/default.jpg',
    'Infinity Mirror Room': 'https://www.artic.edu/iiif/2/17c21125-a849-a0dc-5957-b01ff3b8c945/full/600,/0/default.jpg',
    'Water Lilies (Nympheas)': 'https://www.artic.edu/iiif/2/3c27b499-af56-f0d5-93b5-a7f2f1ad5813/full/600,/0/default.jpg',
    'Bronze Reclining Figure': 'https://www.artic.edu/iiif/2/6b1edb9c-0f3f-0ee3-47c7-ca25c39ee360/full/600,/0/default.jpg',
    'Self Portrait with Thorn Necklace': 'https://www.artic.edu/iiif/2/dd2d21dd-bf0b-4a0f-25d1-f27a127eb226/full/600,/0/default.jpg',
    'Electric Chair (Sunday B. Morning)': 'https://www.artic.edu/iiif/2/97cb5c4b-cce5-c4d8-f303-613ce92832c7/full/600,/0/default.jpg',
}


def update_images():
    init_db()
    db = SessionLocal()
    try:
        updated = 0
        for title, url in IMAGE_MAP.items():
            artwork = db.query(Artwork).filter(Artwork.title == title).first()
            if artwork:
                artwork.image_url = url
                updated += 1
                print(f"  Updated: {title}")
            else:
                print(f"  Not found: {title}")
        db.commit()
        print(f"\nUpdated {updated} artwork images.")
    finally:
        db.close()


if __name__ == '__main__':
    update_images()
