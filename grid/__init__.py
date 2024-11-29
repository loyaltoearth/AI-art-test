import os
import streamlit.components.v1 as components
import base64
from PIL import Image
from io import BytesIO

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "masonry_grid",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("masonry_grid", path=build_dir)

def get_image_base64(img_path):
    """Convert image to base64 string"""
    with Image.open(img_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

def show_masonry_grid(images, titles, answers, user_answers, image_data, key=None):
    """Display images in a responsive masonry grid layout.
    
    Parameters
    ----------
    images : list
        List of image numbers to display
    titles : dict
        Dictionary mapping image numbers to their titles
    answers : dict
        Dictionary mapping image numbers to correct answers
    user_answers : dict
        Dictionary mapping image numbers to user answers
    images_dir : str
        Directory containing the images
    key : str or None
        An optional key that uniquely identifies this component.
    """
    # Create a dictionary of image data

    component_value = _component_func(
        images=images,
        titles=titles,
        answers=answers,
        userAnswers=user_answers,
        imageData=image_data,
        key=key,
    )
    
    return component_value