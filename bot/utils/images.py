import discord
from typing import Dict, Tuple, List
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

from models.tile import TileState
from state.state import state
from utils.board import neighbor_map

COORDINATES: Dict[int, Tuple[int, int]] = {
    # Middle tiles
    1: (600, 32),
    2: (600, 184),
    3: (600, 465),
    4: (600, 592),
    5: (600, 719),
    6: (600, 1050),
    # Side tiles
    7: (447, 160),
    8: (752, 160),
    9: (219, 211),
    10: (981, 211),
    11: (473, 338),
    12: (727, 338),
    13: (193, 389),
    14: (1007, 389),
    15: (320, 440),
    16: (880, 440),
    17: (447, 541),
    18: (752, 541),
    19: (295, 618),
    20: (905, 618),
    21: (447, 694),
    22: (752, 694),
    23: (168, 770),
    24: (1032, 770),
    25: (346, 847),
    26: (524, 847),
    27: (676, 847),
    28: (854, 847),
    29: (40, 973),
    30: (244, 973),
    31: (447, 973),
    32: (754, 973),
    33: (956, 973),
    34: (1159, 973),
    35: (346, 1101),
    36: (854, 1101),
}


def bytes_to_file(b: BytesIO, id: int) -> discord.File:
    return discord.File(fp=b, filename=f"{id}.png")


@dataclass
class ImageState:
    images: Dict[int, discord.File]

    def get_image(self, team_id: int) -> discord.File | None:
        image = self.images.get(team_id)
        if not image:
            return self.generate_image(team_id)
        return image

    def set_image(
        self, team_id: int, image: discord.File | BytesIO | Image.Image
    ) -> bool:
        if isinstance(image, BytesIO):
            image = bytes_to_file(image, team_id)

        if isinstance(image, Image.Image):
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            image = bytes_to_file(image_bytes, team_id)

        self.images[team_id] = image
        return True

    def generate_image(self, team_id: int):
        tiles = [node.value for node in state.teams[team_id].board.get_nodes().values()]

        lines: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

        # Draw lines
        for current, neighbors in neighbor_map.items():
            for neighbor in neighbors:
                # Add 50px to x and y to center the line
                start = (
                    COORDINATES[current][0] + 50,
                    COORDINATES[current][1] + 50,
                )
                end = (
                    COORDINATES[neighbor][0] + 50,
                    COORDINATES[neighbor][1] + 50,
                )

                lines.append((start, end))

        # Green overlay with 100/255 opacity
        accepted_color = (20, 255, 20, 100)

        # Create a new image with higher resolution
        temp_size = (1300 * 2, 1300 * 2)

        temp_image = Image.new("RGB", temp_size, (255, 255, 255))
        draw = ImageDraw.Draw(temp_image)

        # Draw line in the higher resolution
        for line in lines:
            draw.line(
                [
                    tuple(coord * 2 for coord in line[0]),
                    tuple(coord * 2 for coord in line[1]),
                ],
                fill="black",
                width=20,
            )

        # Resize the image back to original size with antialiasing
        image = temp_image.resize((1300, 1300), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(image)

        # Font setup
        font_size = 30
        font = ImageFont.truetype("FreeMono.ttf", font_size)

        for tile in tiles:
            if tile.id not in COORDINATES.keys():
                continue

            red = (tile.theme.value >> 16) & 0xFF
            green = (tile.theme.value >> 8) & 0xFF
            blue = tile.theme.value & 0xFF

            tile_background = Image.new("RGB", (100, 100), (red, green, blue))

            image.paste(tile_background, COORDINATES[tile.id])
            draw.text(
                tuple(coordinate + 5 for coordinate in COORDINATES[tile.id]),
                str(tile.id),
                font=font,
                fill="black",
            )

            if tile.state == TileState.LOCKED:
                continue

            # Fetch the image from the URL and resize it to 100x100
            response = requests.get(tile.image, stream=True)
            tile_image = Image.open(response.raw).resize((92, 92))

            if tile.state == TileState.COMPLETED:
                accepted_overlay = Image.new("RGBA", tile_image.size, accepted_color)
                tile_image = Image.alpha_composite(
                    tile_image.convert("RGBA"), accepted_overlay
                )

            image.paste(
                tile_image, tuple(coordinate + 4 for coordinate in COORDINATES[tile.id])
            )

        self.set_image(team_id, image)
        return self.get_image(team_id)

    def remove_image(self, team_id: int):
        self.images.pop(team_id)


images = ImageState({})
