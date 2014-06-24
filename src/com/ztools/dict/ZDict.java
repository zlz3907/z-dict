package com.ztools.dict;

import java.util.HashMap;
import java.io.InputStream;
import java.util.Map;

public class ZDict {
  private static Map<String, String> wordCache = new HashMap<String, String>();

  private static final String DEFAULT_URL_TRANSLATE = "http://dict.yodao.com/"
    +"search?keyfrom=dict.python&xmlDetail=true&doctype=xml&q=";

  private String urlOfTranslate = DEFAULT_URL_TRANSLATE;

  public static InputStream getTranslationsXml(String word) {
    return null;
  }

  public void init() {
    System.out.println("init...");
  }

  public void startTranslateionService() {
    System.out.println("ZDict translation service is started!");
  }

  public boolean assertServiceIsStarted() {
    return false;
  }

  public String translate(String word) {
    return "OK!" + word;
  }

  public static void usage() {
    System.out.println("usage: zdict word");
  }

  public static void main(String[] args) {
    // 1. create ZDict instance.
    // 2. check zdict server status.
    // 3. if !server.start then
    // 4.   start zdict server
    // 5. translate
    args = new String[]{"hello"};
    if (0 >= args.length) {
      usage();
      System.exit(1);
    }


    ZDict dict = new ZDict();
    dict.init();
    if (!dict.assertServiceIsStarted()) {
      dict.startTranslateionService();
    }
    String result = dict.translate(args[0]);
    System.out.println(result);
  }

}
