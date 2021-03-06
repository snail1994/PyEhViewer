import os

import ui

from core.pygestures import GestureView 
from core.utility import get_coordinate

class ImageWithGestureView (GestureView):
    def __init__(self, **kwargs):
        super().__init__()
        self.frame = kwargs.get('frame')
        image_file = kwargs.get('image_file')
        self.name = kwargs.get('name')
        self.action_prev = kwargs.get('action_prev')
        self.action_next = kwargs.get('action_next')
        image = ui.Image.named(image_file)
        w, h = image.size
        if os.path.splitext(image_file)[1].lower() != '.gif':
            self.imageview = ui.ImageView(
                frame=get_coordinate(0, 0, self.width, self.height, w, h),
                image=image,
                name='imageview'
                )
            self.add_subview(self.imageview)
        else:
            self.imageview = ui.ImageView(
                frame=get_coordinate(0, 0, self.width, self.height, w, h),
                name='imageview'
                )
            if w < self.width and h < self.height:
                v = ui.WebView(
                    background_color='white',
                    height=h,
                    touch_enabled=False,
                    width=w
                    )
                v.center=self.imageview.center
                line_flag = False
            else:
                v = ui.WebView(
                    background_color='white',
                    frame=get_coordinate(0, 0, self.width, self.height, w, h),
                    touch_enabled=False
                    )
                line_flag = True
            v.load_url(image_file)
            self.add_subview(v)
            if line_flag:
                self.add_subview(ui.ImageView(
                    background_color='white',
                    frame=(0, v.y + v.height - 1, self.width, 1)
                    ))
            self.add_subview(self.imageview)
        self.x_prev, self.y_prev, self.w_prev, self.h_prev = self['imageview'].frame
        self.x_orginal, self.y_orginal, self.w_orginal, self.h_orginal = self['imageview'].frame

    def on_pan(self, data):
        if data.no_of_touches == 1:
            if data.state == 1:
                self.x_prev, self.y_prev, self.w_prev, self.h_prev = self['imageview'].frame
            elif data.state in [2, -1]:
                if (self.w_prev > self.w_orginal and
                    self.x_prev + data.translation[0] + self.w_prev >= self.x_orginal + self.w_orginal and
                    self.x_prev + data.translation[0] <= self.x_orginal):
                    self['imageview'].x = self.x_prev + data.translation[0]
                if (self.h_prev > self.h_orginal and
                    self.y_prev + data.translation[1] + self.h_prev >= self.y_orginal + self.h_orginal and
                    self.y_prev + data.translation[1] <= self.y_orginal):
                    self['imageview'].y = self.y_prev + data.translation[1]
        
    def on_pinch(self, data):
        if data.state == 1:
            self.x_prev, self.y_prev, self.w_prev, self.h_prev = self['imageview'].frame
            self.location_prev = data.location
            #print(self.location_prev)
        elif data.state == 2 and data.scale:
            self['imageview'].frame = (
                self.location_prev[0] * (1 - data.scale) + data.scale * self.x_prev,
                self.location_prev[1] * (1 - data.scale) + data.scale * self.y_prev,
                self.w_prev * data.scale,
                self.h_prev * data.scale
                )
        elif data.state == -1 and data.scale:
            if self.w_prev * data.scale <= self.w_orginal:
                self['imageview'].frame = (self.x_orginal, self.y_orginal, self.w_orginal, self.h_orginal)
            else:
                self['imageview'].frame = (
                self.location_prev[0] * (1 - data.scale) + data.scale * self.x_prev,
                self.location_prev[1] * (1 - data.scale) + data.scale * self.y_prev,
                self.w_prev * data.scale,
                self.h_prev * data.scale
                )
        else:
            self['imageview'].frame = (self.x_orginal, self.y_orginal, self.w_orginal, self.h_orginal)

    def on_tap(self, data):
        if data.no_of_touches == 1:
            if data.location[1] <= self.height/2:
                self.action_prev()
            else:
                self.action_next()
