import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import javax.swing.JLabel;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

public class MarcXml {
   public void isoToIso(String inFile, String outFile, String inCode, String outCode, PrintStream log, JLabel lblCount) {
      if (inFile.equals(outFile)) {
         log.println("輸入檔案與輸出檔案必需不同.");
      } else {
         FileInputStream in = null;

         try {
            in = new FileInputStream(inFile);
         } catch (Exception var34) {
            log.println("無法開啟輸入檔案.");
            return;
         }

         FileOutputStream out = null;

         try {
            out = new FileOutputStream(outFile);
         } catch (Exception var33) {
            try {
               in.close();
            } catch (Exception var31) {
            }

            log.println("無法開啟輸出檔案.");
            return;
         }

         try {
            CcciiUniBig5 cuObj = new CcciiUniBig5();
            if (inCode.compareToIgnoreCase(outCode) == 0 || inCode.compareToIgnoreCase(BibData.encodeCccii) != 0 && outCode.compareToIgnoreCase(BibData.encodeCccii) != 0 || cuObj.loadTable()) {
               int offset = 0;
               int itemCount = 0;
               int itemOk = 0;
               boolean eof = false;

               while(!eof) {
                  lblCount.setText(Integer.toString(itemCount));
                  byte[] buf = new byte[100000];
                  int blen = 0;
                  boolean eor = false;

                  do {
                     int b = in.read();
                     if (b != -1) {
                        buf[blen++] = (byte)b;
                     } else {
                        eof = true;
                     }

                     if (b == 29) {
                        eor = true;
                        if (inCode.compareToIgnoreCase(BibData.encodeUnicode) == 0) {
                           b = in.read();
                           if (b != -1) {
                              buf[blen++] = (byte)b;
                              if (b != 0) {
                                 eor = false;
                              }
                           }
                        }
                     }
                  } while(!eof && !eor && blen < 200000);

                  if (blen > 0) {
                     ++itemCount;
                     String iso = "";
                     if (inCode.compareToIgnoreCase(BibData.encodeUnicode) == 0) {
                        iso = new String(buf, 0, blen, "UTF-16LE");
                     } else {
                        iso = new String(buf, 0, blen, "ISO8859_1");
                     }

                     BibData bibData = new BibData(inCode);
                     if (bibData.impIso(iso)) {
                        bibData.cuObj = cuObj;
                        bibData.encode(outCode);
                        out.write(bibData.expIso());
                        ++itemOk;
                     } else {
                        log.println("輸入檔案資料錯誤，筆數：" + itemCount + "  位置：" + offset + "  長度：" + blen);
                        log.println("    Tag 001：" + bibData.getTagData("001"));
                     }

                     offset += blen;
                  }
               }

               log.println("處理筆數：" + itemCount);
               log.println("完成筆數：" + itemOk);
               return;
            }

            log.println("無法載入 CCCII 字碼對照表.");
         } catch (Exception var35) {
            log.println("無法轉換檔案.");
            return;
         } finally {
            try {
               in.close();
               out.close();
            } catch (Exception var32) {
               log.println("無法關閉檔案.");
            }

         }

      }
   }

   public void isoToXml(String inFile, String outFile, String inCode, String outCode, String bibType, PrintStream log, JLabel lblCount) {
      if (inFile.equals(outFile)) {
         log.println("輸入檔案與輸出檔案必需不同.");
      } else {
         FileInputStream in = null;

         try {
            in = new FileInputStream(inFile);
         } catch (Exception var36) {
            log.println("無法開啟輸入檔案.");
            return;
         }

         FileOutputStream out = null;

         try {
            out = new FileOutputStream(outFile);
         } catch (Exception var35) {
            try {
               in.close();
            } catch (Exception var34) {
            }

            log.println("無法開啟輸出檔案.");
            return;
         }

         try {
            CcciiUniBig5 cuObj = new CcciiUniBig5();
            if (inCode.compareToIgnoreCase(outCode) == 0 || inCode.compareToIgnoreCase(BibData.encodeCccii) != 0 && outCode.compareToIgnoreCase(BibData.encodeCccii) != 0 || cuObj.loadTable()) {
               if (outCode.compareToIgnoreCase(BibData.encodeUnicode) != 0 && outCode.compareToIgnoreCase(BibData.encodeUtf8) != 0) {
                  if (outCode.compareToIgnoreCase(BibData.encodeBig5) == 0) {
                     out.write("<?xml version=\"1.0\" encoding=\"BIG5\"?>\n".getBytes("ISO8859_1"));
                  } else {
                     out.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n".getBytes("ISO8859_1"));
                  }
               } else {
                  out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".getBytes("ISO8859_1"));
               }

               out.write("<collection xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"CMARC_schema.xsd\">\n".getBytes("ISO8859_1"));
               int offset = 0;
               int itemCount = 0;
               int itemOk = 0;
               boolean eof = false;

               while(!eof) {
                  lblCount.setText(Integer.toString(itemCount));
                  byte[] buf = new byte[100000];
                  int blen = 0;
                  boolean eor = false;

                  do {
                     int b = in.read();
                     if (b != -1) {
                        buf[blen++] = (byte)b;
                     } else {
                        eof = true;
                     }

                     if (b == 29) {
                        eor = true;
                        if (inCode.compareToIgnoreCase(BibData.encodeUnicode) == 0) {
                           b = in.read();
                           if (b != -1) {
                              buf[blen++] = (byte)b;
                           }
                        }
                     }
                  } while(!eof && !eor && blen < 100000);

                  if (blen > 0) {
                     ++itemCount;
                     String iso = "";
                     if (inCode.compareToIgnoreCase(BibData.encodeUnicode) == 0) {
                        iso = new String(buf, 0, blen, "UTF-16LE");
                     } else {
                        iso = new String(buf, 0, blen, "ISO8859_1");
                     }

                     BibData bibData = new BibData(inCode);
                     if (bibData.impIso(iso)) {
                        bibData.cuObj = cuObj;
                        bibData.encode(outCode);
                        ++itemOk;
                        String id = "ID" + Util.intPadZero(itemOk, 6);
                        bibData.setBibType(bibType);
                        bibData.setXmlId(id);
                        out.write(bibData.expXml());
                     } else {
                        log.println("輸入檔案資料錯誤，筆數：" + itemCount + "  位置：" + offset + "  長度：" + blen);
                        log.println("    Tag 001：" + bibData.getTagData("001"));
                     }

                     offset += blen;
                  }
               }

               out.write("</collection>\n".getBytes("ISO8859_1"));
               log.println("處理筆數：" + itemCount);
               log.println("完成筆數：" + itemOk);
               return;
            }

            log.println("無法載入 CCCII 字碼對照表.");
         } catch (Exception var37) {
            log.println("無法轉換檔案.");
            return;
         } finally {
            try {
               in.close();
               out.close();
            } catch (Exception var33) {
               log.println("無法關閉檔案.");
            }

         }

      }
   }

