import matplotlib.pyplot as plt
from io import BytesIO
import mpld3


class Visualization():

    def __init__(self, name: str, plot: plt.Figure):
        self.plot = plot
        self.name = name

    def get_image(self) -> bytes:
        buffer = self._to_bytes("png")
        return buffer.getvalue()

    def get_interactive(self) -> str:
        """Returns figure in format suitable for
        interactive display on web page
        """
        return mpld3.fig_to_html(self.plot)

    def get_file_in_format(self, format: str) -> bytes:
        """Returns plot in requested format see
        valid_formats
        Args:
            format (str): format of file
        """
        valid_formats = ["png", "svg", "pdf"]
        if format not in valid_formats:
            raise ValueError(f"Unallowed format: {format}. \
                See: {valid_formats}")

        return self._to_bytes(format)

    def _to_bytes(self, format) -> bytes:
        result = BytesIO()
        self.plot.savefig(result, format=format, bbox_inches="tight")
        result.seek(0)
        return result
