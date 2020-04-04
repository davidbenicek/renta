import PyPDF2
pdfs = [
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-01.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-02.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-03.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-04.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-05.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-06.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-07.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-08.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-09.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-10.PDF",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-11.pdf",
    "../../Google Drive/!!!admin/barcelona/tax/2019/19-12.pdf",
    ]
period = 0
print("Period",";","Amount Recived",";","Total Deducted",";","IRPF subject earnings",";","Gross Total",";","IRPF rate",";","IRPF amount")
for pdf in pdfs:
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # N.B. if you have a lot of pages in your pay slip, it might not work very well...
    # you can use the number of pages in the pdf to debbug
    # print(pdfReader.numPages)
    pageObj = pdfReader.getPage(0)
    raw = "".join(pageObj.extractText().split())
    try:
        # hacky way to get around issue where IRPF may be on 2nd page
        indexOfIRPFRate = raw.index("TRIBUTACIONI.R.P.F.")+19
    except:
        if pdfReader.numPages > 1:
            pageObj = pdfReader.getPage(1)
            raw = "".join(pageObj.extractText().split())
            indexOfIRPFRate = raw.index("TRIBUTACIONI.R.P.F.")+19
    irpfRate = raw[indexOfIRPFRate:indexOfIRPFRate+5]
    endOfNumberOffset = raw[indexOfIRPFRate+5:].index(',') + 8
    irpfAmount = raw[indexOfIRPFRate+5:indexOfIRPFRate+endOfNumberOffset]

    indexOfDeducted = raw.index("*PercepcionesSalarialessujetasa")
    deducted = raw[indexOfDeducted-8:indexOfDeducted]
    grossTotal = raw[indexOfDeducted-16:indexOfDeducted-8]
    irpfBase = raw[indexOfDeducted-24:indexOfDeducted-16]
    indexOfTotal = raw.index("LIQUIDOAPERCIBIR")
    total = raw[indexOfTotal+16:indexOfTotal+24]
    print(period,";",total,";",deducted,";",irpfBase,";",grossTotal,";",irpfRate,";",irpfAmount)
    period+=1
