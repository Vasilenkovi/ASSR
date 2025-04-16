
from ..results.utils import parser_factory
from .VisualizationOptions import VisualizationOptions as VisOpt
import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from .Visualization import Visualization
from .DistributionsPlotter import DistributionPlotter


class PlotGenerator():
    """Factory class for visual representation of results"""

    def __init__(self, processing_obj):
        self.parser = parser_factory(processing_obj=processing_obj)
        self.available_visualizations = []
        self._check_visualizations_options()

    def _check_visualizations_options(self) -> None:
        for method in self.parser.get_implemented_sample_methods():
            if method in VisOpt.REL_GRAPH_OPTIONS[VisOpt.REL_GRAPH]:
                self.available_visualizations.append(VisOpt.REL_GRAPH)
            if method in VisOpt.DISTRIBUTION_OPTIONS[VisOpt.DISTRIBUTION]:
                self.available_visualizations.append(VisOpt.DISTRIBUTION)
            if method in VisOpt.WORD_CLOUD_OPTIONS[VisOpt.WORD_CLOUD]:
                self.available_visualizations.append(VisOpt.WORD_CLOUD)

    def _plot_distribution(
        self,
        plot_types: list[str] = None
    ) -> list[
        tuple[str, plt.Figure]
    ]:
        """Returns distributions of requested types

        Args:
            plot_types (list[str], optional): list of requested types (look in
            the DistributionPlotter.AVAILABLE_PLOTS). Defaults to None.
        """
        disPlt = DistributionPlotter()
        samples = self.parser.sample_list
        data_list = [sample.get_values() for sample in samples]
        data_labeled = {
            label: [] for label in self.parser.sample_label_lookup
        }

        for sample_data in data_list:
            for value, label in zip(sample_data, data_labeled.keys()):
                data_labeled[label].append(value)

        result = []
        if plot_types is None:
            plot_types = disPlt.AVAILABLE_PLOTS

        for label, values in data_labeled.items():
            for plot_type in plot_types:
                if plot_type not in disPlt.AVAILABLE_PLOTS:
                    raise ValueError(
                        "Type must be in" +
                        "DistributionPlotter.AVAILABLE_PLOTS =" +
                        f"{disPlt.AVAILABLE_PLOTS}" +
                        f"but got {plot_type}"
                    )

                name, fig = disPlt.call(values, plot_type)
                vis = Visualization(name, fig)
                vis.label = label
                result.append(vis)
        return result

    def _plot_relations_graph(self) -> plt.Figure:
        G = nx.Graph()
        samples = self.parser.sample_list
        max_samples = 100
        samples = samples[:max_samples]

        for i in range(len(samples)):
            for j in range(i + 1, len(samples)):
                if (j - i) > 5:
                    continue
                similarity = samples[i].get_similarity(samples[j])
                if similarity >= 0.3:
                    G.add_edge(i, j, weight=similarity)

        if len(G.edges()) == 0:
            return Visualization(plt.figure())

        pos = nx.spring_layout(G, seed=42, k=0.5)

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)

        edges = G.edges(data=True)
        edge_weights = [e[2]['weight'] for e in edges]

        cmap = plt.cm.get_cmap('plasma')
        edge_colors = [w for w in edge_weights]
        edge_widths = [w*8 for w in edge_weights]

        nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_size=700,
            node_color='lightblue',
            edgecolors='grey',
            linewidths=1.5
        )

        edges = nx.draw_networkx_edges(
            G, pos, ax=ax,
            width=edge_widths,
            edge_color=edge_colors,
            edge_cmap=cmap,
            edge_vmin=0.3,
            edge_vmax=1.0,
            alpha=0.8
        )

        sm = plt.cm.ScalarMappable(
            cmap=cmap,
            norm=plt.Normalize(vmin=0.3, vmax=1.0)
        )
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
        cbar.set_label('Степень схожести', fontsize=12)

        nx.draw_networkx_labels(
            G,
            pos,
            ax=ax,
            font_size=10,
            font_weight='bold'
        )

        ax.set_title("Граф схожести объектов", fontsize=14, pad=20)
        ax.axis('off')
        plt.tight_layout()
        return Visualization("Relations Graph", fig)

    def _plot_word_cloud(self) -> plt.Figure:
        wordcloud = WordCloud(
            background_color='white',
            width=800,
            height=600
        ).generate(
            " ".join(
                [
                    " ".join(tokens.get_tokens()) for tokens in self.
                    parser.
                    sample_list
                ]
            )
        )

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')

        return Visualization("Word Cloud", fig)

    def get_all_available_figures(self) -> list[Visualization]:
        non_distribution = []
        distributions = []

        for fig_type in self.available_visualizations:
            match fig_type:
                case VisOpt.REL_GRAPH:
                    vis = self._plot_relations_graph()
                    non_distribution.append(vis)
                case VisOpt.WORD_CLOUD:
                    vis = self._plot_word_cloud()
                    non_distribution.append(vis)
                case VisOpt.DISTRIBUTION:
                    dist_plots = self._plot_distribution()
                    distributions.extend(dist_plots)

        return non_distribution + distributions
