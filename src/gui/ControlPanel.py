import tkinter as tk

class ControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.on_next = None
        self.on_reset = None

        self.display_message = tk.Label(self, text="", font=("Arial", 16), fg="white")
        self.display_message.pack()

        self.next_button = tk.Button(self, text="Next", command=self._handle_next)
        self.next_button.pack()

        self.reset_button = tk.Button(self, text="Reset", command=self._handle_reset)
        self.reset_button.pack()

        self.press_button_notice = tk.Label(self, text="You can also hold SPACE to perform the next steps", font=("Arial", 16), fg="white")
        self.press_button_notice.pack()

        parent.bind("<space>", self._key_press_next)
        parent.bind("<KeyRelease-space>", self._key_release_next)

        self._auto_step_job = None 

    def _handle_next(self):
        if self.on_next:
            self.on_next()
    
    def _key_press_next(self, event):
        if self._auto_step_job is None:
            self._handle_next()       # do one step
            self._auto_step_job = self.after(300, self._schedule_auto_step)  
            # wait a bit before repeating, like keyboard key repeat

    def _key_release_next(self, event):
        """Stop auto-repeat when key is released."""
        if self._auto_step_job is not None:
            self.after_cancel(self._auto_step_job)
            self._auto_step_job = None

    def _schedule_auto_step(self):
        """Keep stepping repeatedly while key is held."""
        self._handle_next()
        self._auto_step_job = self.after(100, self._schedule_auto_step)  
        # 100 ms = 10 steps/sec (adjust speed as you like)

    def _handle_reset(self):
        if self.on_reset:
            self.on_reset()