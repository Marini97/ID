package analyzer;

import org.apache.lucene.analysis.util.CharTokenizer;

public class SeparatorTokenizer extends CharTokenizer {

    @Override
    protected boolean isTokenChar(int i) {
        return i != 31;
    }
}
