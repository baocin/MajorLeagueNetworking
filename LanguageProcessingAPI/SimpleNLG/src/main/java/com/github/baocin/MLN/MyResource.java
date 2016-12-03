package com.github.baocin.MLN;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;


import simplenlg.framework.NLGFactory;
import simplenlg.lexicon.Lexicon;
import simplenlg.phrasespec.SPhraseSpec;
import simplenlg.realiser.english.Realiser;

/**
 * Root resource (exposed at "myresource" path)
 */
@Path("makeSentence")
public class MyResource {
	Lexicon lexicon;
	NLGFactory nlgFactory;
	Realiser realiser;
	
	public MyResource(){
		lexicon = Lexicon.getDefaultLexicon();
	    nlgFactory = new NLGFactory(lexicon);
	    realiser = new Realiser(lexicon);
	}
    /**
     * Method handling HTTP GET requests. The returned object will be sent
     * to the client as "text/plain" media type.
     *
     * @return String that will be returned as a text/plain response.
     */
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public String getIt(@QueryParam("subject") String subject, @QueryParam("object") String obj, @QueryParam("verb") String verb) {
    	try{
    		return generateSentence(subject, obj, verb);
    	}catch(Exception e){
    		System.out.println(e);
    	}
    	return "";
    }
    
    public String generateSentence(String subject, String obj, String verb){
		    
		/*'{"3": [{"subject": "Golden State Warriors coach Steve Kerr", 
		 * "subjectType": "ORGANIZATION", "object": 
		 * "CSN Bay Area podcast published Friday", "subjectSpan": [4, 10],
		 *  "objectSpan": [13, 19], "relationSpan": [10, 12], "relation": "said on", "objectType": "ORGANIZATION"}, {"subject": "Golden State Warriors coach Steve Kerr", "subjectType": "ORGANIZATION", "object": "CSN Bay Area podcast published", "subjectSpan": [4, 10], "objectSpan": [13, 18], "relationSpan": [10, 12], "relation": "said on", "objectType": "ORGANIZATION"}, {"subject": "Steve Kerr", "subjectType": "PERSON", "object": "Golden State Warriors", "subjectSpan": [8, 10], "objectSpan": [4, 7], "relationSpan": [7, 8], "relation": "is coach of", "objectType": "ORGANIZATION"}, {"subject": "Golden State Warriors coach Steve Kerr", "subjectType": "ORGANIZATION", "object": "CSN Bay Area podcast", "subjectSpan": [4, 10], "objectSpan": [13, 17], "relationSpan": [10, 12], "relation": "said on", "objectType": "ORGANIZATION"}, {"subject": "Steve Kerr", "subjectType": "PERSON", "object": "Golden State Warriors", "subjectSpan": [8, 10], "objectSpan": [4, 7], "relationSpan": [4, 7], "relation": "is", "objectType": "ORGANIZATION"}], "4": [{"subject": "Adam Silver", "subjectType": "PERSON", "object": "NBA", "subjectSpan": [10, 12], "objectSpan": [8, 9], "relationSpan": [9, 10], "relation": "is commissioner of", "objectType": "ORGANIZATION"}, {"subject": "Adam Silver", "subjectType": "PERSON", "object": "NBA", "subjectSpan": [10, 12], "objectSpan": [8, 9], "relationSpan": [8, 9], "relation": "is", "objectType": "ORGANIZATION"}]}',
		 */
    	
		SPhraseSpec p = nlgFactory.createClause();
	    p.setSubject(subject);
	    p.setVerb(verb);
	    p.setObject(obj);
	    
	    String resultSentence = realiser.realiseSentence(p);
	    
	    System.out.println(resultSentence);
		return(resultSentence);
    }
}
