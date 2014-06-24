#! /usr/bin/python
# -*- coding: utf-8 -*-
import re;
import urllib;
import urllib2;
import sys;
import os;
def write_xml_tocache(xml, path):
    afile = open(path, 'w');
    afile.write(xml);
    afile.close();
def crawl_xml_incache(word):
    qw = fix_query_string(word.lower());
    swi_path = "/home/lizhi/gnu/plugins/dict/words/" + qw + ".xml";
    if os.path.exists(swi_path):
        afile = open(swi_path);
        xml = afile.read();
        afile.close();
        return xml;
    httpcn = urllib2.urlopen("http://fanyi.youdao.com/openapi.do?"
    + "keyfrom=3zsocom&key=1620414302&type=data&doctype=xml&version=1.1&q="
    + urllib.quote_plus(qw));
    xml = httpcn.read();
    httpcn.close();
    write_xml_tocache(xml, swi_path);
    return xml;
def debug():
    xml = open("word.xml").read();
    print get_text(xml);
    print get_elements_by_path(xml, "custom-translation/content");
    #print_translations(xml, False, False);
def get_elements_by_path(xml, elem):
    if type(xml) == type(''):
        xml = [xml];
    if type(elem) == type(''):
        elem = elem.split('/');
    if (len(xml) == 0):
        return [];
    elif (len(elem) == 0):
        return xml;
    elif (len(elem) == 1):
        result = [];
        for item in xml:
            result += get_elements(item, elem[0]);
        return result;
    else:
        subitems = [];
        for item in xml:
            subitems += get_elements(item, elem[0]);
        return get_elements_by_path(subitems, elem[1:]);
textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL);
def get_text(xml):
    match = re.search(textre, xml);
    if not match:
        return xml;
    return match.group(1);
def get_elements(xml, elem):
    p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL);
    it = p.finditer(xml);
    result = [];
    for m in it:
        result.append(m.group(1));
    return result;
GREEN = "\033[1;32m";
DEFAULT = "\033[0;49m";
BOLD = "\033[1m";
UNDERLINE = "\033[4m";
NORMAL = "\033[m";
RED = "\033[1;31m";
BOLD = "\033[1m";
queryre = re.compile(u"[^a-zA-Z\u4e00-\u9fa5]", re.DOTALL);
def fix_query_string(queryword):
    match = re.search(queryre, queryword.decode("utf-8"));
    if not match:
        return queryword;
    ret = queryre.sub(" ", queryword);
    return ret;
def crawl_xml(queryword):
    qw = fix_query_string(queryword);
    return urllib2.urlopen("http://fanyi.youdao.com/openapi.do?"
    + "keyfrom=3zsocom&key=1620414302&type=data&doctype=xml&version=1.1&q="
    + urllib.quote_plus(qw)).read();
def print_translations(xml, with_color, detailed):
    #print xml;
    global GREEN;
    global DEFAULT;
    global BOLD;
    global UNDERLINE;
    global NORMAL;
    global RED;
    if not with_color:
        GREEN = "";
        DEFAULT = "";
        BOLD = "";
        UNDERLINE = "";
        NORMAL = "";
        RED = "";

    original_query = get_elements(xml, "query");
    queryword = get_text(original_query[0]);
    custom_translations = get_elements(xml, "basic");
    translated = False;
    el_phonetic = get_elements(xml, "phonetic");
    phonetic_symbol = " ";
    if not len(el_phonetic) <= 0:
        phonetic_symbol = " [" + get_text(get_elements(xml, "phonetic")[0]) + "] ";
    paragraph_symbol = get_text(get_elements(xml, "paragraph")[0]);
    print BOLD + UNDERLINE + queryword + NORMAL + phonetic_symbol + paragraph_symbol;
    #sys.stdout.buffer.write(phonetic_symbol.encode("utf-8"));
    #print phonetic_symbol;
    for cus in custom_translations:
        source = "youdao:"; #get_elements_by_path(cus, "basic/explains");

        print RED + "Translations from " + source + DEFAULT;
        contents = get_elements_by_path(cus, "explains/ex");
        for content in contents[0:5]:
            print " " + GREEN + get_text(content) + DEFAULT;
        translated = True;

    yodao_translations = get_elements(xml, "web");
    printed = False;
    for trans in yodao_translations:
        webtrans = get_elements(trans, "explain");
        for web in webtrans[0:5]:
            if not printed:
                print RED + "Translations from web:" + DEFAULT;
                printed = True;
            keys = get_elements(web, "key");
            values = get_elements_by_path(web, "value/ex");
            #summaries = get_elements_by_path(web, "trans/summary");
            key = keys[0].strip();
            value = values[0].strip();
            web_value = "";
            for v in values[0:5]:
                web_value += get_text(v.strip()) + ";";
            #summary = summaries[0].strip();
            #lines = get_elements(summary, "line");
            print " " + BOLD + get_text(key) + ":\t" +DEFAULT + GREEN + get_text(web_value) + NORMAL;
            #for line in lines:
            # print GREEN + get_text(line) + DEFAULT;
            #print get_text(summary) + DEFAULT;
            #translated = True;
            #if not detailed:
            # break
def usage():
    print "usage: dict.py word_to_translate";
def main(argv):
    if len(argv) <= 0:
        usage();
        #debug();
        sys.exit(1);
    xml = crawl_xml_incache(argv[0]);
    is_color = "True";
    if len(argv) == 2:
        is_color = argv[1];
    print_translations(xml, bool(is_color == "True"), False);
if __name__ == "__main__":
    main(sys.argv[1:]);
