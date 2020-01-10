import java.io.Writer;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Date;
import java.text.DateFormat;
import java.awt.EventQueue;
import java.io.OutputStream;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.Component;
import org.netbeans.lib.awtextra.AbsoluteConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.Insets;
import javax.swing.border.Border;
import javax.swing.border.BevelBorder;
import java.awt.Font;
import java.awt.LayoutManager;
import org.netbeans.lib.awtextra.AbsoluteLayout;
import java.io.File;
import javax.swing.JTextField;
import javax.swing.JTextArea;
import javax.swing.JScrollPane;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JComboBox;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;

// 
// Decompiled by Procyon v0.5.36
// 

public class MX extends JFrame
{
    final JFileChooser fileChooser;
    static int fmtIn;
    static int fmtOut;
    static String inFile;
    static String outFile;
    static String inCode;
    static String outCode;
    static String bibType;
    static JTextAreaStream log;
    private JButton jButton1;
    private JButton jButton2;
    private JButton jButton3;
    private JComboBox jComboBox1;
    private JComboBox jComboBox2;
    private JComboBox jComboBox3;
    private JLabel jLabel1;
    private JLabel jLabel2;
    private JLabel jLabel3;
    private JLabel jLabel4;
    private JLabel jLabel5;
    private JLabel jLabel6;
    private JLabel jLabel7;
    private JLabel jLabel8;
    private JLabel jLabel9;
    private JPanel jPanel1;
    private JPanel jPanel2;
    private JScrollPane jScrollPane1;
    private JTextArea jTextArea1;
    private JTextField jTextField1;
    private JTextField jTextField2;
    
    public MX() {
        this.fileChooser = new JFileChooser();
        this.initComponents();
        this.jComboBox1.addItem("ISO2709 (BIG5)");
        this.jComboBox1.addItem("ISO2709 (UTF-8)");
        this.jComboBox1.addItem("ISO2709 (CCCII)");
        this.jComboBox1.addItem("CMARC3-XML (BIG5, UTF-8)");
        this.jComboBox1.addItem("CMARC3-XML (CCCII)");
        this.jComboBox1.setSelectedIndex(0);
        this.jComboBox2.addItem("ISO2709 (BIG5)");
        this.jComboBox2.addItem("ISO2709 (UTF-8)");
        this.jComboBox2.addItem("ISO2709 (CCCII)");
        this.jComboBox2.addItem("CMARC3-XML (BIG5)");
        this.jComboBox2.addItem("CMARC3-XML (UTF-8)");
        this.jComboBox2.addItem("CMARC3-XML (CCCII)");
        this.jComboBox2.setSelectedIndex(0);
        this.jComboBox3.addItem("Bibliographic");
        this.jComboBox3.addItem("Authority");
        this.jComboBox3.setSelectedIndex(0);
        this.fileChooser.setCurrentDirectory(new File(Util.getApplicationpPath(this.getClass()).getPath()));
    }
    
