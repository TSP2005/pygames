import os
import pygame


class Animations:
    def __init__(self, e_type, anim, dur, loop):
        common_path = 'data/entities'
        self.folder = common_path + '/' + e_type + '/' + anim
        self.anims = self.get_images()
        self.dur = dur
        self.current_frame = 0
        self.current_dur = dur[0]
        self.loop = loop

    def update(self):
        self.current_dur -= 1
        if self.current_dur <= 0:
            self.current_frame += 1
            if self.current_frame >= len(self.dur):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.dur) - 1
            self.current_dur = self.dur[self.current_frame]

    def render(self, surf, loc, scroll, flip):
        frame_img = self.anims[self.current_frame]
        if flip:
            frame_img = pygame.transform.flip(frame_img, True, False)
        surf.blit(frame_img, (loc[0] - scroll[0], loc[1] - scroll[1]))

    def get_images(self):
        images = []
        for file in os.listdir(self.folder):
            img_path = os.path.join(self.folder, file).replace("\\", "/")
            if os.path.isfile(img_path) and img_path.endswith('png'):
                img = pygame.image.load(img_path)
                images.append(img)
        return images

    def get_frame_width(self):
        return self.anims[0].get_width() if self.anims else 0

    def get_frame_height(self):
        return self.anims[0].get_height() if self.anims else 0

