
from ..results.utils import parser_factory
from VisualizationOptions import VisualizationOptions as VisOpt
import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from Visualization import Visualization
from DistributionsPlotter import DistributionPlotter


class PlotGenerator():
    """Factory class for visual representation of results"""

    def __init__(self, processing_obj):
        self.parser = parser_factory(processing_obj=processing_obj)
        self.available_visualizations = []

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
        if plot_types is None:
            return [Visualization(*data) for data in disPlt.all_plots()]
        result = []
        for plot_type in plot_types:
            if plot_type not in disPlt.AVAILABLE_PLOTS:
                raise ValueError(
                    f"Type must be in \
                    DistributionPlotter.AVAILABLE_PLOTS = \
                    {disPlt.AVAILABLE_PLOTS}\
                    but got {plot_type}"
                )
            name, fig = disPlt.call(plot_type)
            Vis = Visualization(name, fig)
            result.append(Vis)
        return result

    def _plot_relations_graph(self) -> plt.Figure:
        G = nx.Graph()

        for i, sample in enumerate(self.parser.sample_list):
            G.add_node(i, object=sample)

        for i in range(len(self.parser.sample_list)):
            for j in range(i + 1, len(self.parser.sample_list)):
                similarity = (
                    self.parser
                    .sample_list[i]
                    .get_similarity(self.parser.sample_list[j])
                )

                G.add_edge(i, j, weight=similarity)

        pos = nx.spring_layout(G)
        edges = G.edges(data=True)
        weights = [edge[2]['weight'] * 5 for edge in edges]

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)

        pos = nx.spring_layout(G)
        edges = G.edges(data=True)
        weights = [edge[2]['weight'] * 2 for edge in edges]

        nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_size=500, node_color='skyblue'
        )
        nx.draw_networkx_edges(G, pos, ax=ax, width=weights, edge_color='gray')
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)

        ax.set_title("Граф схожести объектов", fontsize=14)
        ax.axis('off')
        return Visualization("Relations Graph", fig)

    def _plot_word_cloud(self) -> plt.Figure:
        wordcloud = WordCloud(
            background_color='white',
            width=800,
            height=600
        ).generate(" ".join(self.parser.get_tokens))

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')

        return Visualization("Word Cloud", fig)

    def get_all_available_figures(self) -> list[Visualization]:
        results = []
        for fig_type in self.available_visualizations:
            match fig_type:
                case VisOpt.REL_GRAPHS:
                    results.append(self._plot_relations_graph())
                case VisOpt.WORD_CLOUD:
                    results.append(self._plot_word_cloud())
                case VisOpt.DISTRIBUTION:
                    results.extend(self._plot_distribution)
        return results
