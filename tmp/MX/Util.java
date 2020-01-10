import java.io.File;
import java.net.URL;
import java.net.URLDecoder;
import java.security.CodeSource;
import java.security.ProtectionDomain;

public class Util {
   static char[] hexChar = new char[]{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

   public static File getApplicationpPath(Class clas) {
      ProtectionDomain pd = clas.getProtectionDomain();
      if (pd == null) {
         return null;
      } else {
         CodeSource cs = pd.getCodeSource();
         if (cs == null) {
            return null;
         } else {
            URL url = cs.getLocation();
            if (url == null) {
               return null;
            } else {
               File f = null;

               try {
                  f = new File(URLDecoder.decode(url.getPath(), "UTF-8"));
               } catch (Exception var7) {
                  return null;
               }

               String path = f.getAbsolutePath();
               if (f.isFile()) {
                  int pos = path.lastIndexOf(File.separator);
                  if (pos >= 0) {
                     path = path.substring(0, pos);
                  }
               }

               return new File(path);
            }
         }
      }
   }

   public static String leftJustify(String str, int fieldWidth) {
      if (str == null) {
         str = "";
      }

      if (str.length() >= fieldWidth) {
         return str.substring(0, fieldWidth);
      } else {
         StringBuffer buf = new StringBuffer(fieldWidth);
         buf.append(str);

         for(int i = fieldWidth - str.length(); i > 0; --i) {
            buf.append(' ');
         }

         return buf.toString();
      }
   }

   public static String rightJustify(String str, int fieldWidth) {
      if (str == null) {
         str = "";
      }

      if (str.length() >= fieldWidth) {
         return str.substring(0, fieldWidth);
      } else {
         StringBuffer buf = new StringBuffer(fieldWidth);

         for(int i = fieldWidth - str.length(); i > 0; --i) {
            buf.append(' ');
         }

         buf.append(str);
         return buf.toString();
      }
   }

   public static String intPadZero(int n, int wid) {
      String str = Integer.toString(n);

      for(int i = wid - str.length(); i > 0; --i) {
         str = '0' + str;
      }

      return str;
   }

   public static int zerostrToInt(String s) {
      StringBuffer buf = new StringBuffer(s.length());
      boolean f = false;

      for(int i = 0; i < s.length(); ++i) {
         String c = s.substring(i, i + 1);
         if (f) {
            buf.append(c);
         } else if (!c.equals("0")) {
            buf.append(c);
            f = true;
         }
      }

      if (buf.length() == 0) {
         buf.append("0");
      }

      return Integer.parseInt(buf.toString());
   }

   public static String toHexString(byte[] b) {
      StringBuffer sb = new StringBuffer(b.length * 2);

      for(int i = 0; i < b.length; ++i) {
         sb.append(hexChar[(b[i] & 240) >>> 4]);
         sb.append(hexChar[b[i] & 15]);
      }

      return sb.toString();
   }
}
