package search;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.MultiTerms;
import org.apache.lucene.index.PostingsEnum;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class MergeListSearch {
    private final IndexReader reader;
    private final IndexSearcher searcher;

    public MergeListSearch(String indexLocation) throws IOException {
        this.reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation).toPath()));
        this.searcher = new IndexSearcher(this.reader);

    }

    /**
     * Aggiorna la mappa set2count che contiene per ogni set di colonne (chiave) il numero di volte che è stato trovato.
     * Si prende la posting list del termine e si aggiorna la mappa per ogni documento che contiene il termine.
     */
    public Map<Integer, Integer> updateMap(Map<Integer, Integer> set2count, String termine) {
        PostingsEnum postingList = getTermPostingList(termine);

        try {
            if (postingList != null) {
                int docId;
                System.out.print("Posting list for term " + termine + ": ");
                while ((docId = postingList.nextDoc()) != PostingsEnum.NO_MORE_DOCS) {
                    System.out.print(docId + ", ");
                    if (set2count.get(docId) == null) {
                        set2count.put(docId, 1);
                    } else {
                        set2count.put(docId, set2count.get(docId) + 1);
                    }
                }
                System.out.println();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return set2count;
    }


    /**
     * Restituisce la posting list per un certo termine.
     */
    private PostingsEnum getTermPostingList(String termine) {

        PostingsEnum postingList = null;

        try {
            postingList = MultiTerms.getTermPostingsEnum(getReader(), "testo",
                    new BytesRef(termine), PostingsEnum.NONE);

        } catch (IOException e) {
            e.printStackTrace();
        }

        return postingList;
    }

    private IndexReader getReader() {
        return this.reader;
    }

    /**
     * Stampa i risultati della query
     */
    public void printQuery(Map<Integer, Integer> set2count, long startTime, long endTime) throws IOException {
        // Ordina la mappa in base al numero di volte che è stato trovato (values)
        List<Map.Entry<Integer, Integer>> list = new LinkedList<>(set2count.entrySet());
        list.sort((o1, o2) -> (o2.getValue()).compareTo(o1.getValue()));

        int dim = list.size();

        // Stampa i risultati
        System.out.println("I set sono stati trovati in " + (endTime - startTime) / 1000000 + " millisecondi.");
        if (dim > 0) {
            if (dim > 10) { // Stampa solo i primi 10 risultati
                dim = 10;
            }
            System.out.println("Primi " + dim + " risultati in ordine di score:");
            for (int i = 0; i < dim; i++) {
                int docId = list.get(i).getKey();
                int score = list.get(i).getValue();
                Document d = searcher.doc(docId);
                System.out.println((i + 1) + "- docId: " + docId + ", idTabella: " + d.get("id") + ", colonna: " +
                        d.get("colonna") + ", score = " + score);
            }

        }
        System.out.println();
    }

    public void search(ArrayList<String> termini) throws IOException {
        Map<Integer, Integer> set2count = new HashMap<>();

        long startTime, endTime;
        startTime = System.nanoTime();
        for (String termine : termini) {
            set2count = updateMap(set2count, termine);
        }
        endTime = System.nanoTime();

        printQuery(set2count, startTime, endTime);
    }

}