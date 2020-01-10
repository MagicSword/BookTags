import java.util.ArrayList;

public class BibData {
   static String encodeBig5 = "BIG5";
   static String encodeUnicode = "UNICODE";
   static String encodeUtf8 = "UTF-8";
   static String encodeCccii = "CCCII";
   static char dlmRec = 29;
   static char dlmTag = 30;
   static char dlmFld = 31;
   String leader = null;
   ArrayList tagList = new ArrayList();
   String encoding;
   CcciiUniBig5 cuObj;
   String bibType;
   String xmlId;

   public BibData() {
   }

   public BibData(String enc) {
      this.encoding = enc;
   }

   public void setBibType(String s) {
      this.bibType = s;
   }

   public void setXmlId(String s) {
      this.xmlId = s;
   }

   public boolean impIso(String iso) {
      try {
         if (iso.charAt(iso.length() - 1) != dlmRec) {
            return false;
         } else {
            this.leader = iso.substring(0, 24);
            int baseLen = Util.zerostrToInt(this.leader.substring(12, 17));
            String tagHeaderData = iso.substring(24, baseLen - 1);
            if (iso.charAt(baseLen - 1) != dlmTag) {
               return false;
            } else {
               iso = iso.substring(baseLen);
               this.leader = "     " + this.leader.substring(5, 12) + "     " + this.leader.substring(17);

               for(int i = 0; i < tagHeaderData.length() / 12; ++i) {
                  String tag = tagHeaderData.substring(i * 12, i * 12 + 3);
                  int tagLen = Util.zerostrToInt(tagHeaderData.substring(i * 12 + 3, i * 12 + 7));
                  int tagBase = Util.zerostrToInt(tagHeaderData.substring(i * 12 + 7, i * 12 + 12));
                  String ind = "";
                  String tagiso = iso.substring(tagBase, tagBase + tagLen);
                  if (tagiso.charAt(tagiso.length() - 1) == dlmRec || tagiso.charAt(tagiso.length() - 1) == dlmTag) {
                     tagiso = tagiso.substring(0, tagiso.length() - 1);
                     if (tagiso.charAt(tagiso.length() - 1) == dlmRec || tagiso.charAt(tagiso.length() - 1) == dlmTag) {
                        tagiso = tagiso.substring(0, tagiso.length() - 1);
                     }
                  }

                  if (tagiso.length() > 0) {
                     if (this.encoding.compareToIgnoreCase(encodeUtf8) == 0) {
                        tagiso = new String(tagiso.getBytes("ISO8859_1"), "UTF-8");
                     }

                     BibTag oTag = new BibTag(tag);
                     oTag.impIso(tagiso);
                     this.tagList.add(oTag);
                  }
               }

               return true;
            }
         }
      } catch (Exception var11) {
         return false;
      }
   }

   public byte[] expIso() {
      byte[] retval = null;
      String sLeader = "";
      String sTag = "";
      String sBody = "";

      try {
         int recLen;
         for(recLen = 0; recLen < this.tagList.size(); ++recLen) {
            BibTag thisTag = (BibTag)this.tagList.get(recLen);
            int nBase = sBody.length();
            String tagBody = "";
            if (thisTag.data != null) {
               tagBody = thisTag.data + dlmTag;
            } else {
               tagBody = thisTag.indicator;
               tagBody = tagBody + thisTag.expIso() + dlmTag;
            }

            if (this.encoding.compareToIgnoreCase(encodeUtf8) == 0) {
               tagBody = new String(tagBody.getBytes("UTF-8"), "ISO8859_1");
            }

            sBody = sBody + tagBody;
            String tagHeader = Util.leftJustify(thisTag.id, 3);
            int nLen = sBody.length() - nBase;
            if (nLen > 9999) {
               nLen = 9999;
            }

            tagHeader = tagHeader + Util.intPadZero(nLen, 4) + Util.intPadZero(nBase, 5);
            sTag = sTag + tagHeader;
         }

         sLeader = Util.leftJustify(this.leader, 24);
         recLen = sLeader.length() + sTag.length() + sBody.length() + 2;
         int recBase = sLeader.length() + sTag.length() + 1;
         sLeader = Util.intPadZero(recLen, 5) + sLeader.substring(5, 12) + Util.intPadZero(recBase, 5) + sLeader.substring(17);
         byte[] retval;
         if (this.encoding.compareToIgnoreCase(encodeUnicode) == 0) {
            retval = (sLeader + sTag + dlmTag + sBody + dlmRec).getBytes("UTF-16LE");
         } else {
            retval = (sLeader + sTag + dlmTag + sBody + dlmRec).getBytes("ISO8859_1");
         }

         return retval;
      } catch (Exception var11) {
         return "".getBytes();
      }
   }

   public byte[] expXml() {
      byte[] retval = null;
      String sBody = "";

      try {
         sBody = "\t<record type=\"" + this.bibType + "\" id=\"" + this.xmlId + "\">\n";
         sBody = sBody + "\t\t<leader>" + this.getLeader() + "</leader>\n";

         for(int i = 0; i < this.tagList.size(); ++i) {
            BibTag thisTag = (BibTag)this.tagList.get(i);
            if (thisTag.data != null) {
               sBody = sBody + "\t\t<controlfield tag=\"" + thisTag.id + "\">" + thisTag.data + "</controlfield>\n";
            } else {
               String ind = Util.leftJustify(thisTag.indicator, 2);
               sBody = sBody + "\t\t<datafield tag=\"" + thisTag.id;
               sBody = sBody + "\" ind1=\"" + ind.substring(0, 1) + "\" ind2=\"" + ind.substring(1, 2) + "\">\n";
               sBody = sBody + thisTag.expXml();
               sBody = sBody + "\t\t</datafield>\n";
            }
         }

         sBody = sBody + "\t</record>\n";
         byte[] retval;
         if (this.encoding.compareToIgnoreCase(encodeUnicode) != 0 && this.encoding.compareToIgnoreCase(encodeUtf8) != 0) {
            retval = sBody.getBytes("ISO8859_1");
         } else {
            retval = sBody.getBytes("UTF-8");
         }

         return retval;
      } catch (Exception var6) {
         return "".getBytes();
      }
   }