   public void xmlToIso(String inFile, String outFile, String inCode, String outCode, PrintStream log, JLabel lblCount) {
      if (inFile.equals(outFile)) {
         log.println("輸入檔案與輸出檔案必需不同.");
      } else {
         File in = null;

         try {
            in = new File(inFile);
            if (!in.isFile()) {
               log.println("無法開啟輸入檔案.");
               return;
            }
         } catch (Exception var27) {
            log.println("無法開啟輸入檔案.");
            return;
         }

         FileOutputStream out = null;

         try {
            out = new FileOutputStream(outFile);
         } catch (Exception var24) {
            log.println("無法開啟輸出檔案.");
            return;
         }

         try {
            CcciiUniBig5 cuObj = new CcciiUniBig5();
            if (inCode.compareToIgnoreCase(outCode) == 0 || inCode.compareToIgnoreCase(BibData.encodeCccii) != 0 && outCode.compareToIgnoreCase(BibData.encodeCccii) != 0 || cuObj.loadTable()) {
               BibSaxIso handler = new BibSaxIso();
               handler.cuObj = cuObj;
               handler.outFile = out;
               handler.inCode = inCode;
               handler.outCode = outCode;
               handler.lblCount = lblCount;
               SAXParserFactory factory = SAXParserFactory.newInstance();
               factory.setValidating(true);
               SAXParser parser = factory.newSAXParser();
               parser.parse(in, handler);
               log.println("處理筆數：" + handler.itemCount);
               log.println("完成筆數：" + handler.itemOk);
               return;
            }

            log.println("無法載入 CCCII 字碼對照表.");
         } catch (Exception var25) {
            log.println("輸入 XML 檔案格式錯誤.");
            return;
         } finally {
            try {
               out.close();
            } catch (Exception var23) {
               log.println("無法關閉檔案.");
            }

         }

      }
   }

   public void xmlToXml(String inFile, String outFile, String inCode, String outCode, String bibType, PrintStream log, JLabel lblCount) {
      if (inFile.equals(outFile)) {
         log.println("輸入檔案與輸出檔案必需不同.");
      } else {
         File in = null;

         try {
            in = new File(inFile);
            if (!in.isFile()) {
               log.println("無法開啟輸入檔案.");
               return;
            }
         } catch (Exception var28) {
            log.println("無法開啟輸入檔案.");
            return;
         }

         FileOutputStream out = null;

         try {
            out = new FileOutputStream(outFile);
         } catch (Exception var25) {
            log.println("無法開啟輸出檔案.");
            return;
         }

         try {
            CcciiUniBig5 cuObj = new CcciiUniBig5();
            if (inCode.compareToIgnoreCase(outCode) == 0 || inCode.compareToIgnoreCase(BibData.encodeCccii) != 0 && outCode.compareToIgnoreCase(BibData.encodeCccii) != 0 || cuObj.loadTable()) {
               BibSaxXml handler = new BibSaxXml();
               handler.cuObj = cuObj;
               handler.outFile = out;
               handler.inCode = inCode;
               handler.outCode = outCode;
               handler.lblCount = lblCount;
               SAXParserFactory factory = SAXParserFactory.newInstance();
               factory.setValidating(true);
               SAXParser parser = factory.newSAXParser();
               parser.parse(in, handler);
               log.println("處理筆數：" + handler.itemCount);
               log.println("完成筆數：" + handler.itemOk);
               return;
            }

            log.println("無法載入 CCCII 字碼對照表.");
         } catch (Exception var26) {
            log.println("輸入檔案格式錯誤.");
            return;
         } finally {
            try {
               out.close();
            } catch (Exception var24) {
               log.println("無法關閉檔案.");
            }

         }

      }
   }
}