    private void initComponents() {
        this.jButton1 = new JButton();
        this.jScrollPane1 = new JScrollPane();
        this.jTextArea1 = new JTextArea();
        this.jPanel1 = new JPanel();
        this.jLabel1 = new JLabel();
        this.jTextField1 = new JTextField();
        this.jButton2 = new JButton();
        this.jLabel3 = new JLabel();
        this.jComboBox1 = new JComboBox();
        this.jPanel2 = new JPanel();
        this.jLabel2 = new JLabel();
        this.jTextField2 = new JTextField();
        this.jButton3 = new JButton();
        this.jLabel4 = new JLabel();
        this.jComboBox2 = new JComboBox();
        this.jLabel5 = new JLabel();
        this.jComboBox3 = new JComboBox();
        this.jLabel6 = new JLabel();
        this.jLabel7 = new JLabel();
        this.jLabel8 = new JLabel();
        this.jLabel9 = new JLabel();
        this.getContentPane().setLayout(new AbsoluteLayout());
        this.setDefaultCloseOperation(3);
        this.setTitle("CMARC3-XML\u8f49\u63db\u7a0b\u5f0f");
        this.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.setResizable(false);
        this.jButton1.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jButton1.setText("\u57f7\u884c");
        this.jButton1.setBorder(new BevelBorder(0));
        this.jButton1.setMargin(new Insets(2, 2, 2, 2));
        this.jButton1.addActionListener(new ActionListener() {
            public void actionPerformed(final ActionEvent evt) {
                MX.this.jButton1ActionPerformed(evt);
            }
        });
        this.getContentPane().add(this.jButton1, new AbsoluteConstraints(20, 208, 68, 24));
        this.jTextArea1.setEditable(false);
        this.jTextArea1.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jScrollPane1.setViewportView(this.jTextArea1);
        this.getContentPane().add(this.jScrollPane1, new AbsoluteConstraints(20, 240, 388, 128));
        this.jPanel1.setLayout(new AbsoluteLayout());
        this.jPanel1.setBorder(new BevelBorder(1));
        this.jLabel1.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel1.setText("\u8f38\u5165\u6a94\u6848");
        this.jPanel1.add(this.jLabel1, new AbsoluteConstraints(8, 16, -1, -1));
        this.jTextField1.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jPanel1.add(this.jTextField1, new AbsoluteConstraints(60, 12, 300, -1));
        this.jButton2.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jButton2.setText("...");
        this.jButton2.setMargin(new Insets(2, 2, 2, 2));
        this.jButton2.addActionListener(new ActionListener() {
            public void actionPerformed(final ActionEvent evt) {
                MX.this.jButton2ActionPerformed(evt);
            }
        });
        this.jPanel1.add(this.jButton2, new AbsoluteConstraints(360, 12, -1, 20));
        this.jLabel3.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel3.setText("\u683c\u5f0f");
        this.jPanel1.add(this.jLabel3, new AbsoluteConstraints(32, 44, -1, -1));
        this.jComboBox1.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jPanel1.add(this.jComboBox1, new AbsoluteConstraints(60, 40, 212, -1));
        this.getContentPane().add(this.jPanel1, new AbsoluteConstraints(20, 16, 388, 72));
        this.jPanel2.setLayout(new AbsoluteLayout());
        this.jPanel2.setBorder(new BevelBorder(1));
        this.jLabel2.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel2.setText("\u8f38\u51fa\u6a94\u6848");
        this.jPanel2.add(this.jLabel2, new AbsoluteConstraints(8, 16, -1, -1));
        this.jTextField2.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jPanel2.add(this.jTextField2, new AbsoluteConstraints(60, 12, 300, -1));
        this.jButton3.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jButton3.setText("...");
        this.jButton3.setMargin(new Insets(2, 2, 2, 2));
        this.jButton3.addActionListener(new ActionListener() {
            public void actionPerformed(final ActionEvent evt) {
                MX.this.jButton3ActionPerformed(evt);
            }
        });
        this.jPanel2.add(this.jButton3, new AbsoluteConstraints(360, 12, 20, 20));
        this.jLabel4.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel4.setText("\u683c\u5f0f");
        this.jPanel2.add(this.jLabel4, new AbsoluteConstraints(32, 44, -1, -1));
        this.jComboBox2.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jPanel2.add(this.jComboBox2, new AbsoluteConstraints(60, 40, 212, -1));
        this.jLabel5.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel5.setText("\u66f8\u76ee\u7a2e\u985e");
        this.jPanel2.add(this.jLabel5, new AbsoluteConstraints(8, 72, -1, -1));
        this.jComboBox3.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jPanel2.add(this.jComboBox3, new AbsoluteConstraints(60, 68, 108, -1));
        this.jLabel6.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel6.setText("(\u53ea\u91dd\u5c0d ISO2709 => CMARC3-XML)");
        this.jPanel2.add(this.jLabel6, new AbsoluteConstraints(176, 72, -1, -1));
        this.getContentPane().add(this.jPanel2, new AbsoluteConstraints(20, 96, 388, 104));
        this.jLabel7.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel7.setText("\u570b\u5bb6\u5716\u66f8\u9928\u8457\u4f5c\u6b0a\u8072\u660e ® \u9078\u5c07\u8cc7\u8a0a\u7cfb\u7d71\u88fd\u4f5c");
        this.getContentPane().add(this.jLabel7, new AbsoluteConstraints(96, 380, 252, 12));
        this.jLabel8.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel8.setText("\u8655\u7406\u7b46\u6578\uff1a");
        this.getContentPane().add(this.jLabel8, new AbsoluteConstraints(100, 212, -1, -1));
        this.jLabel9.setFont(new Font("\u65b0\u7d30\u660e\u9ad4", 0, 12));
        this.jLabel9.setText("    ");
        this.getContentPane().add(this.jLabel9, new AbsoluteConstraints(160, 212, -1, -1));
        final Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        this.setBounds((screenSize.width - 433) / 2, (screenSize.height - 426) / 2, 433, 426);
    }
    
    private void jButton3ActionPerformed(final ActionEvent evt) {
        final int returnVal = this.fileChooser.showOpenDialog(this);
        if (returnVal == 0) {
            final File file = this.fileChooser.getSelectedFile();
            this.jTextField2.setText(file.getAbsolutePath());
        }
    }
    
    private void jButton2ActionPerformed(final ActionEvent evt) {
        final int returnVal = this.fileChooser.showOpenDialog(this);
        if (returnVal == 0) {
            final File file = this.fileChooser.getSelectedFile();
            this.jTextField1.setText(file.getAbsolutePath());
        }
    }
    
