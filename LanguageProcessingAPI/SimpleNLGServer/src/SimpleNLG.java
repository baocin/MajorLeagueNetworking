/**
 * Spark Server interface for Simple NLG 
 */
import static spark.Spark.*;
import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;

/**
 * @author aoi
 *
 */
public class SimpleNLG {
//	Lexicon lexicon;
//	NLGFactory nlgFactory;
//	Realiser realiser;
//	
//	public SimpleNLG(){
//		lexicon = Lexicon.getDefaultLexicon();
//		nlgFactory = new NLGFactory(lexicon);
//		realiser = new Realiser(lexicon);
//	}
//	
	
	public static void main(String[] args) {
		Lexicon lexicon = Lexicon.getDefaultLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);
        
        
        get("/hello", (req, res) -> "Hello World");
    }

	private void generateSentence(String subject, String relation, String object){
			
	}
}

