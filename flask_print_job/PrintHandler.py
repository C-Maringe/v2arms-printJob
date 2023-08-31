from flask import Flask, request
from flask_cors import CORS
from SendToPrinterJob import PrintTrigger
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.enums import TA_CENTER

styleSheet = getSampleStyleSheet()
Headingstyle = ParagraphStyle(name='Normal',
                              fontSize=10,
                              leading=10,
                              alignment=TA_CENTER,
                              spaceAfter=3)

middletablecolumnstyle = ParagraphStyle(name='Normal',
                                        fontSize=8,
                                        leading=10)

app = Flask(__name__)
CORS(app)


@app.route('/upload/receipt/', methods=["POST"])
def PrintHandler():
    data = request.json.get('data')
    for i in data:
        i[0] = Paragraph(i[0], middletablecolumnstyle)

    def run():
        doc = SimpleDocTemplate('receipt.pdf',
                                pagesize=(2.84*inch, 20*inch),
                                # pagesize=(8.5*inch, 11*inch),
                                rightMargin=0,
                                leftMargin=0,
                                topMargin=0,
                                bottomMargin=0,
                                )
        lst = []
        lst.append(Paragraph("Jinga Investments(Pvt) Ltd", Headingstyle))
        lst.append(Paragraph("14 Shumba Road", Headingstyle))
        lst.append(Paragraph("Masasa Park", Headingstyle))
        lst.append(Paragraph("Harare", Headingstyle))
        lst.append(
            Paragraph("Cashier: "+request.json.get('teller')+"", Headingstyle))

        lst.append(Spacer(0, 20))

        dataHead = [
            ['Date:', ""+request.json.get('date')+""],
            ['Ref:', request.json.get('reference')],
            ['Payment Method:', ""+request.json.get('payment_method')+""]
        ]

        style = TableStyle([
            ('FONTSIZE', (0, 0), (2, 2), 10),
            ('ALIGN', (1, 0), (1, 2), 'RIGHT'),
            ('ALIGN', (0, 0), (0, 2), 'LEFT'),
            ('LEFTPADDING', (1, 0), (1, 2), 10),
            ('BOTTOMPADDING', (0, 0), (2, 2), 2)
        ])

        table = Table(dataHead)
        table.setStyle(style)
        lst.append(table)

        lst.append(Spacer(0, 20))

        datamiddle = [['PRODUCT', 'PRICE', 'QTY', 'TOTAL'], ] + data

        def datamidlelength():
            if len(datamiddle) < 4:
                datalenght = 4
            else:
                datalenght = len(datamiddle)
            return datalenght

        datamiddlelenght = datamidlelength()
        stylemiddle = TableStyle([
            ('FONTSIZE', (0, 0), (3, 0), 10),
            ('FONTSIZE', (0, 1), (datamiddlelenght, datamiddlelenght), 8),
            ('ALIGN', (1, 0), (1, datamiddlelenght), 'CENTRE'),
            ('ALIGN', (1, 0), (2, datamiddlelenght), 'CENTRE'),
            ('ALIGN', (1, 0), (3, datamiddlelenght), 'CENTRE'),
            ('BOTTOMPADDING', (0, 0), (datamiddlelenght, datamiddlelenght), 2)
        ])

        tablemiddle = Table(datamiddle, colWidths=[
            1.604*inch, 0.4733*inch, 0.2893*inch, 0.4733*inch])
        tablemiddle.setStyle(stylemiddle)
        lst.append(tablemiddle)

        lst.append(Spacer(0, 20))

        databottom = [
            ['SUB TOTAL:', "$ "+request.json.get('totalprice')+""],
            ['VAT:', "$ "+request.json.get('vat')+""],
            ['TOTAL:', "$ "+request.json.get('totalprice')+""],
            ['PAYED AMOUNT:', "$ "+request.json.get('payedamount')+""],
            ['CHANGE:', "$ "+request.json.get('change')+""]
        ]
        stylebottom = TableStyle([
            ('FONTSIZE', (0, 0), (4, 4), 10),
            ('ALIGN', (1, 0), (1, 4), 'RIGHT'),
            ('ALIGN', (0, 0), (0, 4), 'LEFT'),
            ('LEFTPADDING', (1, 0), (1, 4), 60),
            ('BOTTOMPADDING', (0, 0), (4, 4), 2)
        ])
        tablebottom = Table(databottom)
        tablebottom.setStyle(stylebottom)
        lst.append(tablebottom)
        lst.append(Spacer(0, 40))
        lst.append(Paragraph("Thank you for your valued support.", Headingstyle))
        lst.append(Spacer(0, 130))
        lst.append(Paragraph("------------------------------------------------", Headingstyle))
        doc.build(lst)

    run()

    PrintTrigger()

    return ({"message": "Success"})


if __name__ == '__main__':
    app.run(debug=True, port=7000)