   private String getLeader() {
      String sHeader = Util.leftJustify(this.leader, 24);
      String sTag = "";
      String sBody = "";

      try {
         int recLen;
         for(recLen = 0; recLen < this.tagList.size(); ++recLen) {
            BibTag thisTag = (BibTag)this.tagList.get(recLen);
            int nBase = sBody.length();
            String tagBody = "";
            if (thisTag.data != null) {
               tagBody = dlmTag + thisTag.data;
            } else {
               tagBody = dlmTag + thisTag.indicator;
               tagBody = tagBody + thisTag.expIso();
            }

            if (this.encoding.compareToIgnoreCase(encodeUtf8) == 0) {
               tagBody = new String(tagBody.getBytes("UTF-8"), "ISO8859_1");
            }

            sBody = sBody + tagBody;
            String tagHeader = Util.leftJustify(thisTag.id, 3);
            int nLen = sBody.length() - nBase;
            if (nLen > 9999) {
               nLen = 9999;
            }

            tagHeader = tagHeader + Util.intPadZero(nLen, 4) + Util.intPadZero(nBase, 5);
            sTag = sTag + tagHeader;
         }

         recLen = sHeader.length() + sTag.length() + sBody.length() + 1;
         int recBase = sHeader.length() + sTag.length() + 1;
         sHeader = Util.intPadZero(recLen, 5) + sHeader.substring(5, 12) + Util.intPadZero(recBase, 5) + sHeader.substring(17);
         return sHeader;
      } catch (Exception var10) {
         return "";
      }
   }

   public String getTagData(String tag) {
      String retval = "";

      for(int i = 0; i < this.tagList.size(); ++i) {
         BibTag thisTag = (BibTag)this.tagList.get(i);
         if (tag.equals(thisTag.id)) {
            retval = thisTag.data;
            break;
         }
      }

      return retval;
   }

   public boolean encode(String newencoding) {
      boolean retval = true;
      if (this.encoding.compareToIgnoreCase(newencoding) != 0 && (this.encoding.compareToIgnoreCase(encodeUnicode) != 0 || newencoding.compareToIgnoreCase(encodeUtf8) != 0) && (this.encoding.compareToIgnoreCase(encodeUtf8) != 0 || newencoding.compareToIgnoreCase(encodeUnicode) != 0)) {
         int i;
         if (this.encoding.compareToIgnoreCase(encodeBig5) == 0) {
            if (newencoding.compareToIgnoreCase(encodeUnicode) != 0 && newencoding.compareToIgnoreCase(encodeUtf8) != 0) {
               if (newencoding.compareToIgnoreCase(encodeCccii) == 0) {
                  for(i = 0; i < this.tagList.size(); ++i) {
                     retval = ((BibTag)this.tagList.get(i)).big5ToCccii(this.cuObj);
                     if (!retval) {
                        break;
                     }
                  }

                  if (retval) {
                     this.encoding = newencoding;
                  }
               }
            } else {
               for(i = 0; i < this.tagList.size(); ++i) {
                  retval = ((BibTag)this.tagList.get(i)).big5ToUnicode(this.cuObj);
                  if (!retval) {
                     break;
                  }
               }

               if (retval) {
                  this.encoding = newencoding;
               }
            }
         } else if (this.encoding.compareToIgnoreCase(encodeUnicode) != 0 && this.encoding.compareToIgnoreCase(encodeUtf8) != 0) {
            if (this.encoding.compareToIgnoreCase(encodeCccii) == 0) {
               if (newencoding.compareToIgnoreCase(encodeBig5) == 0) {
                  for(i = 0; i < this.tagList.size(); ++i) {
                     retval = ((BibTag)this.tagList.get(i)).ccciiToBig5(this.cuObj);
                     if (!retval) {
                        break;
                     }
                  }

                  if (retval) {
                     this.encoding = newencoding;
                  }
               } else if (newencoding.compareToIgnoreCase(encodeUnicode) == 0 || newencoding.compareToIgnoreCase(encodeUtf8) == 0) {
                  for(i = 0; i < this.tagList.size(); ++i) {
                     retval = ((BibTag)this.tagList.get(i)).ccciiToUnicode(this.cuObj);
                     if (!retval) {
                        break;
                     }
                  }

                  if (retval) {
                     this.encoding = newencoding;
                  }
               }
            }
         } else if (newencoding.compareToIgnoreCase(encodeBig5) == 0) {
            for(i = 0; i < this.tagList.size(); ++i) {
               retval = ((BibTag)this.tagList.get(i)).unicodeToBig5(this.cuObj, this.encoding);
               if (!retval) {
                  break;
               }
            }

            if (retval) {
               this.encoding = newencoding;
            }
         } else if (newencoding.compareToIgnoreCase(encodeCccii) == 0) {
            for(i = 0; i < this.tagList.size(); ++i) {
               retval = ((BibTag)this.tagList.get(i)).unicodeToCccii(this.cuObj, this.encoding);
               if (!retval) {
                  break;
               }
            }

            if (retval) {
               this.encoding = newencoding;
            }
         }

         return retval;
      } else {
         this.encoding = newencoding;
         return true;
      }
   }
}
