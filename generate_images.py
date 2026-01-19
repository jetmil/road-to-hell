#!/usr/bin/env python3
"""
Generate chapter illustrations for "Путь в АД" book using ComfyUI Qwen-Image model.
Style: Dante's Inferno - dark, infernal, spiraling circles of hell, fire, dramatic lighting
"""

import json
import requests
import time
import random
import os

COMFYUI_URL = "http://127.0.0.1:8190"
OUTPUT_DIR = "/home/jetmil/comfyui/output"
BOOK_DIR = "/var/www/road-to-hell/images/chapters"

# Workflow template based on квен_создание_быстрый.json
def create_workflow(prompt: str, seed: int = None, filename_prefix: str = "chapter"):
    if seed is None:
        seed = random.randint(1, 2**53)

    return {
        "prompt": {
            "60": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": filename_prefix,
                    "images": ["75", 0]
                }
            },
            "75": {
                "class_type": "2c61139d-9c34-4c7e-a083-7a67cc4770ad",
                "inputs": {
                    "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                    "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                    "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
                    "width": 1328,
                    "height": 1328,
                    "batch_size": 1,
                    "seed": seed,
                    "steps": 4,
                    "text": prompt
                }
            }
        }
    }

# Chapter prompts in Dante's Inferno style
CHAPTERS = {
    "00": {
        "title": "Введение",
        "prompt": "dark infernal book cover, ancient tome floating in void, spiraling circles of hell behind, fire and ember particles, dramatic red and black lighting, cinematic epic art, dante inferno style, book of darkness, mystical atmosphere, high contrast"
    },
    "01": {
        "title": "Нулевое доверие",
        "prompt": "solitary figure standing in center of concentric fiery circles, hands covering heart protectively, translucent walls of distrust surrounding, shattered glass floor reflecting paranoia, dark void background, red ember glow, dante inferno style, psychological horror, cinematic lighting"
    },
    "02": {
        "title": "Эхо-камера",
        "prompt": "infinite mirror maze with distorted reflections, person trapped inside seeing only their own face everywhere, sound waves bouncing and amplifying, claustrophobic spiral tunnel, dark crimson lighting, dante inferno style, psychological prison, echo chamber visualization"
    },
    "03": {
        "title": "Трусость",
        "prompt": "cowering human figure beneath gigantic shadow monster, running away from opportunity door, chains of fear binding ankles, comfort zone as golden cage, fire behind the door, dark atmosphere, dante inferno style, psychological fear visualization, dramatic contrast"
    },
    "04": {
        "title": "Искренность как негатив",
        "prompt": "face split in two halves, one side bright and honest, other side dark and hidden, mask falling away revealing darkness within, emotional duality, fire reflecting on tears, dante inferno style, psychological portrait, dramatic chiaroscuro lighting"
    },
    "05": {
        "title": "Философия как защита",
        "prompt": "philosopher knight holding ancient book as shield, surrounded by chaos and flames, ivory tower crumbling, abstract concepts floating as armor, wisdom versus action, dante inferno style, intellectual fortress, dark academia aesthetic, dramatic fire lighting"
    },
    "06": {
        "title": "На сегодня всё",
        "prompt": "massive hourglass with time sand flowing into dark void, procrastination demon watching, tomorrow written in fading letters, endless staircase going nowhere, fire consuming opportunities, dante inferno style, time wasted visualization, dark surrealism"
    },
    "07": {
        "title": "Тест vs Реальность",
        "prompt": "two opposing mirrors showing different realities, one polished and perfect, one cracked showing truth, person standing between confused, simulated success versus real failure, dante inferno style, duality visualization, dramatic red lighting, psychological split"
    },
    "08": {
        "title": "Никогда vs Всегда сдаваться",
        "prompt": "ancient balance scales with NEVER on one side and ALWAYS on other, warrior figure finding middle path, extremes as burning cliffs, wisdom as narrow bridge between, dante inferno style, balance concept, fire and shadow, epic composition"
    },
    "09": {
        "title": "Аккаунт как завещание",
        "prompt": "digital ghost emerging from glowing screen, social media icons as tombstones, digital footprints leading into darkness, legacy written in code and fire, dante inferno style, digital afterlife, cyber-inferno aesthetic, dramatic neon and fire lighting"
    },
    "10": {
        "title": "И это пройдёт",
        "prompt": "river of time flowing through spiral of hell, carrying joy and sorrow equally downstream, ancient ring with inscription, impermanence visualization, fire and water mixing, dante inferno style, philosophical river, dramatic atmospheric lighting"
    },
    "11": {
        "title": "Трёхкратный проход",
        "prompt": "three concentric rotating circles of evidence, single data point versus triple confirmation, detective magnifying glass over patterns, truth emerging from repetition, dante inferno style, pattern recognition visualization, geometric fire circles, analytical mysticism"
    },
    "12": {
        "title": "Слушай что не сказано",
        "prompt": "figure with sealed mouth but enormous ears, negative space forming hidden message, silence visualized as heavy atmosphere, words unsaid floating as ghosts, dante inferno style, communication darkness, psychological depth, dramatic shadow play"
    },
    "13": {
        "title": "Когда бьют — танцуй",
        "prompt": "elegant dancer gracefully moving between attacking flames, aikido master redirecting fire strikes, pain transforming into motion, resilience as art, dante inferno style, martial grace visualization, fire dance, dramatic dynamic composition"
    },
    "14": {
        "title": "Нарушай когда чуешь что надо",
        "prompt": "breaking chains that were actually rules, intuition visualized as inner flame, master versus follower split, wise rebellion against blind obedience, dante inferno style, liberation through wisdom, dramatic chain-breaking moment, fire of consciousness"
    },
    "15": {
        "title": "Фильтр, не эхо-камера",
        "prompt": "two water pipes side by side, one filtering dirt keeping clean water, one only passing comfortable temperature letting poison through, information flow visualization, dante inferno style, filter versus echo comparison, dramatic industrial-infernal aesthetic"
    }
}

