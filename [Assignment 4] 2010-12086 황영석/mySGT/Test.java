package mySGT;

import java.io.IOException;

public class Test {
	public static void main(String[] args) throws IOException {
		Surfer sf = new Surfer();
		
		String startURL = "http://en.wikipedia.org/wiki/Data_mining";  
		int maxPage = 30;
		
		sf.surfer(startURL, maxPage);
		sf.drawCloud();
	}
}