    private void jButton1ActionPerformed(final ActionEvent evt) {
        this.jTextArea1.setText("");
        MX.log = new JTextAreaStream(this.jTextArea1, System.out);
        MX.inFile = this.jTextField1.getText().trim();
        MX.outFile = this.jTextField2.getText().trim();
        if (MX.inFile.length() == 0 || MX.outFile.length() == 0) {
            MX.log.println("\u5fc5\u9808\u6307\u5b9a\u8f38\u5165\u8207\u8f38\u51fa\u6a94\u6848.");
            return;
        }
        MX.log.flush();
        final int sIn = this.jComboBox1.getSelectedIndex();
        final int sOut = this.jComboBox2.getSelectedIndex();
        MX.fmtIn = 0;
        MX.fmtOut = 0;
        MX.inCode = BibData.encodeBig5;
        MX.outCode = BibData.encodeBig5;
        MX.bibType = this.jComboBox3.getSelectedItem().toString();
        if (sIn == 0) {
            MX.fmtIn = 0;
            MX.inCode = BibData.encodeBig5;
        }
        else if (sIn == 1) {
            MX.fmtIn = 0;
            MX.inCode = BibData.encodeUtf8;
        }
        else if (sIn == 2) {
            MX.fmtIn = 0;
            MX.inCode = BibData.encodeCccii;
        }
        else if (sIn == 3) {
            MX.fmtIn = 1;
            MX.inCode = BibData.encodeUtf8;
        }
        else if (sIn == 4) {
            MX.fmtIn = 1;
            MX.inCode = BibData.encodeCccii;
        }
        if (sOut == 0) {
            MX.fmtOut = 0;
            MX.outCode = BibData.encodeBig5;
        }
        else if (sOut == 1) {
            MX.fmtOut = 0;
            MX.outCode = BibData.encodeUtf8;
        }
        else if (sOut == 2) {
            MX.fmtOut = 0;
            MX.outCode = BibData.encodeCccii;
        }
        else if (sOut == 3) {
            MX.fmtOut = 1;
            MX.outCode = BibData.encodeBig5;
        }
        else if (sOut == 4) {
            MX.fmtOut = 1;
            MX.outCode = BibData.encodeUtf8;
        }
        else if (sOut == 5) {
            MX.fmtOut = 1;
            MX.outCode = BibData.encodeCccii;
        }
        final SwingWorker worker = new SwingWorker() {
            public Object construct() {
                return MX.this.doWork(MX.this.jButton1, MX.this.jLabel9);
            }
        };
        worker.start();
    }
    
    public static void main(final String[] args) {
        EventQueue.invokeLater(new Runnable() {
            public void run() {
                new MX().setVisible(true);
            }
        });
    }
    
    Object doWork(final JButton btnStart, final JLabel lblCount) {
        this.jButton1.setEnabled(false);
        this.setCursor(3);
        final DateFormat df = DateFormat.getDateTimeInstance();
        MX.log.println("\u958b\u59cb\u6642\u9593\uff1a" + df.format(new Date()));
        MX.log.println("\u8cc7\u6599\u8655\u7406\u4e2d ... ");
        final MarcXml obj = new MarcXml();
        if (MX.fmtIn == 0 && MX.fmtOut == 0) {
            obj.isoToIso(MX.inFile, MX.outFile, MX.inCode, MX.outCode, MX.log, lblCount);
        }
        else if (MX.fmtIn == 0 && MX.fmtOut == 1) {
            obj.isoToXml(MX.inFile, MX.outFile, MX.inCode, MX.outCode, MX.bibType, MX.log, lblCount);
        }
        else if (MX.fmtIn == 1 && MX.fmtOut == 0) {
            obj.xmlToIso(MX.inFile, MX.outFile, MX.inCode, MX.outCode, MX.log, lblCount);
        }
        else if (MX.fmtIn == 1 && MX.fmtOut == 1) {
            obj.xmlToXml(MX.inFile, MX.outFile, MX.inCode, MX.outCode, MX.bibType, MX.log, lblCount);
        }
        MX.log.println("\u7d50\u675f\u6642\u9593\uff1a" + df.format(new Date()));
        this.setCursor(0);
        this.jButton1.setEnabled(true);
        final String logFile = Util.getApplicationpPath(this.getClass()).getPath() + File.separator + "MX.log";
        try {
            final BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(logFile), "BIG5"));
            writer.write(MX.log.getText());
            writer.close();
        }
        catch (Exception e) {
            MX.log.println("\u7121\u6cd5\u8f38\u51fa\u8a18\u9304\u6a94");
            MX.log.println(logFile);
        }
        return null;
    }
    
    static {
        MX.fmtIn = 0;
        MX.fmtOut = 0;
        MX.inFile = "";
        MX.outFile = "";
        MX.inCode = "";
        MX.outCode = "";
        MX.bibType = "";
        MX.log = null;
    }
}