def queue_prompt(workflow):
    """Send workflow to ComfyUI queue"""
    try:
        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json=workflow,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def get_queue_status():
    """Check ComfyUI queue status"""
    try:
        response = requests.get(f"{COMFYUI_URL}/queue", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def wait_for_completion(prompt_id, timeout=300):
    """Wait for generation to complete"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
            if response.status_code == 200:
                history = response.json()
                if prompt_id in history:
                    return history[prompt_id]
        except:
            pass
        time.sleep(2)
    return None

def generate_all_chapters():
    """Generate images for all chapters"""
    print("=" * 60)
    print("Generating chapter illustrations for 'Путь в АД'")
    print("Style: Dante's Inferno - dark, fire, spiraling circles of hell")
    print("=" * 60)

    results = {}

    for chapter_num, chapter_data in CHAPTERS.items():
        title = chapter_data["title"]
        prompt = chapter_data["prompt"]
        filename = f"chapter_{chapter_num}_{title.replace(' ', '_')}"

        print(f"\n[{chapter_num}] Generating: {title}")
        print(f"    Prompt: {prompt[:80]}...")

        workflow = create_workflow(prompt, filename_prefix=filename)
        response = queue_prompt(workflow)

        if response and "prompt_id" in response:
            prompt_id = response["prompt_id"]
            print(f"    Queued: {prompt_id}")
            results[chapter_num] = {
                "title": title,
                "prompt_id": prompt_id,
                "filename": filename
            }
        else:
            print(f"    FAILED to queue!")
            results[chapter_num] = {"title": title, "error": "Failed to queue"}

        # Small delay between requests
        time.sleep(1)

    print("\n" + "=" * 60)
    print("All chapters queued. Waiting for completion...")
    print("=" * 60)

    # Wait for all to complete
    for chapter_num, data in results.items():
        if "prompt_id" in data:
            print(f"\nWaiting for chapter {chapter_num}: {data['title']}...")
            result = wait_for_completion(data["prompt_id"])
            if result:
                print(f"    Completed!")
                results[chapter_num]["completed"] = True
            else:
                print(f"    Timeout or error")
                results[chapter_num]["completed"] = False

    print("\n" + "=" * 60)
    print("Generation complete!")
    print("=" * 60)

    return results

if __name__ == "__main__":
    generate_all_chapters()
