import win32print
import win32ui
from PIL import Image, ImageWin


def print_file(file_name):
    # return True
    print('printing: ', file_name)

    try:
        # 常数变量设置
        HORZSIZE = 4
        VERTSIZE = 6

        # Constants for GetDeviceCaps
        #
        HORZRES = 8
        VERTRES = 10
        #
        # LOGPIXELS = dots per inch
        #
        LOGPIXELSX = 88
        LOGPIXELSY = 90
        #
        # PHYSICALWIDTH/HEIGHT = total area
        #
        PHYSICALWIDTH = 110
        PHYSICALHEIGHT = 111
        #
        # PHYSICALOFFSETX/Y = left / top margin
        #
        PHYSICALOFFSETX = 112
        PHYSICALOFFSETY = 113

        # 获取打印机
        printer_name = win32print.GetDefaultPrinter()
        pHandle = win32print.OpenPrinter(printer_name)
        printinfo = win32print.GetPrinter(pHandle, 2)
        pDevModeObj = printinfo["pDevMode"]

        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        printable_size = hDC.GetDeviceCaps(
            HORZSIZE), hDC.GetDeviceCaps(VERTSIZE)
        printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
        printer_size = hDC.GetDeviceCaps(
            PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps(
            PHYSICALOFFSETX), hDC.GetDeviceCaps(PHYSICALOFFSETY)

        # 图片打开，if旋转
        bmp = Image.open(file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.transpose(Image.ROTATE_90)

        # 默认6寸打印，resize？

        # 缩放比例
        ratios = [1.0 * printable_area[0] / bmp.size[0],
                  1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)

        # 打印
        hDC.StartDoc(file_name)
        hDC.StartPage()
        dib = ImageWin.Dib(bmp)
        scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
        x1 = int((printer_size[0] - scaled_width) / 2)
        y1 = int((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
        return True
    except Exception as e:
        print(e)
        return False


# if __name__ == '__main__':
#   file_name = "C:\\Users\\wx\\Desktop\\Print\\photos\\190423.jpg"
#   print_file(file_name)
