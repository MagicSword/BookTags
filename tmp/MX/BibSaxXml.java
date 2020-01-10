import java.io.FileOutputStream;
import javax.swing.JLabel;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

public class BibSaxXml extends DefaultHandler {
   FileOutputStream outFile;
   CcciiUniBig5 cuObj;
   String inCode;
   String outCode;
   JLabel lblCount;
   BibData bibData;
   BibTag bibTag;
   BibFld bibFld;
   String elmName;
   String elmData;
   int itemCount;
   int itemOk;

   public void startDocument() {
      this.itemCount = 0;
      this.itemOk = 0;
   }

   public void endDocument() {
   }

   public void startElement(String uri, String name, String qName, Attributes atts) {
      this.elmName = qName;
      if ("collection".equals(qName)) {
         try {
            if (this.outCode.compareToIgnoreCase(BibData.encodeUnicode) != 0 && this.outCode.compareToIgnoreCase(BibData.encodeUtf8) != 0) {
               if (this.outCode.compareToIgnoreCase(BibData.encodeBig5) == 0) {
                  this.outFile.write("<?xml version=\"1.0\" encoding=\"BIG5\"?>\n".getBytes("ISO8859_1"));
               } else {
                  this.outFile.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n".getBytes("ISO8859_1"));
               }
            } else {
               this.outFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".getBytes("ISO8859_1"));
            }

            this.outFile.write("<collection xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"CMARC_schema.xsd\">\n".getBytes("ISO8859_1"));
         } catch (Exception var9) {
         }

         this.elmData = "";
      } else {
         String code;
         String ind1;
         if ("record".equals(qName)) {
            ++this.itemCount;
            this.lblCount.setText(Integer.toString(this.itemCount));
            this.bibData = new BibData(this.inCode);
            this.bibData.cuObj = this.cuObj;
            if (atts != null) {
               code = "";
               ind1 = "";

               for(int i = 0; i < atts.getLength(); ++i) {
                  if (atts.getQName(i).equals("type")) {
                     code = atts.getValue(i);
                  } else if (atts.getQName(i).equals("id")) {
                     ind1 = atts.getValue(i);
                  }
               }

               this.bibData.setBibType(code);
               this.bibData.setXmlId(ind1);
            }

            this.elmData = "";
         } else if ("leader".equals(qName)) {
            this.elmData = "";
         } else {
            int i;
            if ("controlfield".equals(qName)) {
               code = "";
               if (atts != null) {
                  for(i = 0; i < atts.getLength(); ++i) {
                     if (atts.getQName(i).equals("tag")) {
                        code = atts.getValue(i);
                     }
                  }
               }

               this.bibTag = new BibTag(code);
               this.elmData = "";
            } else if ("datafield".equals(qName)) {
               code = "";
               ind1 = "";
               String ind2 = "";
               if (atts != null) {
                  for(int i = 0; i < atts.getLength(); ++i) {
                     if (atts.getQName(i).equals("tag")) {
                        code = atts.getValue(i);
                     } else if (atts.getQName(i).equals("ind1")) {
                        ind1 = atts.getValue(i);
                     } else if (atts.getQName(i).equals("ind2")) {
                        ind2 = atts.getValue(i);
                     }
                  }
               }

               this.bibTag = new BibTag(code);
               this.bibTag.indicator = ind1 + ind2;
               this.elmData = "";
            } else if ("subfield".equals(qName)) {
               code = "";
               if (atts != null) {
                  for(i = 0; i < atts.getLength(); ++i) {
                     if (atts.getQName(i).equals("code")) {
                        code = atts.getValue(i);
                     }
                  }
               }

               this.bibFld = new BibFld(code);
               this.elmData = "";
            }
         }
      }

   }

   public void endElement(String uri, String name, String qName) {
      this.elmName = qName;
      if ("collection".equals(qName)) {
         try {
            this.outFile.write("</collection>\n".getBytes("ISO8859_1"));
         } catch (Exception var8) {
         }
      } else if ("record".equals(qName)) {
         try {
            this.bibData.encode(this.outCode);
            ++this.itemOk;
            this.outFile.write(this.bibData.expXml());
         } catch (Exception var7) {
         }
      } else if ("leader".equals(qName)) {
         this.bibData.leader = Util.leftJustify(this.elmData, 24);
      } else if ("controlfield".equals(qName)) {
         try {
            if (this.inCode.compareToIgnoreCase(BibData.encodeBig5) == 0) {
               this.elmData = new String(this.elmData.getBytes("BIG5"), "ISO8859_1");
            }
         } catch (Exception var6) {
         }

         this.bibTag.data = this.elmData;
         this.bibData.tagList.add(this.bibTag);
      } else if ("datafield".equals(qName)) {
         this.bibData.tagList.add(this.bibTag);
      } else if ("subfield".equals(qName)) {
         try {
            if (this.inCode.compareToIgnoreCase(BibData.encodeBig5) == 0) {
               this.elmData = new String(this.elmData.getBytes("BIG5"), "ISO8859_1");
            }
         } catch (Exception var5) {
         }

         this.bibFld.data = this.elmData;
         this.bibTag.fldList.add(this.bibFld);
      } else if ("esc".equals(qName)) {
         this.elmData = this.elmData + '\u001b';
      }

   }

   public void characters(char[] ch, int start, int length) {
      this.elmData = this.elmData + new String(ch, start, length);
   }
}
