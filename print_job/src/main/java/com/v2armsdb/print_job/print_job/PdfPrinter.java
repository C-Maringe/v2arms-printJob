package com.v2armsdb.print_job.print_job;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import javax.print.*;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/print")
public class PdfPrinter {
    @GetMapping("/receipt")
    public void printPdf(String filePath) throws IOException, PrintException {
        System.out.println("printing now" );
        PDDocument document = PDDocument.load(new File("./receipt.pdf"));
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        document.save(baos);
        byte[] documentData = baos.toByteArray();
        Doc doc = new SimpleDoc(documentData, DocFlavor.BYTE_ARRAY.AUTOSENSE, null);
        PrintService printService = PrintServiceLookup.lookupDefaultPrintService();
        DocPrintJob printJob = printService.createPrintJob();
        printJob.print(doc, null);
        createreceipt data = new createreceipt();
        new createreceipt.BillPrintable();
        document.close();
    }
}
