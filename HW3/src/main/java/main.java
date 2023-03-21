import search.MergeListSearch;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class main {
    public static void main(String[] args) throws IOException {
        //call to mergeListSearch
        MergeListSearch mergeListSearch = new MergeListSearch("lucene-index");

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = "";
        ArrayList<String> query = new ArrayList<>();

        // Ciclo di ricerca. Termina quando viene inserita la stringa "q"
        System.out.println("Inserire i termini da ricercare: (q per uscire)");
        while (!s.equalsIgnoreCase("q")) {
            try {
                s = br.readLine();
                if (s.equalsIgnoreCase("q")) {
                    break;
                }
                query.add(s);

            } catch (Exception e) {
                System.out.println("Errore nella ricerca di " + s + " : " + e.getMessage());
            }
        }

        mergeListSearch.search(query);
    }
}
