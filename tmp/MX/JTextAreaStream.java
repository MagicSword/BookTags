import java.io.OutputStream;
import java.io.PrintStream;
import javax.swing.JTextArea;

public class JTextAreaStream extends PrintStream {
   JTextArea textArea;

   public JTextAreaStream(JTextArea ta, OutputStream os) {
      super(os);
      this.textArea = ta;
   }

   public String getText() {
      return this.textArea.getText();
   }

   public void print(String s) {
      this.textArea.append(s);
   }

   public void println() {
      String xf = "\r\n";
      this.textArea.append(xf);
   }

   public void println(String x) {
      String xf = "" + x + "\r\n";
      this.textArea.append(xf);
      this.flush();
   }

   public void replaceLastLine(String s) {
      int line = this.textArea.getLineCount();

      try {
         this.textArea.replaceRange(s, this.textArea.getLineStartOffset(line - 1), this.textArea.getLineEndOffset(line - 1));
      } catch (Exception var4) {
         var4.printStackTrace();
      }

   }

   public boolean checkError() {
      return false;
   }

   public void close() {
   }

   public void flush() {
   }

   protected void setError() {
   }
}
