package plot;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.ui.ApplicationFrame;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class GenGrafColonne extends ApplicationFrame {

    private final JFreeChart chart;

    public GenGrafColonne(final String titolo, HashMap<Long, Integer> map) {
        super(titolo);
        final DefaultCategoryDataset dataset = createDataset(map);
        chart = ChartFactory.createBarChart(titolo, "Numero di colonne", "Quantità",
                dataset, PlotOrientation.VERTICAL, false, true, false);
        final ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 270));
        setContentPane(chartPanel);
    }

    /**
     * Creazione del dataset da utilizzare per la generazione del grafi
     * Ogni grafico ha un suo dataset specifico
     *
     * @return un dataset di default.
     */
    private DefaultCategoryDataset createDataset(HashMap<Long, Integer> map) {
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        List<Long> lista = new ArrayList<>(map.keySet());
        for (Long l : lista) {
            dataset.setValue(map.get(l), "Quantità", l);
        }

        return dataset;
    }

    public JFreeChart getChart() {
        return chart;
    }
}