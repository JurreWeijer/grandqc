# EXTRACTION OF META-DATA FROM SLIDE

from PIL import Image
from grandqc_fork.WSI_inference_OPENSLIDE_QC.wsi_stain_norm import standardizer
import numpy as np
import os


def slide_info(slide, slide_path, m_p_s, mpp_model):
    props = slide.properties

    # 1) Objective power
    obj_power = props.get("openslide.objective-power", 99)

    # 2) Compute MPP
    ext = os.path.splitext(slide_path)[1].lower()
    if ext in (".tif", ".tiff"):
        # TIFF → compute from resolution tags
        try:
            res_x = float(props["tiff.XResolution"])
            unit = props.get("tiff.ResolutionUnit", "").lower()
        except KeyError:
            raise RuntimeError(f"TIFF tags missing in {slide_path!r}")

        if unit in ("centimeter", "cm"):
            unit_um = 10_000.0      # 1 cm = 10 000 μm
        elif unit in ("inch",):
            unit_um = 25_400.0      # 1 in = 25 400 μm
        else:
            raise RuntimeError(f"Unknown ResolutionUnit '{unit}' in {slide_path!r}")

        if res_x <= 0:
            raise RuntimeError(f"Invalid XResolution={res_x} in {slide_path!r}")

        mpp = unit_um / res_x

    else:
        # Non‐TIFF → OpenSlide’s own MPP value
        try:
            mpp = float(props["openslide.mpp-x"])
        except KeyError:
            raise RuntimeError(f"No openslide.mpp-x for {slide_path!r}")

    p_s = int(mpp_model / mpp * m_p_s)

    # Vendor
    vendor = slide.properties["openslide.vendor"]

    # Extract and save dimensions of level [0]
    dim_l0 = slide.level_dimensions[0]
    w_l0 = dim_l0[0]
    h_l0 = dim_l0[1]

    # Calculate number of patches to process
    patch_n_w_l0 = int(w_l0 / p_s)
    patch_n_h_l0 = int(h_l0 / p_s)

    # Number of levels
    num_level = slide.level_count

    # Level downsamples
    down_levels = slide.level_downsamples

    # Output BASIC DATA
    print("")
    print("Basic data about processed whole-slide image")
    print("")
    print("Vendor: ", vendor)
    print("Scan magnification: ", obj_power)
    print("Number of levels: ", num_level)
    print("Level downsamples: ", down_levels)
    print("Microns per pixel (slide):", mpp)
    print("Height: ", h_l0)
    print("Width: ", w_l0)
    print("Model patch size at slide MPP: ", p_s, "x", p_s)
    print("Width - number of patches: ", patch_n_w_l0)
    print("Height - number of patches: ", patch_n_h_l0)
    print("Overall number of patches / slide (without tissue detection): ", patch_n_w_l0 * patch_n_h_l0)

    return p_s, patch_n_w_l0, patch_n_h_l0, mpp, w_l0, h_l0, obj_power
