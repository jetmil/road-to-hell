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
import sys

COMFYUI_URL = "http://127.0.0.1:8190"

# Disable proxy for local connections
os.environ['NO_PROXY'] = '127.0.0.1,localhost'
os.environ['no_proxy'] = '127.0.0.1,localhost'

# Create session without proxy
session = requests.Session()
session.trust_env = False

def create_api_workflow(prompt: str, seed: int = None, filename_prefix: str = "chapter"):
    """Create API workflow for Qwen text-to-image with 4-step LoRA"""
    if seed is None:
        seed = random.randint(1, 2**53)

    return {
        # VAELoader - node 39
        "39": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "qwen_image_vae.safetensors"
            }
        },
        # CLIPLoader - node 38
        "38": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "type": "qwen_image",
                "device": "default"
            }
        },
        # UNETLoader - node 37
        "37": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                "weight_dtype": "default"
            }
        },
        # LoraLoaderModelOnly - node 73 (4-step LoRA for speed)
        "73": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["37", 0],
                "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
                "strength_model": 1.0
            }
        },
        # ModelSamplingAuraFlow - node 66
        "66": {
            "class_type": "ModelSamplingAuraFlow",
            "inputs": {
                "model": ["73", 0],
                "shift": 3.1
            }
        },
        # EmptySD3LatentImage - node 58
        "58": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {
                "width": 1328,
                "height": 1328,
                "batch_size": 1
            }
        },
        # CLIPTextEncode (Positive) - node 6
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["38", 0],
                "text": prompt
            }
        },
        # CLIPTextEncode (Negative) - node 7
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["38", 0],
                "text": ""
            }
        },
        # KSampler - node 3
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["66", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["58", 0],
                "seed": seed,
                "steps": 4,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0
            }
        },
        # VAEDecode - node 8
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["39", 0]
            }
        },
        # SaveImage - node 60
        "60": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["8", 0],
                "filename_prefix": filename_prefix
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
        response = session.post(
            f"{COMFYUI_URL}/prompt",
            json={"prompt": workflow},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def wait_for_completion(prompt_id, timeout=300):
    """Wait for generation to complete"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = session.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
            if response.status_code == 200:
                history = response.json()
                if prompt_id in history:
                    return history[prompt_id]
        except:
            pass
        time.sleep(3)
    return None

def generate_single(chapter_num, chapter_data):
    """Generate single chapter image"""
    title = chapter_data["title"]
    prompt = chapter_data["prompt"]
    filename = f"chapter_{chapter_num}"

    print(f"\n[{chapter_num}] {title}")
    print(f"    Prompt: {prompt[:60]}...")

    workflow = create_api_workflow(prompt, filename_prefix=filename)
    response = queue_prompt(workflow)

    if response and "prompt_id" in response:
        prompt_id = response["prompt_id"]
        print(f"    Queued: {prompt_id}")
        print(f"    Waiting for completion...")

        result = wait_for_completion(prompt_id, timeout=180)
        if result:
            print(f"    ✓ Completed!")
            return True
        else:
            print(f"    ✗ Timeout")
            return False
    else:
        print(f"    ✗ Failed to queue")
        return False

def generate_all_chapters():
    """Generate images for all chapters"""
    print("=" * 60)
    print("Generating chapter illustrations for 'Путь в АД'")
    print("Style: Dante's Inferno - dark, fire, spiraling circles of hell")
    print("=" * 60)

    # Check connection
    try:
        response = session.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        if response.status_code != 200:
            print("ERROR: ComfyUI not available!")
            return
        print("ComfyUI: Connected")
    except:
        print("ERROR: Cannot connect to ComfyUI!")
        return

    success = 0
    total = len(CHAPTERS)

    for chapter_num, chapter_data in CHAPTERS.items():
        if generate_single(chapter_num, chapter_data):
            success += 1
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"Generation complete: {success}/{total} images")
    print(f"Output: /home/jetmil/comfyui/output/")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Generate specific chapter
        ch = sys.argv[1].zfill(2)
        if ch in CHAPTERS:
            generate_single(ch, CHAPTERS[ch])
        else:
            print(f"Chapter {ch} not found!")
    else:
        # Generate all
        generate_all_chapters()
