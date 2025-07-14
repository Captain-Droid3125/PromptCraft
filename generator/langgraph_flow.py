from langgraph.graph import StateGraph, END
from typing import TypedDict

import os
import uuid
import requests

from PIL import Image
from io import BytesIO

class GenerationState(TypedDict, total=False):
    prompt: str
    clean_prompt: str
    base_prompt: str
    final_prompt: str
    image_bytes: bytes
    output: dict


# Node 1: Validate and clean input prompt
def validate_input(state):
    # print("[validate_input] state received:", state)

    if "prompt" not in state or not state["prompt"]:
        raise ValueError("Prompt is required")

    state["clean_prompt"] = state["prompt"].strip()
    return state


# Node 2: Apply a prompt template
def template_prompt(state):
    base_template = "An image of {content}"
    state["base_prompt"] = base_template.format(content=state["clean_prompt"])
    return state

# Node 3: Enhance prompt with styling modifiers
def enhance_prompt(state):
    modifiers = [
        "ultra-detailed",
        "high quality",
        "studio lighting",
        "trending on ArtStation"
    ]
    state["final_prompt"] = state["base_prompt"] + ", " + ", ".join(modifiers)
    return state

# Node 4: Generate image
def generate_image(state):
    prompt = state["final_prompt"]
    api_key = os.getenv("STABILITY_API_KEY")

    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "png",  # or webp
        },
    )

    if response.status_code == 200:
        # filename = f"{uuid.uuid4().hex}.png"
        # image_path = os.path.join("media", filename)
        # with open(image_path, 'wb') as file:
        #     file.write(response.content)
        # state["image_path"] = f"/media/{filename}"
        state["image_bytes"] = response.content
        return state
    else:
        raise Exception(f"Stability API failed: {response.status_code} - {response.text}")

# Node 5: Final response formatting
def wrap_response(state):
    state["output"] = {
        "final_prompt": state["final_prompt"],
        # "image_path": state["image_path"]
        "image_bytes": state["image_bytes"],
    }
    return state

# ✅ Graph definition
def build_graph():
    graph = StateGraph(GenerationState)

    graph.add_node("ValidateInput", validate_input)
    graph.add_node("TemplatePrompt", template_prompt)
    graph.add_node("EnhancePrompt", enhance_prompt)
    graph.add_node("GenerateImage", generate_image)
    graph.add_node("WrapResponse", wrap_response)

    graph.set_entry_point("ValidateInput")
    graph.add_edge("ValidateInput", "TemplatePrompt")
    graph.add_edge("TemplatePrompt", "EnhancePrompt")
    graph.add_edge("EnhancePrompt", "GenerateImage")
    graph.add_edge("GenerateImage", "WrapResponse")
    graph.add_edge("WrapResponse", END)

    return graph.compile()
