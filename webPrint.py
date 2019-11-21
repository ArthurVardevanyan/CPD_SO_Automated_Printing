__version__ = "v20191112"
import Print
import printer


def main(ORDER_NUMBER, OUTPUT_DIRECTORY, PRINTER, COLOR, AUTORUN, EMAILPRINT, BOOKLETS):
    print_que = []
    output = Print.printing(ORDER_NUMBER, OUTPUT_DIRECTORY, PRINTER,
                            COLOR, print_que, AUTORUN, EMAILPRINT, BOOKLETS)
    printer.print_processor
    return output
