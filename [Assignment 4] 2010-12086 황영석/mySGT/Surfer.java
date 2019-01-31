package mySGT;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.mcavallo.opencloud.Cloud;
import org.mcavallo.opencloud.Tag;

public class Surfer {
	List<Elements> keywordList = new ArrayList<Elements>();
	
	String baseUrl = "http://en.wikipedia.org";
	String checkUrl = "/wiki/";
	
	String fileUrl = "/wiki/File:";
	String exceptUrl = "/wiki/Wikipedia:";
	String uselessUrl1 = "/wiki/International_Standard_Book_Number";
	String uselessUrl2 = "/wiki/Digital_object_identifier";

	// check validUrl
	public boolean isValidUrl(String url) {
		// check if the url only have two slashes
		boolean hasTwoSlash = false;
		int length = url.length();
		int slashCount = 0;
		for (int i = 0; i < length; i++) {
			if (url.charAt(i) == '/')	slashCount++;
		}
		if (slashCount == 2)	hasTwoSlash = true;
		
		return url.startsWith(checkUrl) && hasTwoSlash && !url.startsWith(fileUrl) && !url.startsWith(exceptUrl)&&!url.startsWith(uselessUrl1)&&!url.startsWith(uselessUrl2); 
	}

	public void surfer(String firstLink, int maxPage) throws IOException {
		String landingLink = firstLink;
		Queue<String> que = new LinkedList<String>();

		int cnt = 1;
		// Breath First Search
		for (int page = 0; page < maxPage; page++) {
			Document randoc = Jsoup.connect(landingLink).get();
			Elements atags = randoc.select("div[id=mw-content-text] a[href]");
			Elements keywords = new Elements();
			
			for (Element atag : atags) {
				if (isValidUrl(atag.attr("href"))) {
//					System.out.println(page + "-" + cnt + " " + baseUrl + atag.attr("href"));
					keywords.add(atag);
					que.add(baseUrl + atag.attr("href"));
					cnt += 1;
				}
				keywordList.add(keywords);
			}
			landingLink = que.poll();
		}
	}

	public void drawCloud() {
		Cloud cloud = new Cloud();
		cloud.setMaxWeight(100.0);
		for (Elements keywords : keywordList) {
			for (Element e : keywords) {
//				System.out.println("Add tag: " + e.attr("title"));
				cloud.addTag(e.attr("title"));
			}
		}

		// Java Swing GUI
		JFrame frame = new JFrame(Surfer.class.getSimpleName());
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		JPanel panel = new JPanel();

		for (Tag tag : cloud.tags()) {
			final JLabel label = new JLabel(tag.getName());
			label.setOpaque(false);
			label.setFont(label.getFont().deriveFont((float) tag.getWeight()/2));
			panel.add(label);
		}
		frame.add(panel);
		frame.setSize(800, 600);
		frame.setVisible(true);
	}
}
