package index;

import analyzer.SeparatorAnalyzer;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.FSDirectory;
import org.jfree.chart.ChartUtils;
import org.jfree.ui.RefineryUtilities;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import plot.GenGrafColonne;
import plot.GenGrafRighe;
import plot.GenGrafUniv;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class IndexWriter {

    String indexPath;

    String jsonFilePath;

    org.apache.lucene.index.IndexWriter indexWriter = null;

    int numeroTabelle;
    int sommaValoriNulli;
    Long sommaRigheTabelle;
    Long sommaColonneTabelle;
    HashMap<Long, Integer> disRighe = new HashMap<>();
    HashMap<Long, Integer> disColonne = new HashMap<>();
    HashMap<Integer, Integer> disValDist = new HashMap<>();

    public IndexWriter(String indexPath, String jsonFilePath) {
        this.indexPath = indexPath;
        this.jsonFilePath = jsonFilePath;
    }

    public static void main(String[] args) {
        IndexWriter indice = new IndexWriter("lucene-index", "src/main/resources/tables.json");
        indice.createIndex();
    }

    public void createIndex() {
        if (openIndex()) {
            parseJSONFile();
            finish();
        } else
            System.out.println("Errore nell'apertura dell'indice");
    }

    // metodo che memorizza le statistiche all interno di variabili
    public void statistiche(int numTabelle, Long sommaRigheTabelle, Long sommaColonneTabelle, int sommaValoriNulli,
                            HashMap<Long, Integer> dR, HashMap<Long, Integer> dC, HashMap<Integer, Integer> dVD) {
        double numMedioRighe = (double) sommaRigheTabelle / (double) numTabelle;
        double numMedioColonne = (double) sommaColonneTabelle / (double) numTabelle;
        double numMedioValNulli = (double) sommaValoriNulli / (double) numTabelle;

        // print dei valori
        System.out.println("numero tabelle " + numTabelle);
        System.out.println("numero di righe " + sommaRigheTabelle);
        System.out.println("numero di colonne " + sommaColonneTabelle);
        System.out.println("numero di valori nulli " + sommaValoriNulli);
        System.out.println("numero medio di righe " + numMedioRighe);
        System.out.println("numero medio di colonne " + numMedioColonne);
        System.out.println("numero medio di valori nulli " + numMedioValNulli);
        System.out.println("distribuzione numero di righe " + dR);
        System.out.println("distribuzione numero di colonne " + dC);
        System.out.println("distribuzione valori distinti " + dVD.toString());

        HashMap<Long, Integer> dR1 = new HashMap<>();
        HashMap<Long, Integer> dR2 = new HashMap<>();
        HashMap<Long, Integer> dC1 = new HashMap<>();
        HashMap<Integer, Integer> dVD1 = new HashMap<>();
        HashMap<Integer, Integer> dVD2 = new HashMap<>();

        // submap delle distribuzioni da 0 a 30
        for (int i = 0; i < 31; i++) {
            dR1.put((long) i, dR.get((long) i));
            dR2.put((long) i + 90, dR.get((long) i + 90));
            dC1.put((long) i, dC.get((long) i));
            dVD1.put(i, dVD.get(i));
            dVD2.put(i + 90, dVD.get(i + 90));
        }

        GenGrafRighe demo = new GenGrafRighe("Distribuzione Numero Di Righe da 0 a 30", dR1);
        demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);

        GenGrafRighe demo2 = new GenGrafRighe("Distribuzione Numero Di Righe da 90 a 120", dR2);
        demo2.pack();
        demo2.setVisible(false);

        GenGrafColonne demo3 = new GenGrafColonne("Distribuzione Numero Di Colonne", dC1);
        demo3.pack();
        demo3.setVisible(false);

        GenGrafUniv demo4 = new GenGrafUniv("Distribuzione Numero Di Valori Univoci da 0 a 30", dVD1);
        demo4.pack();

        demo4.setVisible(false);

        GenGrafUniv demo5 = new GenGrafUniv("Distribuzione Numero Di Valori Univoci da 90 a 120", dVD2);
        demo5.pack();
        demo5.setVisible(false);

        try {

            ChartUtils.saveChartAsJPEG(new File("charts/righe1.jpg"), demo.getChart(), 1500, 1000);
            ChartUtils.saveChartAsJPEG(new File("charts/righe2.jpg"), demo2.getChart(), 1500, 1000);
            ChartUtils.saveChartAsJPEG(new File("charts/colonne.jpg"), demo3.getChart(), 1500, 1000);
            ChartUtils.saveChartAsJPEG(new File("charts/valori1.jpg"), demo4.getChart(), 1500, 1000);
            ChartUtils.saveChartAsJPEG(new File("charts/valori2.jpg"), demo5.getChart(), 1500, 1000);

        } catch (IOException e) {

            System.err.println("Problema nella creazione dei grafici: " + e.getMessage());

        }

    }

    public HashMap<Long, Integer> creaMappa(Long n, HashMap<Long, Integer> map) {
        if (map.containsKey(n)) {
            map.put(n, map.get(n) + 1);
        } else {
            Integer i = 1;
            map.put(n, i);
        }
        return map;
    }


    public HashMap<Integer, Integer> creaMappaUnivoca(HashMap<Long, ArrayList<String>> map, HashMap<Integer, Integer> disVal) {

        for (Long k : map.keySet()) {
            Set<String> set = new HashSet<>(map.get(k));
            if (disVal.containsKey(set.size())) {
                disVal.put(set.size(), disVal.get(set.size()) + 1);
            } else {
                disVal.put(set.size(), 1);
            }
        }

        return disVal;

    }

    /**
     * Parse a Json file. The file path should be included in the constructor
     */
    public void parseJSONFile() {

        JSONParser jsonParser = new JSONParser();
        HashMap<Long, ArrayList<String>> colonna2elementi;

        try (BufferedReader br = new BufferedReader(new FileReader(jsonFilePath))) {
            String line;
            sommaRigheTabelle = 0L;
            sommaColonneTabelle = 0L;
            sommaValoriNulli = 0;

            while ((line = br.readLine()) != null) {

                numeroTabelle++;
                JSONObject jsonLine = (JSONObject) jsonParser.parse(line);
                String idTabella = (String) jsonLine.get("id");
                JSONArray cells = (JSONArray) jsonLine.get("cells");

                colonna2elementi = new HashMap<>();

                for (Object cell : cells) {
                    JSONObject cellJson = (JSONObject) cell;
                    String testo = (String) cellJson.get("cleanedText");
                    if (!isEmpty(testo)) {

                        if (cellJson.get("isHeader").equals(false)) {

                            JSONObject coordinate = (JSONObject) cellJson.get("Coordinates");
                            Long chiave = (Long) coordinate.get("column");

                            if (colonna2elementi.containsKey(chiave)) {
                                colonna2elementi.get(chiave).add(testo);
                            } else {
                                ArrayList<String> testi = new ArrayList<>();
                                testi.add(testo);
                                colonna2elementi.put(chiave, testi);
                            }
                        }
                    } else {
                        sommaValoriNulli++;
                    }

                }

                // per le stats
                JSONObject dim = (JSONObject) jsonLine.get("maxDimensions");
                sommaRigheTabelle = sommaRigheTabelle + ((Long) (dim.get("row")) + 1);
                sommaColonneTabelle = sommaColonneTabelle + ((Long) (dim.get("column")) + 1);

                disRighe = creaMappa(((Long) (dim.get("row")) + 1), disRighe);
                disColonne = creaMappa(((Long) (dim.get("column")) + 1), disColonne);
                disValDist = creaMappaUnivoca(colonna2elementi, disValDist);

                // Aggiunge le colonne come documenti in Lucene
                addDocuments(idTabella, colonna2elementi);
            }

            statistiche(numeroTabelle, sommaRigheTabelle, sommaColonneTabelle, sommaValoriNulli, disRighe, disColonne,
                    disValDist);

        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }

    }

    private boolean isEmpty(String cleanedText) {
        return (cleanedText.equals("") || cleanedText.equals("–") || cleanedText.equals("—") ||
                cleanedText.equals("N/A") || cleanedText.equals("N/A.") || cleanedText.equals("?"));
    }

    public boolean openIndex() {
        try {
            FSDirectory dir = FSDirectory.open(new File(indexPath).toPath());
            Analyzer analyzer = new SeparatorAnalyzer();
            IndexWriterConfig iwc = new IndexWriterConfig(analyzer);

            // Always overwrite the directory
            iwc.setOpenMode(OpenMode.CREATE);
            //iwc.setCodec(new SimpleTextCodec());
            indexWriter = new org.apache.lucene.index.IndexWriter(dir, iwc);
            indexWriter.deleteAll();
            return true;
        } catch (Exception e) {
            System.err.println("Error opening the index. " + e.getMessage());

        }
        return false;

    }

    /**
     * Add documents to the index
     */
    public void addDocuments(String idTabella, Map<Long, ArrayList<String>> colonna2elementi) {
        Document doc;
        for (Long colonna : colonna2elementi.keySet()) {
            doc = new Document();
            doc.add(new StringField("id", idTabella, Field.Store.YES));
            doc.add(new TextField("colonna", colonna.toString(), Field.Store.YES));
            doc.add(new TextField("testo", concatenaCelle(colonna2elementi.get(colonna), (char) 0x1F),
                    Field.Store.YES));

            try {
                indexWriter.addDocument(doc);
            } catch (IOException ex) {
                System.err.println("Error adding documents to the index. " + ex.getMessage());
            }
        }

    }

    public static String concatenaCelle(ArrayList<String> testi, char separatore) {
        StringBuilder result = new StringBuilder();
        for (String testo : testi) {
            result.append(testo).append(separatore);
        }
        return result.toString();
    }

    /**
     * Write the document to the index and close it
     */
    public void finish() {
        try {
            indexWriter.commit();
            indexWriter.close();
        } catch (IOException ex) {
            System.err.println("We had a problem closing the index: " + ex.getMessage());
        }
    }

}