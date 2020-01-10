import java.io.InputStream;
import java.util.HashMap;

public class CcciiUniBig5 {
   static byte shiftChar = 27;
   static String CiToUni = "CiToUni.tbl";
   static String UniToCi = "UniToCi.tbl";
   static int CiSize = 29975;
   static int UniSize = 26411;
   HashMap cuMap = new HashMap();
   HashMap ucMap = new HashMap();

   public boolean loadTable() {
      boolean retval = true;
      this.cuMap.clear();
      this.ucMap.clear();

      try {
         InputStream in = this.getClass().getResourceAsStream(CiToUni);
         int cnt = 0;
         boolean eof = false;

         while(true) {
            byte[] buf;
            int nr;
            int unicode;
            int nr2;
            int cccii;
            while(!eof) {
               buf = new byte[4];

               for(nr = 0; nr < 4; nr += unicode) {
                  unicode = in.read(buf, nr, 4 - nr);
                  if (unicode < 0) {
                     break;
                  }
               }

               unicode = ((buf[2] & 255) << 16) + ((buf[1] & 255) << 8) + (buf[0] & 255);

               for(nr2 = 0; nr2 < 4; nr2 += cccii) {
                  cccii = in.read(buf, nr2, 4 - nr2);
                  if (cccii < 0) {
                     break;
                  }
               }

               cccii = ((buf[2] & 255) << 16) + ((buf[1] & 255) << 8) + (buf[0] & 255);
               if (nr == 4 && nr2 == 4) {
                  ++cnt;
                  this.cuMap.put(new Integer(unicode), new Integer(cccii));
               } else {
                  eof = true;
               }
            }

            in.close();
            in = this.getClass().getResourceAsStream(UniToCi);
            cnt = 0;
            eof = false;

            while(true) {
               while(!eof) {
                  buf = new byte[4];

                  for(nr = 0; nr < 4; nr += unicode) {
                     unicode = in.read(buf, nr, 4 - nr);
                     if (unicode < 0) {
                        break;
                     }
                  }

                  unicode = ((buf[2] & 255) << 16) + ((buf[1] & 255) << 8) + (buf[0] & 255);

                  for(nr2 = 0; nr2 < 4; nr2 += cccii) {
                     cccii = in.read(buf, nr2, 4 - nr2);
                     if (cccii < 0) {
                        break;
                     }
                  }

                  cccii = ((buf[2] & 255) << 16) + ((buf[1] & 255) << 8) + (buf[0] & 255);
                  if (nr == 4 && nr2 == 4) {
                     ++cnt;
                     this.ucMap.put(new Integer(unicode), new Integer(cccii));
                  } else {
                     eof = true;
                  }
               }

               in.close();
               return retval;
            }
         }
      } catch (Exception var10) {
         retval = false;
         return retval;
      }
   }

   public byte[] ccciiToUnicode(byte[] cccii) {
      StringBuffer sb = new StringBuffer();
      byte[] retval = new byte[0];

      try {
         boolean sin = false;

         for(int i = 0; i < cccii.length; ++i) {
            if (cccii[i] == shiftChar && i + 2 < cccii.length) {
               if (cccii[i + 1] == 36 && cccii[i + 2] == 49) {
                  sin = true;
                  i += 2;
                  continue;
               }

               if (cccii[i + 1] == 40 && cccii[i + 2] == 66) {
                  sin = false;
                  i += 2;
                  continue;
               }
            }

            if (!sin) {
               sb.append((char)cccii[i]);
            } else {
               if (i + 2 < cccii.length) {
                  byte[] c = new byte[]{cccii[i], cccii[i + 1], cccii[i + 2]};
                  byte[] u = this.cToU(c);
                  if (u[0] == 0 && u[1] == 0) {
                     sb.append("{");
                     sb.append(Util.toHexString(c));
                     sb.append("}");
                  } else {
                     sb.append(new String(u, "UTF-16LE"));
                  }
               }

               i += 2;
            }
         }

         retval = sb.toString().getBytes("UTF-16LE");
      } catch (Exception var8) {
      }

      return retval;
   }

