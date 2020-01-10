import java.util.ArrayList;

public class BibTag {
   static char dlmFld = 31;
   String id;
   String indicator;
   String data;
   ArrayList fldList;

   public BibTag() {
      this.id = null;
      this.indicator = null;
      this.data = null;
      this.fldList = new ArrayList();
   }

   public BibTag(String tag) {
      this.id = tag;
      this.indicator = "";
      this.data = null;
      this.fldList = new ArrayList();
   }

   public boolean impIso(String iso) {
      try {
         int pos = iso.indexOf(dlmFld);
         if (pos < 0) {
            this.data = iso;
            return true;
         } else {
            if (pos != 0 && pos != 2) {
               this.fldList.add(new BibFld(iso.substring(0, 1), iso.substring(1)));
            } else {
               this.indicator = iso.substring(0, pos);
            }

            String tmp;
            for(iso = iso.substring(pos + 1); iso.length() > 0; this.fldList.add(new BibFld(tmp.substring(0, 1), tmp.substring(1)))) {
               pos = iso.indexOf(dlmFld);
               if (pos < 0) {
                  tmp = iso;
                  iso = "";
               } else {
                  tmp = iso.substring(0, pos);
                  iso = iso.substring(pos + 1);
               }
            }

            return true;
         }
      } catch (Exception var4) {
         return false;
      }
   }

   public String expIso() {
      String retval = "";

      try {
         try {
            for(int i = 0; i < this.fldList.size(); ++i) {
               retval = retval + dlmFld + Util.leftJustify(((BibFld)this.fldList.get(i)).id, 1) + ((BibFld)this.fldList.get(i)).data;
            }

            return retval;
         } catch (Exception var3) {
            return "";
         }
      } catch (Exception var4) {
         return "";
      }
   }

   public String expXml() {
      String retval = "";

      try {
         try {
            for(int i = 0; i < this.fldList.size(); ++i) {
               String tmp = ((BibFld)this.fldList.get(i)).data;
               tmp = tmp.replaceAll("&", "&amp;");
               tmp = tmp.replaceAll("<", "&lt;");
               tmp = tmp.replaceAll(">", "&gt;");
               tmp = tmp.replaceAll("\"", "&quot;");
               tmp = tmp.replaceAll("'", "&apos;");
               tmp = tmp.replaceAll("\u001b", "<esc/>");
               StringBuffer sb = new StringBuffer(tmp.length());

               for(int j = 0; j < tmp.length(); ++j) {
                  char ch = tmp.charAt(j);
                  if (ch >= ' ') {
                     sb.append(ch);
                  }
               }

               retval = retval + "\t\t\t<subfield code=\"" + ((BibFld)this.fldList.get(i)).id + "\">";
               retval = retval + sb.toString() + "</subfield>\n";
            }

            return retval;
         } catch (Exception var7) {
            return "";
         }
      } catch (Exception var8) {
         return "";
      }
   }

   public boolean unicodeToBig5(CcciiUniBig5 cuObj, String encoding) {
      boolean retval = true;

      try {
         if (this.data != null) {
            this.data = new String(cuObj.unicodeToBig5(this.data.getBytes("UTF-16LE"), encoding), "ISO8859_1");
         }

         for(int i = 0; i < this.fldList.size(); ++i) {
            BibFld thisFld = (BibFld)this.fldList.get(i);
            thisFld.data = new String(cuObj.unicodeToBig5(thisFld.data.getBytes("UTF-16LE"), encoding), "ISO8859_1");
         }

         return retval;
      } catch (Exception var6) {
         return false;
      }
   }

   public boolean big5ToUnicode(CcciiUniBig5 cuObj) {
      boolean retval = true;

      try {
         if (this.data != null) {
            this.data = new String(cuObj.big5ToUnicode(this.data.getBytes("ISO8859_1")), "UTF-16LE");
         }

         for(int i = 0; i < this.fldList.size(); ++i) {
            BibFld thisFld = (BibFld)this.fldList.get(i);
            thisFld.data = new String(cuObj.big5ToUnicode(thisFld.data.getBytes("ISO8859_1")), "UTF-16LE");
         }

         return retval;
      } catch (Exception var5) {
         return false;
      }
   }

   public boolean ccciiToUnicode(CcciiUniBig5 cuObj) {
      boolean retval = true;

      try {
         if (this.data != null) {
            this.data = new String(cuObj.ccciiToUnicode(this.data.getBytes("ISO8859_1")), "UTF-16LE");
         }

         for(int i = 0; i < this.fldList.size(); ++i) {
            BibFld thisFld = (BibFld)this.fldList.get(i);
            thisFld.data = new String(cuObj.ccciiToUnicode(thisFld.data.getBytes("ISO8859_1")), "UTF-16LE");
         }

         return retval;
      } catch (Exception var5) {
         return false;
      }
   }

   public boolean unicodeToCccii(CcciiUniBig5 cuObj, String encoding) {
      boolean retval = true;

      try {
         if (this.data != null) {
            this.data = new String(cuObj.unicodeToCccii(this.data.getBytes("UTF-16LE"), encoding), "ISO8859_1");
         }

         for(int i = 0; i < this.fldList.size(); ++i) {
            BibFld thisFld = (BibFld)this.fldList.get(i);
            thisFld.data = new String(cuObj.unicodeToCccii(thisFld.data.getBytes("UTF-16LE"), encoding), "ISO8859_1");
         }

         return retval;
      } catch (Exception var6) {
         return false;
      }
   }

   public boolean ccciiToBig5(CcciiUniBig5 cuObj) {
      boolean retval = true;

      try {
         if (this.data != null) {
            this.data = new String(cuObj.ccciiToBig5(this.data.getBytes("ISO8859_1")), "ISO8859_1");
         }

         for(int i = 0; i < this.fldList.size(); ++i) {
            BibFld thisFld = (BibFld)this.fldList.get(i);
            thisFld.data = new String(cuObj.ccciiToBig5(thisFld.data.getBytes("ISO8859_1")), "ISO8859_1");
         }

         return retval;
      } catch (Exception var5) {
         return false;
      }
   }

   public boolean big5ToCccii(CcciiUniBig5 cuObj) {
      boolean retval = true;

      try {
         if (this.data != null) {
            this.data = new String(cuObj.big5ToCccii(this.data.getBytes("ISO8859_1")), "ISO8859_1");
         }

         for(int i = 0; i < this.fldList.size(); ++i) {
            BibFld thisFld = (BibFld)this.fldList.get(i);
            thisFld.data = new String(cuObj.big5ToCccii(thisFld.data.getBytes("ISO8859_1")), "ISO8859_1");
         }

         return retval;
      } catch (Exception var5) {
         return false;
      }
   }
}
