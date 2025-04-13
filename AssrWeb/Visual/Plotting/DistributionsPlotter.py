import matplotlib.pyplot as plt
import seaborn as sns


class DistributionPlotter:  # Параметры для отображения украдены из различных 
    # гайдов и не являются осмысленными 
    """Class to generate various distribution plots for data from parser"""
    AVAILABLE_PLOTS = ["violin", "hist", "kde", "box", "combined"]

    def __init__(self, figsize: tuple = (10, 6), style: str = 'seaborn-v0_8'):
        self.figsize = figsize
        self.style = style
        plt.style.use(style)

    def call(self, data, plot_type):
        if plot_type == "violin":
            return self.violin_plot(data)
        if plot_type == "hist":
            return self.histogram(data)
        if plot_type == "kde":
            return self.kde_plot(data)
        if plot_type == "box":
            return self.box_plot(data)
        if plot_type == "combined":
            return self.combined_plot(data)

    def histogram(
        self,
        data: list[float],
        bins: str | int = 'auto',
        color: str = 'skyblue',
        edgecolor: str = 'black',
        title: str = 'Histogram Distribution',
        xlabel: str = 'Values',
        ylabel: str = 'Frequency'
    ) -> plt.Figure:

        """
        Create a histogram plot

        Args:
            bins: Number of bins or 'auto' for automatic calculation
            color: Fill color for bars
            edgecolor: Edge color for bars.

        """
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.hist(data, 
                bins=bins,
                color=color,
                edgecolor=edgecolor,
                alpha=0.7)

        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        return "hist plot", self._config_fig(ax, ylabel, fig)

    def kde_plot(
        self,
        data: list[float],
        color: str = 'blue',
        fill: bool = True,
        title: str = 'Kernel Density Estimation',
        xlabel: str = 'Values',
        ylabel: str = 'Density'
    ) -> plt.Figure:
        """
        Create a Kernel Density Estimation plot

        Args:
            color: Line color for KDE
            fill: Whether to fill under the curve
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.kdeplot(
            data,
            ax=ax,
            color=color,
            fill=fill,
            alpha=0.3 if fill else 1.0,
            linewidth=2
        )

        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        return "KDE plot", self._config_fig(ax, ylabel, fig)

    def box_plot(
        self,
        data: list[float],
        vert: bool = True,
        color: str = 'lightblue',
        median_color: str = 'red',
        title: str = 'Boxplot',
        ylabel: str = 'Values'
    ) -> plt.Figure:
        """
        Create a box plot

        Args:
            vert: Whether to draw vertical boxplot
            color: Box fill color
            median_color: Median line color

        """
        fig, ax = plt.subplots(figsize=self.figsize)

        box = ax.boxplot(
            data,
            vert=vert,
            patch_artist=True,
            showfliers=True
        )

        box['boxes'][0].set_facecolor(color)
        box['medians'][0].set_color(median_color)
        box['medians'][0].set_linewidth(2)

        ax.set_title(title, fontsize=16)
        return "box plot", self._config_fig(ax, ylabel, fig)

    def combined_plot(
        self,
        data: list[float],
        bins: str | int = 'auto',
        hist_color: str = 'skyblue',
        kde_color: str = 'blue',
        title: str = 'Combined Histogram and KDE',
        xlabel: str = 'Values',
        ylabel: str = 'Density'
    ) -> plt.Figure:
        """
        Create a combined histogram and KDE plot

        Args:
            bins: Number of bins for histogram
            hist_color: Histogram fill color
            kde_color: KDE line color

        """
        fig, ax = plt.subplots(figsize=self.figsize)

        ax.hist(data,
                bins=bins,
                density=True,
                color=hist_color,
                edgecolor='black',
                alpha=0.5,
                label='Histogram')

        sns.kdeplot(
            data,
            ax=ax,
            color=kde_color,
            linewidth=2,
            label='KDE'
        )

        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        return "combined", self._config_fig(ax, ylabel, fig)

    def violin_plot(
        self,
        data: list[float],
        color: str = 'lightblue',
        title: str = 'Violin Plot',
        ylabel: str = 'Values'
    ) -> plt.Figure:
        """
        Create a violin plot (combination of boxplot and KDE)

        Args:
            data: List of numerical values
            color: Fill color for violins
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        sns.violinplot(
            y=data,
            ax=ax,
            color=color,
            inner='quartile'
        )

        ax.set_title(title, fontsize=16)
        return "violin", self._config_fig(ax, ylabel, fig)

    def _config_fig(self, ax, ylabel, fig):
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        return fig

    def all_plots(self, data):
        return [
            self.histogram(data),
            self.kde_plot(data),
            self.box_plot(data),
            self.combined_plot(data),
            self.violin_plot(data)
        ]
