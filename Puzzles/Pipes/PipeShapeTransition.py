﻿from Pipes.PipeShape import PipeShape


class PipeShapeTransition:
    def __init__(self, initial_pipe_shape: PipeShape, final_pipe_shape: PipeShape):
        if initial_pipe_shape.shape != final_pipe_shape.shape:
            raise ValueError("Pipe shapes must be of the same type")
        self.shape = final_pipe_shape
        self.initial_clockwise_rotation = initial_pipe_shape.clockwise_rotation
        self.final_clockwise_rotation = final_pipe_shape.clockwise_rotation
        self.clockwise_rotation = self.get_clockwise_rotation()
        self.counterclockwise_rotation = (4 - self.clockwise_rotation) % 4

    def __str__(self):
        return str(self.shape)

    def __repr__(self):
        return str(self.shape)

    def get_clockwise_rotation(self):
        diff = self.final_clockwise_rotation - self.initial_clockwise_rotation
        if self.shape == 'I':
            return 0 if diff == 0 else 1
        return (diff + 4) % 4