   private byte[] cToU(byte[] cccii) {
      byte[] retval = new byte[]{0, 0};
      int ci = ((cccii[0] & 255) << 16) + ((cccii[1] & 255) << 8) + (cccii[2] & 255);
      Integer ro = (Integer)this.cuMap.get(new Integer(ci));
      if (ro != null) {
         int ui = ro;
         retval[0] = (byte)(ui >> 0 & 255);
         retval[1] = (byte)(ui >> 8 & 255);
      }

      return retval;
   }

   public byte[] unicodeToCccii(byte[] unicode, String encoding) {
      StringBuffer sb = new StringBuffer();
      byte[] retval = new byte[0];

      try {
         String unis = new String(unicode, "UTF-16LE");
         boolean sin = false;

         for(int i = 0; i < unis.length(); ++i) {
            char c = unis.charAt(i);
            if (c < 128) {
               if (sin) {
                  sb.append((char)shiftChar);
                  sb.append('(');
                  sb.append('B');
                  sin = false;
               }

               sb.append(c);
            } else {
               byte[] u = new byte[]{(byte)(c >> 0 & 255), (byte)(c >> 8 & 255)};
               byte[] cccii = this.uToC(u);
               if (cccii[0] == 0 && cccii[1] == 0 && cccii[2] == 0) {
                  if (sin) {
                     sb.append((char)shiftChar);
                     sb.append('(');
                     sb.append('B');
                     sin = false;
                  }

                  sb.append("{");
                  if (encoding.equals(BibData.encodeUtf8)) {
                     sb.append(Util.toHexString((c + "").getBytes("UTF-8")));
                  } else {
                     sb.append(Util.toHexString((c + "").getBytes("UTF-16BE")));
                  }

                  sb.append("}");
               } else {
                  if (!sin) {
                     sb.append((char)shiftChar);
                     sb.append('$');
                     sb.append('1');
                     sin = true;
                  }

                  sb.append(new String(cccii, "ISO8859_1"));
               }
            }
         }

         if (sin) {
            sb.append((char)shiftChar);
            sb.append('(');
            sb.append('B');
            sin = false;
         }

         retval = sb.toString().getBytes("ISO8859_1");
      } catch (Exception var11) {
      }

      return retval;
   }

   private byte[] uToC(byte[] unicode) {
      byte[] retval = new byte[]{0, 0, 0};
      int ui = ((unicode[1] & 255) << 8) + (unicode[0] & 255);
      Integer ro = (Integer)this.ucMap.get(new Integer(ui));
      if (ro != null) {
         int ci = ro;
         retval[0] = (byte)(ci >> 16 & 255);
         retval[1] = (byte)(ci >> 8 & 255);
         retval[2] = (byte)(ci >> 0 & 255);
      }

      return retval;
   }

   public byte[] unicodeToBig5(byte[] unicode, String encoding) {
      StringBuffer sb = new StringBuffer();
      byte[] retval = new byte[0];

      try {
         String unis = new String(unicode, "UTF-16LE");
         boolean sin = false;

         for(int i = 0; i < unis.length(); ++i) {
            char c = unis.charAt(i);
            if (c < 128) {
               sb.append(c);
            } else {
               byte[] big5 = (c + "").getBytes("BIG5");
               if (big5[0] == 63) {
                  sb.append("{");
                  if (encoding.equals(BibData.encodeUtf8)) {
                     sb.append(Util.toHexString((c + "").getBytes("UTF-8")));
                  } else {
                     sb.append(Util.toHexString((c + "").getBytes("UTF-16BE")));
                  }

                  sb.append("}");
               } else {
                  sb.append(new String(big5, "ISO8859_1"));
               }
            }
         }

         retval = sb.toString().getBytes("ISO8859_1");
      } catch (Exception var10) {
      }

      return retval;
   }

