import os
import cv2
import albumentations as A
from glob import glob
from tqdm import tqdm
import random
import shutil

# --- Set your dataset root here ---
root_dir = r'E:\syn_data\Image_Generation\dataset'

# Probability to apply augmentation (e.g., 0.7 means 70% images augmented, 30% copied as-is)
aug_prob = 0.7

# 1) Define your transform
# Use OneOf to randomly apply exactly one of: translation, rotation, or shear (with X and Y shearing)
transform = A.Compose(
    [
        A.OneOf([
            A.Affine(
                translate_percent=0.1,      # ±10% shift
                fit_output=True,            # keep full warped image
                border_mode=cv2.BORDER_CONSTANT
            ),
            A.Affine(
                rotate=(-15, 15),           # random rotation between -15° and +15°
                fit_output=True,
                border_mode=cv2.BORDER_CONSTANT
            ),
            A.Affine(
                shear={"x": (-15, 15), "y": (-15, 15)},  # random shear in both X and Y directions
                fit_output=True,
                border_mode=cv2.BORDER_CONSTANT
            ),
        ], p=1.0)
    ],
    bbox_params=A.BboxParams(
        format='yolo',                  # labels in YOLO format
        label_fields=['class_labels']
    )
)

# 2) Define dataset splits and base paths
splits = ['train', 'val']
img_base     = os.path.join(root_dir, 'images')
lbl_base     = os.path.join(root_dir, 'labels')
out_img_base = os.path.join(root_dir, 'augmented_local_images_new')
out_lbl_base = os.path.join(root_dir, 'augmented_local_labels_new')

# Create output directories for each split
for split in splits:
    os.makedirs(os.path.join(out_img_base, split), exist_ok=True)
    os.makedirs(os.path.join(out_lbl_base, split), exist_ok=True)

# 3) Process each split with progress logging
for split in splits:
    img_dir = os.path.join(img_base, split)
    lbl_dir = os.path.join(lbl_base, split)
    img_paths = glob(os.path.join(img_dir, '*.jpg'))  # adjust extension if needed

    print(f"Processing split '{split}': {len(img_paths)} images")
    for img_path in tqdm(img_paths, desc=f"Augmenting [{split}]"):
        fname = os.path.splitext(os.path.basename(img_path))[0]
        lbl_path = os.path.join(lbl_dir, f'{fname}.txt')
        out_img_path = os.path.join(out_img_base, split, f'{fname}.jpg')
        out_lbl_path = os.path.join(out_lbl_base, split, f'{fname}.txt')

        # Randomly decide whether to augment or copy raw
        if random.random() < aug_prob:
            # Load image
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: could not read {img_path}")
                continue
            # Load labels
            bboxes, class_labels = [], []
            with open(lbl_path) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 5:
                        continue
                    cls, x_c, y_c, bw, bh = map(float, parts)
                    class_labels.append(int(cls))
                    bboxes.append([x_c, y_c, bw, bh])
            # Apply augmentation
            augmented = transform(image=img, bboxes=bboxes, class_labels=class_labels)
            aug_img    = augmented['image']
            aug_boxes  = augmented['bboxes']
            aug_labels = augmented['class_labels']
            # Save augmented image and labels
            cv2.imwrite(out_img_path, aug_img)
            with open(out_lbl_path, 'w') as f:
                for cls, (x_c, y_c, bw, bh) in zip(aug_labels, aug_boxes):
                    f.write(f"{cls} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")
        else:
            # Copy original image and label
            shutil.copy(img_path, out_img_path)
            shutil.copy(lbl_path, out_lbl_path)

    print(f"Finished '{split}' — outputs in: {out_img_base}/{split}, {out_lbl_base}/{split}\n")