   public byte[] big5ToUnicode(byte[] big5) {
      StringBuffer sb = new StringBuffer();
      byte[] retval = new byte[0];

      try {
         for(int i = 0; i < big5.length; ++i) {
            if (big5[i] > 0) {
               sb.append((char)big5[i]);
            } else if (i + 1 < big5.length) {
               byte[] b = new byte[]{big5[i], big5[i + 1]};
               String u = new String(b, "BIG5");
               if (!u.equals("?") && u.length() <= 1) {
                  sb.append(u);
               } else {
                  sb.append("{");
                  sb.append(Util.toHexString(b));
                  sb.append("}");
               }

               ++i;
            }
         }

         retval = sb.toString().getBytes("UTF-16LE");
      } catch (Exception var7) {
      }

      return retval;
   }

   public byte[] ccciiToBig5(byte[] cccii) {
      StringBuffer sb = new StringBuffer();
      byte[] retval = new byte[0];

      try {
         boolean sin = false;

         for(int i = 0; i < cccii.length; ++i) {
            if (cccii[i] == shiftChar && i + 2 < cccii.length) {
               if (cccii[i + 1] == 36 && cccii[i + 2] == 49) {
                  sin = true;
                  i += 2;
                  continue;
               }

               if (cccii[i + 1] == 40 && cccii[i + 2] == 66) {
                  sin = false;
                  i += 2;
                  continue;
               }
            }

            if (!sin) {
               sb.append((char)cccii[i]);
            } else {
               if (i + 2 < cccii.length) {
                  byte[] c = new byte[]{cccii[i], cccii[i + 1], cccii[i + 2]};
                  byte[] u = this.cToU(c);
                  if (u[0] == 0 && u[1] == 0) {
                     sb.append("{");
                     sb.append(Util.toHexString(c));
                     sb.append("}");
                  } else {
                     byte[] big5 = (new String(u, "UTF-16LE")).getBytes("BIG5");
                     if (big5[0] == 63) {
                        sb.append("{");
                        sb.append(Util.toHexString(c));
                        sb.append("}");
                     } else {
                        sb.append(new String(big5, "ISO8859_1"));
                     }
                  }
               }

               i += 2;
            }
         }

         retval = sb.toString().getBytes("ISO8859_1");
      } catch (Exception var9) {
      }

      return retval;
   }

   public byte[] big5ToCccii(byte[] big5) {
      StringBuffer sb = new StringBuffer();
      byte[] retval = new byte[0];

      try {
         boolean sin = false;

         for(int i = 0; i < big5.length; ++i) {
            if (big5[i] > 0) {
               if (sin) {
                  sb.append((char)shiftChar);
                  sb.append('(');
                  sb.append('B');
                  sin = false;
               }

               sb.append((char)big5[i]);
            } else if (i + 1 < big5.length) {
               byte[] b = new byte[]{big5[i], big5[i + 1]};
               String uc = new String(b, "BIG5");
               if (!uc.equals("?") && uc.length() <= 1) {
                  byte[] u = new byte[]{(byte)(uc.charAt(0) >> 0 & 255), (byte)(uc.charAt(0) >> 8 & 255)};
                  byte[] cccii = this.uToC(u);
                  if (cccii[0] == 0 && cccii[1] == 0 && cccii[2] == 0) {
                     if (sin) {
                        sb.append((char)shiftChar);
                        sb.append('(');
                        sb.append('B');
                        sin = false;
                     }

                     sb.append("{");
                     sb.append(Util.toHexString(u));
                     sb.append("}");
                  } else {
                     if (!sin) {
                        sb.append((char)shiftChar);
                        sb.append('$');
                        sb.append('1');
                        sin = true;
                     }

                     sb.append(new String(cccii, "ISO8859_1"));
                  }
               } else {
                  if (sin) {
                     sb.append((char)shiftChar);
                     sb.append('(');
                     sb.append('B');
                     sin = false;
                  }

                  sb.append("{");
                  sb.append(Util.toHexString(b));
                  sb.append("}");
               }

               ++i;
            }
         }

         if (sin) {
            sb.append((char)shiftChar);
            sb.append('(');
            sb.append('B');
            sin = false;
         }

         retval = sb.toString().getBytes("ISO8859_1");
      } catch (Exception var10) {
      }

      return retval;
   }

   class UCObj {
      int cccii;
      int unicode;

      public UCObj(int c, int u) {
         this.cccii = c;
         this.unicode = u;
      }
   }
}
